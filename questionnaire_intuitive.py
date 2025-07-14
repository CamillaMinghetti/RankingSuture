import streamlit as st
from PIL import Image

st.set_page_config(page_title="Ranking of sutures by complexity", layout="wide")

if 'started' not in st.session_state:
    st.session_state.started = False
if 'finished' not in st.session_state:
    st.session_state.finished = False

if not st.session_state.started:
    st.title("Welcome to the Suture Complexity Ranking")
    st.write("""
    Please classify the sutures based on their level of complexity,  
    assigning a rank from 1 to 12, where **1** is the simplest suture and **12** the most complex.
    """)
    if st.button("Start"):
        st.session_state.started = True
        st.session_state.img_index = 0
        st.session_state.punteggi = [None] * 12

elif not st.session_state.finished:
    st.title("Classify the complexity of sutures")

    immagini = [f"sutura_{i}.jpg" for i in range(1, 13)]

    if 'img_index' not in st.session_state:
        st.session_state.img_index = 0
    if 'punteggi' not in st.session_state:
        st.session_state.punteggi = [None] * len(immagini)

    col_img, col_val = st.columns([3, 1])

    with col_img:
        img_path = immagini[st.session_state.img_index]
        img = Image.open(img_path)
        st.image(img, width=500)

    with col_val:
        st.subheader(f"Ranking for suture #{st.session_state.img_index + 1}:")

        current_score = st.session_state.punteggi[st.session_state.img_index]
        options = list(range(1, 13))
        default_index = options.index(current_score) if current_score in options else 0

        # key unica per ogni immagine
        key_radio = f"rank_selector_{st.session_state.img_index}"

        selected = st.radio(
            label="Select the rank:",
            options=options,
            index=default_index,
            key=key_radio
        )

        # aggiorna solo se cambia
        if selected != current_score:
            st.session_state.punteggi[st.session_state.img_index] = selected

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("◀️ Previous"):
            st.session_state.img_index = (st.session_state.img_index - 1) % len(immagini)
    with col_next:
        if st.button("Next ▶️"):
            st.session_state.img_index = (st.session_state.img_index + 1) % len(immagini)

    st.divider()
    st.subheader("Current rankings:")
    for i, score in enumerate(st.session_state.punteggi, start=1):
        st.write(f"Suture {i}: {score if score else 'Not ranked yet'}")

    if st.button("Finish"):
        st.session_state.finished = True

else:
    st.title("Thank you for completing the ranking!")
    st.write("Your responses have been recorded.")
