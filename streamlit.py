import streamlit as st
from typing import Dict, Any, List
from game.question_tree import QuestionTree
from data.parsing import Parsing
from game.question_node import QuestionNode
from api.animal_info import AnimalInfo
from game.player import Player
from scoring.score import Score
from scoring.csv_score_repository import CSVScoreRepository
import sys

st.set_page_config(
    page_title="Animal Oracle",
    page_icon="🐶",
    layout="centered",
    menu_items=None
)

# Initialize session state
if "tree" not in st.session_state:
    # Get username from session or sidebar
    if "username" not in st.session_state:
        st.session_state.username = None
    
    filepath: str
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else :
        filepath = "data/animals_tree.json"

    try:
        st.session_state.tree = QuestionTree(filepath)
        st.session_state.parsing = Parsing(filepath)
    except Exception as e:
        st.error(
            f"Could not load '{filepath}'. Falling back to 'animals_tree.json'. Error: {e}"
        )
        st.session_state.filepath = "data/animals_tree.json"
        st.session_state.tree = QuestionTree("data/animals_tree.json")
        st.session_state.parsing = Parsing("data/animals_tree.json")
    st.session_state.current_node = st.session_state.tree.root
    st.session_state.game_state = "playing"  # 'playing', 'won', 'learning'
    st.session_state.question_history = []
    st.session_state.animal_info = AnimalInfo()
    st.session_state.parsing = Parsing("data/animals_tree.json")
    st.session_state.score_repository = CSVScoreRepository()


bg_color = "#f0f2f6"
text_color = "#000000"
question_text_color = "#1f77b4"
succes_box_color = "#d4edda"
error_box_color = "#f8d7da"


# Custom CSS
st.markdown(
    f"""
    <style>
    .big-font {{
        font-size:24px !important;
        font-weight: bold;
        color: {question_text_color};
    }}
    .question-box {{
        background-color: {bg_color};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    .success-box {{
        background-color: {succes_box_color};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #28a745;
    }}
    .error-box {{
        background-color: {error_box_color};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #dc3545;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_game() -> None:
    """Reset the game to initial state"""
    st.session_state.current_node = st.session_state.tree.root
    st.session_state.game_state = "playing"
    st.session_state.question_history = []
    st.session_state.player.score.actual_score = 0
    # Reset flags to allow score saving in the next game
    if "score_saved" in st.session_state:
        del st.session_state.score_saved
    if "just_learned" in st.session_state:
        del st.session_state.just_learned


def handle_answer(answer: bool) -> None:
    """Process user's answer to a question"""
    # Add to history
    st.session_state.question_history.append(
        {"question": st.session_state.current_node.value, "answer": answer}
    )

    # Add points for each question answered
    st.session_state.player.score.add_point()

    # Navigate tree
    if answer:
        st.session_state.current_node = st.session_state.current_node.yes
    else:
        st.session_state.current_node = st.session_state.current_node.no


def is_leaf_node(node: QuestionNode) -> bool:
    """Check if node is a leaf (animal guess)"""
    return node.yes is None and node.no is None


def improve_tree(
    correct_animal: str, distinguishing_question: str, answer_for_correct: bool
) -> None:
    """Add new knowledge to the tree"""
    node: QuestionNode = st.session_state.current_node

    # Create new question node
    new_node: QuestionNode = QuestionNode(distinguishing_question)

    # Create leaf nodes for animals
    yes_node: QuestionNode = QuestionNode(correct_animal)
    no_node: QuestionNode = QuestionNode(node.value)

    # Assign yes/no based on answer
    if answer_for_correct:
        new_node.yes = yes_node
        new_node.no = no_node
    else:
        new_node.yes = no_node
        new_node.no = yes_node

    # Replace current node content
    node.value = new_node.value
    node.yes = new_node.yes
    node.no = new_node.no

    # Save tree
    st.session_state.parsing.save_json_tree(st.session_state.tree.root)


# Main UI
st.title("Animal Oracle")
st.markdown("---")

# Login section if no username is set
if st.session_state.username is None:
    st.header("Welcome! Please enter your username to play")
    username_input = st.text_input("Username:", placeholder="Enter your username")
    if st.button("Start Playing", type="primary", use_container_width=True):
        if username_input:
            st.session_state.username = username_input
            # Create Score with repository injection
            score = Score(username_input, st.session_state.score_repository)
            st.session_state.player = Player(username_input, score)
            st.rerun()
        else:
            st.error("Please enter a username to continue")
    st.stop()

# Sidebar with game info
with st.sidebar:
    st.header("🎮 Game Statistics")
    st.write(f"**Player:** {st.session_state.username}")
    # Get total score from database using the session player instance
    total_score = st.session_state.player.score.get_user_score(st.session_state.username)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions Asked", len(st.session_state.question_history))
    with col2:
        st.metric("Session Score", st.session_state.player.score.actual_score)

    st.metric("Total Score", total_score)

    st.markdown("---")
    st.header("Question History")
    if st.session_state.question_history:
        for i, item in enumerate(st.session_state.question_history, 1):
            answer_emoji = "✅" if item["answer"] else "❌"
            st.write(f"{i}. {item['question']}")
            st.write(f"   {answer_emoji} {'Yes' if item['answer'] else 'No'}")
    else:
        st.write("No questions yet")

    st.markdown("---")
    # Disable New Game button if player is in learning mode and hasn't completed the form
    is_learning_incomplete = (
        st.session_state.game_state == "learning"
        and not st.session_state.get("just_learned", False)
    )
    if st.button("New Game", use_container_width=True, disabled=is_learning_incomplete):
        reset_game()
        st.rerun()

    # Show message if button is disabled
    if is_learning_incomplete:
        st.caption("⚠️ Complete the learning form first!")

# Game intro
if len(st.session_state.question_history) == 0:
    st.markdown(
        """
    <div class="question-box">
    <h2>Welcome to the Animal Oracle!</h2>
    <p>Think of an animal, and I'll try to guess it by asking you questions.</p>
    <p>Answer <b>Yes</b> or <b>No</b> to each question, and I'll narrow down my guess!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Game logic
if st.session_state.game_state == "playing":
    current: QuestionNode = st.session_state.current_node

    if is_leaf_node(current):
        # Final guess
        st.markdown(
            f"""
        <div class="question-box">
        <h3>My guess is...</h3>
        <h2 style="color: #ff6b6b;">{current.value}</h2>
        <p>Am I correct?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "✅ Yes, you got it!", use_container_width=True, type="primary"
            ):
                st.session_state.game_state = "won"
                st.rerun()
        with col2:
            if st.button("❌ No, wrong guess", use_container_width=True):
                st.session_state.game_state = "learning"
                st.rerun()
    else:
        # Ask question
        st.markdown(
            f"""
        <div class="question-box">
            <p class="big-font">{current.value}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes / True", use_container_width=True, type="primary"):
                handle_answer(True)
                st.rerun()
        with col2:
            if st.button("❌ No / False", use_container_width=True):
                handle_answer(False)
                st.rerun()

elif st.session_state.game_state == "won":
    # Victory screen
    st.balloons()

    # Update player score for victory
    if "score_saved" not in st.session_state:
        st.session_state.player.score.victory()
        st.session_state.score_saved = True

    st.markdown(
        f"""
    <div class="success-box">
    <h2>Yay! I guessed it right!</h2>
    <h3>It was a {st.session_state.current_node.value}!</h3>
    <h4>You earned {st.session_state.player.score.actual_score} points! 🎉</h4>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Show animal info
    with st.spinner("Fetching information from Wikipedia..."):
        try:
            info: str = st.session_state.animal_info.get_animal_info(
                st.session_state.current_node
            )
            st.markdown("### Learn more about this animal:")

            infos: Dict[str, Any] = st.session_state.animal_info.search(
                st.session_state.current_node.value
            )

            if infos["summary"]:
                st.write(infos["summary"])

            if infos["thumbnail"]:
                st.image(
                    infos["thumbnail"],
                    caption=st.session_state.current_node.value,
                    use_container_width=True,
                )

            # Display other images if available
            if infos["images"] and len(infos["images"]) > 0:
                st.markdown("### More images:")
                # Filter out non-image files (like .svg, .pdf, etc.)
                image_extensions: tuple = (".jpg", ".jpeg", ".png", ".gif", ".webp")
                valid_images: List[str] = [
                    img
                    for img in infos["images"]
                    if any(img.lower().endswith(ext) for ext in image_extensions)
                ]

                if valid_images:
                    # Display images in a grid (3 columns)
                    cols = st.columns(3)
                    idx: int
                    img_url: str
                    for idx, img_url in enumerate(
                        valid_images[:9]
                    ):  # Limit to 9 images
                        with cols[idx % 3]:
                            st.image(img_url, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not fetch animal information: {str(e)}")


elif st.session_state.game_state == "learning":
    # Learning mode - get new information
    # Update player score for loss if not already saved
    if "score_saved" not in st.session_state:
        st.session_state.player.score.game_over()
        st.session_state.score_saved = True

    st.markdown(
        f"""
    <div class="error-box">
    <h3>Oops! I was wrong.</h3>
    <p>I guessed <b>{st.session_state.current_node.value}</b>, but that wasn't right.</p>
    <p>You lost {st.session_state.player.score.actual_score} points! Help me learn so I can do better next time!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check if we just learned something
    if "just_learned" not in st.session_state:
        st.session_state.just_learned = False

    if not st.session_state.just_learned:
        with st.form("learning_form"):
            st.markdown("### Teach me about your animal")

            # Use stable keys to prevent widget identity changes when labels change
            correct_animal: str = st.text_input(
                "What animal were you thinking of?",
                placeholder="e.g., Lion, Elephant, Penguin...",
                key="learning_correct_animal",
            )

            distinguishing_question: str = st.text_input(
                f"What question would distinguish your animal from a {st.session_state.current_node.value}?",
                placeholder="e.g., Does it live in Europe?, Is it a carnivore?, Can it swim?",
                key="learning_distinguishing_question",
            )

            # Keep the radio label stable and show the actual question below for context
            st.write(
                "For your animal, what would be the answer to your distinguishing question?"
            )
            if distinguishing_question:
                st.caption(f'Question preview: "{distinguishing_question}"')

            answer_for_correct: bool = st.radio(
                "Select the answer for your animal:",
                options=[True, False],
                format_func=lambda x: "Yes / True" if x else "No / False",
                key="learning_answer_for_correct",
            )

            submitted: bool = st.form_submit_button(
                "Teach Me", use_container_width=True, type="primary"
            )

            if submitted:
                # Read values from the widget variables (they persist via keys)
                if correct_animal and distinguishing_question:
                    improve_tree(
                        correct_animal, distinguishing_question, answer_for_correct
                    )
                    st.session_state.just_learned = True
                    st.session_state.learned_animal = correct_animal
                    st.session_state.learned_question = distinguishing_question
                    st.rerun()
                else:
                    st.error("Please fill in all fields to help me learn!")
    else:
        # Show success message and play again button
        st.success("Got it! I'll remember that for next time.")
        st.info(
            f"New knowledge added: '{st.session_state.learned_question}' helps distinguish {st.session_state.learned_animal} from {st.session_state.current_node.value}"
        )

        if st.button("Play Again", use_container_width=True, type="primary"):
            st.session_state.just_learned = False
            reset_game()
            st.rerun()
