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

st.write("Username:  ",st.session_state.username)
   
st.title("GFR")
st.markdown("# 📈 GFR")
st.write(
    """
    Berechnung der GFR
    """
)

# Daten aus Datei laden
data = load_key(api_key, bin_id, username)

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

# Neues Dataframe für den Graphen vorbereiten und darstellen
df_chart = pd.DataFrame(df)
#df_chart['Kreatinin in mg/dL']
chart = st.line_chart(df_chart, x = 'Datum', use_container_width = True)

# Liste darstellen
st.dataframe(df, use_container_width=True)
