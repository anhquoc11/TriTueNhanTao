# 🤖 Artificial Intelligence Projects

> A collection of Artificial Intelligence projects and classical AI algorithms implemented in **Python** as part of the Artificial Intelligence course.

![Python](https://img.shields.io/badge/Python-3.11.9-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-Supported-brightgreen)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-Educational-orange)

---

# 📖 Introduction

This repository demonstrates the implementation and visualization of classical Artificial Intelligence algorithms through three practical projects. It covers a wide range of AI topics, including search algorithms, local search, Constraint Satisfaction Problems (CSP), and adversarial search.

---

# 🚀 Projects

| Project | Description |
|----------|-------------|
| 🧹 **Vacuum Cleaner** | Robot vacuum simulator implementing multiple AI search algorithms for autonomous path planning and environment exploration. |
| 🗺️ **Map Coloring** | Solves the map coloring problem using Constraint Satisfaction Problem (CSP) algorithms. |
| ❌ **Tic-Tac-Toe** | AI agent playing Tic-Tac-Toe using classical adversarial search algorithms. |

---

# 📚 Supported Algorithms

## 🔵 Uninformed Search

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Iterative Deepening Search (IDS)
- Uniform Cost Search (UCS)

---

## 🟡 Informed Search

- Greedy Best-First Search
- A* Search
- Iterative Deepening A* (IDA*)

---

## 🟢 Local Search

- Simple Hill Climbing
- Steepest Ascent Hill Climbing
- Stochastic Hill Climbing
- Random Restart Hill Climbing
- Local Beam Search
- Simulated Annealing

---

## 🟣 Search in Unobservable Environments

- Multi-Source Breadth-First Search (BFS_MTPT)
- AND-OR Graph Search

---

## 🔴 Constraint Satisfaction Problems (CSP)

- Backtracking Search
- Forward Checking
- AC-3 (Arc Consistency Algorithm)
- Min-Conflicts

---

## ⚫ Adversarial Search

- Minimax
- Alpha-Beta Pruning
- Expectimax

---

# 📁 Project Structure

```text
Artificial-Intelligence/
│
├── Caro/
│   ├── algorithms/
│   │   ├── alpha_beta.py
│   │   ├── expectimax.py
│   │   ├── Minimax.py
│   │   └── Utility.py
│   └── tic_tac_toe_ui.py
│
├── ToMauBanDo/
│   ├── algorithms/
│   │   ├── ac3.py
│   │   ├── backtracking.py
│   │   ├── Forward_Checking.py
│   │   └── min_conflicts.py
│   ├── DATA/
│   │   └── Wards.json
│   ├── frontend_CSP.py
│   └── map_output.png
│
├── Vacuum/
│   ├── algorithms/
│   │   ├── BFS.py
│   │   ├── DFS.py
│   │   ├── UCS.py
│   │   ├── IDF.py
│   │   ├── greedy.py
│   │   ├── A_sao.py
│   │   ├── IDA_sao.py
│   │   ├── BFS_MTPT.py
│   │   ├── Simple_Hill_Climbing.py
│   │   ├── Steepest_hill_climbing.py
│   │   ├── Stochastic_HillClimbing.py
│   │   ├── Random_Restart_Hill_Climbing.py
│   │   ├── Local_Beam_Search.py
│   │   ├── SA.py
│   │   ├── And_Or_search.py
│   │   └── Utility.py
│   ├── assets/
│   │   ├── dirt.jpg
│   │   ├── robot.jpg
│   │   └── wall.jpg
│   └── frontend.py
│
└── README.md
```
---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/anhquoc11/TriTueNhanTao.git
```

## 2. Navigate to the project directory

```bash
cd TriTueNhanTao
```

## 3. Install the required dependency

```bash
pip install pygame
```

> **Requirements**
>
> - Python **3.11.9**
> - Pygame
> - Tkinter (included with the standard Python installation)

---

# ▶️ Running the Projects

## 🧹 Vacuum Cleaner

```bash
cd Vacuum
python frontend.py
```

---

## 🗺️ Map Coloring

```bash
cd ToMauBanDo
python frontend_CSP.py
```

---

## ❌ Tic-Tac-Toe

```bash
cd Caro
python tic_tac_toe_ui.py
```

---

# 🎯 Learning Objectives

This repository aims to:

- Understand classical AI search algorithms.
- Compare uninformed and informed search techniques.
- Explore local search strategies.
- Solve Constraint Satisfaction Problems (CSP).
- Implement search in unobservable environments.
- Develop intelligent game-playing agents using adversarial search.

---

# 🛠️ Technologies

- Python 3.11.9
- Pygame
- Tkinter

---

# 👨‍💻 Author

**Nguyen Tran Anh Quoc**

Student Project – Artificial Intelligence

GitHub: https://github.com/anhquoc11

---
