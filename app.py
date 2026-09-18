import streamlit as st
import random
import colorama

def valid(guess):
    """Return True if the user's guess is 5 letters, otherwise return False"""
    if len(guess)!=5:
        return False
    if not guess.isalpha():
        return False
    return True

def check_answer(guess, target):
    """Return a list of 5 colors representing highlights for the Wordle guess feedback"""
    # turn guess and target words into lists of letters
    guess=list(guess)
    target=list(target)
    # start with 5 copies of the default color
    highlights=[colorama.Back.RESET+colorama.Fore.RESET]*5
    # check for greens
    for i in range(5):
        if guess[i]==target[i]:
            highlights[i]=colorama.Back.LIGHTGREEN_EX+colorama.Fore.BLACK
            # eliminate the letter from the target word w/o changing positions of other letters
            target[i]="*"
    # check for yellows
    for i in range(5):
        # make sure it's not already green!
        if highlights[i]!=colorama.Back.LIGHTGREEN_EX+colorama.Fore.BLACK and guess[i] in target:
            highlights[i]=colorama.Back.LIGHTYELLOW_EX+colorama.Fore.BLACK
            # remove the letter from the target word--note this changes positions of other letters
            target.remove(guess[i])
    return highlights


# STREAMLIT CHANGE:
# colorama's terminal highlighting cannot display in a web browser, so this
# converts the SAME highlight values returned by check_answer() to HTML colors.
def show_guess(guess, highlights):
    output=""
    for i in range(5):
        if highlights[i]==colorama.Back.LIGHTGREEN_EX+colorama.Fore.BLACK:
            color="#6aaa64"
        elif highlights[i]==colorama.Back.LIGHTYELLOW_EX+colorama.Fore.BLACK:
            color="#c9b458"
        else:
            color="#787c7e"

        output += (
            f'<span style="display:inline-block; background-color:{color}; '
            f'color:white; font-size:28px; font-weight:bold; '
            f'width:45px; height:45px; line-height:45px; text-align:center; '
            f'margin:3px;">{guess[i]}</span>'
        )

    st.markdown(output, unsafe_allow_html=True)


# decide target word
bank=["ABOUT", "APPLE", "BEACH", "BRAIN", "BREAD", "BRING", "CHAIR", "CLEAN",
    "CLOCK", "CLOUD", "DANCE", "DREAM", "DRIVE", "EARTH", "ENJOY", "FIELD",
    "FLOOR", "FOCUS", "FRONT", "FRUIT", "GLASS", "GRACE", "GRASS", "GREEN",
    "GROUP", "HAPPY", "HEART", "HOUSE", "IMAGE", "LIGHT", "LUNCH", "MAGIC",
    "MONEY", "MOUSE", "NIGHT", "OCEAN", "PAPER", "PEACE", "PHONE", "PLANT",
    "POINT", "POWER", "QUIET", "RIVER", "ROUND", "SHARE", "SMILE", "SOUND",
    "TABLE", "WATER"]


# STREAMLIT CHANGE:
# Streamlit reruns the whole script after each interaction, so the target word
# and previous guesses have to be saved in session_state.
if "target" not in st.session_state:
    st.session_state.target=random.choice(bank)
    st.session_state.guesses=[]
    st.session_state.game_over=False


st.title("Wordle")

st.markdown("""
This is a real first-year computer science project at Susquehanna. In **CSCI-181 Principles of Computer Science**, students recreate the basic functionality of Wordle using Python, including checking guesses correctly and giving color-coded feedback.

This demo shows the core functionality we expect, but students are encouraged to make the project their own. They can add features like a color-coded on-screen keyboard, a larger word bank, or win/loss statistics.

**Curious about the code?** Click the GitHub icon (the cat) in the upper-right corner to see the code behind this demo, including the same core logic CSCI-181 students write.
""")


# STREAMLIT CHANGE:
# input() cannot be used in a Streamlit app.  A form replaces the original
# input()/while loop. Invalid guesses are rejected without using up a turn.
if not st.session_state.game_over:
    with st.form("guess_form", clear_on_submit=True):
        guess=st.text_input("Guess the word:").upper()
        submitted=st.form_submit_button("Guess")

    if submitted:
        if not valid(guess):
            st.warning("Try again. Enter 5 letters in all caps to guess the word:")
        else:
            # get the list of highlights for feedback
            highlights=check_answer(guess,st.session_state.target)

            # save this guess so it is still visible after Streamlit reruns
            st.session_state.guesses.append((guess,highlights))

            # if it was right, end the game
            if guess==st.session_state.target:
                st.session_state.game_over=True

            # stop after 6 wrong guesses
            elif len(st.session_state.guesses)==6:
                st.session_state.game_over=True


# print the highlighted feedback for every guess made so far
for guess,highlights in st.session_state.guesses:
    show_guess(guess,highlights)


# same win/lose messages as the original
if st.session_state.game_over:
    if st.session_state.guesses[-1][0]==st.session_state.target:
        st.success("You got it! Congrats!")
    else:
        st.error("You lose... The word was "+st.session_state.target)

    # lets the next visitor play without needing to restart the app
    if st.button("Play again"):
        del st.session_state.target
        del st.session_state.guesses
        del st.session_state.game_over
        st.rerun()
