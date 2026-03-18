import streamlit as st
import google.generativeai as genai

# KONFIGURACJA
API_KEY = "AIzaSyDTx6939mygMgJm4B-pwIkB30LQRy_WtzQ"
genai.configure(api_key=API_KEY)

# INSTRUKCJE SYSTEMOWE - EKSPERT NGO I FUNDUSZY
system_instruction = (
    "Jesteś elitarnym Asystentem Prawno-Społecznym Jerzego Kamieńskiego. "
    "Twoją specjalnością są organizacje pozarządowe (NGO), spółdzielnie socjalne oraz fundusze unijne na rok 2026. "
    "Gdy Jerzy pyta o konkursy, wymieniaj konkretne programy (np. FERS, FEnIŚ, programy regionalne) "
    "i kieruj go do portalu mapadotacji.gov.pl lub funduszeeuropejskie.gov.pl. "
    "Pomagaj w sprawach KRS, tłumacząc jak sprawdzić status organizacji i złożyć wniosek przez Portal Rejestrów Sądowych."
)

@st.cache_resource
def load_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(model_name=m.name)
    return None

model = load_model()

# WYGLĄD
st.set_page_config(page_title="Centrum Jerzego Kamieńskiego", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .stButton>button { border-radius: 8px; font-weight: bold; background-color: #003366; color: white; width: 100%; }
    .nav-link { 
        display: block; padding: 10px; margin: 5px 0; background-color: #0056b3; 
        color: white !important; text-align: center; border-radius: 8px; text-decoration: none; font-size: 14px;
    }
    .krs-link { background-color: #6c757d !important; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: #666; font-size: 12px; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("Panel Zarządzania")
    st.markdown(f"Witaj, **Jerzy Kamieński**")
    st.divider()
    
    # SEKCJA: KRS I REJESTRY
    st.subheader("🏢 KRS i Rejestry Sądowe")
    st.markdown('<a href="https://prs.ms.gov.pl/" target="_blank" class="nav-link krs-link">Portal Rejestrów Sądowych (PRS) 🏛️</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://ekrs.ms.gov.pl/pdi/searcher" target="_blank" class="nav-link krs-link">Wyszukiwarka Podmiotów KRS 🔍</a>', unsafe_allow_html=True)
    
    st.divider()
    
    # SEKCJA: KONKURSY UNIJNE
    st.subheader("🇪🇺 Fundusze Unijne 2026")
    st.markdown('<a href="https://www.funduszeeuropejskie.gov.pl/wyszukiwarka/" target="_blank" class="nav-link" style="background-color: #e67e22 !important;">Wyszukiwarka Konkursów 🎯</a>', unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("🔍 Szukaj Dotacji/Wniosku")
    query = st.text_input("Wpisz temat (np. ekologia, seniorzy):")
    if query:
        if st.button("Znajdź konkurs/instrukcję"):
            st.session_state.user_query = f"Znajdź aktualne konkursy unijne lub granty na temat: {query}. Podaj gdzie szukać dokumentacji."

    st.divider()
    st.write("© 2026 **Jerzy Kamieński**")

st.title("⚖️ System Wspierania Prawno-Społecznego i NGO")

# CZAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

chat_input = st.chat_input("Zadaj pytanie o NGO, KRS lub fundusze...")

final_query = chat_input if chat_input else st.session_state.get("user_query")
if "user_query" in st.session_state: del st.session_state.user_query

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.markdown(final_query)

    with st.chat_message("assistant"):
        if model:
            try:
                full_prompt = f"{system_instruction}\n\nZapytanie: {final_query}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")

st.markdown('<div class="footer">Autor: Jerzy Kamieński | © 2026</div>', unsafe_allow_html=True)
