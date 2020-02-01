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

  def move(self, state, die1, die2):
    # Returns the best move found through miniMax algorithm
    ans = self.miniMax(state = state, whose_move = state.whose_move, max_depth = 3, die1 = die1, die2 = die2, alpha = -1e10, beta = 1e10, depth = 0)
    return ans
  
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
  
  def miniMax(self, state, whose_move, max_depth, die1, die2, alpha = -1e10, beta = 1e10, depth = 0):
    if(depth == max_depth):
      return staticEval(state)
    admis_moves = findAdmissibleMoves(state, whose_move, die1, die2)
    for m in admis_moves:
      val = self.miniMax(updateState(state, m, die1, die2, whose_move), 1 - whose_move, max_depth, die1, die2, alpha, beta, depth + 1)
      self.STATES += 1
      if(m == admis_moves[0]):
        best_val = val
        best_move = m
      else:
        if(whose_move == W):
          if val > best_val:
            best_val = val
            best_move = m
            if self.A_B:
              if best_val >= beta:
                self.CUTOFFS += 1
                break
              if best_val > alpha:
                alpha = best_val
        else:
          if val < best_val:   
            best_val = val
            best_move = m
            if self.A_B:
              if best_val <= alpha:
                self.CUTOFFS += 1
                break
              if best_val < beta:
                beta = best_val            
    if(depth == 0):
      return best_move
    else:
      return best_val

def staticEval(state):
  # Takes in state and returns a real number that is positive when good for
  # maximizing player (white) and negative when relatively good for the 
  # minimizing player (red)
  
  # Total distance of W pieces from being off
  w_position = [i.count(False) for i in state.pointLists]
  w_dist = sum([(24 - i[0])*i[1] for i in enumerate(w_position)])
  # Total distance of R pieces from being off
  r_position = [i.count(True) for i in state.pointLists]
  r_dist = sum([(i[0] + 1)*i[1] for i in enumerate(r_position)])
  # Take the net of the two, with R distance being positive and W being bad
  net = r_dist - w_dist
  return(net)



def findAdmissibleMoves(state, whose_move, die1, die2):
  ## Enumerate all possible moves
  # Identify the positions of the pieces
  position = [i + 1 for i, e in enumerate(state.pointLists) if e.count(whose_move) > 0]
  # All combos that don't involve the same checker
  move_combos = [','.join((str(x), str(y))) for x in position for y in position if x != y]
  # Add in reverses
  r_combos = [','.join((str(x), 'R')) for x in move_combos]
  # All same checker moves
  dice_list = [die1, die2]
  same_combos = [','.join((str(x),str(x + d))) for d in dice_list for x in position]
  move_combos.extend(same_combos)
  # Add in passes
  move_combos.append('p')
  pass_combos = [','.join((str(x),'p')) for x in position]
  move_combos.extend(pass_combos)

  ## Remove combos that include moving two pieces from a position with only one
  admissible_moves = [i for i in move_combos if check_move(i, state, whose_move, die1, die2)]
  
  return(admissible_moves)

# Check if a move is allowed (we took most of this from gameMaster)
def check_move (move, state, whose_move, die1, die2):
  move_list = move.split(',')
  if len(move_list)==3 and move_list[2] in ['R','r']:
    dice_list = [die2, die1]
  else:
    dice_list = [die1, die2]
  if move == 'p':
    return True
  checker1, checker2 = move_list[:2]
  tempState = bgstate(state)
  for i in range(2):
    if i == 1 and checker2 == 'p':
      return True
    pt = int([checker1, checker2][i])
    die = dice_list[i]
    # Check first for a move from the bar:
    if pt==0:
      # Player must have a checker on the bar.
      if not whose_move in tempState.bar:
        return False
      # Player must be able to move into place off bar
      if whose_move==W: 
        target_point=die
      else: 
        target_point=25-die
      pointList = tempState.pointLists[target_point-1]
      if pointList!=[] and pointList[0]!=who and len(pointList)>1:
        return False
      return True
    # Now make sure player does NOT have a checker on the bar.
    if any_on_bar(tempState, whose_move):
      return False 
    # Is checker available on point pt?
    if pt < 1 or pt > 24:
      return False
    if not whose_move in tempState.pointLists[pt-1]:
      return False
    # Determine whether destination is legal.
    if whose_move==W:
      dest_pt = pt + die
    else:
      dest_pt = pt - die
    if dest_pt > 24 or dest_pt < 1:
      return bearing_off_allowed(tempState, whose_move)
    dest_pt_list = tempState.pointLists[dest_pt-1]
    if len(dest_pt_list) > 1 and dest_pt_list[0]!=whose_move:
      return False
    if(i == 0):
      tempState = updateState(tempState, ','.join((checker1, 'p')), die1, die2, whose_move)
  return True

def updateState(state, m, die1, die2, whose_move):
  tempState = bgstate(state)
  moves = m.split(',')
  if (len(moves) == 1):
    return state
  pos1 = int(moves[0])
  if (moves[1] == 'p'):
    tempState.pointLists[pos1 - 1].pop()
    dest1 = getDest(pos1, die1, whose_move)
    tempState.pointLists[dest1 - 1].append(whose_move)
    return tempState
  if (len(moves) == 3):
    pos2 = pos1
    pos1 = int(moves[1])
  else:
    pos2 = int(moves[1])
  dest1 = getDest(pos1, die1, whose_move)
  dest2 = getDest(pos2, die2, whose_move)
  tempState.pointLists[pos1 - 1].pop()
  tempState.pointLists[dest1 - 1].append(whose_move)
  tempState.pointLists[pos2 - 1].pop()
  tempState.pointLists[dest2 - 1].append(whose_move)
  return tempState
  # if whose_move==W:
  #   dest_pt1 = pos1 + die1
  #   dest_pt2 = pos2 + die2
  # else:
  #   dest_pt1 = pos1 - die1
  #   dest_pt2 = pos2 - die2

def getDest(pos, die, whose_move):
  return (pos + die) if (whose_move == W) else (pos - die)

def bearing_off_allowed(state, who):
  # True provided no checkers of this color on the bar or in
  # first three quadrants.
  if any_on_bar(state, who): return False
  if who==W: point_range=range(0,18)
  else: point_range=range(6,24)
  pl = state.pointLists
  for i in point_range:
    if pl[i]==[]: continue
    if pl[i][0]==who: return False
  return True

def any_on_bar(state, who):
  return who in state.bar