from collections import deque
from typing import Any
from itertools import product

class FiniteStateMachine:
    def __init__(
        self,
        alphabet: set[str],
        Q: None | set[Any] = None,
        Qi: None | set[Any] = None,
        Qf: None | set[Any] = None,
        table: None | set[tuple[Any, str, Any]] = None,
    ) -> None:
        """Initialise a FiniteStateMachine object.

        For more information about finite state automaton (or finite state
        machine), see this arcticle :
        https://en.wikipedia.org/wiki/Finite-state_machine

        Parameters
        ----------
        alphabet : set[str]
            The alphabet to work with
        Q : set[Any] | None
            Differents states of the automaton
        Qi : set[Any] | None
            Initials states must be part of 'Q'
        Qf : set[Any] | None
            Finals states, must be part of 'Q'
        table : set[tuple[Any, str, Any]] | None
            List of transitions/relmations between differents states,
            and the condition to go from one to another.
            Must follow this pattern :
                (q1, l, q2) with :
                    - 'q1' correspond to "from" of the relation, and must be
                      include in 'Q'
                    - 'q2' correspond to "to" of the relation, and must be
                      include in 'Q'
                    - 'l' is the condition to go from 'q1' to 'q2'
        """
        self.alphabet = alphabet
        if Q is None:
            Q = set()
        self.Q = Q
        if Qi is None:
            Qi = set()
        self.Qi = Qi
        if Qf is None:
            Qf = set()
        self.Qf = Qf
        self.relations = {}
        self.conditions = {}
        if table is not None:
            self.load_table(table)

    def __str__(self) -> str:
        """Print automaton.

        Returns
        -------
        str
            Print automaton
        """
        ch = "FiniteStateMachine(\n"
        ch += f"\talphabet: {self.get_alphabet()}\n"
        ch += f"\tstates: {self.get_states()}\n"
        ch += f"\tinitial states: {self.get_initials_states()}\n"
        ch += f"\tfinal states: {self.get_finals_states()}\n"
        ch += f"\ttransition table: {self.create_table()}\n"
        ch += ")"
        return ch

    def __repr__(self) -> str:
        return self.__str__()

    def get_states(self) -> set[Any]:
        """Get all states.

        Returns
        -------
        set[Any]
            States of the automaton
        """
        return self.Q

    def get_finals_states(self) -> set[Any]:
        """Get all finals states.

        Returns
        -------
        set[Any]
            Final states of the automaton
        """
        return self.Qf

    def get_initials_states(self) -> set[Any]:
        """Get all initals states.

        Returns
        -------
        set[Any]
            Initials states of the automaton
        """
        return self.Qi

    def get_alphabet(self) -> set[str]:
        """Get current alphabet.

        Returns
        -------
        set[str]
            Letters that compose the automaton's alphabet
        """
        return self.alphabet
    
    def get_relations(self) -> dict[Any, set[Any]]:
        """Get all relations of the finite state machine.

        Returns
        -------
        dict[Any, set[Any]]
            Relations
        """
        return self.relations
    
    def get_rel(self, a: Any) -> set[Any]:
        """Get all states that are connected to `a`.

        Parameters
        ----------
        a : Any
            State, must be include in 'Q'

        Returns
        -------
        set[Any]
            Set of neighbours states
        """
        relations = self.get_relations()
        if a in relations:
            return relations[a]
        return {}
    
    def get_conditions(self) -> dict[tuple[Any, Any], set[str]]:
        """Get all conditions between states of the finie state machine.

        Returns
        -------
        dict[tuple[Any, Any], set[str]]
            Conditions between states
        """
        return self.conditions

    def get_cond(self, a: Any, b: Any) -> set[str]:
        """Get all conditions that are applied to the relation
        between `a` and `b`.

        Parameters
        ----------
        a : Any
            Initial state of the relation, must be include in `Q`
        b : Any
            Final state of the relation, must be include in `Q`

        Returns
        -------
        set[str]
            Set of conditions used between `a` and `b`
        """
        conditions = self.get_conditions()
        if (a, b) in conditions:
            return conditions[(a, b)]
        return {}

    def check_rel(func):
        """Decorator to check args states and conditions when
        adding/removing relations or conditions.

        Parameters
        ----------
        func : function
            Function to check the validity of its arguments
        """

        def check_rel_decorator(self, *args):
            # Sall test about the length of *args, to know
            # if we are testing/adding a relation or a condition
            if len(args) == 2:
                a, b = args
            elif len(args) == 3:
                a, b, c = args
                # if the condition belongs to the current alphabet
                if c not in self.get_alphabet():
                    raise ValueError(f" : {c}")
            # if the initial and final states of the relations are valids
            # states
            states = self.get_states()
            if a not in states or b not in states:
                raise ValueError
            return func(self, *args)

        return check_rel_decorator

    def exist_rel(self, a: Any, b: Any) -> bool:
        """Test if a relation exists between states `a` and `b`.

        Parameters
        ----------
        a : Any
            Initial state of the relation, must be part of 'Q'
        b : Any
            Final state of the relation, must be part of 'Q'

        Returns
        -------
        bool
            True if a relation exist, else False
        """
        relations = self.get_relations()
        if a in relations:
            return b in relations[a]
        return False
    
    def add_state(self, a: Any):
        """Add a new state in 'Q' called 'a'.

        Parameters
        ----------
        a : Any
            New state
        """
        self.Q.add(a)

    @check_rel
    def add_relation(self, a: Any, b: Any) -> None:
        """Add a relation between states `a` and `b`.

        Parameters
        ----------
        a : Any
            Initial state of the relation, must be part of 'Q'
        b : Any
            Final state of the relation, must be part of 'Q'
        """
        relations = self.get_relations()
        if a in relations:
            relations[a].add(b)
        else:
            relations[a] = {b}

    @check_rel
    def add_condition(self, a: Any, b: Any, c: str) -> None:
        """Add a condition `c` between relation `a` and `b`
        If there are no relation between (`a`, `b`), creates one.

        Parameters
        ----------
        a : Any
            Initial state of the relation, must be part of 'Q'
        b : Any
            Final state of the relation, must be part of 'Q'
        c : str
            New condition between (`a`, `b`), must be part of 'alphabet'
        """
        if not self.exist_rel(a, b):
            self.add_relation(a, b)
        key = (a, b)
        conditions = self.get_conditions()
        if key in conditions:
            conditions[key].add(c)
        else:
            conditions[key] = {c}
        
    def remove_condition(self, a: Any, b: Any, c: str) -> None:
        """Remove a condition `c` between two states `a` and `b`.

        Parameters
        ----------
        a : Any
            State "from", must be part of 'Q'
        b : Any
            State "to", must be part of 'Q'
        c : str
            The condition to remove, must be part of 'alphabet'
        """
        if not self.exist_rel(a, b):
            return
        cond = self.get_cond(a, b)
        if c in cond:
            cond.remove(c)
    
    def remove_relation(self, a: Any, b: Any):
        """Remove a relation between two states `a` and `b`.

        Parameters
        ----------
        a : Any
            State "from", must be part of 'Q'
        b : Any
            State "to", must be part of 'Q'
        """
        if not self.exist_rel(a, b):
            return
        rel = self.get_relations()
        rel[a].remove(b)
        conditions = self.get_conditions()
        conditions.pop((a, b))

    def remove_state(self, q: Any):
        """Remove state `q` from the automaton.

        Parameters
        ----------
        q : Any
            The state to remove, must be part of 'Q'
        """
        states = self.get_states()
        Qi = self.get_initials_states()
        Qf = self.get_finals_states()
        relations = self.get_relations()
        if q not in states:
            return
        for state in states:
            self.remove_relation(q, state)
            self.remove_relation(state, q)
        if q in relations:
            relations.pop(q)
        if q in Qi:
            Qi.remove(q)
        if q in Qf:
            Qf.remove(q)
        states.remove(q)

    def copy(self):
        """Create a copy of the current automaton `self`.

        Returns
        -------
        automaton
            Copy of the current automaton with no overflow issues
        """
        from copy import copy, deepcopy

        a = FiniteStateMachine(
            copy(self.get_alphabet()),
            copy(self.get_states()),
            copy(self.get_initials_states()),
            copy(self.get_finals_states()),
            {},
        )
        a.relations = deepcopy(self.get_relations())
        a.conditions = deepcopy(self.get_conditions())
        return a

    def load_table(self, table: set[tuple[Any, str, Any]]) -> None:
        """Load a transition table.

        Parameters
        ----------
        table : set[tuple[Any, str, Any]]
            List of transitions/relmations between differents states,
            and the condition to go from one to another.
            Must follow this pattern :
                (q1, l, q2) with :
                    - 'q1' correspond to "from" of the relation, and must be
                      include in 'Q'
                    - 'q2' correspond to "to" of the relation, and must be
                      include in 'Q'
                    - 'l' is the condition to go from 'q1' to 'q2', and
                      must be part of `alphabet`
        """
        for src, label, dest in table:
            self.add_condition(src, dest, label)

    def create_table(self) -> set[tuple[Any, str, Any]]:
        """Create a transition table.

        Parameters
        ----------
        table : set[tuple[Any, str, Any]]
            List of transitions/relmations between differents states,
            and the condition to go from one to another.
            Must follow this pattern :
                (q1, l, q2) with :
                    - 'q1' correspond to "from" of the relation, and must be
                      include in 'Q'
                    - 'q2' correspond to "to" of the relation, and must be
                      include in 'Q'
                    - 'l' is the condition to go from 'q1' to 'q2'
        """
        table = set()
        states = self.get_states()
        for a in states:
            for b in states:
                if self.exist_rel(a, b):
                    for c in self.get_cond(a, b):
                        table.add((a, c, b))
        return table

    def create_loop(self, state: Any):
        """Create a 'loop' for `state`. A 'loop' means that
        there is a relation on the same state for each letters
        of the current alphabet.

        Parameters
        ----------
        state : Any
            The state to create the loop on
        """
        for letter in self.get_alphabet():
            self.add_condition(state, state, letter)

    def possible_path(self, src: Any, cond: str) -> set[Any]:
        """Get all neighbours states that you can access with `cond`
        condition from `src` state.

        Parameters
        ----------
        src : Any
            Initial state, must be include in `Q`
        cond : str
            Condition from 'src' to any other states. Must be include
            in 'alphabet'

        Returns
        -------
        set[Any]
            Sets with accessible neighbours states
        """
        res = set()
        for state in self.get_states():
            if self.exist_rel(src, state):
                if cond in self.get_cond(src, state):
                    res.add(state)
        return res

    def exist_path(self, src: Any, dest: Any) -> bool:
        """Test if a path exits between two states `str` and `dest`.

        Parameters
        ----------
        src : Any
            Origin state, must be include in 'Q'
        dest : Any
            Destination state, must be include in 'Q'

        Returns
        -------
        bool
            True if a path exists, else False
        """
        black = set()
        gray = set()
        return self._exist_path(src, dest, black, gray)

    def _exist_path(self, src: Any, dest: Any, black: set[Any],
                    gray: set[Any]) -> bool:
        """Test if a path exists between two states
        This function is no ment to be used directly. The user should
        use 'exist_path' instead, except if he knows what he is doing.

        Parameters
        ----------
        src : Any
            Origin state, must be include in 'Q'
        dest : Any
            Destination state, must be include in 'Q'
        black : set[Any]
            States that have been visited at least two times, and which
            will not be treated anymore
        gray : set[Any]
            States that have been visited at least one time, and which
            will be treated one more time

        Returns
        -------
        bool
            True if a path exists, else False
        """
        if src == dest:
            return True
        if src in black:
            return
        if src in gray:
            gray.remove(src)
            black.add(src)
        else:
            gray.add(src)
        for s in self.get_rel(src):
            if self._exist_path(s, dest, black, gray):
                return True
        return False

    def admit_empty_word(self) -> bool:
        """Check if the current automaton admits the empty word epsilon.

        Returns
        -------
        bool
            True if the automaton admit epsilon, else False
        """
        init = self.get_initials_states()
        final = self.get_finals_states()
        return len(init & final) != 0

    def _admit(self, word: str, src: Any, i: int = 0) -> bool:
        """Test if the automaton admits `word`, depending on the alphabet
        and the relations. This function is not ment to used directly.
        The user should use 'admit' instead, except if he knows what he
        is doing.

        Parameters
        ----------
        word : str
            The word to test
        src : Any
            Starting state
        i : int, optional
            current letter of the world. `i` will range between
            (0, len(word) - 1), by default 0

        Returns
        -------
        bool
            Return True if `word` is admitted, else False
        """
        # Word's parsing finished on a final state : the word is admitted
        if src in self.get_finals_states() and i == len(word):
            return True
        if i == len(word):
            return False

        paths = self.possible_path(src, word[i])

        for p in paths:
            if self._admit(word, p, i + 1):
                return True
        return False

    def admit(self, word: str) -> bool:
        """Test if the automaton admits `word`, depending on the alphabet and
        the relations.

        Parameters
        ----------
        word : str
            Word to be checked

        Returns
        -------
        bool
            True if the word is admitted, else False
        """
        if not len(word):
            return self.admit_empty_word()
        for src in self.Qi:
            if self._admit(word, src):
                return True
        return False
    
    def is_state_accessible(self, q: Any) -> bool:
        """Check is a state `q` is accessible. `q` is accessible
        if there is a path from one initital state to `q`.

        Parameters
        ----------
        q : Any
            The state to check, must be part of 'Q'

        Returns
        -------
        bool
            True if `q` is accessible, else False
        """
        for qi in self.get_initials_states():
            if self.exist_path(qi, q):
                return True
        return False
    
    def is_state_co_accessible(self, q: Any) -> bool:
        """Check is a state `q` is co-accessible. `q` is co-accessible
        if there is a path from `q` to one final state.

        Parameters
        ----------
        q : Any
            The state to check, must be part of 'Q'

        Returns
        -------
        bool
            True if `q` is co-accessible, else False
        """
        for qf in self.get_finals_states():
            if self.exist_path(q, qf):
                return True
        return False
    
    def is_deterministic(self) -> bool:
        """Check if the automaton is deterministic.
        An automaton is deterministic if for each state of the automaton,
        the relation from one state to another is unique for a condition.

        See this arcticle for more information about deterministic automaton:
        https://en.wikipedia.org/wiki/Deterministic_finite_automaton

        Returns
        -------
        bool
            True if the automaton is deterministic, else False
        """
        for state in self.get_states():
            for letter in self.get_alphabet():
                # If from one state you can go to at least 2 states with the
                # same condition, the automaton is not deterministic
                if len(self.possible_path(state, letter)) >= 2:
                    return False
        return True

    def is_complete(self) -> bool:
        """Check if the automaton is complete.
        An automaton is complete if each states have a relation to another
        state with all possibles conditions.

        No arcticle ...

        Returns
        -------
        bool
            True if the automaton is deterministic, else False
        """
        for state in self.get_states():
            for letter in self.get_alphabet():
                if not len(self.possible_path(state, letter)):
                    return False
        return True

    def is_accessible(self) -> bool:
        """Check if the automaton is accessible
        An automaton is accessible if there is a path between each
        initials states and all other states of 'Q'.

        No arcticle ...

        Returns
        -------
        bool
            True if the automaton is accessible, else False
        """
        for q in self.get_states():
            if not self.is_state_accessible(q):
                return False
        return True

    def is_co_accessible(self) -> bool:
        """Check if the automaton is co-accessible
        An automaton is co-accessible if there is a path between each
        states 'q' of 'Q' and a final state 'qf' of 'Qf'.

        No arcticle ...

        Returns
        -------
        bool
            True if the automaton is co-accessible, else False
        """
        for q in self.get_states():
            if not self.is_state_co_accessible(q):
                return False
        return True

    def set_complete(self) -> None:
        """Convert the current automaton into a complete automaton that
        guarantee the same language.

        Returns
        -------
        FiniteStateMachine
            The completed automaton
        """
        a = self.copy()
        if a.is_complete():
            return a
        # add a new state call 'trash state' : once you are in this state,
        # you can't go out. This will not change the accepted language
        trash = max(a.get_states()) + 1
        a.add_state(trash)

        # `trash` is looping over itself for all letters of the alphabet
        a.create_loop(trash)

        # for all states of 'Q', if a state have less relation than
        # expected, add a relation between this states and the trash
        # state
        for q in a.get_states():
            # getting all missing conditions
            neighbours = a.get_rel(q)
            if not neighbours:
                for letter in self.get_alphabet():
                    a.add_condition(q, trash, letter)
            else:
                cond = set()
                for neighbour in neighbours:
                    cond |= a.get_alphabet() - a.get_cond(q, neighbour)
                for c in cond:
                    a.add_condition(q, trash, c)
        return a

    def set_deterministic(self) -> None:
        """Convert the current automaton into a deterministic automaton that
        guarantee the same language.

        Returns
        -------
        FiniteStateMachine
            New deterministic finite state machine
        """
        if self.is_deterministic():
            return self.copy()

        # Create an empty FiniteStateMachine
        init = tuple(self.get_initials_states())
        a = FiniteStateMachine(self.alphabet, {init}, {init})

        done = set()
        trash_states = 0

        # Work with FIFO structures
        queue = deque([init])
        while len(queue):
            states = tuple(queue.popleft())
            done.add(states)
            
            # for a letter from each q that compose `states`,
            # get all the possible states
            for letter in a.get_alphabet():
                next_states = set()
                is_final = False
                for q in states:
                    # add all next states that you can reach from one letter
                    next_states |= self.possible_path(q, letter)
                
                # check if there are finals states in the new_states
                if len(next_states & self.get_finals_states()):
                    is_final = True
                new_state = tuple(next_states)
                if not len(new_state):
                    
                    # new_state is empty. You can reach no states with current
                    # letter : create a trash_states
                    a.add_state(trash_states)
                    a.create_loop(trash_states)
                    
                    # add a condition between states and the new trash_state
                    a.add_condition(states, trash_states, letter)
                    trash_states += 1
                else:
                    # add the new state and create relations for it
                    if new_state not in a.get_states():
                        a.add_state(new_state)
                    a.add_condition(states, new_state, letter)
                    if new_state not in done:
                        queue.append(new_state)
                    if is_final:
                        a.Qf.add(new_state)
        return a
    
    def set_accessible(self):
        """Convert the current automaton into an accessible automaton
        that guarantee the same language (because you can't go to some
        states, we can just delete them ...).

        Returns
        -------
        FiniteStateMachine
            The accessible automaton
        """
        a = self.copy()
        if self.is_accessible():
            return a
        for q in self.get_states():
            # if a state is not accessible, remove it
            if not a.is_state_accessible(q):
                a.remove_state(q)
        return a
    
    def set_co_accessible(self):
        """Convert the current automaton into an co-accessobme automaton
        that guarantee the same language (because when you are in this state,
        you can't go back to a final state).

        Returns
        -------
        FiniteStateMachine
            The co-accessible automaton
        """
        a = self.copy()
        if a.is_co_accessible():
            return a
        for q in self.get_states():
            # if a state is not co-accessible, remove it
            if not a.is_state_co_accessible(q):
                a.remove_state(q)
        return a

    def complementary(self):
        """Create an automaton that accept the complementary
        of the current accepted language.

        Returns
        -------
        FiniteStateMachine
        """
        # to create the automaton that accept the complementary of a language
        # the automaton must be deterministic and complete
        if not (self.is_deterministic() and self.is_complete()):
            # the algorithm to make an automaton deterministic also
            # make it complete
            a = self.set_deterministic()
        else:
            a = self.copy()
        # Once the automaton is deterministic and complete, the final states
        # becomes older non-final states
        a.Qf = a.Q - a.Qf
        return a
    
    def __neg__(self):
        """Create an automaton that accept the complementary
        of the current accepted language.

        Returns
        -------
        FiniteStateMachine
        """
        return self.complementary()
        

    def rework_states(self, d_states: None | dict[Any, Any] = None) -> 'FiniteStateMachine':
        """Rework the names of states and return a new FiniteStateMachine
        with new states name.

        Parameters
        ----------
        d_states : None | dict[Any, Any], optional
            contains the current states names and the new ones,
            by default None

        Returns
        -------
        FiniteStateMachine
            Reworked finite state machine
        """
        if d_states is None:
            # create a dictionnary with all the states and their new names
            d_states = {name: (new_name + 1) 
                        for new_name, name in enumerate(self.get_states())}
        
        # creates the new named collections `states`, `initial_states` and 
        # `final_states`
        new_states = {d_states[q] for q in self.get_states()}
        new_init_states = {d_states[q] for q in self.get_initials_states()}
        new_final_states = {d_states[q] for q in self.get_finals_states()}
        
        # re-create relations with the new names
        new_rel = {
            d_states[q]: {d_states[p] for p in self.get_rel(q)} 
            for q in self.get_relations()
        }
        
        # re-create conditions with the new names
        new_cond = {
            (d_states[q[0]], d_states[q[1]]): self.get_conditions()[q].copy()
            for q in self.get_conditions()
        }
        
        # Create a new FiniteStateMachine with all new names for states 
        a = FiniteStateMachine(self.alphabet.copy())
        a.Q = new_states
        a.Qi = new_init_states
        a.Qf = new_final_states
        a.relations = new_rel
        a.conditions = new_cond
        return a

    def to_dot(self, name: str) -> None:
        """Create a .dot file that draw the current finte state machine.
        User can turn the .dot to be a .png with this command :
        `dot -Tpng <name>.dot -o <name>.png`.

        Parameters
        ----------
        name : str
            Name of the .dot file
        """
        s = self.get_states()
        Qf = self.get_finals_states()
        Qi = self.get_initials_states()
        d_index_init = {}
        aliases = {q: f'q{i}' for i, q in enumerate(s)}
        others = s - Qf
        with open(name + ".dot", "w") as f:
            # header and propreties of the digraph
            f.write("digraph finite_state_machine {\n")
            f.write("\trankdir=LR;\n")
            f.write('\tsize="8,5"\n\n')
            
            # draw arrow for initials states
            for ind, qi in enumerate(Qi):
                f.write(f"\tnode [shape = point] qi_{ind};\n")
                d_index_init[qi] = ind
            
            # draw finals states
            for qf in Qf:
                f.write(f'\tnode [shape = doublecircle, label="{qf}"] {aliases[qf]};\n')
                if qf in Qi:
                    f.write(f"\tqi_{d_index_init[qf]} -> {aliases[qf]}\n")
            
            # draw states that are not final states
            for q in others:
                f.write(f'\tnode [shape = circle, label="{q}"] {aliases[q]};\n')
                if q in Qi:
                    f.write(f"\tqi_{d_index_init[q]} -> {aliases[q]}\n")
            
            # draw relations between states
            for a, b in self.get_conditions():
                r = ",".join(sorted(list(self.get_cond(a, b))))
                f.write(f'\t{aliases[a]} -> {aliases[b]} [label="{r}"];\n')
            
            # footer
            f.write("}")
    
    def create_different_states_names(self, fsm: 'FiniteStateMachine') -> 'FiniteStateMachine':
        """Create differents names for the states of `fsm` if `self` and `fsm`
        have common names states.

        Parameters
        ----------
        fsm : FiniteStateMachine
            The automaton to change the states names

        Returns
        -------
        FiniteStateMachine
            An automaton where self.Q & fsm.Q = empty_set

        Raises
        ------
        TypeError
            fsm must be a FiniteStateMachine
        """
        if not isinstance(fsm, FiniteStateMachine):
            raise TypeError
        # if `self` and `fsm` have common name states
        if self.get_states() & fsm.get_states():
            rename = {}
            new_name = 1
            # create alternatives names
            for q in fsm.get_states():
                while new_name in self.get_states():
                    new_name += 1
                rename[q] = new_name
                new_name += 1
            return fsm.rework_states(rename)
        return fsm
    
    def union(self, fsm: 'FiniteStateMachine') -> 'FiniteStateMachine':
        """Create a FiniteStateMachine that admit the union of two 
        langaguges represented by two FiniteStateMachines : `self` and `fsm`.

        Parameters
        ----------
        fsm : FiniteStateMachine
            The state machine that represent the other language

        Returns
        -------
        FiniteStateMachine
            A new automaton that admit the union of two languages

        Raises
        ------
        NotImplementedError
            if `fsm` is not a FiniteStateMachine
        """
        if not isinstance(fsm, FiniteStateMachine):
            raise NotImplementedError
        # Check if they have common states name. If so, rename them
        fsm = self.create_different_states_names(fsm)
        a = self.copy()
        # To create the union of two automatons, just create a third one 
        # that includes them
        a.Q |= fsm.get_states()
        a.Qi |= fsm.get_initials_states()
        a.Qf |= fsm.get_finals_states()
        a.conditions = {**a.get_conditions(), **fsm.get_conditions()}
        a.relations = {**a.get_relations(), **fsm.get_relations()}
        return a

    def __or__(self, fsm: 'FiniteStateMachine') -> 'FiniteStateMachine':
        """Create a FiniteStateMachine that admit the union of two 
        langaguges represented by two FiniteStateMachines : `self` and `fsm`.

        Parameters
        ----------
        fsm : FiniteStateMachine
            The state machine that represent the other language

        Returns
        -------
        FiniteStateMachine
            A new automaton that admit the union of two languages

        Raises
        ------
        NotImplementedError
            if `fsm` is not a FiniteStateMachine
        """
        return self.union(fsm)
    
    def product(self, fsm: 'FiniteStateMachine') -> 'FiniteStateMachine':
        """Create the product of two FiniteStateMachine.

        Parameters
        ----------
        fsm : FiniteStateMachine
            The FiniteStateMachine to create the product with

        Returns
        -------
        FiniteStateMachine
            A new FiniteStateMachine that does not have final states. The 
            choosing of the final states depends on what the user wants to
            do with the product

        Raises
        ------
        NotImplementedError
            `fsm` isn't a FiniteStateMachine
        ValueError
            The alphabet of two FiniteStateMachine must have the same languages
        """
        if not isinstance(fsm, FiniteStateMachine):
            raise NotImplementedError
        if self.get_alphabet() != fsm.get_alphabet():
            return ValueError("Alphabets must be similar")
        fsm = self.create_different_states_names(fsm)
        new_states = set(product(self.get_states(), fsm.get_states()))
        
        a = FiniteStateMachine(self.get_alphabet())
        a.Q = new_states
        
        # for each new states, create relations between them
        for q, p in new_states:
            for letter in self.get_alphabet():
                # for each letter, check the relations from q to another state in `self`               
                next_states_q = {state for state in self.get_rel(q) if letter in self.get_cond(q, state)}
                
                # for each letter, check the relations from p to another state in `fsm`
                next_states_p = {state for state in fsm.get_rel(p) if letter in fsm.get_cond(p, state)}
                
                # the next states from (q, p) is the product of the two sets above
                # add the relations
                for next_state in set(product(next_states_q, next_states_p)):
                    a.add_condition((q, p), next_state, letter)
                        
        a.Qi = set(product(self.get_initials_states(), fsm.get_initials_states()))
        return a
        
    def intersection(self, fsm: 'FiniteStateMachine') -> 'FiniteStateMachine':
        """Create a FubuteStateMachine that admit the intersection of two 
        languages represented by two FiniteStateMachines : `self` and `fsm`.

        Parameters
        ----------
        fsm : FiniteStateMachine
            The state machine that represent the other language

        Returns
        -------
        FiniteStateMachine
            A new automaton that admit the intersection of two languages
        """
        a = self.product(fsm)
        a.Qf = set(product(self.get_finals_states(), fsm.get_finals_states()))
        return a
    
    def __and__(self, fsm: 'FiniteStateMachine') -> 'FiniteStateMachine':
        """Create a FubuteStateMachine that admit the intersection of two 
        languages represented by two FiniteStateMachines : `self` and `fsm`.

        Parameters
        ----------
        fsm : FiniteStateMachine
            The state machine that represent the other language

        Returns
        -------
        FiniteStateMachine
            A new automaton that admit the intersection of two languages
        """
        return self.intersection(fsm)
