# Multi-Board Notakto (AI Assistant)

This is a web application for playing the game **Notakto** against an AI Assistant. The app is built using Python and [Streamlit](https://streamlit.io/).

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
- **AI vs AI Simulation**: Run thousands of simulated games between two AI bots of varying difficulties to analyze strategies and win rates.
