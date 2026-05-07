import streamlit as st
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
    div[data-testid="column"] div[data-testid="stButton"] button {
        aspect-ratio: 1 / 1;
        font-size: 5rem !important;
        font-weight: bold !important;
        border-radius: 12px;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        background: rgba(0, 229, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #00e5ff !important; /* Glowing neon blue text */
        text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff;
        padding: 0;
        line-height: 1;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 229, 255, 0.05);
    }
    
    div[data-testid="column"] div[data-testid="stButton"] button p {
        font-size: 5rem !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    
    /* Hover effect for active grid buttons */
    div[data-testid="column"] div[data-testid="stButton"] button:hover:not(:disabled) {
        border-color: rgba(0, 229, 255, 0.6) !important;
        background: rgba(0, 229, 255, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4), inset 0 0 15px rgba(0, 229, 255, 0.1);
        transform: translateY(-2px);
    }
    
    /* Style for disabled buttons (dead boards or played spots) */
    div[data-testid="column"] div[data-testid="stButton"] button:disabled {
        opacity: 1 !important; /* Removed grayed out effect */
        background: rgba(0, 229, 255, 0.05) !important; /* Keep it looking like active empty cells */
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        color: #00e5ff !important;
        text-shadow: 0 0 10px #00e5ff;
        box-shadow: none;
        transform: none;
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

st.write("### Rules")
st.write("Both players play 'X'. Getting 3-in-a-row kills that board. The player who gets 3-in-a-row on the **final** active board **LOSES**.")

if st.session_state.game_over:
    st.success(f"Game Over! {st.session_state.winner} wins!")
else:
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
                    st.button(
                        label,
                        key=f"btn_{cell_idx}",
                        on_click=make_move,
                        args=(cell_idx,),
                        disabled=disabled,
                        use_container_width=True
                    )
