import pygame
import random

# 게임 보드 크기
BOARD_WIDTH = 15
BOARD_HEIGHT = 22
BLOCK_SIZE = 30

# 블록들의 모양
SHAPES = [
    [[1, 1, 1, 1]],  # 직선 블록
    [[1, 1, 1], [0, 1, 0]],  # T 블록
    [[1, 1, 1], [1, 0, 0]],  # L 블록
    [[1, 1, 1], [0, 0, 1]],  # J 블록
    [[1, 1], [1, 1]],  # 사각형 블록
    [[1, 1, 0], [0, 1, 1]],  # Z 블록
    [[0, 1, 1], [1, 1, 0]]   # S 블록
]

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_block = self.new_block()
        self.score = 0

    def new_block(self):
        return {
            'shape': random.choice(SHAPES),
            'x': BOARD_WIDTH // 2 - 2,
            'y': 0
        }

    def draw_block(self, x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    pygame.draw.rect(self.screen, COLORS[random.randint(1, len(COLORS) - 1)],
                                     pygame.Rect((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, BLACK, pygame.Rect((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

    def draw_board(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(self.screen, COLORS[self.board[y][x]],
                                     pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

    def check_collision(self, x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] and ((x + j < 0 or x + j >= BOARD_WIDTH) or (y + i >= BOARD_HEIGHT) or (y + i >= 0 and self.board[y + i][x + j])):
                    return True
        return False

    def merge_block(self):
        for i in range(len(self.current_block['shape'])):
            for j in range(len(self.current_block['shape'][i])):
                if self.current_block['shape'][i][j]:
                    block_y = self.current_block['y'] + i
                    block_x = self.current_block['x'] + j
                    if 0 <= block_y < BOARD_HEIGHT and 0 <= block_x < BOARD_WIDTH:
                        self.board[block_y][block_x] = random.randint(1, len(COLORS) - 1)

    # 블록이 보드의 가장 아래에 닿았는지 확인
        if self.current_block['y'] + len(self.current_block['shape']) >= BOARD_HEIGHT:
            self.current_block['y'] = BOARD_HEIGHT - len(self.current_block['shape'])  # 블록 위치 보정
            self.merge_block()
            self.remove_lines()
            self.current_block = self.new_block()
            

    def remove_lines(self):
        lines_removed = 0
        for i in range(BOARD_HEIGHT - 1, -1, -1):
            if all(self.board[i]):
                del self.board[i]
                self.board.insert(0, [0] * BOARD_WIDTH)
                lines_removed += 1
        self.score += lines_removed * 100

    def game_over(self):
        return any(self.board[0]) or self.current_block['y'] <= 0

    def run(self):
        while True:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and not self.check_collision(self.current_block['x'] - 1, self.current_block['y'], self.current_block['shape']):
                self.current_block['x'] -= 1
            if keys[pygame.K_RIGHT] and not self.check_collision(self.current_block['x'] + 1, self.current_block['y'], self.current_block['shape']):
                self.current_block['x'] += 1
            if keys[pygame.K_DOWN]:
                if not self.check_collision(self.current_block['x'], self.current_block['y'] + 1, self.current_block['shape']):
                    self.current_block['y'] += 1
            if keys[pygame.K_UP]:
                rotated_block = [list(reversed(row)) for row in zip(*self.current_block['shape'])]
                if not self.check_collision(self.current_block['x'], self.current_block['y'], rotated_block):
                    self.current_block['shape'] = rotated_block
            if keys[pygame.K_SPACE]:
                while not self.check_collision(self.current_block['x'], self.current_block['y'] + 1, self.current_block['shape']):
                    self.current_block['y'] += 1

            if not self.check_collision(self.current_block['x'], self.current_block['y'] + 1, self.current_block['shape']):
                self.current_block['y'] += 1
            else:
                # 블록이 바닥에 닿았을 때 현재 블록을 보드에 병합하고 새로운 블록 생성
                self.merge_block()
                self.remove_lines()
                self.current_block = self.new_block()
                # 새로운 블록 생성 후에도 게임 종료 조건 확인
                if self.game_over():
                    pygame.quit()
                    return

            self.draw_board()
            self.draw_block(self.current_block['x'], self.current_block['y'], self.current_block['shape'])

            pygame.display.flip()
            self.clock.tick(5)  # 게임의 속도를 절반으로 늦추기 위해 tick 값 수정


if __name__ == '__main__':
    Tetris().run()
