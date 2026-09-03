# -*- coding: utf-8 -*-
"""
Indy7 / IndyDCP3 다이렉트 티칭 (5개 포인트) & 양솔레노이드 그리퍼 제어 스크립트
- 실행 10초 후 양솔레노이드 공압 그리퍼 자동 Close (닫힘)
- 다이렉트 티칭 모드로 5개 포인트 순차 기록 (Joint q, Task p)
- 완료 후 좌표 요약 및 재생(Play)용 코드 포맷 출력
"""

import os
import sys
import time
import threading

# neuromeka 패키지 경로 추가
PACKAGE_PATH = r"C:\Users\user\Desktop\neuromeka-package-develop\python"
if PACKAGE_PATH not in sys.path:
    sys.path.append(PACKAGE_PATH)

from neuromeka import IndyDCP3

# ==============================================================================
# [1] 사용자 환경 설정 (IP 및 핀 번호)
# ==============================================================================
ROBOT_IP = "192.168.3.7"     # 로봇 제어기 IP (실제 로봇 IP: 192.168.3.2 또는 192.168.3.7 등)

# 양솔레노이드(Double Solenoid) 밸브 제어 핀 설정 (컨트롤러 박스 DO 기준)
# * 공압 양솔 밸브 특성상 한쪽 코일을 ON할 때 반대쪽 코일은 반드시 OFF해야 합니다.
SOL_OPEN_DO  = 0            # 그리퍼 열림(Open) 솔레노이드 DO 핀 번호
SOL_CLOSE_DO = 1           # 그리퍼 닫힘(Close) 솔레노이드 DO 핀 번호

# 툴 플랜지(Endtool)의 DO 포트를 사용할 경우 아래 플래그를 True로 변경하세요.
USE_ENDTOOL_DO = False      # True: 툴 플랜지 DO 사용, False: 제어기 박스 DO 사용

TOTAL_POINTS = 5            # 티칭할 포인트 개수
CLOSE_DELAY_SEC = 10        # 실행 후 그리퍼 Close까지 대기 시간 (초)

# ==============================================================================
# [2] 그리퍼 제어 함수 (양솔레노이드 공압 방식)
# ==============================================================================
def gripper_close(robot: IndyDCP3):
    """양솔레노이드 그리퍼 닫힘 (Close): 열림 솔 OFF, 닫힘 솔 ON"""
    try:
        if USE_ENDTOOL_DO:
            # Endtool DO 예시: [('A', [False, True])]
            robot.set_endtool_do([('A', [False, True])])
        else:
            # 제어기 DO: Open 핀 OFF(False), Close 핀 ON(True)
            robot.set_do([
                (SOL_OPEN_DO, False),
                (SOL_CLOSE_DO, True)
            ])
        print("\n" + "=" * 55)
        print(" [GRIPPER] >>> 그리퍼가 CLOSE (닫힘) 되었습니다! <<<")
        print("=" * 55 + "\n")
    except Exception as e:
        print(f"\n[경고] 그리퍼 Close 동작 실패: {e}")

def gripper_open(robot: IndyDCP3):
    """양솔레노이드 그리퍼 열림 (Open): 열림 솔 ON, 닫힘 솔 OFF"""
    try:
        if USE_ENDTOOL_DO:
            robot.set_endtool_do([('A', [True, False])])
        else:
            # 제어기 DO: Open 핀 ON(True), Close 핀 OFF(False)
            robot.set_do([
                (SOL_OPEN_DO, True),
                (SOL_CLOSE_DO, False)
            ])
        print("\n>> [GRIPPER] 그리퍼가 OPEN (열림) 되었습니다.")
    except Exception as e:
        print(f"\n[경고] 그리퍼 Open 동작 실패: {e}")

# ==============================================================================
# [3] 10초 타이머 백그라운드 스레드
# ==============================================================================
timer_stop_flag = threading.Event()

def auto_close_timer(robot: IndyDCP3, delay_sec: int):
    """백그라운드에서 delay_sec초 대기 후 그리퍼 Close 실행"""
    for sec in range(delay_sec):
        if timer_stop_flag.is_set():
            return
        time.sleep(1)
    
    if not timer_stop_flag.is_set():
        gripper_close(robot)

# ==============================================================================
# [4] 메인 티칭 로직
# ==============================================================================
def main():
    print("=" * 65)
    print("       Indy7 / IndyDCP3 다이렉트 티칭 & 양솔 그리퍼 제어")
    print("=" * 65)
    print(f"* 연결 로봇 IP : {ROBOT_IP}")
    print(f"* 그리퍼 타입  : 양솔레노이드 공압 (Open DO:{SOL_OPEN_DO}, Close DO:{SOL_CLOSE_DO})")
    print(f"* 티칭 포인트  : 총 {TOTAL_POINTS}개")
    print(f"* 그리퍼 동작  : 프로그램 시작 {CLOSE_DELAY_SEC}초 후 자동 CLOSE")
    print("=" * 65)

    # 1. 로봇 연결
    try:
        print("\n[1/4] 로봇 제어기에 연결 중...")
        robot = IndyDCP3(ROBOT_IP)
        print("  -> 로봇 연결 성공!")
    except Exception as e:
        print(f"[에러] 로봇 연결 실패: {e}")
        return

    # 2. 다이렉트 티칭 모드 시작
    try:
        print("\n[2/4] 다이렉트 티칭 모드를 활성화합니다...")
        robot.set_direct_teaching(True)
        print("  -> 다이렉트 티칭 ON! (로봇 팔을 자유롭게 움직일 수 있습니다.)")
    except Exception as e:
        print(f"[에러] 다이렉트 티칭 활성화 실패: {e}")
        return

    # 3. 10초 후 그리퍼 Close 타이머 시작 (백그라운드 스레드)
    timer_thread = threading.Thread(target=auto_close_timer, args=(robot, CLOSE_DELAY_SEC), daemon=True)
    timer_thread.start()
    print(f"\n[알림] 지금부터 {CLOSE_DELAY_SEC}초 뒤에 그리퍼가 자동으로 닫힙니다!")
    print("       (손으로 그리퍼를 물체/워크 위치로 가져가서 맞추세요.)\n")

    saved_points = []

    try:
        # 4. 5개 포인트 순차 티칭
        print("[3/4] 5개 포인트 티칭을 진행합니다.")
        for i in range(1, TOTAL_POINTS + 1):
            print("------------------------------------------------------------")
            print(f"▶ 포인트 #{i} 번 위치로 로봇을 손으로 이동시킨 후 [Enter]를 누르세요.")
            input(f"   (Point {i} 준비 완료 시 Enter 입력) >> ")

            # 현재 상태 읽기
            state = robot.get_control_state()
            q = state.get("q", [])  # Joint 위치 (각도)
            p = state.get("p", [])  # Task 위치 [X, Y, Z, U, V, W]

            point_data = {
                "index": i,
                "q": q,
                "p": p
            }
            saved_points.append(point_data)

            print(f"\n  [Point {i} 저장 완료]")
            print(f"   - Joint (q) : {[round(v, 3) for v in q]}")
            print(f"   - Task  (p) : {[round(v, 3) for v in p]}\n")

    except KeyboardInterrupt:
        print("\n\n[알림] 사용자에 의해 티칭이 중단되었습니다.")
    except Exception as e:
        print(f"\n[에러 발생] {e}")
    finally:
        # 5. 안전 종료: 타이머 중지, 그리퍼 OPEN 및 다이렉트 티칭 OFF
        timer_stop_flag.set()
        print("\n[4/4] 안전 종료 처리 중 (그리퍼 OPEN 및 티칭 모드 OFF)...")
        
        # 중지/종료 시 그리퍼 Open
        gripper_open(robot)
        
        try:
            robot.set_direct_teaching(False)
            print("  -> 다이렉트 티칭 모드 OFF (안전 고정 완료)")
        except Exception as e:
            print(f"  [경고] 다이렉트 티칭 OFF 실패: {e}")

    # 6. 결과 요약 출력
    if saved_points:
        print("\n" + "=" * 65)
        print(f"                티칭 결과 요약 (총 {len(saved_points)}개 포인트)")
        print("=" * 65)
        for pt in saved_points:
            idx = pt["index"]
            q_str = ", ".join([f"{v:8.3f}" for v in pt["q"]])
            p_str = ", ".join([f"{v:8.3f}" for v in pt["p"]])
            print(f"Point {idx}:")
            print(f"  Joint q = [{q_str}]  (deg)")
            print(f"  Task  p = [{p_str}]  (mm, deg)")
            print("-" * 65)

        # 파이썬 코드 복사용 포맷 출력
        print("\n[Tip] 추후 자동 운전 스크립트에 바로 복사해서 사용할 수 있는 배열 코드:")
        print("TEACH_POINTS_P = [")
        for pt in saved_points:
            print(f"    {pt['p']},  # Point {pt['index']}")
        print("]")

        print("TEACH_POINTS_Q = [")
        for pt in saved_points:
            print(f"    {pt['q']},  # Point {pt['index']}")
        print("]\n")

if __name__ == '__main__':
    main()
