import streamlit as st
import pandas as pd
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

DATA_FILE = "data.json"

# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]
# -------- user login --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()
data = load_key(api_key, bin_id, username)

st.write("Username:  ",st.session_state.username)

# Seite darstellen
st.markdown("# 📊 Kreatinin Bestimmung")
st.write(
    """
    Die Häufigkeit der Kreatinin-Bestimmung muss mit dem behandelten Arzt besprochen werden. 
    Auf dieser Seite können die Daten erfasst werden. 
    """
)

# Daten aus Datei laden
data = load_key(api_key, bin_id, username)

if data == {}:
 data = []

# Seite aufbauen
creatinine = st.number_input("Kreatinin in in mg/dL", min_value=0.1, max_value=20.0, step=0.1, key="creatinine")
date = st.date_input("Datum", key="date")
creatinine_data = {"date": str(date), "value": creatinine}
st.write("Bitte drücken sie auf den Button um die Daten anzuzeigen!")
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
    save_key(api_key, bin_id, username, data)
             
        
# Alle Datensätze löschen und in Datei speichern 
if delete_all_button == True:
    data = []
    save_key(api_key, bin_id, username, data)
   
# Datenframe erzeugen und als Graphen anzeigen. X-Achse ist das Datum.
df = pd.DataFrame(data)
chart = st.line_chart(df, 
                      x = "Datum", 
                      use_container_width = True)

# Alle Daten als Liste darstellen
st.dataframe(df, use_container_width=True)
