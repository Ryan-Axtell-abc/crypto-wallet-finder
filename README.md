# Visualizer for Maze Generation and Maze Solving Algorithms

A JavaScript site that uses Three.js to animate maze generation and maze-solving algorithms in 3D. It features algorithms like A\* and depth-first search, with an interactive step-by-step mode to help users better understand the processes behind the algorithms.


![Cloth Simulation Screenshot](https://github.com/Ryan-Axtell-abc/three-js-maze/blob/main/assets/screenshot.png)

## Demo

[Live Demo Link](https://maze.ryanaxtell.dev/)

# Controls

| Command          | Action                                   |
|------------------|------------------------------------------|
| **Left click**   | Pan camera                               |
| **Middle Click** | Rotate camera                            |
| **Right click**  | Toggle walls / drag start and end points |

## Installation

### Prerequisites

- **Node.js** (v12 or higher recommended)
- **npm** (comes with Node.js)

### Clone the Repository

```bash
git clone https://github.com/Ryan-Axtell-abc/three-js-maze.git
cd three-js-maze
```

### Install Dependencies

```bash
npm install
```

## Usage

### Running the Simulation

```bash
npx vite
```

Open your web browser and navigate to `http://localhost:5173` to view the simulation.

### Building for Production

```bash
npx vite build
```

The production-ready files will be in the `dist/` directory.