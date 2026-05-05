import streamlit as st
from game_logic import get_active_boards, is_game_over
from ai_agent import get_ai_move, get_best_move

st.set_page_config(page_title="Notakto Game", layout="wide")

# Custom CSS to make buttons perfectly square and large
st.markdown("""
<style>
    /* Make grid buttons square and text large (only targets buttons inside columns) */
    div[data-testid="column"] div[data-testid="stButton"] button {
        aspect-ratio: 1 / 1;
        font-size: 3rem !important;
        font-weight: bold !important;
        border-radius: 10px;
    }
    
    /* Style for disabled buttons (dead boards or played spots) inside columns */
    div[data-testid="column"] div[data-testid="stButton"] button:disabled {
        opacity: 0.6 !important;
        background-color: #f0f2f6 !important;
        color: #555555 !important;
        border: none !important;
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
    # Ignore invalid moves
    if st.session_state.game_over or st.session_state.board_array[index] != 0:
        return
        
    # Ignore clicks on dead boards
    board_idx = index // 9
    if not st.session_state.active_boards[board_idx]:
        return

    # Player makes a move
    st.session_state.board_array[index] = 1
    update_game_state("Player")
    
    # AI's turn if game is not over
    if not st.session_state.game_over:
        st.session_state.current_turn = "AI"
        
        # AI move calculation
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
                st.warning(f"💡 AI Tutor Suggests: Board {board_num}, Row {row}, Col {col} (Index {best_move})")

# Render boards
cols = st.columns(3)
for board_idx in range(3):
    with cols[board_idx]:
        st.subheader(f"Board {board_idx + 1}")
        is_active = st.session_state.active_boards[board_idx]
        if not is_active:
            st.error("DEAD")
        else:
            st.success("ACTIVE")
            
        # Draw 3x3 grid
        for row in range(3):
            grid_cols = st.columns(3)
            for col in range(3):
                cell_idx = board_idx * 9 + row * 3 + col
                val = st.session_state.board_array[cell_idx]
                label = "X" if val == 1 else " "
                
                with grid_cols[col]:
                    # Disable button if board is dead, spot is taken, or game is over
                    disabled = not is_active or val == 1 or st.session_state.game_over
                    st.button(
                        label,
                        key=f"btn_{cell_idx}",
                        on_click=make_move,
                        args=(cell_idx,),
                        disabled=disabled,
                        use_container_width=True
                    )
