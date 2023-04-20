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
        # Datensatz mit einem Element zurückgeben
        data = []
    return data
        
def calculate_gfr(age: int, SCr: float, female: bool, darkskinned: bool) -> float:
    """
    CKD-EPI-Formel: https://en.wikipedia.org/wiki/Glomerular_filtration_rate & https://flexikon.doccheck.com/de/CKD-EPI-Formel
    """
    
    if (female == False and darkskinned == False):
        if (SCr <= 0.9):
            eGFR = 141 * (SCr/0.9)**-0.411 * 0.993**age
        else:
            eGFR = 141 * (SCr/0.9)**-1.209 * 0.993**age    

    if (female == True and darkskinned == False):
        if (SCr <= 0.7):
            eGFR = 144 * (SCr/0.7)**-0.329 * 0.993**age
        else:
            eGFR = 144 * (SCr/0.7)**-1.209 * 0.993**age

    if (female == False and darkskinned == True):
        if (SCr <= 0.9):
            eGFR = 163 * (SCr/0.9)**-0.411 * 0.993**age
        else:
            eGFR = 163 * (SCr/0.9)**-1.209 * 0.993**age

    if (female == True and darkskinned == True):
        if (SCr <= 0.7):
            eGFR = 166 * (SCr/0.7)**-0.329 * 0.993**age
        else:
            eGFR = 166 * (SCr/0.7)**-1.209 * 0.993**age
    
    return round(eGFR, 2)

st.set_page_config(page_title="GFR", page_icon="📈")

st.markdown("# 📈 GFR")
st.write(
    """
    Berechnung der GFR
    """
)

# Daten aus Datei laden
data = load_data()

# Seite aufbauen
age = st.number_input("Alter (in Jahren)", min_value=1, max_value=100, step=1, value=25)
gender = st.radio("Geschlecht (biologisch)", ['weiblich', 'mänlich'])
skin = st.radio("Hautfarbe", ['hell', 'dunkel'])

st.write(
    """
    Darstellung der GFR
    """
)

# Datenframes erzeugen
df = pd.DataFrame(data)

# Kreatinin herausholen
creatinin = df['Kreatinin in mg/dL'].to_numpy()

# Und GFR ausrechnen
gfr = []
for SCr in creatinin:
    gfr.append(calculate_gfr(age, SCr, gender == 'weiblich', skin == 'dunkel'))
    
# GFR als neue Spalte anhängen (das wird später als Liste angezeigt)
df['GFR in ml/min/1.73m²'] = gfr
# df = pd.DataFrame(df)

# Neues Dataframe für den Graphen vorbereiten und darstellen
df_chart = pd.DataFrame(df)
del df_chart['Kreatinin in mg/dL']
chart = st.line_chart(df_chart, 
                      x = 'Datum',
                      use_container_width = True)

# Liste darstellen
st.dataframe(df, use_container_width=True)
    