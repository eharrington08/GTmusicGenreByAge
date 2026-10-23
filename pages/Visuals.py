# This creates the page for displaying data visualizations.
import json
import streamlit as st
import os
import pandas as pd
import altair as alt
# # Finds the folder this script is in
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Goes up one folder level to lab02 where data.json lives
# json_path = os.path.join(script_dir, "..", "data.json")

# Opens the json file in read only and sets it to data
with open("data.json", "r") as file:
    data = json.load(file)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)
 
def loadResponses():
    if os.path.exists("responses.json"):
        try:
            with open("responses.json", "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    return []
def saveResponses(responses):
    with open("responses.json", "w") as f:
        json.dump(responses, f)
    
if "responses" not in st.session_state:
    st.session_state["responses"] = loadResponses()

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
st.subheader(data["chart_title"])
source = pd.DataFrame(data["data_points"]) 
st.scatter_chart(source, x="genre", y="age", color="genre")

 
with st.form("survey_form", clear_on_submit=True):
    genre = st.selectbox(
        "Favorite music genre?",
        ["Pop", "Rock", "Rap", "Country", "Classic Rock", "Alt Rock", "Indie-Pop", "Metal", "Alternative", "Other"],
    )
    
    otherGenre = st.text_input("If you chose **other** input your favorite genre.")
    
    age = st.number_input("Age", min_value=1, max_value=120, value=18)
    hours = st.number_input(
        "Hours per week listening to this genre",
        min_value=0.0, max_value=168.0, value=5.0, step=0.5,
    )
    submitted = st.form_submit_button("Submit")

if submitted: 
    if genre == "Other":
        genre = otherGenre.strip()
    if not genre:
        st.error("Please enter a genre.")
    else:
        responses = loadResponses()
        responses.append({"genre": genre, "age": age, "hours_per_week": hours})
        saveResponses(responses)
        st.session_state['responses'] = responses
        st.success("Response recorded!")


responses = st.session_state["responses"]

if len(responses) == 0:
    st.info("No responses yet. Submit the form above to see the chart.")
else: 
    dynamicData = pd.DataFrame(responses) 

    chart = (
        alt.Chart(dynamicData) 
        .mark_circle(size=120, opacity=0.8) 
        .encode( 
            x=alt.X("age:Q", title="Age"),
            y=alt.Y("hours_per_week:Q", title="Hours Per Week Listened"),
            color=alt.Color("genre:N", title="Genre"),
            tooltip=["genre", "age", "hours_per_week"], 
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---


