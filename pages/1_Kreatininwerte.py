import streamlit as st
import pandas as pd
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

DATA_FILE = "data.json"

# Funktion zum Laden der Standards aus einer JSON-Datei
# def load_key(api_key, bin_id, key, empty_value=[]):
 #   if os.path.isfile(DATA_FILE):
  #      with open(DATA_FILE, "r", encoding="utf-8") as file:
   #         data = json.load(file)
   # else:
    #    data = []
    #return data
    
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

# Funktion zum Speichern der Standards in einer JSON-Datei
#def save_key(api_key, bin_id, key, data):
 #   with open(DATA_FILE, "w", encoding="utf-8") as file:
  #      json.dump(data, file, indent=2, ensure_ascii=False)

# Seite darstellen
st.title("Kreatinin Bestimmung")
st.markdown("# 📊 Kreatinin Bestimmung")
st.write(
    """
    Auf dieser Seite können die Daten erfasst werden.
    """
)

# Daten aus Datei laden
data = load_key(api_key, bin_id, username)

# Seite aufbauen
creatinine = st.number_input("Kreatinin in in mg/dL", min_value=0.1, max_value=20.0, step=0.1, key="creatinine")
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
    save_key((api_key, bin_id, username, data)

# Alle Datensätze löschen und in Datei speichern 
if delete_all_button == True:
    data = []
    save_key(api_key, bin_id, username, data)
    
# Datenframe erzeugen und als Graphen anzeigen. X-Achse ist das Datum.
#df = pd.DataFrame(data)
#chart = st.line_chart(df, 
 #                     x = "Datum", 
  #                    use_container_width = True)
  
# Datenframe erzeugen und als Graphen anzeigen. X-Achse ist das Datum.
df = pd.DataFrame(data)
df.rename(columns={"Datum": "date", "Kreatinin in mg/dL": "creatinine"}, inplace=True)  # Spaltennamen anpassen
chart = st.line_chart(df, x="date", use_container_width=True)

# Alle Daten als Liste darstellen
#st.dataframe(df, use_container_width=True)
