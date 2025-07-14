import streamlit as st
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Questionario Suture", layout="wide")

# Stato iniziale
if 'pagina' not in st.session_state:
    st.session_state.pagina = 0
if 'finished' not in st.session_state:
    st.session_state.finished = False

# Pagina 0: Ranking delle suture
if st.session_state.pagina == 0 and not st.session_state.finished:
    st.title("Classificazione della complessità delle suture")
    st.write("""
    Si prega di classificare le suture in base al loro livello di complessità,  
    assegnando un punteggio da 1 a 12, dove **1** è la sutura più semplice e **12** la più complessa.
    """)

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
                        f"Classifica la complessità per la sutura {idx+1}",
                        options=options,
                        format_func=lambda x: "Seleziona..." if x is None else str(x),
                        index=options.index(st.session_state.punteggi[idx]) if st.session_state.punteggi[idx] in options else 0,
                        key=f"rank_selector_{idx}"
                    )
                    if selected != st.session_state.punteggi[idx] and selected is not None:
                        st.session_state.punteggi[idx] = selected

    st.divider()
    st.subheader("Classifiche attuali:")
    for i, score in enumerate(st.session_state.punteggi, start=1):
        st.write(f"Sutura {i}: {score if score else 'Non ancora classificata'}")

    if st.button("Avanti"):
        st.session_state.pagina = 1

# Pagina 1: Spiegazione e introduzione
elif st.session_state.pagina == 1 and not st.session_state.finished:
    st.title("How do surgeons learn?")
    st.subheader("Toward personalized robotic-assisted laparoscopy training based on high-density EEG")
    st.write("""
    Gentilissimo Dottore,

    Nell’ambito di un progetto volto allo studio dell’attività corticale durante il training in laparoscopia robot-assistita e di come questa descriva l’expertise del chirurgo, Le chiediamo di compilare questo breve questionario della durata di circa 5 minuti. L’obiettivo è raccogliere il punto di vista di professionisti esperti come Lei su alcuni dei parametri che definiscono una sutura “ben eseguita”.

    Le informazioni raccolte saranno utilizzate per identificare gli indicatori più rilevanti ai fini di un’analisi oggettiva delle performance da utilizzare con l’obiettivo di valutare specializzandi o chirurghi all’inizio di un percorso di training in laparoscopia robot-assistita.
    """)

    if st.button("Avanti"):
        st.session_state.pagina = 2

# Pagina 2: Valutazione parametri
elif st.session_state.pagina == 2 and not st.session_state.finished:
    st.title("Valutazione dei parametri di una sutura")
    st.write("Indichi quanto ritiene importanti i seguenti parametri nella valutazione di una sutura (Scala da 1 = per niente importante a 10 = molto importante):")

    parametri = [
        ("Tempo di esecuzione della sutura", "Durata totale della procedura di sutura"),
        ("Accuratezza del punto di inserzione dell’ago", "Precisione del punto di ingresso e uscita dell’ago rispetto alla linea di sutura ideale"),
        ("Errori, ossia punti in cui l’ago non ha trapassato la pelle", "Errori di penetrazione: numero di tentativi incompleti o punti non eseguiti correttamente")
    ]
    if 'valutazioni' not in st.session_state:
        st.session_state.valutazioni = [None] * len(parametri)

    for i, (titolo, descrizione) in enumerate(parametri):
        st.write(f"**{titolo}**")
        st.caption(descrizione)
        selected = st.radio(
            "Importanza:",
            options=list(range(1, 11)),
            index=st.session_state.valutazioni[i] - 1 if st.session_state.valutazioni[i] else 0,
            key=f"parametro_{i}",
            horizontal=True
        )
        st.session_state.valutazioni[i] = selected

    if st.button("Invia e termina"):
        st.session_state.finished = True

def salva_su_google_sheet(punteggi, valutazioni):
    # Autenticazione
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenziali.json", scope)
    client = gspread.authorize(creds)

    # Apri il foglio
    sheet = client.open("Questionario Suture").sheet1

    # Calcola il prossimo soggetto
    records = sheet.get_all_records()
    soggetto = len(records) + 1

    # Prepara la riga
    row = [soggetto] + [p if p is not None else "" for p in punteggi] + [v if v is not None else "" for v in valutazioni]
    sheet.append_row(row)

# Pagina finale
if st.session_state.finished:
    st.title("Grazie per aver completato il questionario!")
    st.write("Le sue risposte sono state registrate.")

    # Salva su Google Sheet solo una volta
    if 'saved' not in st.session_state:
        salva_su_google_sheet(st.session_state.punteggi, st.session_state.valutazioni)
        st.session_state.saved = True
        st.success("Risposte salvate su Google Sheet!")
