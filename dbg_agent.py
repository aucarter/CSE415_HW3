'''dbg_agent.py
This Backgammon player implements the Minimax and Alpha-Beta pruning algorithms
in identifying the best move in the Deterministic Simplified Backgammon game.

'''
#%%
from backgState import *
from testStates import *

# Define a class for agent

# Implement two counter variables:
#   1) Number of states created by agent
#   2) Number of cutoffs made by Alpha-Beta pruning
class Agent:
  def __init__(self):
    # Instance variables for the number of states created and cutoffs made
    self.STATES = 0
    self.CUTOFFS = 0
    # Variable for whether or not to use Alpha-Beta pruning
    self.A_B = False
    # Variable for limit on depth of agent's searxh
    self.MAX_PLY = -1

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
  
  def useAlphaBetaPruning(self, prune=False):
    # Turn off Alpha-Beta pruning
      self.A_B = prune
    # Reset counters for states created and Alpha-Beta cutoffs to 0
      self.STATES = 0
      self.CUTOFFS = 0
  
  def statesAndCutoffsCounts(self):
    # Returns a tuple with states and cutoffs
    ans = (self.STATES, self.CUTOFFS)
    return(ans)

  def setMaxPly(self, maxply=-1):
    # set a specific limit on the depth of your agent's searches
    self.MAX_PLY = maxply

  def useSpecialStaticEval(self, func):
    # force the agent of use the supplied evaluation function
    pass

  def staticEval(self, state):
    # Takes in state and returns a real number that is positive when good for
    # maximizing player (white) and negative when relatively good for the 
    # minimizing player (red)
    
    # Total distance of W pieces from being off
    w_position = [i.count(False) for i in state.pointLists]
    w_dist = sum([(i[0] + 1)*i[1] for i in enumerate(w_position)])
    # Total distance of R pieces from being off
    r_position = [i.count(True) for i in state.pointLists]
    r_dist = sum([(len(r_position) - i[0])*i[1] for i in enumerate(r_position)])
    # Take the net of the two, with R distance being positive and W being bad
    net = r_dist - w_dist
    return(net)

  def miniMax(self, state, depth, maxTurn, die1, die2):
    # admissible_moves = findAdmissibleMoves(state)
    # if(depth == self.MAX_PLY):
    #   ans = [m, staticEval()]
    #   return
    # if(maxTurn):
    #   max([minimax(self, updateState(state, m), depth, False, die1, die2) for m in admissible_moves])
    pass

  def findAdmissibleMoves(self, state, die1, die2):
    # Identify the positions of the pieces
    w_position = [i for i, e in enumerate(s.pointLists) if e.count(False) > 0]
    r_position = [i for i, e in enumerate(s.pointLists) if e.count(True) > 0]

    # Check if it is ok to move pieces off
    off_possible = all([i > 17 for i in w_position])

    # Identify moves that don't hit others pieces
    if(off_possible):
      w_d1_moves = [i for i in w_position if i + die1 not in r_position]
      w_d2_moves = [i for i in w_position if i + die2 not in r_position]
    else:
      w_d1_moves = [i for i in w_position if i + die1 not in r_position and i + die1 < 24]
      w_d2_moves = [i for i in w_position if i + die2 not in r_position and i + die2 < 24]

    # Make all combinations of admissible moves
    move_combos = [[i, j] for i in w_d1_moves for j in w_d2_moves]
    # Remove combos that include moving two pieces from a position with only one
    admissible_moves = [i for i in move_combos if not (i[0] == i[1] and s.pointLists[i[0]].count(False) < 2)]
    
    return(admissible_moves)


  def alphaBetaPrune(state):
    cutoff_found = False
    if(cutoff_found):
      self.CUTOFFS += 1

  def move(state, die1, die2):
    ans = miniMax(state, die1, die2)
    return ans
  
test = Agent()
print(test.statesAndCutoffsCounts())

#%%
s = bgstate()
die1 = 1
die2 = 6
# Identify the positions of the pieces
w_position = [i for i, e in enumerate(s.pointLists) if e.count(False) > 0]
r_position = [i for i, e in enumerate(s.pointLists) if e.count(True) > 0]

# Check if it is ok to move pieces off
off_possible = all([i > 17 for i in w_position])

# Identify moves that don't hit others pieces
if(off_possible):
  w_d1_moves = [i for i in w_position if i + die1 not in r_position]
  w_d2_moves = [i for i in w_position if i + die2 not in r_position]
else:
  w_d1_moves = [i for i in w_position if i + die1 not in r_position and i + die1 < 24]
  w_d2_moves = [i for i in w_position if i + die2 not in r_position and i + die2 < 24]

# Make all combinations of admissible moves
move_combos = [[i, j] for i in w_d1_moves for j in w_d2_moves]
admissible_moves = [i for i in move_combos if s.pointLists[i[0]].count(False) > 1]
return(admissible_moves)
#%%
