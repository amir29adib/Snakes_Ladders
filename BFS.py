
class QueueEntry(object):
    def __init__(self, nodeNumberInQueue=0, numberOfMove=0, path=None):
        self.nodeNumberInQueue = nodeNumberInQueue
        self.numberOfMove = numberOfMove
        self.path = path if path is not None else []


def getMinThrows(move, tableCellsNumber):
    visited = [False] * (tableCellsNumber + 1)
    queue = []

    visited[0] = True
    queue.append(QueueEntry(0, 0, []))

    while queue:
        qe = queue.pop(0)
        nodeNumberInQueue = qe.nodeNumberInQueue

        if nodeNumberInQueue == tableCellsNumber:
            return qe.path

        j = nodeNumberInQueue + 1
        while j <= nodeNumberInQueue + 2 and j < tableCellsNumber + 1:
            if not visited[j]:
                visited[j] = True
                new_path = qe.path + [j]
                if moves[j] != j and moves[j] != -1:
                    print(str(j) + '=>' + str(moves[j]))
                    new_path += [moves[j]]
                queue.append(QueueEntry(move[j] if move[j] != -1 else j, qe.numberOfMove + 1, new_path))
            j += 1


# Input number of cells
table_size = input("Enter size of table: ")
tableX, tableY = map(int, table_size.split('*'))
tableCellsNumber = tableX * tableY
moves = [-1] * (tableCellsNumber + 1)

# Input number and location of ladders
LaddersNumber = int(input("Enter number of ladders: "))
for i in range(LaddersNumber):
    ladder_location = input(f'Enter location of ladder {i + 1}: ')
    LadderStart, LadderEnd = map(int, ladder_location.split(','))

    if LadderStart >= LadderEnd:
        print("For Ladders location of start cell can't be greater or equal to end cell")
        exit()

    moves[LadderStart] = LadderEnd

# Input number and location of snakes
SnakesNumber = int(input("Enter number of snakes: "))
for i in range(SnakesNumber):
    snake_location = input(f'Enter location of snake {i + 1}: ')
    SnakeEnd, SnakeStart = map(int, snake_location.split(','))

    if SnakeStart <= SnakeEnd:
        print("For Snakes location of end cell can't be greater or equal to start cell")
        exit()

    moves[SnakeStart] = SnakeEnd


# Calculate number and location of marginal jumps
count = 1
for i in range(tableY - 1):
    moves[count] = count + (tableX * 2 - 1)
    if (count - 1) != 0:
        moves[count - 1] = count

    count += tableX

result_path = getMinThrows(moves, tableCellsNumber)
print("Optimal path is:", result_path)
if result_path is not None:
    MinThrows = len(result_path)
    print("Min throws required is {0}".format(MinThrows))
