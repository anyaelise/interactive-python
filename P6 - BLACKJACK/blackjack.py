# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        string_rep = "Hand contains"
        for card in self.cards:
            string_rep += " " + str(card)
        return string_rep

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total = 0
        aces = 0
        for card in self.cards:
            rank = card.get_rank()
            if rank == 'A':
                aces += 1
            total += VALUES[rank]
        while aces > 0:
            if total + 10 <= 21:
                total += 10
            aces -= 1
        return total
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [] # create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards) # use random.shuffle()

    def deal_card(self):
        card = self.cards.pop() # deal a card object from the deck
        return card
    
    def __str__(self):
        string_rep = "Deck contains"
        for card in self.cards: # return a string representing the deck
            string_rep += " " + str(card)
        return string_rep



#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, dealer_hand, player_hand
    
    if in_play == True:
        outcome = "You have lost."
        score -= 1

    deck = Deck()
    deck.shuffle()
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    in_play = True
    outcome = "Hit or stand?"

def hit():
    global outcome, score, in_play
    # if the hand is in play, hit the player
    if in_play == True:
        player_hand.add_card(deck.deal_card())
   
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        outcome = "You have busted."
        score -= 1
        in_play = False
       
def stand():
    global outcome, score, in_play
    in_play = False
    if player_hand.get_value() > 21:
        outcome = "You have busted."
        
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == False:
        while(dealer_hand.get_value() < 17 ):
            dealer_hand.add_card(deck.deal_card())

    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() > 21:
        outcome = "Dealer has busted. You have won!"        
        score += 1
    else: 
        if dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer has won."
            score -= 1
        else:
            outcome = "You have won!"
            score += 1

# draw handler    
def draw(canvas):
    global in_play
    # draw hand
    canvas.draw_text("BLACKJACK", [250,50], 30, 'Black')
    canvas.draw_text("Score: " + str(score), [450,300], 30, 'White')
    dealer_hand.draw(canvas, [100, 100])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 100 + CARD_CENTER[1]], CARD_BACK_SIZE)
    player_hand.draw(canvas, [100, 400])
    canvas.draw_text(outcome, [100, 380], 20, 'White')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric