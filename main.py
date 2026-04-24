import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty

Window.size = (500, 650)

class Paddle(Widget):
    pass

class Ball(Widget):
    velocity = ListProperty([4, -4])

class Brick(Widget):
    def __init__(self, brick_type="normal", **kwargs):
        super().__init__(**kwargs)
        self.brick_type = brick_type
        self.health = 2 if brick_type == "hard" else 1

class GameWidget(Widget):
    score = NumericProperty(0)
    lives = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60)
        self.start_game()

    def start_game(self):
        self.canvas.clear()
        self.bricks = []
        self.score = 0
        self.lives = 3

        # Paddle
        self.paddle = Paddle(size=(120, 15), pos=(200, 20))

        # Ball
        self.ball = Ball(size=(15, 15), pos=(250, 50))

        # Bricks
        for i in range(5):
            for j in range(8):
                btype = random.choice(["normal", "hard", "explosive"])
                brick = Brick(brick_type=btype,
                              size=(50, 20),
                              pos=(j*60+10, 500 - i*30))
                self.bricks.append(brick)

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Paddle
            Color(0, 1, 0)
            Rectangle(pos=self.paddle.pos, size=self.paddle.size)

            # Ball
            Color(1, 1, 1)
            Ellipse(pos=self.ball.pos, size=self.ball.size)

            # Bricks
            for b in self.bricks:
                if b.brick_type == "normal":
                    Color(1, 0, 0)
                elif b.brick_type == "hard":
                    Color(0, 0, 1)
                else:
                    Color(1, 1, 0)
                Rectangle(pos=b.pos, size=b.size)

    def on_touch_move(self, touch):
        self.paddle.center_x = touch.x

    def update(self, dt):
        # Move ball
        self.ball.x += self.ball.velocity[0]
        self.ball.y += self.ball.velocity[1]

        # Wall collision
        if self.ball.x <= 0 or self.ball.right >= self.width:
            self.ball.velocity[0] *= -1
        if self.ball.top >= self.height:
            self.ball.velocity[1] *= -1

        # Paddle collision (skill-based)
        if self.ball.collide_widget(self.paddle):
            offset = (self.ball.center_x - self.paddle.center_x) / (self.paddle.width/2)
            self.ball.velocity[0] = offset * 6
            self.ball.velocity[1] *= -1

        # Missed ball
        if self.ball.y <= 0:
            self.lives -= 1
            self.ball.pos = (250, 50)
            self.ball.velocity = [4, -4]

            if self.lives <= 0:
                self.start_game()

        # Brick collision
        for b in self.bricks[:]:
            if self.ball.collide_widget(b):
                b.health -= 1
                self.ball.velocity[1] *= -1

                if b.health <= 0:
                    if b.brick_type == "explosive":
                        for other in self.bricks[:]:
                            if abs(other.x - b.x) < 60 and abs(other.y - b.y) < 30:
                                if other in self.bricks:
                                    self.bricks.remove(other)
                                    self.score += 10

                    self.bricks.remove(b)
                    self.score += 10

                break

        self.draw()

class BrickBreakerApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    BrickBreakerApp().run()