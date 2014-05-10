
import simplegui
import random


CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
deck = []
in_play = False
outcome = ""
outcome_dealer = ""
score = 0
show_back_card = False

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
        self.cards = []

    def __str__(self):
        hand = "Hand contains "
        
        for card in self.cards:
            hand += str(card) + " "   
        return hand
    
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        ace_found = False
        hand_value = 0
        
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                ace_found = True
                
        if ace_found == True:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        else:
            return hand_value
            
   
    def draw(self, canvas, pos, player_type):
        global show_back_card
        npos1 = 0
        card_pos = 1
        
        for card in self.cards:
            if player_type == "player":
                card.draw(canvas, [pos[0] + npos1, pos[1]])
                npos1 += 100
                
            if player_type == "dealer":
                if not show_back_card:
                    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0] + npos1, pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
                    npos1 += 100
                    player_type = "player"
                else:
                    card.draw(canvas, [pos[0] + npos1, pos[1]])
                    npos1 += 100
       
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        self.choose = 0
        
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r))
        
    def shuffle(self):
        self.choose = 0
        random.shuffle(self.cards)

    def deal_card(self):
        self.choose = len(self.cards) - 1
        removed = self.cards[self.choose]
        self.cards.pop()
        return removed
    
    def __str__(self):
        deck = "Deck Contains"
        for c in self.cards:
            deck = deck + " " + str(c) + " "
        return deck    


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, show_back_card, outcome_dealer
    show_back_card = False
    outcome_dealer = ""
    
    # New Deck Object
    deck = Deck()
    
    # Shuffled the deck    
    deck.shuffle()
    
    # Players Hand and Dealers Hand Object created
    player = Hand()
    dealer = Hand()
    
    # Added two cards to the players deck
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    # Added two cards to the dealers deck
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    
    if in_play:
        score -= 1
        outcome = "You loose! New deal?"
        outcome_dealer = "Dealer Won !"
    else:
        outcome = "Hit or stand?"
    
    in_play = True
    
    
def hit():
    global in_play, score, outcome, outcome_dealer
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() <= 21:
            outcome = "Hit or stand?"
        else:
            outcome = "You have busted! New deal?"
            outcome_dealer = "Dealer Won !"
            score = score - 1
            in_play = False

       
def stand():
    global in_play, outcome, score, show_back_card, outcome_dealer
   # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    show_back_card = True
    
    
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            
            
        if dealer.get_value() > 21:
            score = score + 1
            outcome = "You won! New deal?"
            outcome_dealer = "Dealer Busted !"
        
        elif dealer.get_value() >= player.get_value():
            score = score - 1
            outcome = "You loose! New deal?"
            outcome_dealer = "Dealer Won !"
            
        else:
            score = score + 1
            outcome = "You won! New deal?"
            outcome_dealer = "Dealer loose !"
            
        in_play = False     

    else:
        in_play = False
        if player.get_value() > 21:
            score = score - 1
            outcome = "You have busted! New deal?"
            outcome_dealer = "Dealer Busted !"
            
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text("Blackjack", [230, 45], 50, "Blue")
    canvas.draw_text("Player", [25, 435], 30, "BLACK")
    canvas.draw_text("Dealer", [25, 180], 30, "BLACK")
    canvas.draw_text(outcome_dealer, [200, 180], 30, "BLACK")
    canvas.draw_text("Score: " + str(score), [450, 180], 35, "Yellow")
    canvas.draw_text(outcome, [200, 435], 30, "BLACK")
    
    
    dealer.draw(canvas, [100, 200], "dealer")
    player.draw(canvas, [100, 450], "player")
    
    


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