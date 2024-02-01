import random


class QLearning:
    def __init__(self, table_size, ladders, snakes):
        self.tableX, self.tableY = map(int, table_size.split('*'))
        self.tableCellsNumber = self.tableX * self.tableY
        self.moves = [-1] * (self.tableCellsNumber + 1)
        self.q_table = {}
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 1.0  # Exploration probability
        self.epsilon_decay = 0.95  # Exploration probability decay rate

        # Input number and location of ladders
        for start, end in ladders:
            if start >= end:
                print("For ladders, the start cell must be less than the end cell.")
                exit()
            self.moves[start] = end

        # Input number and location of snakes
        for end, start in snakes:
            if start <= end:
                print("For snakes, the end cell must be less than the start cell.")
                exit()
            self.moves[start] = end

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Explore: Choose a random action
            return random.choice(self.get_possible_actions(state))
        else:
            # Exploit: Choose the action with the highest Q-value
            return self.get_best_action(state)

    def get_possible_actions(self, state):
        return list(range(state + 1, min(state + 3, self.tableCellsNumber + 1)))

    def get_best_action(self, state):
        possible_actions = self.get_possible_actions(state)

        # Check if there are any possible actions
        if not possible_actions:
            return state

        return max(possible_actions, key=lambda a: self.get_q_value(state, a))

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        old_q_value = self.get_q_value(state, action)
        best_next_action = self.get_best_action(next_state)
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * self.get_q_value(next_state, best_next_action) - old_q_value)
        self.q_table[(state, action)] = new_q_value

    def decay_epsilon(self):
        self.epsilon *= self.epsilon_decay

    def run_q_learning(self, start_state):
        current_state = start_state
        total_moves = 0

        while current_state != self.tableCellsNumber:
            action = self.choose_action(current_state)

            # Move to the next state
            next_state = self.moves[action] if self.moves[action] != -1 else action

            # Reward calculation (you can adjust this based on your requirements)
            if next_state > current_state:
                reward = 1.0  # Moving forward
            else:
                reward = -1.0  # Moving backward

            # Update Q-value
            self.update_q_value(current_state, action, reward, next_state)

            # Move to the next state
            current_state = next_state
            total_moves += 1

        return total_moves

    def get_optimal_path(self, start_state):
        current_state = start_state
        path = []

        while current_state != self.tableCellsNumber:
            action = self.get_best_action(current_state)

            # Move to the next state
            next_state = self.moves[action] if self.moves[action] != -1 else action

            # Update path
            if self.moves[action] != -1:
                path.append(action)

            path.append(next_state)

            # Move to the next state
            current_state = next_state

        return path


# Input number of cells
table_size = input("Enter size of table: ")

# Input number and location of ladders
ladders = []
LaddersNumber = int(input("Enter number of ladders: "))
for i in range(LaddersNumber):
    ladder_location = input(f'Enter location of ladder {i + 1}: ')
    ladders.append(tuple(map(int, ladder_location.split(','))))


# Calculate number and location of marginal jumps
tableX, tableY = map(int, table_size.split('*'))
count = 1
for i in range(tableY - 1):
    jump_location = str(count) + ',' + str(count + (tableX * 2 - 1))
    ladders.append(tuple(map(int, jump_location.split(','))))

    if (count - 1) != 0:
        jump_location = str(count - 1) + ',' + str(count)
        ladders.append(tuple(map(int, jump_location.split(','))))

    count += tableX


# Input number and location of snakes
snakes = []
SnakesNumber = int(input("Enter number of snakes: "))
for i in range(SnakesNumber):
    snake_location = input(f'Enter location of snake {i+1}: ')
    snakes.append(tuple(map(int, snake_location.split(','))))

# Create and run Q-learning
ql = QLearning(table_size, ladders, snakes)

# Number of training episodes (you can adjust this based on your requirements)
epochs = 100

for epoch in range(epochs):
    start_state = 0
    total_moves = ql.run_q_learning(start_state)
    ql.decay_epsilon()

# Get the optimal path
result_path = ql.get_optimal_path(start_state)

print("Optimal path is:", result_path)
print("Min Dice throws required is {0}".format(len(result_path)))  # Subtract 1 to get the number of moves
