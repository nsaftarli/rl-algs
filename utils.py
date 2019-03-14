import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Get the state in specified direction of this state
def getUpwardsOf(state_num):
    return state_num - 10


def getRightOf(state_num):
    return state_num + 1


def getDownwardsOf(state_num):
    return state_num + 10


def getLeftOf(state_num):
    return state_num - 1


# Check if a state is on the border of the grid
def isTopRow(state):
    return True if state - 10 < 0 else False


def isRightCol(state):
    return True if state % 10 == 9 else False


def isBottomRow(state):
    return True if state + 10 >= 100 else False


def isLeftCol(state):
    return True if state % 10 == 0 else False


# Check if a state has a wall in a direction (border or otherwise)
def hasWallEast(state):
    return True if (
        (state % 10 == 4 and state != 24 and state != 74)
        or
        (isRightCol(state)))\
        else False


def hasWallWest(state):
    return True if (
        (state % 10 == 5 and state != 25 and state != 75)
        or
        (isLeftCol(state)))\
        else False


def hasWallNorth(state):
    return True if (
        (state >= 50 and state < 60 and state != 52 and state != 57)
        or
        (isTopRow(state)))\
        else False


def hasWallSouth(state):
    return True if (
        (state >= 40 and state < 50 and state != 42 and state != 47)
        or
        (isBottomRow(state)))\
        else False



def print_policy(pi):
    unicode_map = ['\u2191', '\u2192', '\u2193', '\u2190']

    buff = ''
    for i, act in enumerate(pi):
        if i % 10 == 5 and i != 25 and i != 75:
            buff += '|'
        if i == 25 or i == 75:
            buff += ' '
        if i == 60:
            print('-- -- -- --')
        if i % 10 == 0 and i != 0:
            print(buff)
            buff = ''
        buff += unicode_map[act]
        # if i % 10 == 0 and i != 0:
        #     print(buff)
        #     buff = ''
    print(buff)

def fill_policy(pi):
    unicode_map = ['\u2191', '\u2192', '\u2193', '\u2190']
    buff = ''
    for i, act in enumerate(pi):
        if i % 10 == 5 and i != 25 and i != 75:
            buff += '|'
        if i == 25 or i == 75:
            buff += ' '
        if i == 60:
            # print('-- -- -- --')
            buff += '\n-- -- -- --'
        if i % 10 == 0 and i != 0:
            print(buff)
            buff += '\n'
        buff += unicode_map[act]
    return buff



def draw_policy(pi, params):
    filename = '' + params['alg'] + '_' + str(params['it']) + '_' + str(params['a']) + '_' + str(params['e'])
    print(filename)
    text = fill_policy(pi)
    img = Image.new('RGB', (250, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    unicode_font = ImageFont.truetype("DejaVuSansMono.ttf", 32)
    d.text((10, 10), text, font=unicode_font, fill=(0,0,0))
    img.save('./Report/images/' + filename + 'reduce_e.jpg')

if __name__ == '__main__':
    draw_policy([0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3,
                 0, 1, 2, 3, 0, 1, 2, 3, 2, 3])




