🚀 Harness-Control: A Control-Theoretic Framework for Improving LLM Performance

📘 Project Overview

Harness-Control is an experimental repository designed to explore and validate a new harness framework for evaluating and improving large language models (LLMs).The core objective is to apply control-theoretic thinking to structure prompts, task flows, and model behaviors, enabling systematic performance improvements across diverse tasks.

This repository includes:

A new controllable harness framework

Control-based structured prompt templates

Multi-task, multi-model performance comparison experiments

Reproducible evaluation scripts and dataset interfaces

🎯 Motivation

Traditional LLM evaluation frameworks (e.g., EleutherAI’s lm-evaluation-harness) mainly focus on:

Task input → Model output

Metric computation → Performance reporting

However, real-world model performance heavily depends on:

The structure of prompts

The design of control variables (context, instructions, reasoning depth)

Multi-step control and feedback mechanisms

This project aims to build a “controllable, adjustable, and composable” harness framework, making evaluation not just measurement, but control + measurement.

🧠 Core Concept: Control-Theoretic Performance Enhancement

This project applies several key ideas from control theory:

1. State Modeling

Treat the model’s input context as a system state:

Initial state (initial prompt)

Intermediate state (reasoning steps)

Target state (desired output)

2. Control Variable Design

Introduce structured control variables such as:

Instruction strength

Chain-of-thought depth

Constraints

Role-based control

3. Closed-Loop Control

Implement feedback:

Model output → Evaluation → Automatic adjustment of prompts or control variablesForming a lightweight closed-loop control cycle.

4. Multi-Step Control

Decompose complex tasks into controllable sub-tasks, guiding the model step-by-step toward the target output.

🏗️ Repository Structure

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

⚙️ Usage Examples

1. Install Dependencies

pip install -r requirements.txt

2. Run a Single Task Evaluation

python run.py --task math --model gpt-4o --controller state

3. Enable Closed-Loop Control

python run.py --task qa --model deepseek-v2 --controller closed_loop

4. Multi-Step Control Pipeline

python run.py --task reasoning --pipeline multi_step

📊 Preliminary Results (Placeholder)

Model

Task

Baseline

Harness-Control

Improvement

GPT-4o

Math

72.1

78.4

+6.3

DeepSeek-V2

QA

83.5

88.2

+4.7

Qwen2.5

Reasoning

68.9

74.6

+5.7

Note: Replace with your actual experimental results.

🔮 Future Work

Automated search for optimal control variables

Control-based evaluation for RLHF / RLAIF

Extension to multimodal tasks

Visualizing control flows and state transitions

Systematic comparison with existing harness frameworks

📄 License

This project is licensed under the MIT License.
