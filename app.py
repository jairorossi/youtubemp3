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
    .stButton>button:hover { background-color: #144870; border: none; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 HyperCam MP3 Downloader")
st.write("Versão Final com Cookies e Burlar 403/Format Error")

# 3. Campos de Entrada
url = st.text_input("Cole o link do YouTube aqui:", placeholder="https://www.youtube.com/watch?v=...")

quality_map = {"128 kbps": "128", "192 kbps": "192", "320 kbps": "320"}
quality_choice = st.select_slider("Qualidade do Áudio", options=list(quality_map.keys()), value="192 kbps")

# 4. Lógica de Download
if st.button("GERAR DOWNLOAD MP3"):
    if url:
        try:
            with st.spinner("Conectando ao YouTube..."):
                output_dir = "downloads"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Opções Ultra-Robustas
                ydl_opts = {
                    'format': 'bestaudio/best', # Tenta o melhor áudio
                    'cookiefile': 'cookies.txt', # SEU ARQUIVO NO GITHUB
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web', 'android'], # Web primeiro para mais formatos
                        }
                    },
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality_map[quality_choice],
                    }],
                    'quiet': True,
                    'noplaylist': True,
                    'force_overwrites': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extração e Download
                    info = ydl.extract_info(url, download=True)
                    temp_filename = ydl.prepare_filename(info)
                    
                    # O FFmpeg sempre converte para .mp3 devido ao postprocessor
                    base, _ = os.path.splitext(temp_filename)
                    final_filename = base + ".mp3"

                # 5. Entrega do Arquivo
                if os.path.exists(final_filename):
                    with open(final_filename, "rb") as f:
                        st.success(f"✅ Pronto: {info['title']}")
                        st.audio(f.read(), format="audio/mp3")
                        st.download_button(
                            label="BAIXAR AGORA",
                            data=f,
                            file_name=f"{info['title']}.mp3",
                            mime="audio/mpeg"
                        )
                    
                    # Limpa o servidor para não travar o Streamlit
                    os.remove(final_filename)
                else:
                    st.error("Erro: O conversor não gerou o arquivo MP3.")

        except Exception as e:
            st.error(f"Erro ao processar: {str(e)}")
            st.info("💡 Se aparecer 'Format not available', tente outro vídeo para testar.")
    else:
        st.warning("Por favor, insira uma URL.")

st.markdown("---")
st.caption("Acesso Restrito - HyperCam Strike Project")
