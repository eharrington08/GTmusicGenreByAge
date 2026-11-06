# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv
# PAGE CONFIGURATION
game_genres = [
    "Action",
    "Platformer",
    "Fighting",
    "Beat 'em up",
    "Hack and Slash",
    "Shooter",
    "First-Person Shooter",
    "Third-Person Shooter",
    "Battle Royale",
    "Stealth",
    "Survival Horror",
    "Adventure",
    "Action-Adventure",
    "Point-and-Click",
    "Visual Novel",
    "Interactive Fiction",
    "Walking Simulator",
    "Metroidvania",
    "RPG",
    "Action RPG",
    "JRPG",
    "Western RPG",
    "Tactical RPG",
    "MMORPG",
    "Roguelike",
    "Roguelite",
    "Dungeon Crawler",
    "Strategy",
    "Real-Time Strategy",
    "Turn-Based Strategy",
    "4X",
    "Tower Defense",
    "MOBA",
    "Grand Strategy",
    "Auto Battler",
    "Card Game",
    "Deck Builder",
    "Simulation",
    "Life Simulation",
    "City Builder",
    "Farming Simulation",
    "Vehicle Simulation",
    "Flight Simulation",
    "Management",
    "Tycoon",
    "Sandbox",
    "Survival",
    "Crafting",
    "Sports",
    "Racing",
    "Kart Racing",
    "Football",
    "Basketball",
    "Soccer",
    "Wrestling",
    "Extreme Sports",
    "Puzzle",
    "Match-Three",
    "Hidden Object",
    "Trivia",
    "Party",
    "Casual",
    "Idle",
    "Clicker",
    "Rhythm",
    "Music",
    "Dance",
    "Educational",
    "Horror",
    "Open World",
    "Arcade",
    "Pinball",
    "Board Game",
    "Fitness",
    "Virtual Reality",
    "Text-Based",
    "Idle RPG",
    "Looter Shooter",
    "Souls-like",
    "Co-op",
    "Multiplayer Online",
]
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    genre_input = st.selectbox(
            "Favorite video game genre?",
            sorted(game_genres),
        )
    age_input = st.number_input(
        "How old are you?",
        min_value=1,
        max_value=120,
        step=1
    )
    time_input = st.slider("How many hours do you play this genre per week?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        row = [genre_input, age_input, time_input]
        with open("data.csv", "a", newline="") as data:
            writer = csv.writer(data)
            writer.writerow(row)
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Genre:** {genre_input}, **Age:** {age_input}, **Time:** {time_input}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")