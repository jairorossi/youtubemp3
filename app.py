import streamlit as st
import yt_dlp
import os

# 1. Configuração da Página
st.set_page_config(page_title="HyperCam Strike MP3", page_icon="🎵")

# Estilo visual Dark
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #e63946; color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 HyperCam MP3 - Strike Mode")
st.write("Bypassing YouTube Signatures...")

url = st.text_input("Link do vídeo:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("FORÇAR DOWNLOAD"):
    if url:
        try:
            with st.spinner("Bypassing..."):
                output_dir = "downloads"
                if not os.path.exists(output_dir): os.makedirs(output_dir)

                # ESTRATÉGIA STRIKE:
                # Usamos o cliente 'ios' que costuma ter menos travas de assinatura
                # e removemos a exigência de 'bestaudio' para deixar o yt-dlp escolher
                ydl_opts = {
                    'format': 'ba/b', # Tenta áudio, se não der, pega o que tiver (vídeo+áudio)
                    'cookiefile': 'cookies.txt',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['ios'],
                            'skip': ['webpage', 'hls', 'dash'] # Pula protocolos que dão erro 403
                        }
                    },
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                    },
                    'nocheckcertificate': True,
                    'ignoreerrors': False,
                    'logtostderr': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Tenta extrair e baixar
                    info = ydl.extract_info(url, download=True)
                    if not info:
                        st.error("Erro: O YouTube recusou a conexão. Atualize seus cookies.")
                    else:
                        temp_filename = ydl.prepare_filename(info)
                        base, _ = os.path.splitext(temp_filename)
                        final_filename = base + ".mp3"

                        if os.path.exists(final_filename):
                            with open(final_filename, "rb") as f:
                                st.success("Download liberado!")
                                st.download_button("BAIXAR MP3 AGORA", f, file_name=f"{info['title']}.mp3")
                            os.remove(final_filename)
                        else:
                            # Se o arquivo não virou MP3, tentamos achar o arquivo original que baixou
                            st.error("O download ocorreu, mas a conversão falhou. Verifique o packages.txt.")

        except Exception as e:
            st.error(f"Erro de Conexão: {str(e)}")
            st.info("Dica de Modder: O YouTube bloqueou o IP do servidor. Tente novamente em 5 minutos ou atualize o arquivo cookies.txt.")
    else:
        st.warning("Insira a URL.")
