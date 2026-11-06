# This creates the page for displaying data visualizations.
import json
import streamlit as st
import os
import pandas as pd
import altair as alt
import plotly.express as px


st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

tab1, tab2 = st.tabs(["Part 1", "Part 2"])


def loadResponses():
    if os.path.exists("responses.json"):
        try:
            with open("responses.json", "r") as f:
                return json.load(f)
        except:
            return []

    return []


def saveResponses(responses):
    with open("responses.json", "w", newline="") as f:
        json.dump(responses, f)


def updateMetrics(key, current):
    currentKey = key + "_current"
    previousKey = key + "_previous"

    if currentKey not in st.session_state:
        st.session_state[currentKey] = current
        st.session_state[previousKey] = None
    elif st.session_state[currentKey] != current:
        st.session_state[previousKey] = st.session_state[currentKey]
        st.session_state[currentKey] = current
    return st.session_state[previousKey]


def showMetrics(key, df, ageColumn, hoursColumn):
    current = {
        "Mean Age": round(df[ageColumn].mean(), 2),
        "Median Age": round(df[ageColumn].median(), 2),
        "Mean Hours/Week": round(df[hoursColumn].mean(), 2),
        "Median Hours/Week": round(df[hoursColumn].median(), 2),
    }
    previous = updateMetrics(key, current)

    columns = st.columns(4)
    index = 0
    for name in current:
        delta = None
        if previous is not None:
            delta = round(current[name] - previous[name], 2)
        columns[index].metric(name, current[name], delta=delta)
        index += 1


# PART 1
with tab1:
    with open("data.json", "r") as file:
        data = json.load(file)
    if "responses" not in st.session_state:
        st.session_state["responses"] = loadResponses()

    # PAGE TITLE
    st.title("Data Visualizations for Part 1📈")

    # PART 1: GRAPHS FROM data.json
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
            st.session_state["responses"] = responses
            st.success("Response recorded!")

    responses = st.session_state["responses"]

    if len(responses) == 0:
        st.info("No responses yet. Submit the form above to see the chart.")
    else:
        st.subheader("Favorite Music Genre of User Considering Their Age")
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
        st.subheader("Survey Summary Metrics")
        showMetrics("p1", dynamicData, "age", "hours_per_week")


with tab2:
    st.title("Data Visualizations for part 2📈")
    if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
        df = pd.read_csv('data.csv')
    else:
        st.warning("The 'data.csv' file is empty or does not exist yet.")
        st.stop()  

    vegaSpec = {
        "mark": "point",
        "encoding": {
            "x": {
                "field": "HoursPerWeek",
                "type": "quantitative",
            },
            "y": {
                "field": "Age",
                "type": "quantitative",
            },
            "color": {"field": "GameGenre", "type": "nominal"},
            "shape": {"field": "GameGenre", "type": "nominal"},
        },
    }
    st.subheader("Time Playe of Favorite Video Game Genre Considering Their Age")
    st.vega_lite_chart(
        df, vegaSpec, theme="streamlit", width="stretch"
    )

    all_genres = sorted(df["GameGenre"].unique())

    if "selected_genres" not in st.session_state:
        st.session_state.selected_genres = all_genres

    st.multiselect(
        label="Select Game Genres to Display:",
        options=all_genres,
        key="selected_genres",
    )

  
    filtered_df = df[df["GameGenre"].isin(st.session_state.selected_genres)]

    
    if not filtered_df.empty:
        filtered_df = filtered_df.sort_values(by="HoursPerWeek")

        st.subheader("Time Playe of Favorite Video Game Genre Considering Their Age")       
        fig = px.line(
            filtered_df,
            x="HoursPerWeek",
            y="Age",
            color="GameGenre",
            markers=True,
            category_orders={"GameGenre": all_genres},
            labels={"HoursPerWeek": "Hours Per Week"},
        )

        
        fig.update_layout(legend_title_text="All Game Genres")

        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Selected Genres Summary Metrics")
        showMetrics("p2", filtered_df, "Age", "HoursPerWeek")
    else:
        st.warning("Please select at least one genre to display the chart.")