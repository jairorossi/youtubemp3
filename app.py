import streamlit as st
import yt_dlp
import os

# 1. Configuração da Página
st.set_page_config(page_title="HyperCam MP3 Downloader", page_icon="🎵", layout="centered")

# 2. Estilo Visual (Dark Mode Moderno)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        background-color: #1f6aa5; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #144870; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 HyperCam MP3 Downloader")
st.write("Versão de Contingência - Forçando busca de áudio")

# 3. Campos de Entrada
url = st.text_input("Cole o link do YouTube aqui:", placeholder="https://www.youtube.com/watch?v=...")

quality_map = {"128 kbps": "128", "192 kbps": "192", "320 kbps": "320"}
quality_choice = st.select_slider("Qualidade do Áudio", options=list(quality_map.keys()), value="192 kbps")

# 4. Lógica de Download
if st.button("GERAR DOWNLOAD MP3"):
    if url:
        try:
            with st.spinner("Buscando qualquer formato de áudio disponível..."):
                output_dir = "downloads"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Opções de Contingência: 
                # Se não achar o 'bestaudio', ele pega o vídeo com áudio e extrai
                ydl_opts = {
                    'format': 'bestaudio/best', 
                    'cookiefile': 'cookies.txt',
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                    },
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web'], # 'web' é o mais confiável para formatos comuns
                        }
                    },
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality_map[quality_choice],
                    }],
                    'quiet': False, # Deixamos False para você ver o log se der erro no Streamlit
                    'noplaylist': True,
                    # Se o formato pedido falhar, ele tenta o próximo melhor automaticamente
                    'ignoreerrors': True, 
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if info is None:
                        st.error("Não foi possível encontrar um formato compatível. O YouTube bloqueou este vídeo específico.")
                    else:
                        temp_filename = ydl.prepare_filename(info)
                        base, _ = os.path.splitext(temp_filename)
                        final_filename = base + ".mp3"

                        # 5. Entrega do Arquivo
                        if os.path.exists(final_filename):
                            with open(final_filename, "rb") as f:
                                st.success(f"✅ Pronto: {info.get('title', 'Audio')}")
                                st.audio(f.read(), format="audio/mp3")
                                st.download_button(
                                    label="BAIXAR AGORA",
                                    data=f,
                                    file_name=f"{info.get('title', 'audio')}.mp3",
                                    mime="audio/mpeg"
                                )
                            os.remove(final_filename)
                        else:
                            st.error("Erro na conversão: O FFmpeg não conseguiu gerar o MP3.")

        except Exception as e:
            st.error(f"Erro crítico: {str(e)}")
    else:
        st.warning("Insira uma URL.")

st.markdown("---")
st.caption("HyperCam Project - Bypass Mode")
