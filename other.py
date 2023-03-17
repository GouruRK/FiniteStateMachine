from automaton import FiniteStateMachine
from random import choices, randint, choice

def gen_words(alpha, n_words, len_words):
    return ["".join(choices(alpha, k=len_words)) for _ in range(n_words)]
        

def random_fsm(alpha, n_states):
    states = {i for i in range(1, n_states + 1)}
    ni_states = randint(1, n_states)
    nf_states = randint(1, n_states)
    i_states = {randint(1, n_states) for _ in range(ni_states)}
    f_states = {randint(1, n_states) for _ in range(nf_states)}
    table = set()
    for _ in range(n_states * 2 + 1):
        table.add((randint(1, n_states), choice(alpha), randint(1, n_states)))
    return FiniteStateMachine(alpha, states, i_states, f_states, table)
