import time
import sys
import math
from neuromeka import IndyDCP3
from neuromeka.enums import TaskBaseType, StopCategory

# =============================================================
# 1. 시스템 설정 및 티칭 좌표 정의
# =============================================================
ROBOT_IP = "192.168.3.7"    # 제어기 통신 IP
APPROACH_OFFSET_Z = 100.0   # 접근 및 후퇴 안전 여유 높이 (mm)
LAYER_HEIGHT_OFFSET = 40.0  # 2층 Z축 적재 높이 간격 (mm)

# [중요] 모든 좌표는 Task 직교 좌표 [X, Y, Z, U, V, W] (단위: mm, deg)
# 다이렉트 티칭의 관절각(Joint q)을 로봇 순기구학(Forward Kinematics)으로 변환한 직교 좌표입니다.
SUPPLY_POINT   = [239.15, 520.71, 257.03, -21.77, -177.36, 90.33]  # 적재물 공급 위치
RETRIEVE_POINT = [-6.046, 504.743, 342.409, -21.858, 175.023, 93.199]  # 적재물 회수 위치 (Point 5)

# 팔레트 베이스 포인트 (1층 4개 위치: 2x2 패턴, Point 1~4)
PALLET_BASE_POINTS = [
    [201.034, 332.441, 304.935, -3.460, 178.355, 85.307],   # Point 1 (X~201, Y~332)
    [201.621, 251.679, 304.112, -3.106, 177.629, 87.710],   # Point 2 (X~201, Y~252)
    [124.126, 263.375, 304.294, -4.151, -176.981, 90.540],  # Point 3 (X~124, Y~263)
    [124.170, 339.890, 304.246, -5.092, -178.577, 87.091],  # Point 4 (X~124, Y~340)
]

# 양솔레노이드(Double Solenoid) 공압 그리퍼 핀 매핑 (제어기 DO 기준)
# * DO 0: 열림(Open) 솔레노이드 코일
# * DO 1: 닫힘(Close) 솔레노이드 코일
SOL_OPEN_DO  = 0   # 그리퍼 열림(Open) 솔레노이드 DO 핀
SOL_CLOSE_DO = 1   # 그리퍼 닫힘(Close) 솔레노이드 DO 핀

# =============================================================
# 2. 로봇 인스턴스 초기화 및 저수준 제어 래퍼
# =============================================================
robot = IndyDCP3(robot_ip=ROBOT_IP)

def read_signal(address: int) -> bool:
    """
    PLC 인터록 및 기동 신호 조회
    - 로봇 DI(디지털 입력) 우선 확인 (PLC 출력 -> 로봇 입력)
    - state == 1 (ON_STATE)인 경우만 True 반환 (2: UNUSED_STATE 제외)
    """
    # 1. DI 확인
    res_di = robot.get_di()
    for sig in res_di.get("signals", []):
        if sig.get("address") == address:
            return sig.get("state") == 1

    # 2. DO 확인
    res_do = robot.get_do()
    for sig in res_do.get("signals", []):
        if sig.get("address") == address:
            return sig.get("state") == 1

    return False

def wait_do_3_on():
    """
    3번(적재 동작 허가) 인터록 대기 (사이클 완료 정지 방식)
    - 적재 중 3번 신호가 꺼지더라도 현재 작업은 팔레트까지 끝까지 완료한 뒤,
      '다음 작업 사이클 진입 직전'에 여기서 일시 정지하여 대기합니다.
    """
    if not read_signal(3):
        print("  [일시정지] 3번(동작 허가) 신호 OFF 감지 -> 현재 작업 완료 후 다음 작업 진입 대기 (3번 ON 대기)...")
        while not read_signal(3):
            time.sleep(0.05)
        print("  >> [동작 재개] 3번 신호 ON 감지 -> 다음 작업 사이클 시작!")

def linear_move(pose: list, vel_ratio: float = 40, acc_ratio: float = 40):
    """
    직선 모션 실행:
    - 진행 중인 모션은 도중에 끊김 없이 끝까지 완주
    - 목표 지점 완전 도달(정지)까지 동기화 대기
    """
    res = robot.movel(pose, base_type=TaskBaseType.ABSOLUTE, vel_ratio=vel_ratio, acc_ratio=acc_ratio)
    if isinstance(res, dict) and res.get("code") not in (0, "0", None):
        print(f"[경고] MoveL 실패: {res}")
        return res

    # 컨트롤러가 명령을 수신하고 궤적 생성을 시작할 최소 시간 대기
    time.sleep(0.1)

    # 로봇이 물리적으로 이동을 마치고 정지할 때까지 동기화 대기
    t_start = time.time()
    while robot.get_motion_data().get("is_in_motion", False):
        if time.time() - t_start > 30.0:
            print("[경고] 모션 도달 대기 시간 초과(Timeout)")
            break
        time.sleep(0.02)

def get_pallet_pose(index: int) -> list:
    """인덱스(0~7)에 따른 1층(0~3) 및 2층(4~7) 목표 좌표 계산"""
    base_idx = index % 4
    layer = index // 4
    pose = list(PALLET_BASE_POINTS[base_idx])
    pose[2] += (layer * LAYER_HEIGHT_OFFSET)
    return pose

def get_offset_pose(pose: list, distance: float) -> list:
    """
    진입각(Tool 축)을 그대로 유지한 채 반대 방향으로 후퇴/접근하는 3차원 위치 계산
    - 베이스 Z축만 올리면 경사각(U=-21.77도) 때문에 공급대 측벽과 충돌하므로,
      엔드툴 진입 축(Tool -Z) 방향으로 직선 후퇴하여 충돌 없는 완벽한 진입/후퇴 궤적을 만듭니다.
    """
    try:
        res = robot.calculate_current_pose_rel(
            current_pos=pose,
            relative_pos=[0.0, 0.0, -distance, 0.0, 0.0, 0.0],
            base_type=TaskBaseType.TCP
        )
        if res and "calculated_pos" in res and res["calculated_pos"]:
            return [round(v, 2) for v in res["calculated_pos"]]
    except Exception:
        pass

    # 예비 계산: U축 경사각(-21.77도)에 따른 X-Z 벡터 분해 후퇴
    target = list(pose)
    rad_u = math.radians(abs(pose[3]))
    target[0] += distance * math.sin(rad_u)  # 경사각에 따른 X축 보정 후퇴
    target[2] += distance * math.cos(rad_u)  # 경사각에 따른 Z축 상승
    return [round(v, 2) for v in target]

# =============================================================
# 3. 양솔레노이드 그리퍼 제어 래퍼 함수
# =============================================================
def gripper_open(dwell_time: float = 0.5):
    """그리퍼 열림: Open(DO 0) ON, Close(DO 1) OFF"""
    print(">> [GRIPPER] OPEN (열림) [DO 0: ON, DO 1: OFF]")
    robot.set_do([(SOL_OPEN_DO, True), (SOL_CLOSE_DO, False)])
    time.sleep(dwell_time)

def gripper_close(dwell_time: float = 0.6):
    """그리퍼 닫힘: Open(DO 0) OFF, Close(DO 1) ON"""
    print(">> [GRIPPER] CLOSE (닫힘) [DO 0: OFF, DO 1: ON]")
    robot.set_do([(SOL_OPEN_DO, False), (SOL_CLOSE_DO, True)])
    time.sleep(dwell_time)

# =============================================================
# 4. 픽 앤 플레이스 단위 시퀀스
# =============================================================
def execute_pick(pick_pos: list):
    """
    Pick 시퀀스:
    1. 그리퍼 Open (닫힌 상태로 접근하는 사고 방지)
    2. 접근 안전 위치로 이동 후 완전 정지
    3. 파지 위치(Target Point)로 정밀 하강 후 완전 정지
    4. 그리퍼 Close 실행 및 0.6초 충분한 공압 압력 대기
    5. 물체를 파지한 상태로 안전 높이 후퇴
    """
    app_pos = get_offset_pose(pick_pos, APPROACH_OFFSET_Z)

    # 1. 접근 위치로 가기 전 미리 그리퍼를 확실하게 Open
    gripper_open(dwell_time=0.3)

    # 2. 접근 안전 위치로 이동
    print(f"  [1] Pick 접근 높이 이동...")
    linear_move(app_pos)

    # 3. 파지 위치(Target Point)로 하강
    print(f"  [2] Target Point 파지 위치 도달 중...")
    linear_move(pick_pos)

    # 4. Target Point에 도달하여 정지한 상태에서 그리퍼 Close 실행!
    print(f"  [3] Target Point 도착 완료 -> 그리퍼 파지(CLOSE)!")
    gripper_close(dwell_time=0.6)

    # 5. 물체를 잡고 안전 높이로 후퇴
    print(f"  [4] 안전 높이 상승...")
    linear_move(app_pos)

def execute_place(place_pos: list):
    """Place 시퀀스: 파지 상태로 접근 -> 타겟 도달 후 그리퍼 열림 -> 후퇴"""
    app_pos = get_offset_pose(place_pos, APPROACH_OFFSET_Z)

    # 1. 적재 접근 위치 이동 (그리퍼 파지 상태 유지)
    linear_move(app_pos)

    # 2. 적재 위치 진입 (완전히 정지할 때까지 대기)
    linear_move(place_pos)

    # 3. 타겟 위치 도달 후 그리퍼 Open (적재물 안착)
    print(f"  [Place] 적재 위치 도착 완료 -> 그리퍼 안착(OPEN)!")
    gripper_open(dwell_time=0.6)

    # 4. 안전 높이로 후퇴
    linear_move(app_pos)

# =============================================================
# 5. 메인 제어 루프 (사이클 완료 정지 방식)
# =============================================================
try:
    print("=" * 65)
    print("    팔레타이징 / 디팔레타이징 시스템 시작")
    print(f"    - 로봇 IP: {ROBOT_IP}")
    print(f"    - 공급 위치: {SUPPLY_POINT}")
    print(f"    - 회수 위치: {RETRIEVE_POINT}")
    print(f"    - 팔레트 베이스 Z높이: ~{round(PALLET_BASE_POINTS[0][2], 1)} mm (1층), +{LAYER_HEIGHT_OFFSET} mm (2층)")
    print("=" * 65)

    # 시작 시 그리퍼를 먼저 열어둠 (대기 상태)
    print("초기화: 그리퍼 OPEN...")
    gripper_open(dwell_time=0.5)

    print("시스템 준비 완료. PLC 신호 대기 중 (8: 적재 기동, 9: 회수 기동, 3: 적재 동작 허가)...")

    stacked_count = 4
    is_stacking = False  # 8개 연속 적재 가동 플래그

    while True:
        do_8 = read_signal(8)  # 적재 시작 지령 (PLC DO 8 -> 로봇 DI 8)
        do_9 = read_signal(9)  # 회수 시작 지령 (PLC DO 9 -> 로봇 DI 9)

        # 8번 신호가 감지되면 연속 적재 모드 가동 시작!
        if do_8 and stacked_count < 8 and not is_stacking:
            print("\n[기동 감지] 8번 기동 신호 ON -> 8개 연속 적재 모드 시작!")
            is_stacking = True

        # 1. 적재 시퀀스 (연속 적재 활성화 상태에서 8개 채울 때까지 연속 수행)
        if is_stacking and stacked_count < 8:
            # ★ 핵심: '다음 작업에 들어가기 전'에 3번 신호를 검사!
            # 이전 피스 작업 도중 3번이 OFF되더라도 그 작업은 팔레트까지 완전히 안착시키고,
            # 다음 번 작업 피스를 시작하기 직전 바로 여기서 일시정지하여 대기합니다.
            wait_do_3_on()

            print(f"\n========================================================")
            print(f"[{stacked_count + 1}/8] 적재 사이클 실행 (Pallet 인덱스: {stacked_count})")
            print(f"========================================================")

            # 공급점에서 Pick
            execute_pick(SUPPLY_POINT)

            # 팔레트에 Place (1층: 0~3, 2층: 4~7)
            pallet_target = get_pallet_pose(stacked_count)
            execute_place(pallet_target)

            stacked_count += 1
            print(f">> [{stacked_count}/8] 적재 완료!")

            # 8개 만재 완료 시 자동 정지 및 회수 대기 상태 전환
            if stacked_count == 8:
                is_stacking = False
                print("\n" + "=" * 65)
                print("★ [만재] 8개 전량 적재 완료! -> 회수(9번) 신호 대기 중...")
                print("=" * 65)

        # 2. 회수 시퀀스 (신호 9 ON, 8개 만재 시에만 동작)
        elif do_9 and stacked_count == 8:
            print(f"\n========================================================")
            print("[기동 감지] 9번 신호 ON -> 8개 전량 회수 사이클 실행...")
            print(f"========================================================")

            # 2층 상단부터 역순(7 -> 0)으로 디팔레타이징 회수
            for retrieve_idx in reversed(range(8)):
                pallet_target = get_pallet_pose(retrieve_idx)
                print(f"\n[{8 - retrieve_idx}/8] 팔레트 인덱스 {retrieve_idx} 회수 중...")

                # 팔레트 지점에서 Pick
                execute_pick(pallet_target)

                # 회수점에 Place
                execute_place(RETRIEVE_POINT)

            stacked_count = 0
            print("\n" + "=" * 65)
            print("★ [회수 완료] 전량 회수 완료! 팔레트 카운터 초기화 -> 다음 적재(8번) 대기 중...")
            print("=" * 65)

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n사용자 수동 중단 감지.")
    robot.stop_motion(stop_category=StopCategory.CAT2)
except Exception as ex:
    print(f"\n제어 인터록 예외 발생: {ex}")
    robot.stop_motion(stop_category=StopCategory.CAT0)
finally:
    # 종료 시 솔레노이드 출력 소자 및 gRPC 채널 정상 해제
    try:
        robot.set_do([(SOL_OPEN_DO, False), (SOL_CLOSE_DO, False)])
    except Exception:
        pass
    del robot
    print("IndyDCP3 리소스 해제 완료.")