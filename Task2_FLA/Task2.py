import string
import pandas as pd
import streamlit as st
from graphviz import Digraph

# ============================================================
# FINITE AUTOMATA VALIDATOR LAB — CLA-2 TASK 2
# Password, Email and ATM PIN validators using DFA logic
# ============================================================

st.set_page_config(
    page_title="DFA Lab | CLA-2 Task 2",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------- DFA LOGIC ---------------------------

UPPER = set(string.ascii_uppercase)
LOWER = set(string.ascii_lowercase)
DIGITS = set(string.digits)
SPECIAL = set(string.punctuation)


def password_class(ch):
    if ch in UPPER:
        return "Uppercase"
    if ch in LOWER:
        return "Lowercase"
    if ch in DIGITS:
        return "Digit"
    if ch in SPECIAL:
        return "Special"
    return "Invalid / whitespace"


def password_dfa(value):
    # State: (length capped at 8, uppercase, lowercase, digit, special)
    state = (0, False, False, False, False)
    trace = []

    for position, ch in enumerate(value, start=1):
        before = state
        cls = password_class(ch)

        if cls == "Invalid / whitespace":
            after = "DEAD"
            trace.append({
                "Position": position,
                "Read": repr(ch),
                "Character class": cls,
                "State before": str(before),
                "Transition": "Move to DEAD state",
                "State after": after,
            })
            return False, trace, after, "Spaces and unsupported characters are not allowed."

        length, has_upper, has_lower, has_digit, has_special = state
        after = (
            min(length + 1, 8),
            has_upper or cls == "Uppercase",
            has_lower or cls == "Lowercase",
            has_digit or cls == "Digit",
            has_special or cls == "Special",
        )
        trace.append({
            "Position": position,
            "Read": repr(ch),
            "Character class": cls,
            "State before": str(before),
            "Transition": f"Update length and {cls.lower()} flag",
            "State after": str(after),
        })
        state = after

    accepted = state[0] == 8 and all(state[1:])
    reason = (
        "All password conditions are satisfied."
        if accepted else
        "Use at least 8 characters with one uppercase, one lowercase, one digit and one special character."
    )
    return accepted, trace, state, reason


def email_class(ch):
    if ch.isascii() and ch.isalnum():
        return "Letter / digit"
    return {
        "_": "Underscore",
        "-": "Hyphen",
        ".": "Dot",
        "@": "At sign",
    }.get(ch, "Other")


def email_dfa(value):
    # Simplified pattern:
    # local-part @ domain . extension (at least 2 ASCII letters)
    state = "q0"
    trace = []

    for position, ch in enumerate(value, start=1):
        before = state
        is_alnum = ch.isascii() and ch.isalnum()
        is_letter = ch.isascii() and ch.isalpha()

        if state == "q0":
            after = "q1" if is_alnum or ch == "_" else "DEAD"
        elif state == "q1":
            if is_alnum or ch == "_":
                after = "q1"
            elif ch == "@":
                after = "q2"
            else:
                after = "DEAD"
        elif state == "q2":
            after = "q3" if is_alnum or ch == "-" else "DEAD"
        elif state == "q3":
            if is_alnum or ch == "-":
                after = "q3"
            elif ch == ".":
                after = "q4"
            else:
                after = "DEAD"
        elif state == "q4":
            after = "q5" if is_letter else "DEAD"
        elif state == "q5":
            after = "q6" if is_letter else "DEAD"
        elif state == "q6":
            after = "q6" if is_letter else "DEAD"
        else:
            after = "DEAD"

        trace.append({
            "Position": position,
            "Read": repr(ch),
            "Character class": email_class(ch),
            "State before": before,
            "Transition": f"{before} → {after}",
            "State after": after,
        })
        state = after

    accepted = state == "q6"
    reason = (
        "The input matches the simplified email pattern."
        if accepted else
        "Expected local-part@domain.extension, with an extension of at least 2 letters."
    )
    return accepted, trace, state, reason


def atm_dfa(value):
    # q0 = no digits; q4 = exactly four digits; DEAD = invalid input
    state = "q0"
    trace = []

    for position, ch in enumerate(value, start=1):
        before = state
        if state == "DEAD":
            after = "DEAD"
        elif ch in string.digits and state in ("q0", "q1", "q2", "q3"):
            after = f"q{int(state[1]) + 1}"
        else:
            after = "DEAD"

        cls = "Digit" if ch in string.digits else "Non-digit"
        trace.append({
            "Position": position,
            "Read": repr(ch),
            "Character class": cls,
            "State before": before,
            "Transition": f"{before} → {after}",
            "State after": after,
        })
        state = after

    accepted = state == "q4"
    reason = (
        "Exactly four digits were entered."
        if accepted else
        "PIN must contain exactly four digits. Letters and extra digits are rejected."
    )
    return accepted, trace, state, reason


# --------------------------- DFA DIAGRAMS ---------------------------

def base_graph(name):
    dot = Digraph(name, engine="dot")
    dot.attr(
        rankdir="LR",
        bgcolor="transparent",
        pad="0.35",
        nodesep="0.55",
        ranksep="0.75",
        splines="spline",
        label="",
    )
    dot.attr(
        "node",
        shape="circle",
        style="filled",
        fillcolor="#EAF1FF",
        color="#31527D",
        fontcolor="#172B4D",
        fontname="Arial",
        fontsize="11",
        penwidth="1.7",
        width="0.9",
        height="0.9",
        margin="0.10",
    )
    dot.attr(
        "edge",
        color="#526987",
        fontcolor="#263B59",
        fontname="Arial",
        fontsize="10",
        penwidth="1.35",
        arrowsize="0.8",
    )
    dot.node("start", "", shape="point", width="0.13", color="#172B4D")
    return dot


def password_graph():
    dot = base_graph("Password_DFA")
    # Readable abstraction of the product DFA. Each layer groups
    # states with the same length counter and different flag combinations.
    for i in range(9):
        label = f"L{i}\\nlength {i}" if i < 8 else "L8+\\nlength ≥ 8"
        dot.node(
            f"L{i}", label, shape="box", style="rounded,filled",
            fillcolor="#EAF1FF", width="1.0", height="0.65"
        )
    dot.node(
        "ACCEPT", "ACCEPT\\nU=L=D=S=1",
        shape="doublecircle", fillcolor="#D8F5E2",
        color="#198754", fontcolor="#14532D", penwidth="2.2"
    )
    dot.node(
        "DEAD", "DEAD\\nReject",
        fillcolor="#FDE2E2", color="#C0392B", fontcolor="#8F1D1D"
    )
    dot.edge("start", "L0", label="start")
    for i in range(8):
        dot.edge(f"L{i}", f"L{i+1}", label="valid character")
    dot.edge("L8", "L8", label="more valid characters")
    dot.edge("L8", "ACCEPT", label="all flags = 1")
    dot.edge("L0", "DEAD", label="space", color="#C0392B", fontcolor="#C0392B")
    dot.edge("DEAD", "DEAD", label="any input", color="#C0392B")
    dot.attr(
        label="Password DFA — grouped product states (the exact tuple is shown in the execution trace)",
        labelloc="t", fontsize="11", fontname="Arial", fontcolor="#40536F"
    )
    return dot


def email_graph():
    dot = base_graph("Email_DFA")
    states = [
        ("q0", "q0\\nStart", False),
        ("q1", "q1\\nLocal part", False),
        ("q2", "q2\\nAfter @", False),
        ("q3", "q3\\nDomain", False),
        ("q4", "q4\\nAfter dot", False),
        ("q5", "q5\\n1 extension letter", False),
        ("q6", "q6\\nACCEPT", True),
    ]
    for name, label, final in states:
        if final:
            dot.node(name, label, shape="doublecircle", fillcolor="#D8F5E2",
                     color="#198754", fontcolor="#14532D", penwidth="2.2")
        else:
            dot.node(name, label)
    dot.node("DEAD", "DEAD\\nReject", fillcolor="#FDE2E2",
             color="#C0392B", fontcolor="#8F1D1D")
    dot.edge("start", "q0")
    transitions = [
        ("q0", "q1", "letter / digit / _"),
        ("q1", "q1", "letter / digit / _"),
        ("q1", "q2", "@"),
        ("q2", "q3", "letter / digit / -"),
        ("q3", "q3", "letter / digit / -"),
        ("q3", "q4", "."),
        ("q4", "q5", "letter"),
        ("q5", "q6", "letter"),
        ("q6", "q6", "letter"),
    ]
    for a, b, label in transitions:
        dot.edge(a, b, label=label)
    dot.edge("DEAD", "DEAD", label="any input", color="#C0392B")
    # Invalid symbols are represented by the dead-state rule in the specification.
    dot.attr(label="Simplified email-format DFA", labelloc="t",
             fontsize="11", fontname="Arial", fontcolor="#40536F")
    return dot


def atm_graph():
    dot = base_graph("ATM_PIN_DFA")
    for i in range(5):
        label = f"q{i}\\n{'ACCEPT' if i == 4 else str(i) + ' digit(s)'}"
        if i == 4:
            dot.node(f"q{i}", label, shape="doublecircle",
                     fillcolor="#D8F5E2", color="#198754",
                     fontcolor="#14532D", penwidth="2.2")
        else:
            dot.node(f"q{i}", label)
    dot.node("DEAD", "DEAD\\nReject", fillcolor="#FDE2E2",
             color="#C0392B", fontcolor="#8F1D1D")
    dot.edge("start", "q0")
    for i in range(4):
        dot.edge(f"q{i}", f"q{i+1}", label="digit 0–9")
    dot.edge("q4", "DEAD", label="extra character", color="#C0392B")
    dot.edge("DEAD", "DEAD", label="any input", color="#C0392B")
    for i in range(4):
        dot.edge(f"q{i}", "DEAD", label="non-digit",
                 style="dashed", color="#C0392B", fontcolor="#C0392B")
    dot.attr(label="ATM PIN DFA — exactly four digits", labelloc="t",
             fontsize="11", fontname="Arial", fontcolor="#40536F")
    return dot


# --------------------------- APPLICATION DATA ---------------------------

APPS = {
    "Password Validator": {
        "description": "Checks a password against a defined character and length policy.",
        "alphabet": "A–Z, a–z, 0–9 and punctuation symbols",
        "rule": "Minimum 8 characters; at least one uppercase, one lowercase, one digit and one special character. Spaces are not allowed.",
        "examples": ["Hello@123", "Abcdef1!", "password", "ABC123!!", "Pass word1!"],
        "default": "Hello@123",
        "formal": "State = (n, U, L, D, S), where n is length capped at 8 and each flag records whether a required character class has appeared.",
        "limitation": "This validates password format only. It does not measure password strength, check breached-password lists or authenticate a user.",
        "diagram": password_graph,
        "validator": password_dfa,
    },
    "Email Validator": {
        "description": "Checks a simplified email-address structure using DFA states.",
        "alphabet": "ASCII letters, digits, underscore, @, hyphen and dot",
        "rule": "Local part (letters/digits/underscore) + @ + domain (letters/digits/hyphen) + dot + extension of at least 2 letters.",
        "examples": ["student@example.com", "a_b12@my-domain.in", "name@domain", "@example.com", "studentexample.com"],
        "default": "student@example.com",
        "formal": "States q0–q6 track the local part, @ symbol, domain, dot and extension. q6 is the accepting state.",
        "limitation": "This is not the complete email standard. It does not check whether a mailbox exists or can receive mail.",
        "diagram": email_graph,
        "validator": email_dfa,
    },
    "ATM PIN Verification": {
        "description": "Checks whether the entered PIN contains exactly four numeric digits.",
        "alphabet": "Σ = {0,1,2,3,4,5,6,7,8,9}",
        "rule": "Exactly four digits. Any non-digit or fifth character moves the DFA to a dead state.",
        "examples": ["1234", "0000", "12", "12345", "12a4"],
        "default": "1234",
        "formal": "q0 is the start state; q1, q2 and q3 represent 1, 2 and 3 digits read; q4 is the only accepting state.",
        "limitation": "This checks PIN format only. Real ATM authentication also needs secure comparison, retry limits, encryption and backend verification.",
        "diagram": atm_graph,
        "validator": atm_dfa,
    },
}


# --------------------------- STYLING ---------------------------

st.markdown("""
<style>
:root { color-scheme: light; }
.stApp, [data-testid="stAppViewContainer"] {
    background: #F3F6FB;
    color: #172B4D;
}
[data-testid="stHeader"] { background: rgba(243,246,251,.9); }
.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, p, label { color: #172B4D; }
.hero {
    background: linear-gradient(115deg, #18365D 0%, #28558B 100%);
    color: white;
    padding: 28px 32px;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0 10px 26px rgba(24,54,93,.15);
}
.hero .eyebrow {
    color: #C7D9EF;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 8px;
}
.hero h1 {
    color: white !important;
    font-size: 30px;
    line-height: 1.2;
    margin: 0 0 7px 0;
    font-weight: 800;
}
.hero p { color: #E0EAF7 !important; margin: 0; font-size: 14px; }
.section-kicker {
    color: #6C83A3;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 7px;
}
.section-heading {
    color: #1B3558;
    font-size: 21px;
    font-weight: 800;
    margin: 0 0 4px 0;
}
.muted { color: #71819A; font-size: 13px; }
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: white;
    border: 1px solid #CAD5E3;
    border-radius: 10px;
}
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    color: #40536F;
    font-weight: 700;
}
.stButton > button {
    background: #F5F8FC;
    color: #24466F;
    border: 1px solid #D7E1ED;
    border-radius: 10px;
    font-weight: 650;
    min-height: 42px;
}
.stButton > button:hover {
    background: #E8F0FA;
    border-color: #8EACD0;
    color: #17385F;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #E0E7F0;
    border-radius: 10px;
    overflow: hidden;
}
div[data-testid="stAlert"] { border-radius: 11px; }
hr { border-color: #E5EAF1; }
.footer {
    color: #8190A5;
    text-align: center;
    font-size: 12px;
    padding-top: 18px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------- PAGE HEADER ---------------------------

st.markdown("""
<div class="hero">
  <div class="eyebrow">Formal Language & Automata · CLA-2 · Task 2</div>
  <h1>Finite Automata Validator Lab</h1>
  <p>Explore three deterministic finite automata through live input validation,
  state-transition diagrams and character-by-character execution traces.</p>
</div>
""", unsafe_allow_html=True)

# App selection
if "selected_app" not in st.session_state:
    st.session_state.selected_app = "Password Validator"
if "input_value" not in st.session_state:
    st.session_state.input_value = APPS[st.session_state.selected_app]["default"]

app_name = st.selectbox(
    "SELECT VALIDATION APPLICATION",
    list(APPS.keys()),
    key="selected_app",
)

# Reset input to a relevant example when the selected application changes.
if st.session_state.get("last_app") != app_name:
    st.session_state.input_value = APPS[app_name]["default"]
    st.session_state.last_app = app_name

config = APPS[app_name]

# --------------------------- MAIN WORKSPACE ---------------------------

left, right = st.columns([0.88, 1.65], gap="large")

with left:
    with st.container(border=True):
        st.markdown('<div class="section-kicker">01 · Live validator</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Test your input</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="muted">{config["description"]}</div>', unsafe_allow_html=True)

        value = st.text_input(
            "INPUT STRING",
            key="input_value",
            placeholder="Type a value to validate",
        )
        accepted, trace, final_state, reason = config["validator"](value)

        if accepted:
            st.success(f"ACCEPTED  ·  Final state: {final_state}")
        else:
            st.error(f"REJECTED  ·  Final state: {final_state}")
        st.caption(reason)

        st.divider()
        st.markdown("**Try a test case**")
        for row_start in range(0, len(config["examples"]), 2):
            example_cols = st.columns(2)
            for offset, example in enumerate(config["examples"][row_start:row_start + 2]):
                with example_cols[offset]:
                    st.button(
                        example,
                        key=f"example_{app_name}_{row_start}_{offset}",
                        use_container_width=True,
                        on_click=lambda x=example: st.session_state.update(input_value=x),
                    )



with right:
    with st.container(border=True):
        st.markdown('<div class="section-kicker">02 · Automaton visualization</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">DFA state transition diagram</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="muted">The start arrow, transition labels, accepting state '
            'and dead state are shown where applicable.</div>',
            unsafe_allow_html=True,
        )
        st.graphviz_chart(config["diagram"](), use_container_width=True)

        st.divider()
        st.markdown("**Input execution trace**")
        if trace:
            st.dataframe(
                pd.DataFrame(trace),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No symbols have been processed. Enter an input string to see the transition trace.")


st.markdown(
    '<div class="footer">21CSC301T · Formal Language and Automata · '
    'CLA-2 Task 2 · Educational DFA demonstration</div>',
    unsafe_allow_html=True,
)

