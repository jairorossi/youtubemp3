import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="HyperCam MP3 Ultra", page_icon="🎵")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1f6aa5; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 HyperCam MP3 - Ultra Bypass")
st.write("Tentando extração via YouTube Music Client...")

url = st.text_input("URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("DOWNLOAD FORÇADO"):
    if url:
        try:
            with st.spinner("Bypass em execução..."):
                output_dir = "downloads"
                if not os.path.exists(output_dir): os.makedirs(output_dir)

                ydl_opts = {
                    # Mudamos para pegar qualquer áudio que o player do YT Music entregaria
                    'format': 'bestaudio/best',
                    'cookiefile': 'cookies.txt',
                    'extractor_args': {
                        'youtube': {
                            # O segredo: usar o cliente de TV ou Music que tem assinaturas mais simples
                            'player_client': ['tv', 'web', 'mweb'],
                            'player_skip': ['webpage', 'configs'],
                        }
                    },
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'nocheckcertificate': True,
                    'quiet': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if info:
                        base = os.path.join(output_dir, ydl.prepare_filename(info).rsplit('.', 1)[0])
                        final_file = base + ".mp3"

                        if os.path.exists(final_file):
                            with open(final_file, "rb") as f:
                                st.success("✅ Extraído com sucesso!")
                                st.download_button("BAIXAR MP3", f, file_name=f"{info['title']}.mp3")
                            os.remove(final_file)
                    else:
                        st.error("O YouTube ainda está bloqueando. O IP do servidor Streamlit pode estar na 'black list'.")

        except Exception as e:
            st.error(f"Erro: {str(e)}")
    else:
        st.warning("Insira o link.")

st.caption("HyperCam Strike - Dev Jairo Rossi")
