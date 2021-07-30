# ------------------ Created By Databound Limited ------------------ #

"""
Developed under an MIT License
"""

import pandas as pd
import base64
import streamlit as st

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


def create_session(attendees: List[list], room_size: int) -> dict:
    """
    Function to generate a possible number of scenrios for sessions everyone to meet each other. 

    Parameters:
        attendees : List - A list of the attendees for the session
        room_size : int - A numerical value for the number of people per room
    Return:
        scenarios : dict - A dict of possible scenarios, key is the number of sessions and the value is attendees in session

    """
    randomised_attendees = attendees[:]
    random.shuffle(randomised_attendees)
    session = {}
    room_num = 1
    while bool(randomised_attendees) is True:
        room_attendess = []
        for i in range(room_size):
            if bool(randomised_attendees) is False:
                room_attendess.append("")
            else:
                room_attendess.append(randomised_attendees.pop())
        session[f"Room {room_num}"] = room_attendess
        room_num += 1

    return session


def parse_attendees(attendees_raw: str, delimiter) -> List:

    if delimiter == "space":
        return [attendee.strip() for attendee in attendees_raw.strip().split(" ")]
    elif delimiter == "tab":
        return [attendee.strip() for attendee in attendees_raw.strip().split("\t")]
    elif delimiter == "new line":
        return [attendee.strip() for attendee in attendees_raw.strip().split("\n")]


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

room_size = int(
    st.number_input(
        "Max People Per Room", min_value=1, max_value=len(attendees), value=2
    )
)

# ------------------ Application Triggers ------------------ #

trigger = st.button("Generate Rooms")

attendees_parsed = parse_attendees(attendees, delimiter)
number_of_attendees = len(attendees_parsed)

if trigger and attendees != "" and attendees != " ":

    session = create_session(attendees_parsed, room_size)

    df_sessions = pd.DataFrame(session)

    if len(session) < 11 and number_of_attendees < 100:
        st.table(session)

    st.markdown(get_table_download_link_csv(df_sessions), unsafe_allow_html=True)

# ------------------ Footer ------------------ #

with open("static/html/footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
