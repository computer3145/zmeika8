#!/usr/bin/env python3
import random
import tkinter as tk
from collections import deque

CELL_SIZE = 20
COLS = 30
ROWS = 20
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
DELAY = 110

BG_COLOR = "#14181c"
GRID_COLOR = "#1e242a"
SNAKE_HEAD_COLOR = "#50dc64"
SNAKE_BODY_COLOR = "#2da546"
FOOD_COLOR = "#eb4b4b"
TEXT_COLOR = "#f0f0f0"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.pack()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.reset_game()

    def reset_game(self):
        start_x = (COLS // 2) * CELL_SIZE
        start_y = (ROWS // 2) * CELL_SIZE
        self.snake = deque([
            (start_x, start_y),
            (start_x - CELL_SIZE, start_y),
            (start_x - 2 * CELL_SIZE, start_y),
        ])
        self.direction = (CELL_SIZE, 0)
        self.next_direction = self.direction
        self.score = 0
        self.game_over = False
        self.food = self.spawn_food()
        self.game_loop()

    def spawn_food(self):
        while True:
            pos = (
                random.randrange(0, COLS) * CELL_SIZE,
                random.randrange(0, ROWS) * CELL_SIZE,
            )
            if pos not in self.snake:
                return pos

    def on_key_press(self, event):
        key = event.keysym.lower()

        if self.game_over:
            if key == "r":
                self.reset_game()
            elif key == "q":
                self.root.destroy()
            return

        if key in ("up", "w") and self.direction != (0, CELL_SIZE):
            self.next_direction = (0, -CELL_SIZE)
        elif key in ("down", "s") and self.direction != (0, -CELL_SIZE):
            self.next_direction = (0, CELL_SIZE)
        elif key in ("left", "a") and self.direction != (CELL_SIZE, 0):
            self.next_direction = (-CELL_SIZE, 0)
        elif key in ("right", "d") and self.direction != (-CELL_SIZE, 0):
            self.next_direction = (CELL_SIZE, 0)

    def move_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake.popleft()
        self.snake.appendleft((head_x, head_y))

        dx, dy = self.direction
        nx, ny = head_x + dx, head_y + dy
        new_head = (nx, ny)

        hit_wall = nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT
        hit_self = new_head in self.snake

        if hit_wall or hit_self:
            self.game_over = True
            return

        self.snake.appendleft(new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        for x in range(0, WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOR)
        for y in range(0, HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, WIDTH, y, fill=GRID_COLOR)

        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2 - 35,
                text="Игра окончена!", fill=FOOD_COLOR, font=("Arial", 24, "bold")
            )
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2 + 5,
                text=f"Счёт: {self.score}", fill=TEXT_COLOR, font=("Arial", 18, "bold")
            )
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2 + 45,
                text="R — перезапуск, Q — выход", fill=TEXT_COLOR, font=("Arial", 14)
            )
            return

        fx, fy = self.food
        self.canvas.create_rectangle(
            fx + 2, fy + 2, fx + CELL_SIZE - 2, fy + CELL_SIZE - 2,
            fill=FOOD_COLOR, outline=""
        )

        for i, (sx, sy) in enumerate(self.snake):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            self.canvas.create_rectangle(
                sx + 1, sy + 1, sx + CELL_SIZE - 1, sy + CELL_SIZE - 1,
                fill=color, outline=""
            )

        self.canvas.create_text(
            12, 12, anchor="nw", text=f"Счёт: {self.score}",
            fill=TEXT_COLOR, font=("Arial", 14, "bold")
        )

    def game_loop(self):
        if not self.game_over:
            self.move_snake()
        self.draw()
        if not self.game_over:
            self.root.after(DELAY, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
