# Hub Terra Forte — Streamlit edition

Este template publica um painel no Streamlit com:
- **Login** (usuário e senha via *Secrets* do Streamlit)
- **Seleção** de Produtor → Fazenda → Safra
- **Download real** de ZIPs a partir de **links públicos** (OneDrive/HTTP)

## Como usar

1. Crie um repositório no seu GitHub e envie estes arquivos.
2. No Streamlit Cloud (https://share.streamlit.io), clique **New app** e aponte para o repositório.
3. Em **Settings → Secrets**, configure:
   ```
   STREAMLIT_USERS = {"murilo":"1234","tecnico1":"abc123"}
   STREAMLIT_ALLOWED = {"tecnico1":["Volmar","FuturAgro"], "clienteA":["Cliente_A"]}
   ```
4. Edite `data/config.json` (copie de `data/config.json.example`) com seus links de arquivos ZIP.
5. Deploy — pronto, URL pública com HTTPS.

## Links públicos do OneDrive
No OneDrive Web:
1. Botão direito no arquivo ZIP → **Compartilhar (Share)**
2. Configure **Qualquer pessoa com o link** (*Anyone with the link*)
3. Copie a URL e cole em `data/config.json`

> Para acesso privado (sem links públicos), é possível integrar via Microsoft Graph + OAuth — peça o guia da versão avançada.
