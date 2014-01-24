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

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [1,1]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(1,5)
        ball_vel[1] = random.randrange(1,5)
    elif direction == LEFT:
        ball_vel[0] = -(random.randrange(1,5))
        ball_vel[1] = random.randrange(1,5)
    else:
        print "Invalid direction"

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    spawn_ball(random.randint(0,1))
    paddle1_pos = [0,HEIGHT/2]
    paddle2_pos = [WIDTH-PAD_WIDTH, HEIGHT/2]
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    #check for collision with top or bottom
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1 - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] = ball_pos[1] + ball_vel[1]
        
    #check for collision with gutter
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        #check if ball is hitting paddle1
        if ball_pos[1] - BALL_RADIUS >= paddle1_pos[1] and ball_pos[1] - BALL_RADIUS <= paddle1_pos[1]+PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_pos[0] = ball_pos[0] + ball_vel[0]
        else:
            score2 += 1
            spawn_ball(random.randint(0,1))            
    elif ball_pos[0] >= WIDTH -1 - BALL_RADIUS - PAD_WIDTH:
        #check if ball is hitting paddle2
        if ball_pos[1] - BALL_RADIUS >= paddle2_pos[1] and ball_pos[1] - BALL_RADIUS <= paddle2_pos[1]+PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_pos[0] = ball_pos[0] + ball_vel[0]
        else:
            score1 += 1
            spawn_ball(random.randint(0,1))
        
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    new_pos1 = paddle1_pos[1] + paddle1_vel[1]
    new_pos2 = paddle2_pos[1] + paddle2_vel[1]
    
    if new_pos1 <= HEIGHT - PAD_HEIGHT and new_pos1 >= 0:
        paddle1_pos[1] = new_pos1
        
    if new_pos2 <= HEIGHT - PAD_HEIGHT and new_pos2 >= 0:
        paddle2_pos[1] = new_pos2
    
    # draw paddles
    c.draw_polygon([(paddle1_pos[0], paddle1_pos[1]), (paddle1_pos[0]+PAD_WIDTH, paddle1_pos[1]), (paddle1_pos[0]+PAD_WIDTH, paddle1_pos[1]+PAD_HEIGHT), (paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT)], 1, 'White', 'White')
    c.draw_polygon([(paddle2_pos[0], paddle2_pos[1]), (paddle2_pos[0]+PAD_WIDTH, paddle2_pos[1]), (paddle2_pos[0]+PAD_WIDTH, paddle2_pos[1]+PAD_HEIGHT), (paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT)], 1, 'White', 'White')
    
    # draw scores
    ypos = 40
    c.draw_text(str(score1), [round(WIDTH/3), ypos], 32, 'White')
    c.draw_text(str(score2), [round(2*WIDTH/3), ypos], 32, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 5
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -vel
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = vel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = vel
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game, 100)


# start frame
new_game()
frame.start()
