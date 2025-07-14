import streamlit as st
from PIL import Image

st.set_page_config(page_title="Classificazione Suture", layout="wide")
st.title("Classifica la complessità delle suture")

# Lista immagini (in root)
immagini = [f"sutura_{i}.jpg" for i in range(1, 13)]

# Stato
if 'img_index' not in st.session_state:
    st.session_state.img_index = 0
if 'punteggi' not in st.session_state:
    st.session_state.punteggi = [None] * len(immagini)

# Layout principale
col_img, col_val = st.columns([3, 1])

# Mostra immagine corrente
with col_img:
    img_path = immagini[st.session_state.img_index]
    img = Image.open(img_path)
    st.image(img, width=500)  # Immagine più piccola, regola il valore a piacere

# Selezione punteggio
with col_val:
    st.subheader("Punteggio:")
    punteggio = st.radio(
        label="",
        options=list(range(1, 13)),
        index=(st.session_state.punteggi[st.session_state.img_index] - 1)
        if st.session_state.punteggi[st.session_state.img_index] else 0,
        key=f"radio_{st.session_state.img_index}"
    )
    st.session_state.punteggi[st.session_state.img_index] = punteggio

# Bottoni navigazione
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("◀️ Previous"):
        st.session_state.img_index = (st.session_state.img_index - 1) % len(immagini)
with col_next:
    if st.button("Next ▶️"):
        st.session_state.img_index = (st.session_state.img_index + 1) % len(immagini)

# Mostra punteggi assegnati
st.divider()
st.subheader("Valutazioni correnti:")
for i, score in enumerate(st.session_state.punteggi, start=1):
    st.write(f"Immagine {i}: {score if score else 'Non valutata'}")

