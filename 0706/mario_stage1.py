"""
파이썬 + pygame으로 만든 슈퍼마리오 스타일 1-1 스테이지 플랫포머
------------------------------------------------------------
* 실행 전 설치 필요: pip install pygame   (안 되면 pip install pygame-ce)
* 실행: python mario_stage1.py

조작법
  ← / A : 왼쪽 이동
  → / D : 오른쪽 이동
  Shift : 달리기(이동 속도 증가)
  Space / ↑ / W : 점프
  F : 불꽃 발사 (파이어 파워를 먹었을 때만)
  R : 게임오버/클리어 후 재시작
  ESC : 종료

아이템
  - 버섯 : 물음표 박스에서 나오며 먹으면 캐릭터가 커집니다(1대 맞아도 생존).
  - 불꽃 해바라기 : 물음표 박스에서 나오며 먹으면 커진 상태 + 불꽃(F 키)을
    발사해 적을 멀리서 처치할 수 있습니다.
  - 커진 상태에서 적과 부딪히면 죽지 않고 작아지기만 합니다.
  - 커진 상태에서 벽돌(B) 블록을 아래에서 치면 블록이 부서집니다.

* 실제 닌텐도 스프라이트 대신 단순한 도형으로 캐릭터/타일을 표현했습니다.
"""

import sys
import pygame

# ============================================================
# 1. 기본 설정
# ============================================================
pygame.init()

TILE = 32
SCREEN_W, SCREEN_H = 800, 480
FPS = 60
GRAVITY = 0.55

SKY_BLUE = (92, 148, 252)
GROUND_BROWN = (156, 74, 34)
GROUND_TOP = (100, 200, 60)
BRICK_COLOR = (198, 90, 40)
QUESTION_COLOR = (240, 180, 40)
QUESTION_USED = (140, 100, 60)
PIPE_GREEN = (0, 150, 0)
PIPE_DARK = (0, 100, 0)
COIN_COLOR = (255, 215, 0)
GOOMBA_COLOR = (150, 75, 0)
GOOMBA_DARK = (90, 45, 0)
PLAYER_RED = (220, 30, 30)
PLAYER_WHITE = (250, 250, 250)
PLAYER_SKIN = (255, 200, 150)
FLAG_COLOR = (255, 255, 255)
POLE_COLOR = (200, 200, 200)
MUSHROOM_RED = (230, 40, 40)
MUSHROOM_CREAM = (255, 235, 210)
SUNFLOWER_GREEN = (40, 160, 40)
SUNFLOWER_PETAL = (255, 200, 30)
SUNFLOWER_CENTER = (200, 90, 30)
FIRE_OUTER = (255, 110, 0)
FIRE_INNER = (255, 220, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Python Platformer - Stage 1")
clock = pygame.time.Clock()

try:
    font = pygame.font.SysFont("malgungothic", 24)
    big_font = pygame.font.SysFont("malgungothic", 60)
except Exception:
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 60)

# ============================================================
# 2. 스테이지(레벨) 자동 생성
# ============================================================
LEVEL_COLS = 180
LEVEL_ROWS = 15
GROUND_ROW = 12  # 이 행부터 아래는 지면

grid = [['-' for _ in range(LEVEL_COLS)] for _ in range(LEVEL_ROWS)]

PITS = [(35, 38), (70, 72), (110, 113), (150, 153)]


def in_pit(col):
    return any(a <= col <= b for a, b in PITS)


for col in range(LEVEL_COLS):
    if not in_pit(col):
        for row in range(GROUND_ROW, LEVEL_ROWS):
            grid[row][col] = 'X'

PIPES = [(20, 2), (45, 3), (85, 2), (130, 4)]
for col, height in PIPES:
    if not in_pit(col):
        for h in range(height):
            row = GROUND_ROW - 1 - h
            grid[row][col] = 'P'
            grid[row][col + 1] = 'P'

STAIR_START = LEVEL_COLS - 20
for i in range(6):
    col = STAIR_START + i
    for h in range(i + 1):
        row = GROUND_ROW - 1 - h
        if 0 <= row < LEVEL_ROWS:
            grid[row][col] = 'X'

# 물음표 블록 / 벽돌 배치 + 물음표 블록 내용물 지정
QUESTION_COLS = [10, 11, 12, 25, 55, 60, 95, 100, 140]
question_content = {}
for i, col in enumerate(QUESTION_COLS):
    if not in_pit(col) and col < LEVEL_COLS:
        if i % 2 == 0:
            grid[GROUND_ROW - 4][col] = '?'
            question_content[col] = 'coin'
        else:
            grid[GROUND_ROW - 4][col] = 'B'

# 특정 물음표 박스에 버섯 / 불꽃 해바라기 배정
if 10 in question_content:
    question_content[10] = 'mushroom'
if 55 in question_content:
    question_content[55] = 'fire'
if 95 in question_content:
    question_content[95] = 'mushroom'

COIN_POSITIONS = []
for col in range(5, LEVEL_COLS - 25, 7):
    if not in_pit(col) and grid[GROUND_ROW - 4][col] == '-' and grid[GROUND_ROW - 5][col] == '-':
        COIN_POSITIONS.append((col, GROUND_ROW - 5))

PIPE_COLS = set()
for col, _h in PIPES:
    PIPE_COLS.add(col)
    PIPE_COLS.add(col + 1)

GOOMBA_COLS = []
for col in range(15, LEVEL_COLS - 25, 12):
    if in_pit(col):
        continue
    if any(abs(col - pc) <= 1 for pc in PIPE_COLS):
        continue
    GOOMBA_COLS.append(col)

FLAG_COL = LEVEL_COLS - 6
for h in range(8):
    row = GROUND_ROW - 1 - h
    if 0 <= row < LEVEL_ROWS:
        grid[row][FLAG_COL] = 'F'

LEVEL_WIDTH_PX = LEVEL_COLS * TILE
LEVEL_HEIGHT_PX = LEVEL_ROWS * TILE

# ============================================================
# 3. 타일 Rect 목록
# ============================================================
ALL_SOLID_TILES = []      # 항상 고정인 타일들 (X, P) - 절대 사라지지 않음
ALL_BRICK_TILES = []      # 벽돌(B) - 커진 상태로 부수면 사라짐
question_tiles = []        # [rect, used_flag, content]
flag_rects = []

for row in range(LEVEL_ROWS):
    for col in range(LEVEL_COLS):
        c = grid[row][col]
        rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
        if c == 'X' or c == 'P':
            ALL_SOLID_TILES.append(rect)
        elif c == 'B':
            ALL_BRICK_TILES.append(rect)
        elif c == '?':
            content = question_content.get(col, 'coin')
            question_tiles.append([rect, False, content])
        elif c == 'F':
            flag_rects.append(rect)

flag_trigger_rect = pygame.Rect(FLAG_COL * TILE, 0, TILE, LEVEL_HEIGHT_PX)

# 실제 플레이 중 사용하는 리스트 (매 판마다 초기 상태로 리셋됨)
solid_tiles = []
brick_tiles = []


def reset_level_state():
    global solid_tiles, brick_tiles
    solid_tiles = list(ALL_SOLID_TILES) + [q[0] for q in question_tiles]
    brick_tiles = list(ALL_BRICK_TILES)
    solid_tiles += brick_tiles
    for q in question_tiles:
        q[1] = False


# ============================================================
# 4. 플레이어
# ============================================================
SMALL_H = 30
BIG_H = 44


class Player:
    def __init__(self):
        self.w = 28
        self.reset_full()

    def reset_full(self):
        self.w = 28
        self.h = SMALL_H
        self.x = 2 * TILE
        self.y = (GROUND_ROW - 1) * TILE
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing_right = True
        self.lives = 3
        self.score = 0
        self.coins = 0
        self.power = 0          # 0=작음, 1=커짐(버섯), 2=파이어(해바라기)
        self.alive = True
        self.win = False
        self.invincible_timer = 0
        self.shoot_cooldown = 0

    def reset_position(self):
        old_bottom_unused = None
        self.h = SMALL_H if self.power == 0 else self.h
        self.x = 2 * TILE
        self.y = (GROUND_ROW - 1) * TILE - (self.h - SMALL_H)
        self.vx = 0.0
        self.vy = 0.0
        self.invincible_timer = 90

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def grow_to(self, level):
        """버섯(1) / 불꽃 해바라기(2)를 먹었을 때 파워 레벨 상승"""
        if level <= self.power:
            self.power = level
            return
        old_bottom = self.y + self.h
        self.power = level
        self.h = BIG_H if level >= 1 else SMALL_H
        self.y = old_bottom - self.h

    def shrink(self):
        old_bottom = self.y + self.h
        self.power = 0
        self.h = SMALL_H
        self.y = old_bottom - self.h

    def hit_by_enemy(self):
        if self.invincible_timer > 0:
            return
        if self.power > 0:
            self.shrink()
            self.invincible_timer = 100
        else:
            self.die()

    def die(self):
        if self.invincible_timer > 0:
            return
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
        else:
            self.power = 0
            self.reset_position()

    def update(self, keys, spawn_events):
        SPEED = 4.2
        RUN_SPEED = 6.5
        JUMP_STRENGTH = -12.5
        MAX_FALL = 12

        run = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        move_speed = RUN_SPEED if run else SPEED

        self.vx = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -move_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = move_speed
            self.facing_right = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False

        self.vy += GRAVITY
        if self.vy > MAX_FALL:
            self.vy = MAX_FALL

        # --- 수평 이동 & 충돌 ---
        self.x += self.vx
        self.x = max(0, min(self.x, LEVEL_WIDTH_PX - self.w))
        my_rect = self.rect
        for tile in solid_tiles:
            if my_rect.colliderect(tile):
                if self.vx > 0:
                    self.x = tile.left - self.w
                elif self.vx < 0:
                    self.x = tile.right
                my_rect = self.rect

        # --- 수직 이동 & 충돌 ---
        self.y += self.vy
        my_rect = self.rect
        self.on_ground = False

        # 벽돌 블록 (커지면 부술 수 있음)
        for tile in list(brick_tiles):
            if my_rect.colliderect(tile):
                if self.vy < 0:
                    if self.power >= 1:
                        brick_tiles.remove(tile)
                        if tile in solid_tiles:
                            solid_tiles.remove(tile)
                        self.score += 50
                    else:
                        self.y = tile.bottom
                        self.vy = 0
                elif self.vy > 0:
                    self.y = tile.top - self.h
                    self.vy = 0
                    self.on_ground = True
                my_rect = self.rect

        # 물음표 블록
        for q in question_tiles:
            tile = q[0]
            if my_rect.colliderect(tile):
                if self.vy < 0:
                    self.y = tile.bottom
                    self.vy = 0
                    if not q[1]:
                        q[1] = True
                        content = q[2]
                        if content == 'coin':
                            self.score += 100
                            self.coins += 1
                        else:
                            spawn_events.append((content, tile))
                            self.score += 50
                elif self.vy > 0:
                    self.y = tile.top - self.h
                    self.vy = 0
                    self.on_ground = True
                my_rect = self.rect

        # 그 외 고정 지형(땅, 파이프)
        for tile in ALL_SOLID_TILES:
            if my_rect.colliderect(tile):
                if self.vy > 0:
                    self.y = tile.top - self.h
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = tile.bottom
                    self.vy = 0
                my_rect = self.rect

        if self.y > LEVEL_HEIGHT_PX:
            self.die()

        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if my_rect.colliderect(flag_trigger_rect) and not self.win:
            self.win = True

    def draw(self, surface, cam_x):
        if self.invincible_timer > 0 and self.invincible_timer % 10 < 5:
            return
        r = self.rect
        dr = pygame.Rect(r.x - cam_x, r.y, r.w, r.h)
        body_color = PLAYER_WHITE if self.power == 2 else PLAYER_RED
        pygame.draw.rect(surface, body_color, dr)
        face_w = 12
        face_x = dr.x + (dr.w - face_w) // 2
        pygame.draw.rect(surface, PLAYER_SKIN, (face_x, dr.y + 4, face_w, 10))


# ============================================================
# 5. 굼바 (적)
# ============================================================
class Goomba:
    def __init__(self, col):
        self.w, self.h = 28, 26
        self.x = float(col * TILE)
        self.y = float((GROUND_ROW - 1) * TILE + 4)
        self.vx = -1.5
        self.alive = True
        self.squish_timer = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        if not self.alive:
            self.squish_timer -= 1
            return

        self.x += self.vx
        my_rect = self.rect

        for tile in solid_tiles:
            if my_rect.colliderect(tile):
                self.vx *= -1
                self.x += self.vx * 2
                break

        ahead_x = self.x + (self.w + 2 if self.vx > 0 else -6)
        ahead_rect = pygame.Rect(int(ahead_x), int(self.y + self.h + 2), 4, 4)
        has_ground = any(ahead_rect.colliderect(t) for t in solid_tiles)
        if not has_ground:
            self.vx *= -1

    def draw(self, surface, cam_x):
        if not self.alive and self.squish_timer <= 0:
            return
        r = self.rect
        h = self.h if self.alive else 8
        y_off = 0 if self.alive else self.h - 8
        dr = pygame.Rect(r.x - cam_x, r.y + y_off, r.w, h)
        color = GOOMBA_COLOR if self.alive else GOOMBA_DARK
        pygame.draw.rect(surface, color, dr)
        if self.alive:
            eye_y = dr.y + 6
            pygame.draw.circle(surface, BLACK, (dr.x + 8, eye_y), 3)
            pygame.draw.circle(surface, BLACK, (dr.x + r.w - 8, eye_y), 3)


# ============================================================
# 6. 아이템 (버섯 / 불꽃 해바라기)
# ============================================================
class Item:
    def __init__(self, block_rect, kind):
        self.kind = kind  # 'mushroom' or 'fire'
        self.w, self.h = 26, 26
        self.x = float(block_rect.x + (TILE - self.w) // 2)
        self.y = float(block_rect.top - self.h)
        self.vx = 1.3 if kind == 'mushroom' else 0.0
        self.vy = -3.0
        self.active = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.vy += GRAVITY
        if self.vy > 10:
            self.vy = 10

        if self.kind == 'mushroom':
            self.x += self.vx
            my_rect = self.rect
            for tile in solid_tiles:
                if my_rect.colliderect(tile):
                    self.vx *= -1
                    self.x += self.vx * 2
                    my_rect = self.rect

        self.y += self.vy
        my_rect = self.rect
        for tile in solid_tiles:
            if my_rect.colliderect(tile):
                if self.vy > 0:
                    self.y = tile.top - self.h
                    self.vy = 0
                elif self.vy < 0:
                    self.y = tile.bottom
                    self.vy = 0
                my_rect = self.rect

        if self.y > LEVEL_HEIGHT_PX:
            self.active = False

    def draw(self, surface, cam_x):
        r = self.rect
        dr = pygame.Rect(r.x - cam_x, r.y, r.w, r.h)
        if dr.right < 0 or dr.left > SCREEN_W:
            return
        if self.kind == 'mushroom':
            pygame.draw.rect(surface, MUSHROOM_CREAM, (dr.x + 4, dr.y + 12, dr.w - 8, dr.h - 12))
            pygame.draw.ellipse(surface, MUSHROOM_RED, (dr.x, dr.y, dr.w, dr.h * 0.75))
            pygame.draw.circle(surface, MUSHROOM_CREAM, (dr.x + 6, dr.y + 8), 4)
            pygame.draw.circle(surface, MUSHROOM_CREAM, (dr.x + dr.w - 6, dr.y + 8), 4)
        else:  # fire sunflower
            pygame.draw.rect(surface, SUNFLOWER_GREEN, (dr.x + dr.w // 2 - 2, dr.y + dr.h - 10, 4, 10))
            pygame.draw.circle(surface, SUNFLOWER_PETAL, dr.center, 12)
            pygame.draw.circle(surface, SUNFLOWER_CENTER, dr.center, 6)


# ============================================================
# 7. 불꽃 (파이어볼)
# ============================================================
class Fireball:
    def __init__(self, x, y, direction):
        self.w, self.h = 14, 14
        self.x = float(x)
        self.y = float(y)
        self.vx = 7.0 * direction
        self.vy = -4.0
        self.active = True
        self.bounces = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.vy += GRAVITY
        if self.vy > 10:
            self.vy = 10
        self.x += self.vx
        self.y += self.vy
        my_rect = self.rect
        for tile in solid_tiles:
            if my_rect.colliderect(tile):
                if self.vy > 0:
                    self.y = tile.top - self.h
                    self.vy = -7.0
                    self.bounces += 1
                else:
                    self.active = False
                my_rect = self.rect
                break
        if self.bounces > 4 or self.x < 0 or self.x > LEVEL_WIDTH_PX or self.y > LEVEL_HEIGHT_PX:
            self.active = False

    def draw(self, surface, cam_x):
        r = self.rect
        dr = pygame.Rect(r.x - cam_x, r.y, r.w, r.h)
        pygame.draw.circle(surface, FIRE_OUTER, dr.center, 7)
        pygame.draw.circle(surface, FIRE_INNER, dr.center, 4)


# ============================================================
# 8. 그리기 함수 (지형)
# ============================================================
def draw_tile(surface, char, rect, cam_x, used=False):
    dr = pygame.Rect(rect.x - cam_x, rect.y, rect.w, rect.h)
    if dr.right < 0 or dr.left > SCREEN_W:
        return
    if char == 'X':
        pygame.draw.rect(surface, GROUND_BROWN, dr)
        pygame.draw.rect(surface, GROUND_TOP, (dr.x, dr.y, dr.w, 6))
    elif char == 'B':
        pygame.draw.rect(surface, BRICK_COLOR, dr)
        pygame.draw.line(surface, BLACK, (dr.x, dr.y + dr.h // 2), (dr.x + dr.w, dr.y + dr.h // 2))
    elif char == '?':
        color = QUESTION_USED if used else QUESTION_COLOR
        pygame.draw.rect(surface, color, dr)
        if not used:
            text = font.render("?", True, BLACK)
            surface.blit(text, (dr.x + 9, dr.y + 2))
    elif char == 'P':
        pygame.draw.rect(surface, PIPE_GREEN, dr)
        pygame.draw.rect(surface, PIPE_DARK, dr, 3)


def draw_level(surface, cam_x):
    start_col = max(0, cam_x // TILE - 1)
    end_col = min(LEVEL_COLS, (cam_x + SCREEN_W) // TILE + 2)
    for row in range(LEVEL_ROWS):
        for col in range(start_col, end_col):
            c = grid[row][col]
            if c == 'X' or c == 'P':
                rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
                draw_tile(surface, c, rect, cam_x)

    for tile in brick_tiles:
        draw_tile(surface, 'B', tile, cam_x)

    for q in question_tiles:
        draw_tile(surface, '?', q[0], cam_x, q[1])

    if flag_rects:
        top = min(r.y for r in flag_rects)
        bottom = max(r.y + TILE for r in flag_rects)
        pole_x = flag_rects[0].x + TILE // 2 - cam_x
        pygame.draw.line(surface, POLE_COLOR, (pole_x, top), (pole_x, bottom), 4)
        pygame.draw.polygon(surface, FLAG_COLOR,
                             [(pole_x, top), (pole_x + 22, top + 10), (pole_x, top + 20)])


def draw_coins(surface, cam_x, coins_remaining):
    for col, row in coins_remaining:
        cx = col * TILE + TILE // 2 - cam_x
        cy = row * TILE + TILE // 2
        if -20 < cx < SCREEN_W + 20:
            pygame.draw.circle(surface, COIN_COLOR, (cx, cy), 9)
            pygame.draw.circle(surface, BLACK, (cx, cy), 9, 1)


def draw_hud(surface, player):
    power_name = {0: "작음", 1: "커짐", 2: "파이어"}[player.power]
    score_text = font.render(f"점수: {player.score}", True, WHITE)
    coin_text = font.render(f"코인: {player.coins}", True, WHITE)
    life_text = font.render(f"생명: {player.lives}", True, WHITE)
    power_text = font.render(f"파워: {power_name}", True, WHITE)
    surface.blit(score_text, (20, 15))
    surface.blit(coin_text, (200, 15))
    surface.blit(life_text, (360, 15))
    surface.blit(power_text, (500, 15))


# ============================================================
# 9. 게임 루프
# ============================================================
def run_game():
    """게임 한 판을 실행. 'quit' 또는 'restart'를 반환한다."""
    reset_level_state()

    player = Player()
    goombas = [Goomba(col) for col in GOOMBA_COLS]
    coins_remaining = [list(pos) for pos in COIN_POSITIONS]
    items = []
    fireballs = []

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_r and (not player.alive or player.win):
                    return "restart"
                if event.key == pygame.K_f and player.alive and not player.win:
                    if player.power == 2 and player.shoot_cooldown == 0 and len(fireballs) < 2:
                        direction = 1 if player.facing_right else -1
                        fx = player.x + (player.w if direction > 0 else -14)
                        fy = player.y + player.h / 2
                        fireballs.append(Fireball(fx, fy, direction))
                        player.shoot_cooldown = 20

        keys = pygame.key.get_pressed()

        if player.alive and not player.win:
            spawn_events = []
            player.update(keys, spawn_events)

            for kind, tile in spawn_events:
                items.append(Item(tile, kind))

            for g in goombas:
                g.update()
            for it in items:
                it.update()
            for fb in fireballs:
                fb.update()

            # 플레이어 - 굼바
            p_rect = player.rect
            for g in goombas:
                if g.alive and p_rect.colliderect(g.rect):
                    if player.vy > 0 and p_rect.bottom - g.rect.top < 14:
                        g.alive = False
                        g.squish_timer = 20
                        player.vy = -8
                        player.score += 100
                    else:
                        player.hit_by_enemy()

            # 플레이어 - 아이템
            p_rect = player.rect
            for it in items:
                if it.active and p_rect.colliderect(it.rect):
                    it.active = False
                    if it.kind == 'mushroom':
                        player.grow_to(1)
                    else:
                        player.grow_to(2)
                    player.score += 1000

            # 파이어볼 - 굼바
            for fb in fireballs:
                if fb.active:
                    for g in goombas:
                        if g.alive and fb.rect.colliderect(g.rect):
                            g.alive = False
                            g.squish_timer = 20
                            fb.active = False
                            player.score += 100

            # 동전 획득
            p_rect = player.rect
            for coin in coins_remaining[:]:
                col, row = coin
                coin_rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
                if p_rect.colliderect(coin_rect):
                    coins_remaining.remove(coin)
                    player.coins += 1
                    player.score += 50

            items = [it for it in items if it.active]
            fireballs = [fb for fb in fireballs if fb.active]

        cam_x = int(player.x) - SCREEN_W // 3
        cam_x = max(0, min(cam_x, LEVEL_WIDTH_PX - SCREEN_W))

        screen.fill(SKY_BLUE)
        draw_level(screen, cam_x)
        draw_coins(screen, cam_x, coins_remaining)
        for it in items:
            it.draw(screen, cam_x)
        for g in goombas:
            g.draw(screen, cam_x)
        for fb in fireballs:
            fb.draw(screen, cam_x)
        player.draw(screen, cam_x)
        draw_hud(screen, player)

        if not player.alive:
            msg = big_font.render("GAME OVER", True, (255, 50, 50))
            sub = font.render("R 키를 눌러 재시작 / ESC 키로 종료", True, WHITE)
            screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 40))
            screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, SCREEN_H // 2 + 30))
        elif player.win:
            msg = big_font.render("STAGE CLEAR!", True, (255, 220, 40))
            sub = font.render(f"최종 점수: {player.score}   R 키를 눌러 재시작", True, WHITE)
            screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 40))
            screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, SCREEN_H // 2 + 30))

        pygame.display.flip()


def main():
    while True:
        result = run_game()
        if result != "restart":
            break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
