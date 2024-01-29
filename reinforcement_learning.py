import itertools
import random
from config import POINTS_SYSTEM
import sys

# Define the Q-Learning parameters
alpha = 0.1
gamma = 0.9
initial_epsilon = 1.0  # Start with 100% exploration
min_epsilon = 0.01     # Minimum value of epsilon (% of exploration)
epsilon = initial_epsilon

history_length = 3
encoding_type = 'alternating' # {myAction, opponentAction, myAction, opponentAction}
order = 'old_to_new'

q_table = {}

def print_q_table(very_verbose):
    if very_verbose: print(f"This is the q_table")
    for state, actions in q_table.items():
        action_values = ', '.join([f"{action}: {value:.2f}" for action, value in actions.items()])
        if very_verbose: 
            if q_table[state]['C'] > q_table[state]['D']:
                print(f"State {state}: {action_values} select C")
            elif q_table[state]['D'] > q_table[state]['C']:
                print(f"State {state}: {action_values} select D")
            else:
                print(f"State {state}: {action_values}")

def initialize_q_table(history_length):

    q_table = {}

    # Define the possible actions
    actions = ['C', 'D']

    # Generate all possible states (history_length and encoding_type don't matter for this)
    state_combinations = itertools.product(actions, repeat=history_length * 2)

    # Flatten the tuples to create state strings
    states = [''.join(state) for state in state_combinations]

    # Initialize the Q-table
    q_table = {state: {'C': 0, 'D': 0} for state in states}
    return q_table

def get_best_action(q_table, state, very_verbose): # for a given state, find the best action from the Q table

    # Assuming q_table[state] has keys 'C' and 'D'
    if q_table[state]['C'] == q_table[state]['D']:
        # let's return the value which has overall more weight
        sum_c = 0
        sum_d = 0

        for index_state in q_table:
            sum_c += q_table[index_state].get('C', 0)  # Add the value of 'C', defaulting to 0 if not found
            sum_d += q_table[index_state].get('D', 0)  # Add the value of 'D', defaulting to 0 if not found

        if sum_d > sum_c:
            if very_verbose: print(f"State {state} doesn't have a pref action, but D seems to be the best action overall")
            action = 'D'
        else:
            if very_verbose: print(f"State {state} doesn't have a pref action, but C seems to be the best action overall")
            action = 'C'

        # action = 'C'  # now that I gave negative value to D (-1), let's have a bias for C
        # action = random.choice(['C', 'D'])  # Randomly choose if values are equal
    else:
        action = max(q_table[state], key=q_table[state].get)  # Best action based on Q-table

    # action = max(((action, value) for action, value in q_table[state].items()), key=lambda x: x[1])[0]
    # if action == 'D':
    #     print (f"For state {state}, step {step}, best action is {action}")
    return action

def process_history(myHistory, opponentHistory, who, very_verbose):

    if order == 'old_to_new': #newest moves are at the end of the array
    # Trim histories if they are longer than the maximum single history length
    # we take the latest moves (which is what we want)
        if len(myHistory) > history_length:
            myHistory = myHistory[-history_length:]
        if len(opponentHistory) > history_length:
            opponentHistory = opponentHistory[-history_length:]
    else:
        print(f"This code is meant for old_to_new encoding", file=sys.stderr)

    # Print to stderr
    if very_verbose: print(f"[{who}] [process_history] input myHistory:       {myHistory}")
    if very_verbose: print(f"[{who}] [process_history] input opponentHistory: {opponentHistory}")

    if order == 'old_to_new': #newest moves are at the end of the array
        # Pad each history with 'C' (which encodes to 0) to ensure they are of equal length
        myHistory = (['C'] * (history_length - len(myHistory))) + myHistory
        opponentHistory = (['C'] * (history_length - len(opponentHistory))) + opponentHistory
    else:
        print(f"This code is meant for old_to_new encoding, file=sys.stderr")


    # state = myHistory + opponentHistory
    # Combine both histories into a single list
    if encoding_type == 'alternating':
        # Alternating elements from myHistory and opponentHistory
        state = ''.join(myHistory[i] + opponentHistory[i] for i in range(history_length))
    else:
        print(f"This code is meant for alternating encoding, file=sys.stderr")

    if very_verbose: print(f"[{who}] [process_history] output state: {state}")

    return state

def make_decision(myHistory, opponentHistory, very_verbose):
    global q_table
    global epsilon

    if len(myHistory) == 0:
        q_table = initialize_q_table(history_length)
        if very_verbose: print(f"qtable has been initialized")
        epsilon = initial_epsilon
        if very_verbose: print(f"epsilon has been initialized")

    if random.random() < epsilon:
        if len(opponentHistory) == 0 or 'D' not in opponentHistory:
            nextAction = 'C'
            if very_verbose: print (f"No reason to attack first - random action: {nextAction}")
        else:
            nextAction = random.choice(['C', 'D'])
            if very_verbose: print (f"epsilon: {epsilon} random action: {nextAction}")
            # Update epsilon
            if epsilon > min_epsilon:
                epsilon = max(min_epsilon, epsilon / 2)
    else:
        state = process_history(myHistory, opponentHistory,"make_decision", very_verbose)
        nextAction = get_best_action(q_table, state, very_verbose)
        if very_verbose: print (f"state: {state} q_table[state]: {q_table[state]} best action: {nextAction}")

    return nextAction

def train_model(myHistory, opponentHistory, myAction, opponentAction, very_verbose):
    myReward, opponentReward = POINTS_SYSTEM[myAction+opponentAction]
    if myReward == 0:
        # because 0 is the same value of initialization for q_table,
        # let's try to mark the difference with 0, which is the worst result in prisoner dilemma
        myReward = -1 
    # if myReward == 1:
    #     # DD is 11 CD is 05 and DD is CC
    #     # let's see what happens when DD doesn't start to tip the state
    #     # to incentivate trying to play C next time
    #     myReward = 0
    state = process_history(myHistory, opponentHistory,"train_model", very_verbose)
    if very_verbose: print(f"[train_model] state: {state}")
    nextState = process_history(myHistory+[myAction], opponentHistory+[opponentAction],"train_model", very_verbose)
    if very_verbose: 
        print(f"[train_model] nextState: {nextState}")
        print(f"[train_model] myAction: {myAction} myReward: {myReward}")
        print(f"[train_model] q_table[{state}] before: {q_table[state]}")
        print(f"[train_model] (alpha) {alpha}")
        print(f"[train_model] max(q_table[nextState].values()) {max(q_table[nextState].values())}")
        print(f"[train_model] gamma * max(q_table[nextState].values()) {gamma * max(q_table[nextState].values())}")
        print(f"[train_model] myReward + gamma * max(q_table[nextState].values()) - q_table[state][myAction] {myReward + gamma * max(q_table[nextState].values()) - q_table[state][myAction] }")
        print(f"[train_model] alpha * (myReward + gamma * max(q_table[nextState].values()) - q_table[state][myAction]) {alpha * (myReward + gamma * max(q_table[nextState].values()) - q_table[state][myAction])}")
    # q_table[state][myAction] = (1 - alpha) * q_table[state][myAction] + alpha * (myReward + gamma * max(q_table[nextState].values()))
    q_table[state][myAction] += alpha * (myReward + gamma * max(q_table[nextState].values()) - q_table[state][myAction])

    if very_verbose: print(f"[train_model] q_table[{state}] after: {q_table[state]}")


