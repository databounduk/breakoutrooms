import streamlit as st
import itertools as it
import random

# ------------------ Tab Title & Header ------------------ #

st.set_page_config(
    page_title="Breakout Rooms", initial_sidebar_state="auto",
)
st.title("Breakout Rooms - Prototype")

# ------------------ Markdowns ------------------ #

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

intro_streamlit_style = """
            <h4>Requirements and Recommendations:</h4>
            <li>
            Please provide at least 2 names/attendees.
            </li>
            <li>
            Each name needs to be on a new line, copy and paste a col from a spread sheet.
            </li>
            <li>
            Names must be unique.
            </li>
            <li>
            We do not recommend using this system recomendations for parties over 60.
            </li>
            <li>
            We suggest pressing on generate a few times to get the optimal arrangement
            </li>
            """
st.markdown(intro_streamlit_style, unsafe_allow_html=True)

# ------------------ Application Functions ------------------ #


def group_size_recommender(attendees_num):

    group_size_max = 2
    if attendees_num >= 12:
        group_size_max = 3
    if attendees_num >= 20:
        group_size_max = 4
    if attendees_num >= 30:
        group_size_max = 6

    return group_size_max


def session_recommender(group_size: int, attendees: list):

    chunked_data = generate_groups(group_size, attendees)

    needed_sessions = list(it.combinations(chunked_data, 2))

    session_num = len(needed_sessions) / 2
    if session_num <= 0:
        session_num = 1

    return int(session_num)


def generate_groups(group_size: int, attendees: list):

    chunked_data = [
        attendees[i : i + group_size] for i in range(0, len(attendees), group_size)
    ]

    if len(chunked_data[-1]) == 1:
        lone = chunked_data.pop()
        chunked_data[-1] += lone

    if len(chunked_data) % 2 != 0:
        last_group = chunked_data.pop()
        while last_group:
            for group in chunked_data:
                while last_group:
                    name = last_group.pop()
                    group.append(name)
                    break
                continue

    return chunked_data


def generate_sesisons(sessions: int, group_size: int, attendees: list):

    chunked_data = generate_groups(group_size, attendees)

    rooms = len(chunked_data) / 2
    needed_sessions = list(it.combinations(chunked_data, 2))
    sorted_sessions = {}

    for session in range(sessions):
        sorted_sessions[session] = {}
        picked = []
        for room in range(int(rooms)):
            random.shuffle(needed_sessions)
            for i, pick_session in enumerate(needed_sessions):
                next_sesion = False
                flatted_session = [name for names in pick_session for name in names]

                for name in flatted_session:
                    if name in set(picked):
                        next_sesion = True
                if not next_sesion:
                    picked += flatted_session
                    sorted_sessions[session][room] = flatted_session
                    needed_sessions.pop(i)
                    break
    filter_sessions = {i: session for i, session in sorted_sessions.items() if session}
    print(filter_sessions)
    return filter_sessions


# ------------------ User Input ------------------ #

attendees = st.text_area("Attendee Names").replace("\t", " ").strip().split("\n")

attendees = [
    attendee for attendee in attendees if attendee != ""
]  # filter for blank rows


# ------------------ Responsive Input ------------------ #

if attendees != "" and len(attendees) > 3:

    # Constant Variable Setting
    attendees_num = len(attendees)
    rec_group_size = group_size_recommender(attendees_num)
    rec_session_num = session_recommender(rec_group_size, attendees)

    # On Screen Responses
    responsive_attendees_num = f"You have {attendees_num} attendees"
    responsive_rec_group_size = f"Based on the number of attendees, we recommend a min group size of {rec_group_size}"
    responsive_rec_session = f"Based on this group size, you would require {rec_session_num} session for everyone to meet"
    st.text(responsive_attendees_num)
    st.text(responsive_rec_group_size)
    st.text(responsive_rec_session)

    # Setting the slider value
    group_size = st.slider(
        "Group Size", min_value=2, max_value=attendees_num, value=rec_group_size
    )
    num_sessions = st.slider(
        "Number of Sessions", min_value=2, max_value=12, value=rec_session_num
    )

else:
    group_size = st.slider("Group Size", min_value=2, value=2)
    num_sessions = st.slider("Number of Sessions", min_value=2, max_value=12, value=1)

# ------------------ Application Triggers ------------------ #

trigger = st.button("Generate Rooms")

if trigger:

    original_groups = generate_groups(group_size, attendees)
    planned_sessions: dict = generate_sesisons(num_sessions, group_size, attendees)

    cols = st.beta_columns(num_sessions + 1)
    cols[0].write("<h4><u>Original Groups</u></h4>", unsafe_allow_html=True)
    for i in range(len(original_groups)):
        cols[0].write(f"<b>Room {i+1}</b>", unsafe_allow_html=True)
        for name in original_groups[i]:
            cols[0].write(f"{name}")

    for i in planned_sessions.keys():
        session_number = i + 1
        session_rooms = planned_sessions[i]
        cols[session_number].write(
            f"<h4><u>Session {session_number}</u></h4>", unsafe_allow_html=True
        )
        for i, v in session_rooms.items():
            cols[session_number].write(f"<b>Room {i+1}</b>", unsafe_allow_html=True)
            for name in v:
                cols[session_number].write(f"{name}")

