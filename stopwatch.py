# template for "Stopwatch: The Game"

# define global variables
import simplegui
import math

# global variables
value = 0
stop_count = 0
stopped_correct = 0
solution = "0/0"
is_stopped = False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(text):
    val = int(text)
    A = 0
    B = str(0)
    D = str(val % 10)
    
    # calculation for seconds
    s = int(math.floor((val % 600) / 10) % 10)
    if s <= 9:
        C = str(s)
    else:
        C = str(0)
    
    s1 = int(math.floor((val % 600) / 100))
    if(s1 <= 5):
        B = str(s1)
    else:
        B = str(0)
    
    # calculation for minutes    
    m = int(math.floor(val / 600))
    if m < 10:
        A = str(m)
    else:
        A = str(m)
    
    # print as a string    
    return A+ ":"+B+C+ "." +D
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_stopped
    timer.start()
    is_stopped = False

def stop():
    global is_stopped
    timer.stop()
    game()
    is_stopped = True

def reset():
    global value, solution, stop_count, stopped_correct
    timer.stop()
    value = 0
    stop_count = 0
    stopped_correct = 0
    solution = "0/0"

# define event handler for timer with 0.1 sec interval
def inc():
    global value
    value += 1
    

# define draw handler
def draw(canvas):
    canvas.draw_text(format(value), [110,100],40,"WHITE")
    canvas.draw_text(solution, [250, 30],30,"GREEN")

def game():
    global stop_count, stopped_correct, solution
    if is_stopped == False:
        stop_count += 1
        if value % 10 == 0:
            stopped_correct += 1  
        solution = str(stopped_correct) +"/"+ str(stop_count)
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)
frame.add_button("start", start, 100)
frame.add_button("stop", stop, 100)
frame.add_button("reset", reset, 100)
timer = simplegui.create_timer(100, inc)

# register event handlers
frame.set_draw_handler(draw)

# start frame
frame.start()
# Please remember to review the grading rubric