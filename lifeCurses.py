'''Animating Conway's game of life using curses library. 
Utilizes loose MVC structure.
Author: sandlerj
'''
import curses
from curses.textpad import Textbox, rectangle
from main import *

def init(data, board=None):
  data.loadScreen = False
  data.boardLoaded = False
  if board == None:
    data.lifeBoard = randomState(data.boardMax[0], data.boardMax[1])
  else:
    data.lifeBoard = board
    data.boardLoaded = True
  data.genCount = 0
  data.runBoard = False
  data.pause = False
  data.loadedBoardTitle = None

def loadKeyPressed(data): #present if needed
  pass

def keyPressed(data):
  c = data.stdscr.getch()
  if data.loadScreen:
    loadKeyPressed(data)
  else:
    if c == ord(' '):
      data.runBoard = True
      data.pause = False
    elif c == ord('p'):
      data.pause = not data.pause
    elif c == ord('q'):
      if data.runBoard:
        data.runBoard = False
      else:
        curses.curs_set(True)
        data.breaker = True
    elif c == ord('l'):
      data.loadScreen = True
    if not data.runBoard:
      if c == ord('r'):
        init(data)
        data.runBoard = True

def timerFired(data):
  if data.runBoard:
    if not data.pause:
      data.lifeBoard = nextBoardState(data.lifeBoard)
      data.genCount +=1
      curses.napms(100)

def loadPrintScreen(data): #Screen and actions for loading external files
  data.stdscr.clear()
  data.stdscr.addstr(0, 0, "Enter board file name (including '.txt')" +\
    " and press 'enter'")
  boxH,boxW = 1,30
  startY, startX = 3,1
  editwin = curses.newwin(boxH,boxW, startY,startX)
  rectULY, rectULX = 2, 0
  rectangle(data.stdscr, rectULY, rectULX, rectULY+boxH+1, rectULX+boxW+1)
  data.stdscr.addstr(rectULY+boxH+2,0, "Max size is %d x %d." % data.boardMax \
   + "If loaded board "+\
    "is smaller, rows and columns will be added. If too large, rows and"+\
    " columns will be removed until max dimensions acheived. If more space is"+\
    " needed, quit and resize the console window/reduce font size.")
  data.stdscr.refresh()

  box = Textbox(editwin)

  # Let the user edit until Ctrl-G is struck.
  box.edit()

  # Get resulting contents
  userInput = box.gather()
  try:#attempt to load user generated board
    data.lifeBoard = loadBoardState(userInput)
    data.loadedBoardTitle = userInput
    data.boardLoaded = True
    checkBoardSize(data) #fit to size
  except: #Something went wrong...
    data.stdscr.addstr(1,0, "Entered board state not found. "\
      +"Returning to main menu.", curses.color_pair(1) | curses.A_STANDOUT)
    curses.beep()
    data.stdscr.refresh()
    curses.napms(2000)
  data.loadScreen = False

def checkBoardSize(data):
  #Checking and modifying any rows or cols that might be too long or short -
  # also deals with jagged edges
  maxX, maxY = data.boardMax
  if len(data.lifeBoard) > maxY:
    data.lifeBoard = data.lifeBoard[:maxY]
  else: #check if needs rows added
    while len(data.lifeBoard) < maxY: 
      data.lifeBoard.append([0] * maxX)
  for row in range(len(data.lifeBoard)): #checking each row in case irregular
    if len(data.lifeBoard[row]) > maxX:
      data.lifeBoard[row] = data.lifeBoard[row][:maxX] #trim if needed
    else: #add if needed
      while len(data.lifeBoard[row]) < maxX:
        data.lifeBoard[row].append(0)

def printScreen(data): #For primary menu and life screen
  if data.loadScreen:
    loadPrintScreen(data)
  else:  
    if data.runBoard: #show the board
      data.stdscr.clear()
      printBoard(data)
      data.stdscr.addstr(0,0, "Current Gen: %d" % data.genCount)
      helpText = "Press 'p' to pause or 'q' to quit"
      data.stdscr.addstr(0, data.width//2 - len(helpText)//2, helpText)
      data.stdscr.refresh()
    if not data.runBoard: #main menu
      data.stdscr.clear()
      data.stdscr.addstr(0,0, "CONWAY'S GAME OF LIFE", curses.A_UNDERLINE)
      if data.boardLoaded:
        if data.loadedBoardTitle == None:
          boardText = 'user loaded board'
        else: boardText = data.loadedBoardTitle
      else:
        boardText = "a random %d by %d board"\
        % data.boardMax
      data.stdscr.addstr(1,0, "Press SPACE to start (or resume) Life with " + boardText)
      data.stdscr.addstr(2,0, "Press 'r' to get a new random %d by %d board"\
        % data.boardMax)
      data.stdscr.addstr(3,0, "Press 'l' to load board state from file")

def printBoard(data):
  #prints current life board to screen
  for row in range(len(data.lifeBoard)):
    for col in range(len(data.lifeBoard[0])):
      if data.lifeBoard[row][col] == 1:
        data.stdscr.addstr(row + data.BUFFER, col, data.SQUARE)

def run():
  class Struct(object): pass
  data = Struct()
  data.stdscr = curses.initscr()
  data.breaker = False # used to break running loop
  curses.noecho()
  curses.start_color()
  curses.curs_set(False)
  curses.cbreak()
  curses.noecho()
  data.stdscr.keypad(1)

  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
  #color pair saved if wanted again

  try:
  # Run your code here
      data.height,data.width = data.stdscr.getmaxyx()
      data.SQUARE =u"\u2588" #cell visual
      data.BUFFER = len(data.SQUARE) #buffer for board edges where wanted
      data.stdscr.nodelay(True)
      data.boardMax = (data.width - data.BUFFER, data.height - data.BUFFER)
      init(data)

      while True:
        ##
        keyPressed(data)
        timerFired(data)
        printScreen(data)
        if data.breaker:
          break


  finally:
      curses.nocbreak()
      data.stdscr.keypad(0)
      curses.echo()
      curses.endwin()

if __name__ == "__main__":
  run()