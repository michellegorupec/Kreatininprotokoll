# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:30:05 2023

@author: Michelle & Katja
"""

import streamlit as st
import pandas as pd
import json, os

DATA_FILE = "data.json"

# Funktion zum Laden der Standards aus einer JSON-Datei
def load_data():
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []
    return data

# Funktion zum Speichern der Standards in einer JSON-Datei
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# Seite darstellen
st.set_page_config(page_title="Kreatinin Bestimmung", page_icon="📊")
st.markdown("# 📊 Kreatinin Bestimmung")
st.write(
    """
    Auf dieser Seite können die Daten erfasst werden.
    """
)

# Daten aus Datei laden
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

# Einen neuen Eintrag generieren, anhängen und in Datei schreiben
if save_button == True:
    new_entry = {
        "Datum": str(date), 
        "Kreatinin in mg/dL": creatinine
        }
    data.append(new_entry)
    save_data(data)

# Alle Datensätze löschen und in Datei speichern 
if delete_all_button == True:
    data = []
    save_data(data)
    
# Datenframe erzeugen und als Graphen anzeigen. X-Achse ist das Datum.
df = pd.DataFrame(data)
chart = st.line_chart(df, 
                      x = 'Datum', 
                      use_container_width = True)

# Alle Daten als Liste darstellen
st.dataframe(df, use_container_width=True)
    


