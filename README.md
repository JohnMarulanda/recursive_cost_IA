---

# 🌟 Adventure Time: Recursive Uniform Cost Search Game 🌟

Welcome to **Adventure Time: Recursive Uniform Cost Search Game**! In this project, you will help **Finn** navigate a world full of obstacles to reach **Jake** by using an efficient and recursive uniform cost search algorithm.

[Finn and Jake]

## 📜 Table of Contents

- [📝 Description](#-description)
- [🎮 Features](#-features)
- [📦 Requirements](#-requirements)
- [🚀 How to Play](#-how-to-play)
- [💻 Installation](#-installation)
- [🖼 Screenshots](#-screenshots)

## 📝 Description

This game uses a custom **recursive uniform cost search algorithm** to find the optimal path through a grid. Finn must navigate through various terrains to reach Jake, while facing penalties and bonuses.

The twist on the standard uniform cost algorithm allows the game to efficiently manage memory by re-expanding branches of the search tree as needed.

| **Grid Key**    | **Terrain**                           | **Effect**                |
|-----------------|---------------------------------------|---------------------------|
| 🟩 `0`           | Grass (free path)                    | No effect                 |
| 🌿 `1`           | Bush (obstacle)                      | Impassable                |
| 👦 `2`           | Finn (start point)                   | Starting position         |
| 🐶 `3`           | Jake (goal)                          | Goal of the game          |
| 👹 `4`           | Lich (penalty)                       | +3 cost to path           |
| 🗡️ `5`           | Sword (bonus)                        | -2 cost to path           |

## 🎮 Features

- **🌟 Recursive Uniform Cost Algorithm**: Efficient memory management and optimal pathfinding.
- **🎨 Beautiful Pixel Art**: Characters like Finn, Jake, and the Lich come to life in pixel form.
- **🗺️ Randomly Generated Grid**: Each game generates a unique terrain filled with obstacles, bonuses, and penalties.
- **🖱️ Interactive UI**: Buttons and a clean user interface built with Pygame for an engaging experience.
- **🧩 Dynamic Terrain**: Every grid element affects the cost of Finn’s journey in different ways.

## 📦 Requirements

- Python 3.8+
- Pygame
- System capable of running Pygame

## 🚀 How to Play

1. **Start the game**: Use the play button to generate a new random matrix.
2. **Observe Finn’s journey**: Watch the algorithm compute the best path to Jake, avoiding obstacles like bushes and the Lich.
3. **Collect bonuses**: Swords reduce the total cost of Finn's path, while the Lich adds penalties.

## 💻 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/adventure-time-recursive-cost.git
   cd adventure-time-recursive-cost
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:

   ```bash
   python main.py
   ```

## 🖼 Screenshots

### Gameplay
---
