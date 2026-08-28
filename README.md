# 🚀 Harness-Control: A Control-Theoretic Framework for Agent Tool Development and Validation

## 📘 Project Overview

Harness-Control is an experimental repository focused on the development, validation, measurement, and detection of Agent tools for software engineering and systems engineering scenarios. The project explores how to build controllable, adjustable, and composable Agent toolchains that can be used to test tool behavior, verify task execution, and evaluate performance in realistic workflows.

This repository includes:

- Agent tool development and integration
- Tool validation and behavior verification
- Measurement and detection capabilities for Agent workflows
- Control-based structured prompt templates
- Multi-task, multi-model performance comparison experiments
- Reproducible evaluation scripts and dataset interfaces

## 🎯 Motivation

Traditional evaluation frameworks often focus only on input → output behavior and metric reporting. However, real-world Agent tool performance depends on many factors, including:

- The structure of prompts and instructions
- The design of control variables such as context, constraints, and reasoning depth
- Tool selection, invocation reliability, and execution order
- Verification logic for task completion and output correctness
- Measurement and detection of failure modes in software engineering workflows

This project aims to build a “controllable, adjustable, and composable” Agent tool framework, making evaluation not just measurement, but control + measurement + verification.

## 🧠 Core Concept: Control-Theoretic Agent Evaluation

This project applies several key ideas from control theory to Agent tool development:

1. **State Modeling**

   Treat the Agent’s task context as a system state:

   - Initial state (task description)
   - Intermediate state (tool calls, reasoning, and observations)
   - Target state (verified task completion)

2. **Control Variable Design**

   Introduce structured control variables such as:

   - Instruction strength
   - Chain-of-thought depth
   - Constraints
   - Role-based control
   - Tool-use policies

3. **Closed-Loop Control**

   Implement feedback:

   - Agent output → Evaluation → Automatic adjustment of prompts or control variables
   - Result validation → Error detection → Re-execution or correction

4. **Multi-Step Control**

   Decompose complex tasks into controllable sub-tasks, guiding the Agent step-by-step toward the target output.

5. **Verification and Detection**

   Add checks for:

   - Tool call correctness
   - Output consistency
   - Exception handling
   - Workflow completion detection

## 🏗️ Repository Structure

```text
harness-control/
│
├── core/                # Core logic of the control-based harness
│   ├── controller.py    # Control variables & closed-loop control
│   ├── evaluator.py     # Unified evaluation interface
│   └── pipeline.py      # Multi-step control pipelines
│
├── prompts/             # Control-based prompt templates
│   ├── state_based/
│   └── constraint_based/
│
├── tasks/               # Task definitions (QA, reasoning, math, code, etc.)
│
├── models/              # Model adapters (OpenAI, HF, DeepSeek, etc.)
│
├── results/             # Experiment logs and results
│
└── README.md            # Project documentation
```

## ⚙️ Usage Examples

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Run a Single Task Evaluation**

```bash
python run.py --task math --model gpt-4o --controller state
```

3. **Enable Closed-Loop Control**

```bash
python run.py --task qa --model deepseek-v2 --controller closed_loop
```

4. **Multi-Step Control Pipeline**

```bash
python run.py --task reasoning --pipeline multi_step
```

## 📊 Preliminary Results (Placeholder)

| Model | Task | Baseline | Harness-Control | Improvement |
|---|---|---:|---:|---:|
| GPT-4o | Math | 72.1 | 78.4 | +6.3 |
| DeepSeek-V2 | QA | 83.5 | 88.2 | +4.7 |
| Qwen2.5 | Reasoning | 68.9 | 74.6 | +5.7 |

> Note: Replace with your actual experimental results.

## 🔮 Future Work

- Automated search for optimal control variables
- Control-based evaluation for RLHF / RLAIF
- Extension to multimodal tasks
- Visualizing control flows and state transitions
- Systematic comparison with existing harness frameworks
- Stronger support for agent tool validation, measurement, and detection in software engineering scenarios

## 📄 License

This project is licensed under the MIT License.
