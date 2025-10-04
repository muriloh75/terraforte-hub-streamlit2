import streamlit as st
import json
import os
from urllib.parse import urlparse

CONFIG_PATH = "data/config.json"
if not os.path.exists(CONFIG_PATH):
    st.warning("Arquivo `data/config.json` não encontrado. Copie `data/config.json.example` para `data/config.json` e edite com seus links públicos.")
    if os.path.exists("data/config.json.example"):
        CONFIG_PATH = "data/config.json.example"

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except Exception as e:
    st.error(f"Falha ao carregar configuração: {e}")
    CONFIG = {"produtores": []}

def load_users():
    if st.secrets and "STREAMLIT_USERS" in st.secrets:
        try:
            return dict(st.secrets["STREAMLIT_USERS"])
        except Exception:
            return st.secrets["STREAMLIT_USERS"]
    return {"murilo": "1234", "tecnico1": "abc123", "clienteA": "aprovA"}

USERS = load_users()

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if username in USERS and USERS[username] == password:
            st.session_state["user"] = username
            st.experimental_rerun()
        else:
            st.sidebar.error("Usuário ou senha inválidos.")
    if st.session_state.get("user"):
        st.sidebar.success(f"Logado como {st.session_state['user']}")
        if st.sidebar.button("Sair"):
            del st.session_state["user"]
            st.experimental_rerun()

def user_allowed_produtores(username):
    if username == "murilo":
        return [p["name"] for p in CONFIG.get("produtores", [])]
    allowed = []
    if st.secrets and "STREAMLIT_ALLOWED" in st.secrets:
        allowed_map = st.secrets["STREAMLIT_ALLOWED"]
        allowed = allowed_map.get(username, [])
    return allowed

def get_produtor_obj(name):
    for p in CONFIG.get("produtores", []):
        if p.get("name") == name:
            return p
    return None

def make_download_link(url):
    return url

st.set_page_config(page_title="Hub Terra Forte", layout="centered")
st.title("🌾 Hub Terra Forte (Streamlit)")

if "user" not in st.session_state:
    login()
    st.stop()

user = st.session_state["user"]
st.sidebar.markdown(f"**Usuário:** {user}")

all_produtores = [p["name"] for p in CONFIG.get("produtores", [])]
allowed = user_allowed_produtores(user)
if allowed:
    produtores = [p for p in all_produtores if p in allowed]
else:
    produtores = all_produtores

if not produtores:
    st.warning("Nenhum produtor configurado para este usuário. Verifique `data/config.json` ou Secrets.")
    st.stop()

produtor = st.selectbox("Produtor", produtores)

prod_obj = get_produtor_obj(produtor)
fardos = prod_obj.get("fardos", []) if prod_obj else []
if not fardos:
    st.info("Nenhuma fazenda/safra encontrada para este produtor. Edite data/config.json.")
    st.stop()

fazenda_names = [f.get("fazenda") for f in fardos]
fazenda = st.selectbox("Fazenda", fazenda_names)
f_obj = next((x for x in fardos if x.get("fazenda") == fazenda), None)
safra = st.selectbox("Safra", [f_obj.get("safra")] if f_obj else ["-"])

st.write("---")
st.subheader("Arquivos disponíveis para download")
zips = f_obj.get("zips", []) if f_obj else []
if not zips:
    st.info("Nenhum ZIP configurado para essa fazenda/safra.")
else:
    for z in zips:
        name = z.get("name")
        url = z.get("url")
        col1, col2 = st.columns([6,2])
        col1.write(f"**{name}**")
        host = urlparse(url).netloc if url else ""
        col1.caption(host)
        if url:
            col2.markdown(f"[⬇️ Baixar]({url})")
        else:
            col2.write("—")
st.info("Observação: para que os downloads funcionem automaticamente, os links devem ser públicos (modo 'anyone with link' no OneDrive).")
