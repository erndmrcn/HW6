# Eren Demircan 2237246
# CEng462 - AI - Hidden Markov Models

# global variables and structure 
states = []
start_probabilities = dict()
transition_probabilities = dict()
observation_probabilities = dict()
observations = []

# reads input file and writes into the appropriate variable
def read_input(file_name):
    global states, observations
    global start_probabilities, transition_probabilities, observation_probabilities

    with open(file_name, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line[-1] == '\n':
            lines[i] = line[:-1]

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
        sprobs = lines[3].split('|')
        for prob in sprobs:
            splitted = prob.split(":")
            stt = splitted[0]
            val = float(splitted[1])
            start_probabilities.update({stt: val})

    # transition probabilities
    line = lines[4]
    if line == '[transition probabilities]':
        tprobs = lines[5].split("|")
        for prob in tprobs:
            splitted = prob.split(':')
            transition_probabilities.update({splitted[0]: float(splitted[1])})

    # observation probabilities
    line = lines[6]
    if line == '[observation probabilities]':
        oprobs = lines[7].split('|')
        for prob in oprobs:
            splitted = prob.split(':')
            observation_probabilities.update({splitted[0]: float(splitted[1])})

    # observations
    line = lines[8]
    if line == '[observations]':
        splitted = lines[9].split('|')
        for obs in splitted:
            observations.append(obs)

    return


# resets all global variables
# when imported, sequent viterbi calls, results in stacks in the global variables 
def reset():
    global states, observations
    global start_probabilities, transition_probabilities, observation_probabilities
    states = []
    observations = []
    start_probabilities, transition_probabilities, observation_probabilities = dict(), dict(), dict()
    return


# returns observation probability from global variable
def get_obs_prob(state, evidence):
    query = state + '-' + evidence
    return observation_probabilities[query]


# returns transition probability from global variable
def get_trans_prob(state1, state2):
    query = state1 + '-' + state2
    return transition_probabilities[query]


# implementation of viterbi algorith
def viterbi(file_name):
    global states, observations
    global start_probabilities, transition_probabilities, observation_probabilities

    reset()

    read_input(file_name)

    N = len(observations)
    # for m dict to be used
    m = dict()
    for t in range(N):
        for state in states:
            m.update({f'{t}-'+state: float(0.0)})

    # for a dict to be used
    a = dict()
    for t in range(N):
        for state in states:
            a.update({f'{t}-'+state: ""})

    # N -> total time elapse
    for t in range(N):
        for i, state in enumerate(states):
            # beginning
            if t == 0:
                # calculate time 0 values
                val = start_probabilities[state]*get_obs_prob(state, observations[t])
                ind = f"{t}-"+state
                m[ind] = val
            else:
                # calculate probabilites fot t > 0
                temp_dict = dict()
                ind = f"{t}-"+state
                for s in states:
                    temp_ind = f"{t-1}-"+s
                    temp_val = get_trans_prob(s, state) * m[temp_ind] 
                    temp_dict.update({s: temp_val})

                # keeps selected path at each step
                a_value = max(temp_dict, key=temp_dict.get)
                a[ind] = a_value
                ind2 = f"{t-1}-"+a_value
                # keeps state probabilities
                m_value = get_obs_prob(state, observations[t]) * get_trans_prob(a_value, state) * m[ind2]
                m[ind] = m_value
    
    # preparing output
    path = []
    x_n = []
    t_max = -9999
    max_state = None
    # find last max state 
    for state in states:
        last_step = m[f"{len(observations)-1}-{state}"]
        if t_max <= last_step:
            t_max = last_step
            max_state = state

    # backward-pass
    # find maxes in each turn and go up to the beginning
    x_n.append(max_state)
    path.append(max_state)
    t = len(observations) - 1
    while t >= 1:
        temp = a[f"{t}-{x_n[0]}"]
        path.append(temp)
        x_n.append(temp)
        t -= 1

    path = list(reversed(path))

    # state probabilities
    result = dict()
    for state in states:
        result.update({state: []})

    for i, state in enumerate(states, 0):
        for val in m.keys():
            if state in val:
                s = result[state]
                if s is None or len(s) <= 0:
                    s = [m[val]]
                else:
                    s.append(m[val])
                result.update({state: s})
            else:
                pass

    # max value for the model
    max_value = m[f"{len(observations)-1}-" + max_state]
    return path, max_value, result

# viterbi("process1.txt")