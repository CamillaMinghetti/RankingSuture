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

    if 'punteggi' not in st.session_state:
        st.session_state.punteggi = [None] * len(immagini)

    options = [None] + list(range(1, 13))

    for row in range(4):
        cols = st.columns(3)
        for col_idx in range(3):
            idx = row * 3 + col_idx
            if idx < len(immagini):
                with cols[col_idx]:
                    img = Image.open(immagini[idx])
                    st.image(img, width=250)
                    selected = st.selectbox(
                        f"Rank for suture {idx+1}",
                        options=options,
                        format_func=lambda x: "Seleziona..." if x is None else str(x),
                        index=options.index(st.session_state.punteggi[idx]) if st.session_state.punteggi[idx] in options else 0,
                        key=f"rank_selector_{idx}"
                    )
                    if selected != st.session_state.punteggi[idx] and selected is not None:
                        st.session_state.punteggi[idx] = selected

    st.divider()
    st.subheader("Current rankings:")
    for i, score in enumerate(st.session_state.punteggi, start=1):
        st.write(f"Suture {i}: {score if score else 'Not ranked yet'}")

    if st.button("Finish"):
        st.session_state.finished = True

else:
    st.title("Thank you for completing the ranking!")
    st.write("Your responses have been recorded.")
