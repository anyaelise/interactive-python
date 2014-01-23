# template for "Stopwatch: The Game"
import simplegui

# define global variables
counter = 0
successful_stops = 0
total_stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = t / 600
    tenseconds = t % 600
    seconds = tenseconds/10
    if(seconds < 10):
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
    remainder = t % 10
    return str(minutes) + ':' + seconds + "." + str(remainder)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    timer.start()
    
def stop_timer():
    if timer.is_running():
        timer.stop()
        global total_stops
        total_stops += 1
        if counter % 10 == 0:
            global successful_stops
            successful_stops += 1

def reset_timer():
    global counter
    counter = 0
    global successful_stops
    successful_stops = 0
    global total_stops
    total_stops = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    counter += 1


# define draw handler
def draw_handler(canvas):
    counter_string = format(counter)
    canvas.draw_text(counter_string, [180,150], 32, "Red")
    
    score = str(successful_stops) + "/" + str(total_stops)
    canvas.draw_text(score, [350,30], 24, "White")

    
# create frame
frame = simplegui.create_frame("Timer Game", 400, 300)
frame.set_draw_handler(draw_handler)

timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.add_button("Start", start_timer, 100)
frame.add_button("Stop", stop_timer, 100)
frame.add_button("Reset", reset_timer, 100)
frame.add_label


# start frame
frame.start()


# Please remember to review the grading rubric
