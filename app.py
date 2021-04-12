import streamlit as st
import itertools as it

# ------------------ Tab Title & Header ------------------ #

st.set_page_config(
    page_title="Breakout Rooms", initial_sidebar_state="auto",
)
st.title("Breakout Rooms")

# ------------------ Markdowns ------------------ #

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

intro_streamlit_style = """
            <p>
            Please provide at least 2 names/attendees.
            </p>
            <p>
            Each name needs to be on a new line, copy and paste a col from a spread sheet.
            </p>
            <p>
            Names must be unique.
            </p>
            <p>
            We do not recommend using this system recomendations for parties over 60.
            </p>
            <p>
            A csv will be avaiable for the pre-assigned groups that relate to the starting groups.
            </p>
            """
st.markdown(intro_streamlit_style, unsafe_allow_html=True)

# ------------------ Application Functions ------------------ #


def generate_groups(group_size: int, attendees: list):

    chunked_data = [
        attendees[i : i + group_size] for i in range(0, len(attendees), group_size)
    ]

    return chunked_data


def generate_sesisons(sessions: int, group_size: int, attendees: list):

    chunked_data = [
        attendees[i : i + group_size] for i in range(0, len(attendees), group_size)
    ]

    rooms = len(chunked_data) / 2
    needed_sessions = list(it.combinations(chunked_data, 2))
    sorted_sessions = {}

    for session in range(sessions):
        print(f"Session {session}")
        sorted_sessions[session] = {}
        picked = []
        for room in range(int(rooms)):

            for i, pick_session in enumerate(needed_sessions):
                next_sesion = False
                flatted_session = [name for names in pick_session for name in names]

                for name in flatted_session:
                    if name in set(picked):
                        next_sesion = True
                if not next_sesion:
                    print(f" {room} {pick_session}")
                    picked += flatted_session
                    sorted_sessions[session][room] = flatted_session
                    needed_sessions.pop(i)
                    break
    return sorted_sessions


def session_recommender(group_size: int, attendees: list):

    chunked_data = [
        attendees[i : i + group_size] for i in range(0, len(attendees), group_size)
    ]

    return len(chunked_data) - 1


def group_size_recommender(attendees_num, min_group_size=2):

    if attendees_num / min_group_size >= 1:
        group_size_max = 2
    if attendees_num / min_group_size >= 8:
        group_size_max = 4
    if attendees_num / min_group_size >= 14:
        group_size_max = 6
    if attendees_num / min_group_size >= 24:
        group_size_max = 8
    if attendees_num / min_group_size >= 30:
        group_size_max = 12
    if attendees_num / min_group_size >= 40:
        group_size_max = 16

    if attendees_num % 2 != 0:
        group_size_max += 1

    return group_size_max


# ------------------ User Input ------------------ #

attendees = st.text_area("Attendee Names").replace("\t", " ").strip().split("\n")

attendees = [
    attendee for attendee in attendees if attendee != ""
]  # filter for blank rows


# ------------------ Responsive Input ------------------ #

if attendees != "" and len(attendees) > 3:
    attendees_num = len(attendees)
    rec_group_size = group_size_recommender(attendees_num)
    rec_session_num = session_recommender(rec_group_size, attendees)

    responsive_attendees_num = f"You have {attendees_num} attendees"
    responsive_rec_group_size = f"Based on the number of attendees, we recommend a max group size of {rec_group_size}"
    responsive_rec_session = f"Based on this group size, you would require {rec_session_num} session for everyone to meet"

    st.text(responsive_attendees_num)
    st.text(responsive_rec_group_size)
    st.text(responsive_rec_session)

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
    # st.text(original_groups)
    # st.text(planned_sessions)

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

