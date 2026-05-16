# Multi-Board Notakto (AI Assistant)

This is a web application for playing the game **Notakto** against an AI Opponent. The app is built using Python and [Streamlit](https://streamlit.io/).

## Game Rules
- Notakto is a variant of Tic-Tac-Toe played across multiple boards.
- Both players play the same piece: 'X'. 
- Getting 3-in-a-row kills that specific board. 
- The player who gets 3-in-a-row on the **final** active board **LOSES** the game.

## Prerequisites
To run this application locally, you will need to have **Python 3.8+** installed on your computer.

## Setup & Installation

**1. Clone or download the code**  
Open a terminal (or Command Prompt) and navigate to the directory where you've saved this project.

**2. Create a Virtual Environment (Recommended)**  
It is best practice to create a virtual environment to manage dependencies:
```bash
python -m venv venv
```

**3. Activate the Virtual Environment**  
- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- On **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

**4. Install Dependencies**  
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```
*(Note: The primary dependency for this project is `streamlit`).*

## Running the Application

Once your dependencies are installed, you can start the application by running:

```bash
streamlit run app.py
```

This will automatically launch the Notakto app in your default web browser (typically at `http://localhost:8501`).

## Features
- **Play against AI**: Choose between Easy, Medium, or Hard difficulty levels.
- **AI Tutor**: Turn on the AI Tutor mode to get suggestions on the best optimal move during your turn.
- **AI vs AI Simulation**: Run hundreds of simulated games between two AI bots of varying difficulties to analyze strategies and win rates.

## Code Layout & Architecture
Here is a quick overview of what each file in this repository does:

- **`app.py`**: The main entry point for the Streamlit web application. It handles the user interface (UI), custom CSS styling, game state management (like tracking turns and active boards), and user interactions (button clicks). 
- **`game_logic.py`**: Contains the core rules and mechanics of Notakto. It includes functions to check if boards are "dead" (3-in-a-row achieved), find all valid moves for the current state, and determine if the overall game is over.
- **`ai_agent.py`**: The brain of the AI opponent. It implements an adversarial search algorithm (Negamax with Alpha-Beta pruning) to determine the most optimal move. It dynamically adjusts its search depth based on the number of active boards left and uses a caching mechanism to speed up repeated calculations.
- **`requirements.txt`**: A standard text file listing the Python dependencies required to run the project.
- **`.streamlit/config.toml`**: Configuration file for Streamlit, used to enforce dark mode.
