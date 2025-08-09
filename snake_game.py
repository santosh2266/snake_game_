import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.width, self.height, self.cell = 600, 400, 20
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'Right'
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
        self.master.bind("<KeyPress>", self.change_dir)
        self.update()

    def new_food(self):
        while True:
            x = random.randint(0, (self.width-self.cell)//self.cell) * self.cell
            y = random.randint(0, (self.height-self.cell)//self.cell) * self.cell
            if (x,y) not in self.snake: return (x,y)

    def change_dir(self, event):
        key = event.keysym
        if key in ['Up','Down','Left','Right']:
            if (key == 'Up' and self.direction != 'Down' or
                key == 'Down' and self.direction != 'Up' or
                key == 'Left' and self.direction != 'Right' or
                key == 'Right' and self.direction != 'Left'):
                self.direction = key

    def move(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Up': new = (head_x, head_y-self.cell)
        elif self.direction == 'Down': new = (head_x, head_y+self.cell)
        elif self.direction == 'Left': new = (head_x-self.cell, head_y)
        else: new = (head_x+self.cell, head_y)

        if (new in self.snake or new[0]<0 or new[0]>=self.width or new[1]<0 or new[1]>=self.height):
            self.game_over = True
            return

        self.snake.insert(0, new)
        if new == self.food:
            self.score += 1
            self.food = self.new_food()
        else: self.snake.pop()

    def draw(self):
        self.canvas.delete('all')
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill='white')
        for x,y in self.snake:
            self.canvas.create_rectangle(x, y, x+self.cell, y+self.cell, fill='green')
        fx,fy = self.food
        self.canvas.create_oval(fx, fy, fx+self.cell, fy+self.cell, fill='red')
        if self.game_over:
            self.canvas.create_text(self.width//2, self.height//2, text="GAME OVER!", fill='white', font=('Arial', 30))
            self.canvas.create_text(self.width//2, self.height//2+40, text="Press R to restart", fill='white')

    def update(self):
        if not self.game_over:
            self.move()
            self.draw()
            self.master.after(150, self.update)
        else: self.master.bind('r', lambda e: self.restart())

    def restart(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'Right'
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
        self.master.unbind('r')
        self.update()

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()