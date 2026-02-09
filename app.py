import streamlit as st
import yt_dlp
import os

# Configuração da página
st.set_page_config(page_title="HyperCam Downloader", page_icon="🎵")

st.title("🎵 HyperCam MP3 Downloader")
st.markdown("Converta vídeos do YouTube para MP3 direto no navegador.")

# Campo de entrada da URL
url = st.text_input("Cole a URL do vídeo aqui:", placeholder="https://www.youtube.com/watch?v=...")

# Opções de qualidade
quality = st.selectbox("Qualidade do Áudio", ["128 kbps", "192 kbps", "320 kbps"])

if st.button("Preparar Download"):
    if url:
        try:
            with st.spinner("Processando o áudio..."):
                # Pasta temporária para o download no servidor/PC
                output_dir = "downloads"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality.split(' ')[0],
                    }],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                    
                    # Nome amigável para o arquivo
                    file_name_display = f"{info['title']}.mp3"

                # Lendo o arquivo para oferecer o download no navegador
                with open(filename, "rb") as file:
                    st.success("Pronto!")
                    st.audio(file.read(), format="audio/mp3")
                    st.download_button(
                        label="CLIQUE AQUI PARA BAIXAR MP3",
                        data=file,
                        file_name=file_name_display,
                        mime="audio/mpeg"
                    )
                
                # Opcional: remover arquivo local após processar
                os.remove(filename)

        except Exception as e:
            st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Por favor, insira uma URL válida.")

st.info("Nota: O processamento é feito no servidor onde o script está rodando.")