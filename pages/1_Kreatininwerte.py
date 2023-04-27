import streamlit as st
import pandas as pd
import json
import requests

# JSON-Bin-Konfiguration
BIN_ID = "<BIN_ID>"
API_KEY = "<API_KEY>"
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"

# Funktion zum Laden der Daten
def load_data():
    headers = {"X-Master-Key": API_KEY}
    response = requests.get(JSONBIN_URL, headers=headers)

    if response.status_code == 200:
        data = response.json().get("record")
    else:
        data = []
    return data

# Funktion zum Speichern der Daten
def save_data(data):
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": API_KEY
    }
    payload = {"record": data}
    response = requests.put(JSONBIN_URL, json=payload, headers=headers)

    if response.status_code != 200:
        st.error("Fehler beim Speichern der Daten")

# Seite darstellen
st.set_page_config(page_title="Kreatinin Bestimmung", page_icon="📊")
st.markdown("# 📊 Kreatinin Bestimmung")
st.write("Auf dieser Seite können die Daten erfasst werden.")

# Daten aus JSON-Bin laden
data = load_data()

# Seite aufbauen
creatinine = st.number_input("Kreatinin (in mg/dL)", min_value=0.1, max_value=20.0, step=0.1, key="creatinine")
date = st.date_input("Datum", key="date")
creatinine_data = {"date": str(date), "value": creatinine}
save_button = st.button("Speichern")

# Sidebar
delete_all_button = st.sidebar.button("Alles löschen")

# Leere Zeile einfügen (Abstand zwischen Button und Graphen)
st.write("")

# Einen neuen Eintrag generieren, anhängen und in JSON-Bin schreiben
if save_button:
    new_entry = {
        "Datum": str(date), 
        "Kreatinin in mg/dL": creatinine
    }
    data.append(new_entry)
    save_data(data)

# Alle Datensätze löschen und in JSON-Bin speichern 
if delete_all_button:
    data = []
    save_data(data)

# Datenframe erzeugen und als Graphen anzeigen. X-Achse ist das Datum.
df = pd.DataFrame(data)
chart = st.line_chart(df, x="Datum", use_container_width=True)

# Alle Daten als Liste darstellen
st.dataframe(df, use_container_width=True)

