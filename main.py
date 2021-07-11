# ------------------ Created By Databound Limited ------------------ #

"""
Developed under an MIT License
"""

import pandas as pd
import base64
import streamlit as st

# import streamlit.components.v1 as components
import itertools as it
import random

#  Strict Typing
from typing import List

# Logging
from icecream import ic


# ------------------ Tab Title & Header ------------------ #

st.set_page_config(page_title="Breakout Rooms", initial_sidebar_state="auto")


# ------------------ Markdowns ------------------ #

# Adding the logo
st.image("static/images/app_logo.png", use_column_width=True)

st.title("Breakout Rooms Generator")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with open("static/html/intro.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# ------------------ Constants ------------------ #


# ------------------ Application Functions ------------------ #


def create_unique_sessions(attendees: List[list], room_size: int) -> dict:
    """
    Function to generate a possible number of scenrios for sessions everyone to meet each other. 

    Parameters:
        attendees : List - A list of the attendees for the session
        room_size : int - A numerical value for the number of people per room
    Return:
        scenarios : dict - A dict of possible scenarios, key is the number of sessions and the value is attendees in session

    """

    possible_sessions = list(it.combinations(attendees, room_size))
    scenarios = {}

    for i in range(1000):

        random.shuffle(possible_sessions)
        particpents = attendees[:]
        choosen_sessions = []
        for session in possible_sessions:
            if not particpents:
                break

            for person in session:
                try:
                    particpents.remove(person)
                except:
                    pass

            choosen_sessions.append(session)

            if not particpents:
                break

        scenarios[len(choosen_sessions)] = choosen_sessions

    return scenarios


def parse_attendees(attendees_raw: str, delimiter) -> List:

    if delimiter == "space":
        return [attendee.strip() for attendee in attendees_raw.strip().split(" ")]
    elif delimiter == "tab":
        return [attendee.strip() for attendee in attendees_raw.strip().split("\t")]
    elif delimiter == "new line":
        return [attendee.strip() for attendee in attendees_raw.strip().split("\n")]


def generate_dataframe(sessions):

    table = {}
    for index, session in enumerate(sessions):
        table[f"Room {index + 1}"] = session

    return pd.DataFrame(table)


def get_table_download_link_csv(df):
    csv = df.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"> <a href="data:file/csv;base64,{b64}" class="btn btn-outline-secondary" download="breakout.csv" target="_blank">Download csv file</a>'
    return href


# ------------------ User Input ------------------ #

delimiters = ["space", "tab", "new line"]

attendees = st.text_area("A list of attendees")

delimiter = st.selectbox(
    "Please select the delimiter for your list of attendees", delimiters, index=2
)

room_size = int(st.number_input("Max Room Size", min_value=1, value=2))

# ------------------ Application Triggers ------------------ #

trigger = st.button("Generate Rooms")

attendees_parsed = parse_attendees(attendees, delimiter)
number_of_attendees = len(attendees_parsed)

if number_of_attendees < room_size:
    st.text("Room size is greater that the number of attendees")

elif trigger and attendees != "" and attendees != " ":

    sessions = create_unique_sessions(attendees_parsed, room_size)

    lowest_sessions = min(sessions.keys())
    chosen_session = sessions[lowest_sessions]

    cols = st.beta_columns(lowest_sessions)

    for i in range(lowest_sessions):
        room_num = i + 1
        cols[i].write(f"<h4><u>Room {room_num}</u></h4>", unsafe_allow_html=True)
        for name in chosen_session[i]:
            cols[i].write(f"<b>{name}</b>", unsafe_allow_html=True)

    df = generate_dataframe(chosen_session)

    st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)

# ------------------ Footer ------------------ #

with open("static/html/footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
