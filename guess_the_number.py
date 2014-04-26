import simplegui
import random
import math

# initialize global variables used in your code
myGuess = 0
secret = 0
num_range = 100
restriction = 0


# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range, secret, restriction
    num_range = 100
    restriction = int(math.ceil(math.log((num_range - 0 + 1), 2)))
    secret = random.randrange(0, 100)
    #print secret
    print ""
    print "New Game. Range is from 0 to",num_range
    print "Number of remaining guesses is", restriction    

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range, secret, restriction
    num_range = 1000
    restriction = int(math.ceil(math.log((num_range - 0 + 1), 2)))
    secret = random.randrange(0, 1000)
    print ""
    print "New Game. Range is from 0 to",num_range
    print "Number of remaining guesses is", restriction    

# helper function to start and restart the game
def new_game():
   if num_range == 100:
        range100()
   else:
        renge1000()
    
    
def input_guess(guess):
    # main game logic goes here	
    global myGuess, restriction
    myGuess = int(guess)
    
    if secret > myGuess:
        restriction = restriction - 1
        print ""
        print "Guess was", myGuess
        print "Number of remaining guesses is", restriction
        print "Higher"
    elif secret < myGuess:
        restriction = restriction - 1
        print ""
        print "Guess was", myGuess
        print "Number of remaining guesses is", restriction
        print "Lower"
    else:
        restriction = restriction - 1
        print ""
        print "Guess was", myGuess
        print "Number of remaining guesses is", restriction
        print "correct!"
        new_game()
    
    if(restriction < 1):
        print ""
        print "Snaap, You lose!!"
        print "Number was",secret
        print ""
        range100()
    
# create frame
frame = simplegui.create_frame("The Guessing Game",200, 200)


# register event handlers for control elements
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
# call new_game and start frame
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
