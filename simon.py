from adafruit_circuitplayground.express import cpx
import time
import array
import random

# ID, Pixel Index, Tone, high, low
RED_ID = [1, 1, 440, (125,0,0), (5,0,0)]
YELLOW_ID = [2, 6, 550, (125,125,0), (5,5,0)]
GREEN_ID = [3, 3, 330, (0, 125, 0),(0,5,0)]
BLUE_ID = [4, 8,  660, (0,0,125),(0,0,5)]

# simons sequence 
simon = array.array('b',)

# score needed to win
to_win = 35

# note_e = 330    # green
# note_a = 440    # red
# note_cSH = 550  # yellow
# note_eH = 660   # blue
note_bad = 240


def display_score(score):
    '''
        display the score 
    '''
    print("Score: ", score)
    if len(simon) >= to_win:
        for i in range(16):
            play_color_tone((i % 4) + 1, .2)
        print("Yay!  You beat the game")

    
def reset():
    '''
        Reset game
    '''
    # print('reset')
    cpx.pixels.fill((0,0,0))
    cpx.pixels.brightness = 0.3

    # this will initialize the neopixels    
    for i in range(5):
        play_color_tone(i, .5 )
        
    # seed random generator
    random.seed(int(97 * time.monotonic()))



def play_color_tone(color_id, wait = 1.0):
    '''
        Play selected tone and highlight color
    '''
    if color_id == RED_ID[0]: # RED
        cpx.pixels[RED_ID[1]] = RED_ID[3]
        cpx.play_tone(RED_ID[2], wait)
        cpx.pixels[RED_ID[1]] = RED_ID[4]
        
    elif color_id == YELLOW_ID[0]: # YELLOW
        cpx.pixels[YELLOW_ID[1]] = YELLOW_ID[3]
        cpx.play_tone(YELLOW_ID[2], wait)
        cpx.pixels[YELLOW_ID[1]] = YELLOW_ID[4]

    elif color_id == GREEN_ID[0]: # GREEN
        cpx.pixels[GREEN_ID[1]] = GREEN_ID[3]
        cpx.play_tone(GREEN_ID[2], wait)
        cpx.pixels[GREEN_ID[1]] = GREEN_ID[4]

    elif color_id == BLUE_ID[0]: # BLUE
        cpx.pixels[BLUE_ID[1]] = BLUE_ID[3]
        cpx.play_tone(BLUE_ID[2], wait)
        cpx.pixels[BLUE_ID[1]] = BLUE_ID[4]

    else:
        cpx.play_tone(note_bad, wait)


def play_sequence():
    '''
        Play simon's sequence
    '''
    # set speed for difficulty
    if len(simon) > 0:
        speed = 1.0 - (len(simon) * 2 / 100)
        
        for i in simon:
            time.sleep(speed - 0.25)
            play_color_tone(i,speed)


def get_touch():
    '''
        Get Touch pad
    '''
    while cpx.switch:   # this will handle if the switch is turned off at this stage
        if cpx.touch_A4 or cpx.touch_A5:
            return RED_ID[0]
        
        if cpx.touch_A6 or cpx.touch_A7:
            return GREEN_ID[0]

        if cpx.touch_A1:
            return YELLOW_ID[0]

        if cpx.touch_A2 or cpx.touch_A3:
            return BLUE_ID[0]


def validate_choice(idx, touch):
    '''
        checks if the players choice is correct and
        plays appropriate tone
    '''
    if simon[idx] == touch:
        play_color_tone(touch)
        return True
    else:
        play_color_tone(0, 1.5)
        # let them know what the correct color was...
        time.sleep(1)
        play_color_tone(simon[idx], 0.25)
        play_color_tone(simon[idx], 0.25)
        time.sleep(1)
        return False


def players_guess():
    '''
        gets the players guess at the sequence
    '''
    guess = array.array('b',)
    correct = True
    idx = 0

    while cpx.switch and correct and idx < len(simon):
        correct = validate_choice(idx, get_touch())
        idx += 1

    return correct


def add_to_sequence():
    '''
        adds a random number to the sequence
    '''
    rand_num = random.randint(1,4)
    simon.append(rand_num)


def play_game(verbose_score):
    '''
        Main game loop
    '''
    winning = True

    while cpx.switch and winning:
        # add to sequence
        add_to_sequence()

        # play tones
        play_sequence()

        # wait for player input
        cpx.red_led = True
        winning = players_guess()
        cpx.red_led = False

        if len(simon) >= to_win:
            break;

        if winning:
            if verbose_score:
                display_score(len(simon))
            time.sleep(1)



while cpx.switch:
    reset()
    if len(simon) > 0:
        del simon
        simon = array.array('b',) # (i for i in range(35)))  # test score

    # print a blank line...
    print()
    print("Press Button A or Button B to start new game")
    
    # wait for the player to push a button to restart
    waiting = True
    verbose_score = False

    while waiting and cpx.switch:
        # print("waiting", waiting)
        if cpx.button_a:
            waiting = False

        if cpx.button_b:
            verbose_score = True
            waiting = False
        
        time.sleep(0.1)
    
    play_game(verbose_score)
    display_score(len(simon))

if not cpx.switch:
    print("switch is off")
