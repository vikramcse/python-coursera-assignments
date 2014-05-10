# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [0, 0]
ball_vel = [0, 0]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel,time
    ball_pos = [600 / 2, 400 / 2]
    
    if direction == RIGHT:
        ball_vel = [2,-1]
    elif direction == LEFT:
        ball_vel = [-2,-1]
     
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, turn  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [[0, HEIGHT / 2 - HALF_PAD_HEIGHT], [0, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT],[WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle1_vel = 0
    paddle2_vel = 0
    
    turn = random.randrange(0, 2)
    if turn == 0:
        spawn_ball(LEFT)
    if turn == 1:
        spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # Draw the Paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH * 2, "White")
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH * 2, "White")  
    
    
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # updating the directions and collision 
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[0][1] and ball_pos[1] <= paddle1_pos[1][1]:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            score2 = score2 + 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= ((WIDTH - 1)- BALL_RADIUS) - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos[0][1] and ball_pos[1] <= paddle2_pos[1][1]:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            score1 = score1 + 1
            spawn_ball(LEFT)
    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "SKYBLUE", "WHITE")
    
    # update paddle's vertical position, keep paddle on the screen
    x = paddle1_pos[0][1] - paddle1_vel
    if x >= 0 and x <= (HEIGHT - PAD_HEIGHT):
        paddle1_pos[0][1] = paddle1_pos[0][1] - paddle1_vel
        paddle1_pos[1][1] = paddle1_pos[1][1] - paddle1_vel
        
    y = paddle2_pos[0][1] - paddle2_vel
    if y >= 0 and y <= (HEIGHT - PAD_HEIGHT):
        paddle2_pos[0][1] = paddle2_pos[0][1] - paddle2_vel
        paddle2_pos[1][1] = paddle2_pos[1][1] - paddle2_vel
    
    # draw scores
    canvas.draw_text(str(score1),[WIDTH / 4, 100], 50, "ROYALBLUE");
    canvas.draw_text(str(score2),[WIDTH - WIDTH / 4, 100], 50 ,"ROYALBLUE");
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # W (up), D(right)
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = -5

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def restart():
    global score1, score2
    score1 = score2 = 0
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()