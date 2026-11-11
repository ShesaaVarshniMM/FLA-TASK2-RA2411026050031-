# Finite Automata Validator Lab – CLA-2 Task 2

## Project Overview

The **Finite Automata Validator Lab** is an interactive web application developed using Python and Streamlit for the course 21CSC301T – Formal Language and Automata.

The application demonstrates the working of three Deterministic Finite Automata (DFA) through real-time input validation, state transition diagrams, and character-by-character execution traces.

## Objectives

- Understand the practical implementation of Deterministic Finite Automata.
- Demonstrate how DFA states change based on input symbols.
- Validate different input patterns using automata logic.
- Visualize state transitions and accepting/rejecting states.
- Understand how invalid inputs are handled using a DEAD state.

## Applications Implemented

### 1. Password Format Validator

**Automaton:** Deterministic Finite Automaton (DFA)

Validates whether a password satisfies the following conditions:

- Minimum 8 characters.
- At least one uppercase letter.
- At least one lowercase letter.
- At least one numeric digit.
- At least one special character.
- Spaces are not allowed.

**Example:**
- `Hello@123` – Accepted
- `password` – Rejected
- `ABC123!!` – Rejected

### 2. Email Format Validator

**Automaton:** Deterministic Finite Automaton (DFA)

Checks a simplified email address structure consisting of:

- Local part.
- @ symbol.
- Domain name.
- Dot separator.
- Extension containing at least two letters.

**Example:**
- `student@example.com` – Accepted
- `@example.com` – Rejected
- `studentexample.com` – Rejected

### 3. ATM PIN Verification

**Automaton:** Deterministic Finite Automaton (DFA)

Checks whether an entered PIN contains exactly four numeric digits.

**Example:**
- `1234` – Accepted
- `0000` – Accepted
- `12345` – Rejected
- `12a4` – Rejected

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | DFA implementation and validation logic |
| Streamlit | Interactive web application |
| Graphviz | DFA state transition diagrams |
| Pandas | Execution trace representation |
| HTML & CSS | User interface styling |

## Features

- Three interactive DFA validators.
- Live input validation.
- Accept and reject status display.
- State transition diagrams.
- Character-by-character execution trace.
- Predefined valid and invalid test cases.
- DEAD state handling for invalid transitions.
- Professional and responsive interface.

## Project Structure

```text
FLA/
│
├── TASK2.py
├── README.md
└── requirements.txt
```

## Installation and Execution

### Step 1: Clone the Repository

```bash
git clone <your-repository-link>
```

### Step 2: Navigate to the Project Folder

```bash
cd Task2
```

### Step 3: Install Dependencies

```bash
pip install streamlit pandas graphviz
```

Graphviz must also be installed on your system and available in PATH for diagram rendering.

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## Working Principle

1. The user selects one of the three validation applications.
2. The user enters a string or selects a predefined example.
3. The DFA processes the input character by character.
4. Based on the current state and input symbol, the automaton moves to the next state.
5. The final state determines whether the input is accepted or rejected.
6. The application displays the transition diagram and execution trace.

## Limitations

- Password validation checks format only, not actual password strength.
- Email validation follows a simplified email pattern rather than the complete email standard.
- ATM PIN verification checks only the four-digit format and does not perform actual banking authentication.

## Conclusion

The Finite Automata Validator Lab demonstrates how Deterministic Finite Automata can be applied to real-world input validation problems. Through interactive testing, transition diagrams, and execution traces, the application provides a practical understanding of DFA concepts.

**Course:** 21CSC301T – Formal Language and Automata  
**Assignment:** CLA-2 – Task 2\
**Done by:** SHESAA VARSHNI MM(RA2411026050031)
