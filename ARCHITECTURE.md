# Huemn.AI — System Architecture

This document defines the **structural, behavioral, and execution architecture** of Huemn.AI.

The goal of this architecture is not task completion at all costs, but **provable behavioral improvement** through explicit feedback loops, rule enforcement, and memory-backed adaptation.

---

## Architectural Philosophy

Huemn.AI is designed as a **deterministic, inspectable system**.

Key ideas:

* Every execution has a beginning and an end
* Every failure leaves evidence
* Learning happens through constraints, not parameter updates
* Nothing important is implicit

This architecture deliberately avoids:

* Hidden agent state
* Recursive prompting patterns
* Self-modifying prompts
* Autonomous loops without supervision

---

## High-Level Data Flow

```
Task
 ↓
Planner
 ↓
Execution Engine ──→ Tools
 ↓                   ↓
Final Output      Tool Results
 ↓
Post-Run Evaluator
 ↓
Error Memory
 ↓
Behavioral Adaptation
```

The agent does **not** learn during execution.
Learning only occurs **after** evaluation.

---

## Core Modules

### 1. Agent Orchestrator (`agent/agent.py`)

**Responsibility:**

* Owns a single agent run
* Enforces execution order
* Prevents premature termination

**Key Guarantees:**

* Evaluation always runs
* Memory is always updated
* Adaptation always executes (even if no change is needed)

The orchestrator is intentionally thin. Business logic lives elsewhere.

---

### 2. Planner (`agent/planner.py`)

**Responsibility:**

* Interprets the task
* Decides whether tools are required
* Declares intended tool usage

**Important Constraint:**
The planner may be wrong.

Incorrect plans are treated as learning signals, not system bugs.

---

### 3. Execution Engine (`agent/execution.py`)

**Responsibility:**

* Executes declared tool calls
* Validates tool inputs and outputs
* Captures execution metadata

**Rules:**

* No silent failures
* Tool errors are surfaced explicitly
* Skipped tools are logged, not ignored

---

### 4. Tool Layer (`tools/`)

**Responsibility:**

* Provide deterministic, contract-driven capabilities

Each tool:

* Declares purpose
* Validates inputs
* Returns structured outputs

Tools are intentionally simple.
Complexity belongs in evaluation, not tooling.

---

### 5. Post-Run Evaluator (`agent/evaluator.py`)

**Responsibility:**

* Judge the execution against ground-truth rules
* Detect violations
* Categorize mistakes

Evaluation answers:

* What failed?
* Where did it fail?
* Why is it considered a mistake?

Evaluation output is structured and human-readable.

---

### 6. Mistake Taxonomy (`evaluation/taxonomy.py`)

Defines the **only valid mistake categories** in the system.

Examples:

* REQUIRED_TOOL_NOT_USED
* INCORRECT_TOOL_ORDER
* PREMATURE_FINAL_OUTPUT
* TOOL_OUTPUT_IGNORED

This taxonomy is closed and versioned.
New categories require justification.

---

### 7. Error Memory (`memory/error_memory.py`)

**Responsibility:**

* Persist execution failures across runs

Stored attributes:

* Task type
* Mistake category
* Execution step
* Occurrence count

Memory is lightweight, explicit, and inspectable.

---

### 8. Pattern Detection (`memory/patterns.py`)

**Responsibility:**

* Identify recurring mistakes
* Detect tool-specific misuse

Pattern detection is intentionally heuristic.
Interpretability is favored over sophistication.

---

### 9. Behavioral Adaptation (`agent/adaptation.py`)

**Responsibility:**

* Modify future behavior based on error patterns

Adaptations include:

* Mandatory tool enforcement
* Pre-execution reminders
* Additional validation checkpoints
* Blocking premature outputs

No adaptation modifies model weights or prompts.

---

## Invariants (Must Always Hold)

* Evaluation runs after every execution
* Mistakes are categorized, never ignored
* Memory updates are append-only
* Adaptation decisions are logged
* Final output cannot bypass evaluation

Violation of invariants is considered a system failure.

---

## Observability & Logs

Each run produces:

* A unique run ID
* Execution trace
* Evaluation report
* Memory update summary
* Adaptation decision

Logs are treated as primary artifacts, not debug noise.

---

## Why This Architecture Works

This design ensures:

* Failures are visible
* Improvement is provable
* Behavior changes are explainable
* The agent remains debuggable

Correctness emerges through discipline, not optimism.

---

## Known Architectural Limitations

* Learning is task-specific
* Pattern detection is heuristic
* Memory does not generalize across domains

These limitations are accepted by design.

---

## Architectural Stability

This architecture is considered **stable** once implemented.
Future work should add capabilities without weakening invariants.
