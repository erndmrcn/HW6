# Eren Demircan 2237246
# CEng462 - AI - Hidden Markov Models

# global variables and structure 
states = []
start_probabilities = dict()
transition probabilities = dict()
observation_probabilities = dict()
observations = []

def read_input(file_name):
    global states, observations
    global start_probabilities, transition_probabilities, observation_probabilities
    with open(file_name, 'rb') as f:
        lines = f.readlines()

    # states
    line = lines[0]
    if line == '[states]':
        line = lines[1]
        ss = line.split('|')
        for s in ss:
            states.append(s)

    # start probabilities
    line = lines[2]
    if line == '[start probabilities]':
        pass

    # transition probabilities
    line = lines[4]
    if line == '[transition probabilities]':
        pass

    # observation probabilities
    line = lines[6]
    if line == '[observation probabilities]':
        pass

    # observations
    line = lines[8]
    if line == '[observations]':
        pass

    return


# run hidden markov model
def hmm():
    return

def viterbi(file_name):
    return