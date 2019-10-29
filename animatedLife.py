# Updated Animation Starter Code

from tkinter import *
from main import *

#Run function from 15112 course notes at Carnegie Mellon

def init(data):
    data.boardWidth = len(data.board[0])
    data.boardHeight = len(data.board)
    data.cellWidth = data.width/data.boardWidth
    data.cellHeight = data.height/data.boardHeight
    data.time = 0


def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    data.board = nextBoardState(data.board)
    data.time += 1

def drawLines(canvas, data):
  for col in range(data.boardWidth-1):
    x = (col * data.cellWidth) + data.cellWidth
    canvas.create_line(x,0,x,data.height, fill="#abc")
  for row in range(data.boardHeight-1):
    y = (row * data.cellHeight) + data.cellHeight
    canvas.create_line(0,y,data.width,y, fill="#abc")

def getCoords(row,col,data):
  x1 = col * data.cellWidth
  y1 = row * data.cellHeight
  x2 = (col * data.cellWidth) + data.cellWidth
  y2 = (row * data.cellHeight) + data.cellHeight
  return x1, y1, x2, y2

def drawCells(canvas, data):
  board = data.board
  color = "#7da7db"
  for row in range(len(board)):
    for col in range(len(board[0])):
      if board[row][col] == 1:
        x1,y1,x2,y2 = getCoords(row,col, data)
        canvas.create_rectangle(x1,y1,x2,y2, fill=color, width=0)
      else:
        pass

def redrawAll(canvas, data):
  drawLines(canvas, data)
  drawCells(canvas, data)
  canvas.create_text(data.cellWidth,0,
    text="TIME: " + str(data.time), anchor='nw')

####################################
# use the run function as-is
####################################

def run(width=300, height=300, board = None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    if board == None:
      n = min(data.width, data.height)//10
      data.board = randomState(126, 102)
    else:
      data.board = board
    data.timerDelay = 50 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

if __name__ == "__main__":
  run(800, 800)