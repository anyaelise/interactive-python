# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed, state, counter
    exposed = []
    state = 0
    counter = 0
    cards = range(8)
    cards.extend(range(8))
    random.shuffle(cards)
    for card in cards:
        exposed.append(False)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, prev_index, cur_index, counter
    card_index = pos[0]/50
    if exposed[card_index] == False:
        exposed[card_index] = True
        if state == 0:
            state = 1
            prev_index = card_index
        elif state == 1:
            state = 2
            cur_index = card_index
            counter += 1
            label.set_text("Turns = " + str(counter))
        else: #state == 2
            state = 1
            if cards[cur_index] != cards[prev_index]:
                exposed[cur_index] = False
                exposed[prev_index] = False
            prev_index = card_index
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    start_point = 0
    for i in range(len(cards)):
        if exposed[i] == True:
            canvas.draw_polygon([[start_point,0],[start_point+50,0],[start_point+50,100],[start_point,100]],1,'Red','Black')
            canvas.draw_text(str(cards[i]),[start_point+18,60],30,'White')
        else:
            canvas.draw_polygon([[start_point,0],[start_point+50,0],[start_point+50,100],[start_point,100]],1,'Red','Green')
        start_point += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric