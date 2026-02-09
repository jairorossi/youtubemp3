import streamlit as st
import yt_dlp
import os
import re

# ================= CONFIG STREAMLIT =================
st.set_page_config(
    page_title="HyperCam MP3 Strike",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 HyperCam MP3 - Force Mode")
st.write("Extração forçada de áudio com fallback avançado.")

# ================= INPUT =================
url = st.text_input(
    "Link do vídeo:",
    placeholder="https://www.youtube.com/watch?v=..."
)

# ================= FUNÇÕES =================
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# ================= BOTÃO =================
if st.button("FORÇAR EXTRAÇÃO"):
    if not url:
        st.warning("Insira o link do vídeo.")
    else:
        try:
            with st.spinner("Processando mídia..."):

                output_dir = "downloads"
                os.makedirs(output_dir, exist_ok=True)

                ydl_opts = {
                    # Cadeia de fallback REAL
                    'format': '(bestvideo+bestaudio/best/bv*+ba/b)',

                    # Cookies (se existirem)
                    'cookiefile': 'cookies.txt',

                    # Saída
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',

                    # Força player Android (mais aceito)
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android'],
                        }
                    },

                    # IPv4 costuma passar onde IPv6 falha
                    'force_ipv4': True,

                    # Pós-processamento
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],

                    # Headers realistas
                    'headers': {
                        'User-Agent': (
                            'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/120.0.0.0 Mobile Safari/537.36'
                        )
                    },

                    'nocheckcertificate': True,
                    'quiet': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)

                    # Playlist safety
                    if 'entries' in info:
                        info = info['entries'][0]

                    title = sanitize_filename(info.get('title', 'audio'))
                    filename = ydl.prepare_filename(info)
                    base, _ = os.path.splitext(filename)
                    final_mp3 = base + ".mp3"

                    if os.path.exists(final_mp3):
                        with open(final_mp3, "rb") as f:
                            st.success(f"✅ Extraído: {title}")
                            st.download_button(
                                "⬇️ BAIXAR MP3",
                                f,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        os.remove(final_mp3)
                    else:
                        st.error(
                            "Download ocorreu, mas o FFmpeg falhou. "
                            "Verifique se o FFmpeg está disponível no ambiente."
                        )

        except Exception as e:
            st.error(f"Erro: {str(e)}")

st.caption("HyperCam Strike Dev")
