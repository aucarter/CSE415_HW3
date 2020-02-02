'''dbg_agent.py
This Backgammon player implements the Minimax and Alpha-Beta pruning algorithms
in identifying the best move in the Deterministic Simplified Backgammon game.
'''

from backgState import *
from testStates import *

# Define a class for agent
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
  
  ## Total distance of W pieces from being off
  w_position = [i.count(False) for i in state.pointLists]
  w_dist = sum([(24 - i[0])*i[1] for i in enumerate(w_position)])
  # Total distance of R pieces from being off
  r_position = [i.count(True) for i in state.pointLists]
  r_dist = sum([(i[0] + 1)*i[1] for i in enumerate(r_position)])
  # Take the net of the two, with R distance being positive and W being bad
  net = r_dist - w_dist

  ## Number on the bar
  net += state.bar.count(W)*-24
  net += state.bar.count(R)*24

  ## Number off
  net += len(state.white_off)*25
  net += len(state.red_off)*-25
  return(net)

def findAdmissibleMoves(state, whose_move, die1, die2):
  ## Enumerate all possible moves
  # Identify the positions of the pieces
  position = [i + 1 for i, e in enumerate(state.pointLists) if e.count(whose_move) > 0]
  # All combos that don't involve the same checker
  move_combos = [','.join((str(x), str(y))) for x in position for y in position if x != y]
  # All same checker moves
  dice_list = [die1, die2]
  if whose_move == W:
    same_combos = [','.join((str(x),str(x + d))) for d in dice_list for x in position]
  else:
    same_combos = [','.join((str(x),str(x - d))) for d in dice_list for x in position]
  move_combos.extend(same_combos)
  # Add in passes on second move
  pass_combos = [','.join((str(x),'p')) for x in position]
  move_combos.extend(pass_combos)
  # Add in moves off of the bar
  if whose_move in state.bar:
    move_combos.append(('0,p'))
    if(state.bar.count(whose_move) == 1):
      bar_combos = [','.join(('0', str(x))) for x in position]
      move_combos.extend(bar_combos)
      # add in where the checker ends up after getting moved off
      if whose_move == W:
        move_combos.append(','.join(('0', str(die1))))
        move_combos.append(','.join(('0', str(die2))))
      else:
        move_combos.append(','.join(('0', str(24 - die1 + 1))))
        move_combos.append(','.join(('0', str(24 - die2 + 1))))        
    else:
      move_combos.append('0,0')
  # Add in reverses
  r_combos = [','.join((x, 'R')) for x in move_combos]
  move_combos.extend(r_combos)
  # Add complete pass
  move_combos.append('p')
  ## Remove moves that are not admissible
  admissible_moves = [i for i in move_combos if check_move(i, state, whose_move, die1, die2)]
  
  return(admissible_moves)

def check_move (move, state, whose_move, die1, die2):
  if move in ["P", "p"]:
    return True
  else:
    try:
      move_list = move.split(',')
      if len(move_list)==3 and move_list[2] in ['R','r']:
        dice_list = [die2, die1]
      else:
        dice_list = [die1, die2]
      checker1, checker2 = move_list[:2]
    except:
      return False
    hold_state = bgstate(state)
    for i in range(2):
      # Just in case the player wants to pass after the first checker is moved:
      if i==1 and checker2 in ['P','p']:
        return True

      pt = int([checker1, checker2][i])
      # Check first for a move from the bar:
      if pt==0:
        # Player must have a checker on the bar.
        if not whose_move in hold_state.bar:
          return False
        new_state = handle_move_from_bar(hold_state, whose_move, dice_list[i])
        if not new_state:
          return False
        hold_state = new_state
        continue
      # Now make sure player does NOT have a checker on the bar.
      if any_on_bar(hold_state, whose_move):
        return False
      # Is checker available on point pt?
      if pt < 1 or pt > 24:
        return False
      if not whose_move in hold_state.pointLists[pt-1]:
        return False
      # Determine whether destination is legal.
      die = dice_list[i]
      if whose_move==W:
        dest_pt = pt + die
      else:
        dest_pt = pt - die
      if dest_pt > 24 or dest_pt < 1:
        born_off_state = bear_off(hold_state, pt, dest_pt, whose_move)
        if born_off_state:
          hold_state = born_off_state
          continue
        return False
      
      dest_pt_list = hold_state.pointLists[dest_pt-1]
      if len(dest_pt_list) > 1 and dest_pt_list[0]!=whose_move:
        return False
      # So this checker's move is legal. Update the state.
      new_state = bgstate(hold_state)
      # Remove checker from its starting point.
      new_state.pointLists[pt-1].pop()
      # If the destination point contains a single opponent, it's hit.
      new_state = hit(new_state, dest_pt_list, dest_pt)
      # Now move the checker into the destination point.
      new_state.pointLists[dest_pt-1].append(whose_move)
      hold_state = new_state
    return True

def updateState(current_state, move, die1, die2, whose_move):
  hold_state = bgstate(current_state)
  if move in ["P", "p"]:
    new_state = bgstate(hold_state)
    new_state.whose_move=1-whose_move
    return new_state
  else:
    move_list = move.split(',')
    if len(move_list)==3 and move_list[2] in ['R','r']:
      dice_list = [die2, die1]
    else:
      dice_list = [die1, die2]
    checker1, checker2 = move_list[:2]
    for i in range(2):
      # Just in case the player wants to pass after the first checker is moved:
      if i==1 and checker2 in ['P','p']:
        new_state = bgstate(hold_state)
        new_state.whose_move=1-whose_move
        return new_state
      pt = int([checker1, checker2][i])
      # Move off of bar
      if pt==0:
        new_state = handle_move_from_bar(hold_state, whose_move, dice_list[i])
        hold_state = new_state
        continue
      # Determine whether destination is legal.
      die = dice_list[i]
      if whose_move==W:
        dest_pt = pt + die
      else:
        dest_pt = pt - die
      if dest_pt > 24 or dest_pt < 1:
        born_off_state = bear_off(hold_state, pt, dest_pt, whose_move)
        if born_off_state:
          hold_state = born_off_state
          continue
      dest_pt_list = hold_state.pointLists[dest_pt-1]
      # So this checker's move is legal. Update the state.
      new_state = bgstate(hold_state)
      # Remove checker from its starting point.
      new_state.pointLists[pt-1].pop()
      # If the destination point contains a single opponent, it's hit.
      new_state = hit(new_state, dest_pt_list, dest_pt)
      # Now move the checker into the destination point.
      new_state.pointLists[dest_pt-1].append(whose_move)
      hold_state = new_state
    return hold_state


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

def handle_move_from_bar(state, who, die):
  # We assume there is a piece of this color available on the bar.
  if who==W: target_point=die
  else: target_point=25-die
  pointList = state.pointLists[target_point-1]
  if pointList!=[] and pointList[0]!=who and len(pointList)>1:
     return False
  new_state = bgstate(state)
  new_state = hit(new_state, pointList, target_point)
  remove_from_bar(new_state, who)
  new_state.pointLists[target_point-1].append(who)
  return new_state

def remove_from_bar(new_state, who):
  #removes a white from start of bar list,
  # or a red from the end of the bar list.
  if who==W:
    del new_state.bar[0]
  else:
    new_state.bar.pop()


def hit(new_state, dest_pt_list, dest_pt):
  opponent = 1-new_state.whose_move
  if len(dest_pt_list)==1 and dest_pt_list[0]==opponent:
    if opponent==W:
      new_state.bar.insert(W, 0) # Whites at front of bar
    else:
      new_state.bar.append(R) # Reds at end of bar
    new_state.pointLists[dest_pt-1]=[]
  return new_state

def bear_off(state, src_pt, dest_pt, who):
  # Return False if 'who' is not allowed to bear off this way.
  # Otherwise, create the new state showing the result of bearing
  # this one checker off, and return the new state.

  # First of all, is bearing off allowed, regardless of the dice roll?
  if not bearing_off_allowed(state, who): return False
  # Direct bear-off, if possible:
  pl = state.pointLists[src_pt-1]
  if pl==[] or pl[0]!=who:
    return False
  # So there is a checker to possibly bear off.
  # If it does not go exactly off, then there must be
  # no pieces of the same color behind it, and dest
  # can only be one further away.
  good = False
  if who==W:
    if dest_pt==25:
       good = True
    elif dest_pt==26:
       for point in range(18,src_pt-1):
         if W in state.pointLists[point]: return False
       good = True
  elif who==R:
    if dest_pt==0:
       good = True
    elif dest_pt== -1:
       for point in range(src_pt, 6):
         if R in state.pointLists[point]: return False
       good = True
  if not good: return False 
  born_off_state = bgstate(state)
  born_off_state.pointLists[src_pt-1].pop()
  if who==W: born_off_state.white_off.append(W)
  else:  born_off_state.red_off.append(R)
  return born_off_state
