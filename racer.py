import turtle
from turtle import *
import random
import time
import colorama
import winsound
import math
import platform
from pygame import mixer

# Play background music
mixer.init()
mixer.music.load("background.mp3")
mixer.music.play()

# Game Window
wn = Screen()
wn.bgcolor("white")
wn.title("Racer Game")
WIN_WIDTH = 460
WIN_HEIGHT = 650
wn.setup(460, 650)
# 275
wn.listen()
wn.tracer(0)

# Import The Sound Module That Our System Has
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound isn't available on your system.")
elif platform.system() == "Mac" or platform.system() == "Linux":
    try:
        import os
    except:
        print("Os isn't available in your system")

# Utility Functions
def playsound(soundfile, time = 0):
    # Windows
    if platform.system() == "Windows":
        winsound.PlaySound(soundfile, winsound.SND_ASYNC)
    # Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(soundfile))
    # Mac
    else:
        os.system("afplay {}&".format(soundfile))
    #
    # # Repeat Music
    # if time > 0:
    #     wn.ontimer(lambda: playsound(soundfile, time), t=int(time * 1000))


# Register Shapes
wn.register_shape("road.gif")
wn.register_shape("car.gif")
wn.register_shape("roadrect.gif")
wn.register_shape("heart.gif")

# Global Variables
speed_count = 0.005
score_increase_value = 0.2
common_speed = -4
car_width = 60
car_height = 80

# Global Arrays
coin_frames = ["coin1.gif","coin2.gif", "coin3.gif", "coin4.gif", "coin5.gif", "coin6.gif","coin7.gif", "coin6.gif", "coin5.gif", "coin4.gif","coin3.gif","coin2.gif",]
colors = ["red", "black", "yellow", "green", "blue", "lightblue", "purple", "pink", "magenta", "cyan"]
enemycars = ["enemycar1.gif", "enemycar2.gif", "enemycar3.gif"]

# Register Shapes From Global Arrays
for coin_frame in coin_frames:
    wn.register_shape(coin_frame)

for enemycar in enemycars:
    wn.register_shape(enemycar)

# -------- Classes ---------

class Sprite(Turtle):
    def __init__(self, shapestyle, x, y, width, height):
        super().__init__()
        self.speed(0)
        self.penup()
        self.shape(shapestyle)
        self.goto(x, y)
        self.width = width
        self.height = height

    def isCollision(self, other):
        if self.xcor() - 45 <= other.xcor() <= self.xcor() + 45 and \
            self.ycor() - 77 <= other.ycor() <= self.ycor() + 77:
            return True
        else:
            return False

    def isCollision2(self, other):
        x_collision = (math.fabs(self.xcor() - other.xcor()) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.ycor() - other.ycor()) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Player(Sprite):
    def __init__(self, shapestyle, x, y):
        super().__init__(shapestyle, x, y, width = car_width, height = car_height)
        self.speed = 0

    def turn_right(self):
        self.speed = 10

    def turn_left(self):
        self.speed = -10

    def move(self):
        # Move the player
        self.setx(self.xcor() + self.speed)

        # Check If Player is in the center
        if self.xcor() - 10 < 0 < self.xcor() + 10:
            self.speed = 0

        # Collision With Walls
        if self.xcor() > 150:
            self.setx(150)
        elif self.xcor() < -150:
            self.setx(-150)

class Enemy(Sprite):
    def __init__(self, shapestyle, x, y):
        super().__init__(shapestyle, x, y, width = car_width, height = car_height)
        self.right(90)
        self.shapesize(1.8, 2.1)
        self.speed = common_speed

    def move(self):
        self.sety(self.ycor() + self.speed)

        # Collision checker
        if self.ycor() < -350:
            self.sety(370)
            self.setx(random.choice([-150, 0, 150]))
            self.shape(random.choice(enemycars))

class PlayerScore(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.goto(x, y)

        self.score = 0

    def update(self):
        self.clear()
        self.write(f"Score: {math.floor(self.score)}", font=("Arial", 20, "normal"))

class CoinScore(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.goto(x, y)

        self.coins_collected = 0

    def update(self):
        self.clear()
        self.write(f": {self.coins_collected}", font=("Arial", 25, "normal"))

class Lives(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.goto(x, y)

        self.lives = 0

    def update(self):
        self.clear()
        self.write(f": {self.lives}", align="center", font=("Arial", 25, "normal"))

class EndScreenText(Turtle):
    def __init__(self, x, y, text, size, font_weight):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.goto(x, y)
        self.write(text, align="center", font=("Arial", size, font_weight))

coin_frame = 0
class Coin(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.speed(0)
        self.speed = common_speed
        self.penup()
        self.shape("coin1.gif")
        self.animate()
        self.goto(x, y)
        self.width = 0
        self.height = 0

    def animate(self):
        global coin_frame
        coin_frame += 1

        if coin_frame >= len(coin_frames):
            coin_frame = 0

        self.shape(coin_frames[coin_frame])

        wn.ontimer(self.animate, 50)

    def move(self):
        self.sety(self.ycor() + self.speed)

        # Collision checker
        if self.ycor() < -350:
            self.sety(370)
            self.setx(random.choice([-150, 0, 150]))

        # Collision between player and coin
        if player.isCollision2(coin):
            self.setx(1000)
            playsound("coin.wav")
            coin_score.coins_collected += 1

class Heart(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.speed(0)
        self.speed = common_speed
        self.penup()
        self.shape("heart.gif")
        self.goto(x, y)
        self.width = 0
        self.height = 0

    def move(self):
        global lives

        self.sety(self.ycor() + self.speed)

        # Collision checker
        if self.ycor() < -360:
            self.sety(5000)
            self.setx(random.choice([-150, 0, 150]))

        # # Collision between player and heart
        if player.isCollision2(heart):
            self.setx(1000)
            playsound("powerup.wav")
            lives.lives += 1

class Game():
    def __init__(self):
        self.status = "playing"

    def restart(self):
        global speed_count
        global common_speed
        global score_increase_value
        global game_over_text
        global score_text
        global coins_collected_image
        global coins_collected_text
        global heart
        global play_again_text

        # Draw Status
        game_over_text.clear()
        score_text.clear()
        coins_collected_image.clear()
        coins_collected_text.clear()
        coins_collected_image.hideturtle()
        play_again_text.clear()

        # Change Everything to 0
        player_score.score = 0
        coin_score.coins_collected = 0

        # Change The Place Of All Sprites
        coin.goto(random.choice([-150, 0, 150]), random.choice([0, 200]))
        heart.goto(random.choice([-150, 0, 150]), random.choice([1000, 1200, 1400]))

        # Change The Enemies
        enemy_y = 0
        for enemy in enemies:
            x = random.choice([-150, 0, 150])
            enemy_y += 200
            y = enemy_y
            enemy.goto(x, y)
            enemy.shape(random.choice(enemycars))

        # return all the keyboard bindings
        wn.onkeypress(player.turn_right, "Right")
        wn.onkeypress(player.turn_left, "Left")

        # Sound
        mixer.music.load("background.wav")
        mixer.music.play()

        # Stop everything on the screen
        for enemy in enemies:
            enemy.speed = -common_speed
        for rect in rects:
            rect.sety(rect.ycor() + (common_speed - 2))
        coin.speed = -common_speed
        heart.speed = -common_speed
        speed_count = 0.005
        common_speed = -4
        score_increase_value = 0.2

        wn.onkeypress(lambda: "", "space")

    def lose(self):
        global speed_count
        global common_speed
        global score_increase_value
        global game_over_text
        global score_text
        global coins_collected_image
        global coins_collected_text
        global heart
        global play_again_text

        lives.lives = 0

        wn.onkeypress(lambda: "", "Right")
        wn.onkeypress(lambda: "", "Left")

        # Sound
        mixer.music.pause()
        playsound("lose.wav")

        # Draw Status
        game_over_text = EndScreenText(0, 25, "GAME OVER", 30, "bold")
        score_text = EndScreenText(0, -9, f"Score: {math.floor(player_score.score)}", 20, "normal")
        coins_collected_image = Sprite("coin2.gif", -20, -45, 0, 0)
        coins_collected_text = EndScreenText(20, -50, f": {coin_score.coins_collected}", 20, "normal")
        play_again_text = EndScreenText(0, -90, 'PRESS "SPACE" TO START AGAIN', 17, "normal")

        # Stop everything on the screen
        for enemy in enemies:
             enemy.speed = 0
        for rect in rects:
             rect.sety(rect.ycor())
        coin.speed = 0
        heart.speed = 0
        speed_count = 0
        common_speed = 2
        score_increase_value = 0

        wn.onkeypress(game.restart, "space")

# Create a game class
game = Game()

# Create Sprites
road = Sprite("road.gif", 15, -30, 0, 0)

# Road Rectangles
rects = []
for i in range(0, 12):
     rects.append(Sprite("roadrect.gif", -9, i * WIN_HEIGHT / 8, 0, 0))
     rects[i].color("white")
     rects[i].shapesize(1.7, 1)

player = Player("car.gif", 0, -230)
player.shapesize(2, 2)

# Enemies
enemy_amount = 3
enemies = []
enemy_num = 0
enemy_start_x = -155
enemy_start_y = 500

for i in range(0, enemy_amount):
    y = enemy_start_y
    x = random.choice([-150, 0, 150])
    enemy_num += 1
    enemies.append(Enemy(random.choice(enemycars), x, y))
    if enemy_num == 1:
        enemy_start_y -= 200
        enemy_start_x += 150
        enemy_num = 0

# Create a coin
coin = Coin(random.choice([-150, 0, 150]), random.choice([0, 200]))

# Create Heart
heart = Heart(random.choice([-150, 0, 150]), random.choice([1000, 1200, 1400]))

# Game Status
player_score = PlayerScore(-200, 270)

# Coins Collected Text
Sprite("coin2.gif", 130, 275, 0, 0)
coin_score = CoinScore(160, 270)

# Lives
Sprite("heart.gif", 0, 287, 0, 0)
lives = Lives(40, 270)

# Keyboard Binding
wn.onkeypress(player.turn_right, "Right")
wn.onkeypress(player.turn_left, "Left")

# END SCREEN TEXTS
game_over_text = ""
score_text = ""
coins_collected_image = ""
coins_collected_text = ""
play_again_text = ""

# Main Game Loop
while True:
    wn.update()
    time.sleep(0.02)

    # Increase The Speed Of The Sprites Every Frame
    common_speed -= speed_count
    coin.speed -= speed_count
    heart.speed -= speed_count

    # Move The Player
    player.move()

    # Move The Coin
    coin.move()

    # Move The Heart
    heart.move()

    # Show Status
    player_score.update()
    player_score.score += score_increase_value
    coin_score.update()
    lives.update()

    # Enemies
    for enemy in enemies:
        # Move enemies
        enemy.move()

        # Increase The Enemy Speed
        enemy.speed -= speed_count

        # Check the collision between player and enemy:
        if player.isCollision2(enemy):
            lives.lives -= 1
            enemy.setx(10000)
            playsound("hurt.wav")

    # Check if lives <= 0 lose the game
    if lives.lives < 0:
        game.lose()

    # Move Road Rectangles
    for rect in rects:
        if rect.ycor() < -350:
            rect.sety(WIN_HEIGHT)
        rect.sety(rect.ycor() + (common_speed - 2))

input()