import streamlit as st
import pandas as pd
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

st.set_page_config(page_title="Kreatininprotokoll und GFR")

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

# Startseite mit den wichtigsten Informationen und dem Zugriff zu den weiteren Seiten    
st.title("Das wichtigste zu Kreatinin und GFR")

st.markdown(
        """
        ## Kreatinin:
        Kreatinin ist ein Abbauprodukt des Kreatinphosphats, das in der Muskulatur gebildet wird. 
        Es spielt eine Hauptrolle im Enegiestoffwechsel der Skelettmuskulatur, vor allem bei kurzzeitiger Muskelarbeit.  
        Die Konzentration von Kreatinin um Blut ist ein wichtiger Indikator für die Nierenfunktion. 
        Da die Nieren das Kreatinin aus dem Blut filtrieren und über den Urin ausscheiden.
        
        ### Referenzbereich:
        Je nach Alter und Geschlecht variiert die angemessene Kreatinin-Konzentration im Blut. 
        
        Frauen: 0.58 - 1.20 mg/dL
        
        Männer: 0.77 - 1.47 mg/dL
    
        Ihre Werte sollten Sie am Besten noch mit Ihrem Hausarzt besprechen.
    
        ## Glomeruläre Filtrationsrate:
        Die glomeruläre Filtrationsrate (GFR) ist der wichtigste Parameter zur Abschätzung der Nierenfunktion, 
        da sie anzeigt, wie gut die Nieren das Blut filtern und Abfallprodukte aus dem Körper entfernen.
        Zu hohe Kreatininwerte können auf eine Nierenschwäche, Verlertzung der Muskulatur, Muskeldystrophie
        oder eine Entzündung der Haut und Muskulatur hindeuten. 
        Zu niedrige GFR-Werte weisen auf eine Nierenschwäche hin bis zu einer Niereninsuffizienz.
        Die Therapie einer Niereninsuffizienz erfolgt mit einer Dialyse (Reinigung des Blutes) oder einer Spenderniere.
        
        ### Referenzbereich:
        Das Alter, Hautfarbe und Geschlecht können eine Rolle spielen, da sie alle Einfluss auf die Muskelmasse haben.
        Die Muskelmasse nimmt im Allgemeinen mit dem Alter ab, deswegen kann die GFR bei älteren Menschen niedriger sein.
        Männer haben mehr Muskelmasse als Frauen, was wiederum bedeutet, dass die GFR im Allgemeinen bei Männern höher ist.
        Menschen mit dunkler Haut haben höhere Muskelmasse als Menschen mit heller Haut, was wiederum dazu führt dass sie höhere Werte haben.
        
        Der normale GFR liegt bei ca. 90 - 120 mL/min, jedoch nimmt dieser ab dem 40. Lebensjahr um etwa 1 mL/min pro Jahr altersbedingt ab.
    
        👈 Über die Sidebar gelangen Sie zum Kreatinin-Protokoll und zum GFR-Rechner!
    """
    )
