#gameoflif test suite
from main import *
import copy
# TODO: there's a lot of repeated code here. Can
# you move some of into reusable functions to
# make it shorter and neater?

def testBoard(input, expected):
  actual = nextBoardState(input)
  if not (actual == expected):
    print('Test failed!')
    print('Expected output:')
    renderState(expected)
    print('Actual output:')
    renderState(actual)
  else: print('Passed!')

def test():
  print('Testing game of life.............')
  # TEST 1: dead cells with no live neighbors
    # should stay dead.
  init_state1 = [
      [0,0,0],
      [0,0,0],
      [0,0,0]
  ]
  expected_next_state1 = [
      [0,0,0],
      [0,0,0],
      [0,0,0]
  ]
  print('Testing Dead to dead...', end='')
  testBoard(init_state1, expected_next_state1)
  # TEST 2: dead cells with exactly 3 neighbors
  # should come alive.
  init_state2 = [
      [0,0,1],
      [0,1,1],
      [0,0,0]
  ]
  expected_next_state2 = [
      [0,1,1],
      [0,1,1],
      [0,0,0]
  ]
  #does not work on wrapping board....
  print('Cell-gen (not wrap safe)...', end='')
  testBoard(init_state2, expected_next_state2)

  expected3 = dead_state(5,5)
  expected3[2][2]=1
  expected3[2][3]=1
  expected3[1][3]=1
  expected3[1][2]=1
  input3 = copy.deepcopy(expected3)
  input3[1][2]=0
  print('Wrap-safe cell gen...', end='')
  testBoard(input3, expected3)
  

  print('Microboard death...', end='')
  testBoard([[1]], [[0]])
  

  input5 = [[0,0,0],
            [0,1,0],
            [0,0,0]]
  expect5= [[0,0,0],
            [0,0,0],
            [0,0,0]]
  print('Neighborless Cell death...', end='')
  testBoard(input5, expect5)
  

  input6 = [[0,0,0],
            [1,1,1],
            [0,0,0]]
  expect6= [[0,1,0],
            [0,1,0],
            [0,1,0]]
  print('| to ---...', end='')
  testBoard(input6,expect6)
  
  print('Testing --- to |...', end="")
  testBoard(expect6, input6)


  square = [[0,1,1],
            [0,1,1],
            [0,0,0]]
  print('Testing Square to square...', end='')
  testBoard(square, square)

if __name__ == "__main__":
  test()    
