'''dbg_agent.py
This Backgammon player implements the Minimax and Alpha-Beta pruning algorithms
in identifying the best move in the Deterministic Simplified Backgammon game.

'''

from backgState import *

# Define a class for agent

# Implement two counter variables:
#   1) Number of states created by agent
#   2) Number of cutoffs made by Alpha-Beta pruning
class Agent:
  def __init__(self):
    self.STATES = 0
    self.CUTOFFS = 0

  def __eq__(self,s2):
    for i in range(3):
      for j in range(3):
        if self.b[i][j] != s2.b[i][j]: return False
    return True

  def __str__(self):
    txt = "\n["
    for i in range(3):
      txt += str(self.b[i])+"\n "
    return txt[:-2]+"]"

  def __hash__(self):
    return (self.__str__()).__hash__()
  
  def useAlphaBetaPruning(prune=False):
    # Turn off Alpha-Beta pruning
    # Reset counters for states created and Alpha-Beta cutoffs to 0
  
  def statesAndCutoffsCounts():
    # Returns a tuple with states and cutoffs
    return((self.STATES, self.CUTOFFS))

  def setMaxPly(maxply=-1):
    # set a specific limit on the depth of your agent's searches

  def useSpecialStaticEval(func):
    # force the agent of use the supplied evaluation function

  def staticEval(state):
    # Takes in state and returns a real number that is positive when good for
    # maximizing player (white) and negative when relatively good for the 
    # minimizing player (red)

  def miniMax(state):

  def alphaBetaPrune(state):

  def move(state, die1, die2):
  w = state.whose_move
  print("I'm playing "+get_color(w))
  print("Tell me which checkers to move, with point numbers, e.g., 19,7")
  ans = m1 + ',' + m2
  print("Use 0 to move from the bar.")
  print("If you want your first (or only) checker to move according")
  print("to the 2nd die, add a 3rd argument R: e.g., 19,7,R to reverse the dice.")
  if(reverse):
    ans += ",R"
  print("For only 1 checker to move with both dice, give as 2nd argument the point number")
  print("where the checker will be after the move is half done.")

  return ans
  #return "Q" # quit