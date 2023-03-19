from automaton import FiniteStateMachine
from random import choices, randint, choice

def gen_words(alpha: set[str], n_words: int, len_words: int):
    """Generate a list of random words

    Parameters
    ----------
    alpha : set[str]
        List of letters
    n_words : int
        Number of words to generate
    len_words : int
        Length of words

    Returns
    -------
    lst[str]
        List of random words
    """
    return ["".join(choices(alpha, k=len_words)) for _ in range(n_words)]
        

def random_fsm(alpha: set[str], n_states: int) -> FiniteStateMachine:
    """Create a random FiniteStateMachine

    Parameters
    ----------
    alpha : set[str]
        List of letters
    n_states : int
        Max number of states

    Returns
    -------
    FiniteStateMachine
        An accessible FiniteStateMachine
    """
    states = {i for i in range(1, n_states + 1)}
    ni_states = randint(1, n_states)
    nf_states = randint(1, n_states)
    i_states = {randint(1, n_states) for _ in range(ni_states)}
    f_states = {randint(1, n_states) for _ in range(nf_states)}
    table = set()
    for _ in range(n_states * 2 + 1):
        table.add((randint(1, n_states), choice(alpha), randint(1, n_states)))
    return FiniteStateMachine(alpha, states, i_states, f_states, table).set_accessible()
