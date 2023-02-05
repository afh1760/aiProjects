import heapq




def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    pos = [[0,0], [1,0], [2,0], 
           [0,1], [1,1], [2,1],
           [0,2], [1,2], [2,2]]
    distance = 0
    for x in range(9):
        if from_state[x] == to_state[x] or from_state[x] == 0:
            pass
        else:
            index = from_state[x] - 1
            for y in range(2):
                 distance += abs(pos[x][y]-pos[index][y])
    return distance




def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    pos = [[0,0], [1,0], [2,0], 
           [0,1], [1,1], [2,1],
           [0,2], [1,2], [2,2]]
    zeros = []
    for x in range(9):
        if state[x] == 0:
            zeros.append(x)        
    succ_states = [] 
    for x in zeros:
        for y in range(9):
            tempdist = 0
            for z in range(2):
                tempdist += abs(pos[x][z]-pos[y][z])
            if tempdist == 1 and state[y] != 0:
                tempstate = state.copy()
                tempstate[x] = tempstate[y]
                tempstate[y] = 0
                succ_states.append(tempstate)        
    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    pqOpen = []
    pqClose = []
    initialCost = get_manhattan_distance(state)
    heapq.heappush(pqOpen, (initialCost, state, (0, initialCost, -1)))
    g = 0
    index = -1
    maxQueueLength = 0
    while True:
        if len(pqOpen) == 0:
            break
        
        selected = heapq.heappop(pqOpen)
        
        pqClose.append(selected)
        index += 1
        
        if selected[1] == goal_state:
            index2 = index
            steps = []
            while index2 > -1:
                steps.insert(0, pqClose[index2])
                parentIndex = pqClose[index2][2][2]
                index2 = parentIndex
            for i in steps:    
                print(f'{i[1]} h={i[2][1]} moves: {i[2][0]}')
            print(f'Max queue length: {maxQueueLength}')
            break
        
        g = selected[2][0] + 1
        potential_succ = get_succ(selected[1])
        
        if len(potential_succ) > 0:
            for i in potential_succ:
                isInSet = 0
                for j in pqClose:
                    if i == j[1]:
                        isInSet += 1
                        break
                if isInSet == 0:
                    h = get_manhattan_distance(i)
                    node = (g+h, i, (g, h, index))
                    heapq.heappush(pqOpen, node)
        if len(pqOpen) > maxQueueLength:
            maxQueueLength = len(pqOpen)
                    
        
 
if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
# =============================================================================
#     print_succ([2,5,1,4,0,6,7,0,3])
#     print()
# 
#     print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
#     print()
# 
# =============================================================================
# =============================================================================
#     solve([2,5,1,4,0,6,7,0,3])
#     print()
#     
#     solve([4,3,0,5,1,6,7,2,0])
# =============================================================================
    solve([3, 4, 6, 0, 0, 1, 7, 2, 5])
    solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    solve([0, 4, 7, 1, 3, 0, 6, 2, 5])
    solve([5, 2, 3, 0, 6, 4, 7, 1, 0])
    solve([1, 7, 0, 6, 3, 2, 0, 4, 5])
