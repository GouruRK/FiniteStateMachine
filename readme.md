# Finite State Machine
Automata Theory
___

This is a small library to easily create and manipulate Finite State Machine / Automata. 

- [Finite State Machine](#finite-state-machine)
  - [Requirements](#requirements)
  - [Features](#features)


## Requirements

Python 3.9 or higher is required. \
A new version without typing informations may be pushed later to run on lower versions.

## Features

- [x] Draw a finite state machine into a .dot file. (Note that a dot file can be converted to a .png file using `dot -Tpng <filename>.dot -o <outputname>.png`)
- [x] Check if a word can be admited by the automata
- [x] Check if an automata is deterministic, complete, accessible or co-accessible
- [x] Convert an automata to a deterministic or complete or accessible or co-accessible equivalent
- [ ] Create an automata that accept the complementary, union or intersection of the current accepted language
- [ ] Support regular expressions