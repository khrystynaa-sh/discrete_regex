# FSM Regex Engine (Laboratory Work)

## Description:

This project implements a simple **finite state machine (FSM)** that evaluates simplified regular expressions.

Supported operators:
- `.` → matches any single character
- `*` → zero or more repetitions
- `+` → one or more repetitions
- literal characters (a, b, c, 1, etc.)

The implementation uses:
- Object-Oriented Design
- Abstract State classes
- Depth-First Search (DFS) with backtracking
- ε-transitions (epsilon transitions)
- Cycle detection to avoid infinite loops

---

## Implementation Idea:

The regex is converted into a **non-deterministic finite automaton (NFA-like structure)**:

- Each character becomes a `State`
- `StartState` is the entry point
- `TerminationState` marks successful match
- Transitions between states represent regex flow

### Key design decisions:

### 1. State-based architecture
Each regex token is represented as a class:
- `AsciiState` → literal character
- `DotState` → wildcard
- `StarState` → repetition (0+)
- `PlusState` → repetition (1+)

This makes the system extensible and modular.

---

### 2. DFS matching
Matching is performed using recursion:

- Each state can branch into multiple next states
- Backtracking explores all valid paths
- `visited (state, index)` prevents infinite loops

---

### 3. Handling `*` and `+`
Instead of converting to postfix regex or using a library:
- `*` allows skipping or looping
- `+` requires at least one match before looping

---

### 4. Why FSM instead of regex library?
This implementation is educational:
- demonstrates automata theory
- shows how regex engines work internally
- avoids built-in regex engines intentionally

---

## How to Run:

### 1. Clone repository
```bash
git clone <your-repo-link>
cd <repo-folder>
python regex.py "<pattern>" "<string>"
