import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="HyperCam MP3 Strike", page_icon="🎵")

# Interface Estilo Modder
st.markdown("""
    <style>
    .main { background-color: #0b0d10; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #00ff41; color: black; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 8px; background-color: #1a1c23; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ HyperCam MP3 - Strike Mode")
st.write("Bypassing YouTube Protected Formats...")

url = st.text_input("Cole o link aqui:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("EXECUTAR DOWNLOAD"):
    if url:
        try:
            with st.spinner("Injetando Bypass e extraindo áudio..."):
                output_dir = "downloads"
                if not os.path.exists(output_dir): os.makedirs(output_dir)

                # ESTRATÉGIA DE CONTINGÊNCIA TOTAL
                ydl_opts = {
                    # 'best' garante que ele pegue QUALQUER coisa se o áudio falhar
                    'format': 'bestaudio/best', 
                    'cookiefile': 'cookies.txt',
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    },
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web', 'mweb'], # Tenta versão web mobile também
                        }
                    },
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'nocheckcertificate': True,
                    # Se o formato de áudio der erro, ele tenta baixar o vídeo e converter
                    'format_sort': ['res:480', 'ext:mp4:m4a'], 
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if not info:
                        st.error("YouTube bloqueou a requisição. Tente atualizar o cookies.txt.")
                    else:
                        # Pega o nome do arquivo independente da extensão original
                        base_path = os.path.join(output_dir, ydl.prepare_filename(info).rsplit('.', 1)[0])
                        final_filename = base_path + ".mp3"

                        if os.path.exists(final_filename):
                            with open(final_filename, "rb") as f:
                                st.success(f"✅ {info['title']} - Liberado!")
                                st.audio(f.read(), format="audio/mp3")
                                st.download_button("BAIXAR ARQUIVO MP3", f, file_name=f"{info['title']}.mp3")
                            os.remove(final_filename)
                        else:
                            st.error("Erro no Post-Processor: O FFmpeg não conseguiu converter o arquivo.")

        except Exception as e:
            # Se der o erro de formato de novo, tentamos uma última vez sem filtros
            st.error(f"Erro: {str(e)}")
            st.info("💡 Dica: Se o erro persistir, o YouTube marcou o IP do Streamlit. Tente um vídeo menos 'famoso' para testar.")
    else:
        st.warning("Insira o link.")

st.markdown("---")
st.caption("HyperCam Project | Smali & Python Developer")
