# Self‑Improving Tool‑Aware AI Agent

**Interview Assignment Submission – AI Engineer Role (VE.AI)**

This repository contains a **self‑improving, tool‑aware AI agent** implemented as part of an interview assignment for the **AI Engineer** role at **VE.AI**.

The goal of the assignment was *not* to achieve perfect answers on the first attempt, but to design an agent that **detects its own mistakes, records them, and improves its behavior over time through explicit feedback loops**.

This repository demonstrates that requirement end‑to‑end using a clean, inspectable, and plagiarism‑safe system design.

---

## Assignment Objective

As specified in the assignment brief, the system must:

* Perform a task that may require tool usage
* Allow mistakes in early runs (e.g. skipping required tools)
* Explicitly evaluate each run
* Identify what went wrong and why
* Maintain a record of recurring mistakes
* Adjust future behavior based on those mistakes
* Demonstrate observable improvement over time

This implementation fulfills these requirements using **rule‑based evaluation and behavioral adaptation**, without retraining or prompt modification.

---

## High‑Level Architecture

The agent follows a strict and repeatable execution pipeline:

**Task → Planner → Tool Execution → Output → Evaluation → Memory → Adaptation**

Each component has a single responsibility:

* **Planner** – Decides whether a tool should be used
* **Execution Engine** – Executes tools and records facts
* **Evaluator** – Judges behavior against explicit rules
* **Error Memory** – Stores recurring mistakes across runs
* **Adapter** – Decides when behavioral constraints must be enforced

Learning occurs *only after evaluation*, ensuring transparency and debuggability.

---

## Tools Used

The agent operates with a minimal toolset:

* **Search Tool** – Simulates information retrieval

Tool usage is intentionally simple so that mistakes (such as skipping a required tool) are easy to detect and reason about.

---

## Evaluation Strategy

After every run, the system evaluates:

* Whether a required tool was skipped
* Whether execution failed
* Whether tool output was ignored
* Whether a final answer was produced prematurely

Mistakes are categorized using a fixed taxonomy and logged explicitly. No failures are hidden or silently corrected.

---

## Results (Demonstration of Learning)

The table below summarizes the observed behavior when running the same task repeatedly:

**Task:** `"tell me about ai"`

| Run | Output Behavior                 | Mistakes Detected      | Adaptation State             |
| --- | ------------------------------- | ---------------------- | ---------------------------- |
| 1   | Answered directly without tools | REQUIRED_TOOL_NOT_USED | No adaptation                |
| 2   | Same mistake repeated           | REQUIRED_TOOL_NOT_USED | `force_tool_usage` triggered |
| 3   | Tool used automatically         | None                   | Adaptation enforced          |
| 4   | Correct tool usage              | None                   | Stable behavior              |
| 5   | Correct tool usage              | None                   | Stable behavior              |

### Corresponding Execution Logs

```bash
python -m scripts.simulate_runs
```

```
RUN 1
OUTPUT: tell me about ai
MISTAKES: ['REQUIRED_TOOL_NOT_USED']
MEMORY: [{'task': 'tell me about ai', 'mistake': 'REQUIRED_TOOL_NOT_USED', 'count': 1}]
ADAPTATION RULES: []

RUN 2
OUTPUT: tell me about ai
MISTAKES: ['REQUIRED_TOOL_NOT_USED']
MEMORY: [{'task': 'tell me about ai', 'mistake': 'REQUIRED_TOOL_NOT_USED', 'count': 2}]
ADAPTATION RULES: ['force_tool_usage']

RUN 3
OUTPUT: [{'query': 'tell me about ai', 'results': ['Artificial intelligence is about making machines do smart things']}]
MISTAKES: []
MEMORY: [{'task': 'tell me about ai', 'mistake': 'REQUIRED_TOOL_NOT_USED', 'count': 2}]
ADAPTATION RULES: ['force_tool_usage']
```

**Key Observation:**

* The agent initially fails by skipping a required tool
* The failure is explicitly detected and stored in memory
* After repeated occurrences, a behavioral rule is introduced
* Once enforced, the same mistake no longer appears in subsequent runs

This log‑backed evidence demonstrates **measurable improvement over time**, exactly as required by the assignment.

---

## Limitations

* Learning is task‑specific and rule‑based
* Pattern detection is heuristic, not statistical
* The agent does not generalize across unrelated tasks

These limitations are acknowledged and align with the scope of the assignment.

---

## Conclusion

This project successfully meets the assignment requirements by demonstrating:

* Clear system design
* Explicit evaluation and feedback loops
* Honest handling of mistakes
* Observable behavioral improvement

The implementation emphasizes **engineering discipline and interpretability** over model complexity, aligning closely with real‑world AI agent challenges.

---

**Language:** Python
**Frameworks:** None (custom architecture)
**Submission Type:** Interview Assignment (VE.AI)
