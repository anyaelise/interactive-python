# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui


# initialize global variables used in your code
num_range = 100
secret_number = 0
remaining_guesses = 7

# helper function to start and restart the game
def new_game():
    global num_range
    global secret_number
    global remaining_guesses
    
    secret_number = random.randrange(num_range)
    
    if num_range == 100:
        remaining_guesses = 7
    else: 
        remaining_guesses = 10
    
    print "New game. Range is from 0 to", num_range
    print ""


# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    print "You guessed " + guess
    
    global secret_number    
    global remaining_guesses
    
    guess_num = float(guess)
    if guess_num < secret_number:
        print "Higher!"
    elif guess_num > secret_number:
        print "Lower!"
    else:
        print "Correct!"    
        
    remaining_guesses -= 1
    if remaining_guesses < 0:
        print "You have no more guesses. The number was", secret_number
        new_game()
    elif (remaining_guesses > 0) and (guess_num != secret_number):
        print "Number of remaining guesses is", remaining_guesses
        print ""       

    
# create frame
frame = simplegui.create_frame("Guess The Number", 200, 200)


# register event handlers for control elements
frame.add_input("Guess: ", input_guess, 100)
frame.add_button("Range is from [0,100)", range100, 200)
frame.add_button("Range is from [0,1000)", range1000, 200)                 



# call new_game and start frame
new_game()
frame.start()


# always remember to check your completed program against the grading rubric
