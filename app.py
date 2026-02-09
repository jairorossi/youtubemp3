import streamlit as st
import yt_dlp
import os
import re

# ================= STREAMLIT =================
st.set_page_config(
    page_title="HyperCam MP3 Strike",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 HyperCam MP3 - Ultimate Force")
st.write("Modo máximo de compatibilidade e fallback.")

url = st.text_input(
    "Link do vídeo:",
    placeholder="https://www.youtube.com/watch?v=..."
)

# ================= FUNÇÕES =================
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', "_", text)

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
                    # Cadeia máxima de fallback
                    'format': '(bv*+ba/best/bv*/ba/b)',

                    # Permite formatos não padrão
                    'allow_unplayable_formats': True,

                    # Saída
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',

                    # Cookies (se existirem)
                    'cookiefile': 'cookies.txt',

                    # TODOS os players possíveis
                    'extractor_args': {
                        'youtube': {
                            'player_client': [
                                'android',
                                'web',
                                'ios',
                                'mweb',
                                'tv_embedded'
                            ],
                        }
                    },

                    # Rede
                    'force_ipv4': True,
                    'nocheckcertificate': True,

                    # Headers genéricos
                    'headers': {
                        'User-Agent': (
                            'Mozilla/5.0 (Linux; Android 13) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/120.0.0.0 Mobile Safari/537.36'
                        )
                    },

                    # Pós-processamento
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],

                    'quiet': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)

                    if 'entries' in info:
                        info = info['entries'][0]

                    title = sanitize(info.get("title", "audio"))
                    filename = ydl.prepare_filename(info)
                    base, _ = os.path.splitext(filename)
                    mp3_file = base + ".mp3"

                    if os.path.exists(mp3_file):
                        with open(mp3_file, "rb") as f:
                            st.success(f"✅ Extraído: {title}")
                            st.download_button(
                                "⬇️ BAIXAR MP3",
                                f,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                        os.remove(mp3_file)
                    else:
                        st.error(
                            "Nenhum formato foi disponibilizado pelo YouTube "
                            "para este servidor."
                        )

        except Exception as e:
            st.error(f"Erro: {str(e)}")

st.caption("HyperCam Strike Dev")
