import streamlit as st
import time
from game_logic import get_active_boards, is_game_over
from ai_agent import get_ai_move, get_best_move

st.set_page_config(page_title="Notakto Game", layout="wide")

# Custom CSS to make buttons perfectly square and large
st.markdown("""
<style>
    /* Premium dark gradient background for the whole app */
    .stApp {
        background: linear-gradient(135deg, #0b0c10 0%, #1f2833 100%);
    }

    /* Make grid buttons square, glassmorphism, and glowing */
    div[data-testid="column"] button, div[data-testid="stColumn"] button {
        aspect-ratio: 1 / 1 !important;
        font-size: 5rem !important;
        font-weight: bold !important;
        border-radius: 12px;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        background: rgba(0, 229, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #00e5ff !important; /* Glowing neon blue text */
        text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff;
        padding: 0 !important;
        line-height: 1 !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 229, 255, 0.05);
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Target whatever element Streamlit puts inside the button for the X */
    div[data-testid="column"] button *, div[data-testid="stColumn"] button * {
        font-size: 5rem !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        color: inherit !important;
    }
    
    /* Hover effect for active grid buttons */
    div[data-testid="column"] button:hover:not(:disabled), div[data-testid="stColumn"] button:hover:not(:disabled) {
        border-color: rgba(0, 229, 255, 0.6) !important;
        background: rgba(0, 229, 255, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4), inset 0 0 15px rgba(0, 229, 255, 0.1);
        transform: translateY(-2px);
    }
    
    /* Primary button style for tutor mode glow */
    div[data-testid="column"] button[kind="primary"], div[data-testid="stColumn"] button[kind="primary"] {
        border-color: rgba(0, 255, 102, 0.6) !important;
        background: rgba(0, 255, 102, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.5), inset 0 0 15px rgba(0, 255, 102, 0.2) !important;
        color: #00ff66 !important;
        text-shadow: 0 0 10px #00ff66, 0 0 20px #00ff66 !important;
    }
    
    div[data-testid="column"] button[kind="primary"]:hover:not(:disabled), div[data-testid="stColumn"] button[kind="primary"]:hover:not(:disabled) {
        border-color: rgba(0, 255, 102, 0.8) !important;
        background: rgba(0, 255, 102, 0.2) !important;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.6), inset 0 0 20px rgba(0, 255, 102, 0.3) !important;
    }
    
    /* Style for disabled buttons (dead boards or played spots) */
    div[data-testid="column"] button:disabled, div[data-testid="stColumn"] button:disabled {
        opacity: 1 !important; /* Removed grayed out effect */
        background: rgba(0, 229, 255, 0.05) !important; /* Keep it looking like active empty cells */
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        color: #00e5ff !important;
        text-shadow: 0 0 10px #00e5ff;
        box-shadow: none !important;
        transform: none !important;
    }
    
    /* Sidebar dark mode enforcement */
    [data-testid="stSidebar"] {
        background-color: #0b0c10 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Fix input elements (Dropdown, Checkbox, Button) having white backgrounds in Light Mode */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="popover"] > div,
    [data-testid="stSidebar"] [data-testid="stButton"] button {
        background-color: #1f2833 !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        color: #ffffff !important;
    }
    
    /* Disable typing in the main selectbox */
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        caret-color: transparent !important;
        pointer-events: none !important;
        cursor: pointer !important;
    }
    
    /* Target the Checkbox specifically */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] div[data-baseweb="checkbox"] > div {
        background-color: #1f2833 !important;
        border: 1px solid rgba(0, 229, 255, 0.5) !important;
    }

    /* Global Selectbox Dropdown Menu (Popover) Styling */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div {
        background-color: #1f2833 !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
    }
    ul[role="listbox"], 
    ul[data-baseweb="menu"] {
        background-color: #1f2833 !important;
    }
    li[role="option"], 
    li[data-baseweb="menu-item"] {
        background-color: #1f2833 !important;
        color: #ffffff !important;
    }
    li[role="option"] span, 
    li[data-baseweb="menu-item"] span,
    li[role="option"] div, 
    li[data-baseweb="menu-item"] div {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    li[role="option"]:hover, 
    li[data-baseweb="menu-item"]:hover,
    li[aria-selected="true"] {
        background-color: rgba(0, 229, 255, 0.8) !important; /* Make it brighter to contrast with black text */
    }
    li[role="option"]:hover span, 
    li[data-baseweb="menu-item"]:hover span,
    li[role="option"]:hover div, 
    li[data-baseweb="menu-item"]:hover div,
    li[aria-selected="true"] span,
    li[aria-selected="true"] div {
        color: #0b0c10 !important; /* Black text on hover/selected */
    }
    
    /* Hide the search bar inside the dropdown menu */
    div[data-baseweb="popover"] [data-baseweb="input"] {
        display: none !important;
    }
    div[data-baseweb="popover"] input {
        display: none !important;
    }

    /* Brighter Text for specific elements */
    h1 {
        color: #00e5ff !important;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }
    h3 {
        color: #ffffff !important;
    }
    .stMarkdown p {
        color: #e0e0e0 !important;
        font-size: 1.1rem;
    }
    
    /* Make st.info and st.success alerts dark with bright text */
    [data-testid="stNotification"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    [data-testid="stNotification"] * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_state():
    if "board_array" not in st.session_state:
        st.session_state.board_array = [0] * 27
    if "active_boards" not in st.session_state:
        st.session_state.active_boards = [True, True, True]
    if "current_turn" not in st.session_state:
        st.session_state.current_turn = "Player"
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "winner" not in st.session_state:
        st.session_state.winner = None

def update_game_state(last_player):
    st.session_state.active_boards = get_active_boards(st.session_state.board_array)
    if is_game_over(st.session_state.board_array):
        st.session_state.game_over = True
        # The player who just made a move killed the final board and LOST.
        st.session_state.winner = "AI" if last_player == "Player" else "Player"

def make_move(index):
    if st.session_state.game_over or st.session_state.board_array[index] != 0:
        return
        
    board_idx = index // 9
    if not st.session_state.active_boards[board_idx]:
        return

    st.session_state.board_array[index] = 1
    update_game_state("Player")
    
    if not st.session_state.game_over:
        st.session_state.current_turn = "AI"
        
        move = get_ai_move(st.session_state.board_array, st.session_state.difficulty)
            
        if move is not None:
            st.session_state.board_array[move] = 1
            update_game_state("AI")
        
        st.session_state.current_turn = "Player"

initialize_state()

st.title("Multi-Board Notakto (AI Assistant)")

st.sidebar.header("Settings")
st.session_state.difficulty = st.sidebar.selectbox("AI Difficulty", ["Easy", "Medium", "Hard"], index=2)
show_tutor = st.sidebar.checkbox("Enable AI Tutor", value=False)

if st.sidebar.button("Restart Game"):
    for key in ["board_array", "active_boards", "current_turn", "game_over", "winner"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("AI vs AI Simulation")
sim_games = st.sidebar.number_input("Number of Games", min_value=1, max_value=1000, value=100)
ai1_difficulty = st.sidebar.selectbox("AI 1 (First) Difficulty", ["Easy", "Medium", "Hard"], index=2, key="ai1")
ai2_difficulty = st.sidebar.selectbox("AI 2 (Second) Difficulty", ["Easy", "Medium", "Hard"], index=0, key="ai2")

if st.sidebar.button("Run Simulation"):
    progress_bar = st.sidebar.progress(0)
    ai1_wins = 0
    ai2_wins = 0
    
    for i in range(sim_games):
        board = [0] * 27
        current_ai = 1
        
        while True:
            if is_game_over(board):
                # The game is already over before moving? Should not happen initially, but just in case
                break
                
            diff = ai1_difficulty if current_ai == 1 else ai2_difficulty
            move = get_ai_move(board, diff)
            
            if move is not None:
                board[move] = 1
                if is_game_over(board):
                    # The AI who just moved killed the final board and LOST
                    if current_ai == 1:
                        ai2_wins += 1
                    else:
                        ai1_wins += 1
                    break
            else:
                break
                
            current_ai = 2 if current_ai == 1 else 1
            
        progress_bar.progress((i + 1) / sim_games)
        
    st.sidebar.success(f"**Simulation Complete!**\n\nAI 1 ({ai1_difficulty}): {ai1_wins} Wins\n\nAI 2 ({ai2_difficulty}): {ai2_wins} Wins")

st.write("### Rules")
st.write("Both players play 'X'. Getting 3-in-a-row kills that board. The player who gets 3-in-a-row on the **final** active board **LOSES**.")

if st.session_state.game_over:
    winner = st.session_state.winner
    color_class = "red" if winner == "AI" else "green"
    
    modal_html = f"""
    <style>
    #modal-toggle {{ display: none; }}
    #modal-toggle:checked ~ .modal-wrapper {{ display: none; }}
    .modal-wrapper {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 9999; display: flex; justify-content: center; align-items: center;
    }}
    .modal-bg {{
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8); backdrop-filter: blur(8px);
        cursor: pointer;
    }}
    .modal-content {{
        position: relative; z-index: 10000;
        padding: 3rem 5rem; border-radius: 20px; text-align: center;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .modal-content.red {{
        background: rgba(255, 75, 75, 0.15); border: 2px solid rgba(255, 75, 75, 0.6);
        box-shadow: 0 0 40px rgba(255, 75, 75, 0.4); color: #ff4b4b;
    }}
    .modal-content.green {{
        background: rgba(0, 255, 102, 0.15); border: 2px solid rgba(0, 255, 102, 0.6);
        box-shadow: 0 0 40px rgba(0, 255, 102, 0.4); color: #00ff66;
    }}
    .close-btn {{
        position: absolute; top: 10px; right: 20px;
        font-size: 2.5rem; cursor: pointer; color: inherit; line-height: 1;
        transition: transform 0.2s;
    }}
    .close-btn:hover {{ transform: scale(1.2); }}
    @keyframes popIn {{
        from {{ transform: scale(0.5); opacity: 0; }}
        to {{ transform: scale(1); opacity: 1; }}
    }}
    </style>
    <input type="checkbox" id="modal-toggle">
    <div class="modal-wrapper">
        <label for="modal-toggle" class="modal-bg"></label>
        <div class="modal-content {color_class}">
            <label for="modal-toggle" class="close-btn">&times;</label>
            <h1 style="color: inherit !important; text-shadow: 0 0 20px currentColor; font-size: 4rem; margin: 0;">Game Over!</h1>
            <h2 style="color: inherit !important; margin: 0; margin-top: 10px; font-size: 2.5rem;">{winner} Wins!</h2>
        </div>
    </div>
    """
    st.markdown(modal_html, unsafe_allow_html=True)
else:
    best_move = None
    if st.session_state.current_turn == "Player":
        st.info("Your turn! Place an 'X' on any active board.")
        if show_tutor:
            # Show AI Tutor recommendation
            best_move = get_best_move(st.session_state.board_array)
            if best_move is not None:
                board_num = best_move // 9 + 1
                local_index = best_move % 9
                row = local_index // 3 + 1
                col = local_index % 3 + 1
                st.warning(f"💡 AI Tutor Suggests: Board {board_num}, Row {row}, Col {col}")

# Render boards
cols = st.columns(3)
for board_idx in range(3):
    with cols[board_idx]:
        st.markdown(f"<h3 style='text-align: center;'>Board {board_idx + 1}</h3>", unsafe_allow_html=True)
        is_active = st.session_state.active_boards[board_idx]
        if not is_active:
            st.markdown("<div style='text-align: center; padding: 0.5rem; background: rgba(255, 75, 75, 0.1); backdrop-filter: blur(5px); border: 1px solid rgba(255, 75, 75, 0.3); border-radius: 8px; color: #ff4b4b; font-weight: bold; margin-bottom: 1rem; box-shadow: 0 0 15px rgba(255, 75, 75, 0.2);'>DEAD</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; padding: 0.5rem; background: rgba(0, 255, 102, 0.1); backdrop-filter: blur(5px); border: 1px solid rgba(0, 255, 102, 0.3); border-radius: 8px; color: #00ff66; font-weight: bold; margin-bottom: 1rem; box-shadow: 0 0 15px rgba(0, 255, 102, 0.2); text-shadow: 0 0 5px #00ff66;'>ACTIVE</div>", unsafe_allow_html=True)
            
        col_headers = st.columns([0.3, 1, 1, 1])
        with col_headers[1]: st.markdown("<div style='text-align: center; color: #aaa;'>C1</div>", unsafe_allow_html=True)
        with col_headers[2]: st.markdown("<div style='text-align: center; color: #aaa;'>C2</div>", unsafe_allow_html=True)
        with col_headers[3]: st.markdown("<div style='text-align: center; color: #aaa;'>C3</div>", unsafe_allow_html=True)
        
        for row in range(3):
            grid_cols = st.columns([0.3, 1, 1, 1])
            with grid_cols[0]:
                st.markdown(f"<div style='text-align: center; color: #aaa; padding-top: 3.5rem;'>R{row+1}</div>", unsafe_allow_html=True)
            for col in range(3):
                cell_idx = board_idx * 9 + row * 3 + col
                val = st.session_state.board_array[cell_idx]
                label = "X" if val == 1 else " "
                
                with grid_cols[col+1]:
                    disabled = not is_active or val == 1 or st.session_state.game_over
                    is_recommended = show_tutor and ('best_move' in locals() and cell_idx == best_move)
                    st.button(
                        label,
                        key=f"btn_{cell_idx}",
                        on_click=make_move,
                        args=(cell_idx,),
                        disabled=disabled,
                        type="primary" if is_recommended else "secondary",
                        use_container_width=True
                    )
