import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="HyperCam MP3 Strike", page_icon="🎵")

st.title("🎵 HyperCam MP3 - Force Mode")
st.write("Tentativa de extração bruta para contornar bloqueio de formato.")

url = st.text_input("Link do vídeo:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("FORÇAR EXTRAÇÃO"):
    if url:
        try:
            with st.spinner("Bypassing YouTube Constraints..."):
                output_dir = "downloads"
                if not os.path.exists(output_dir): os.makedirs(output_dir)

                ydl_opts = {
                    # O segredo: Não pedimos 'bestaudio'. Pedimos 'best' (qualquer coisa com vídeo)
                    # O FFmpeg vai arrancar o áudio depois. Isso pula o erro de 'format not available'.
                    'format': 'best', 
                    'cookiefile': 'cookies.txt',
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    },
                    'nocheckcertificate': True,
                    'quiet': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if info:
                        # Pega o caminho do arquivo independente da extensão
                        filename = ydl.prepare_filename(info)
                        base, _ = os.path.splitext(filename)
                        final_mp3 = base + ".mp3"

                        if os.path.exists(final_mp3):
                            with open(final_mp3, "rb") as f:
                                st.success(f"✅ Extraído: {info['title']}")
                                st.download_button("BAIXAR MP3", f, file_name=f"{info['title']}.mp3")
                            os.remove(final_mp3)
                        else:
                            st.error("O download foi feito, mas o FFmpeg falhou na conversão. Verifique o packages.txt")
                    else:
                        st.error("YouTube bloqueou todos os formatos para este servidor.")

        except Exception as e:
            st.error(f"Erro: {str(e)}")
    else:
        st.warning("Insira o link.")

st.caption("HyperCam Strike Dev")
