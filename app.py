import streamlit as st
import yt_dlp
import os

# Configuração da página
st.set_page_config(page_title="HyperCam MP3 Downloader", page_icon="🎵")

# Estilo personalizado para ficar com visual moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3em; 
        background-color: #1f6aa5; 
        color: white; 
        font-weight: bold; 
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 HyperCam MP3 Downloader")
st.write("Versão Web - Converta vídeos do YouTube usando sua conta (Cookies).")

# Campo de entrada da URL
url = st.text_input("URL do Vídeo:", placeholder="https://www.youtube.com/watch?v=...")

# Opções de qualidade
quality_map = {"128 kbps": "128", "192 kbps": "192", "320 kbps": "320"}
quality_choice = st.select_slider("Qualidade do Áudio", options=list(quality_map.keys()), value="192 kbps")

if st.button("GERAR DOWNLOAD"):
    if url:
        try:
            with st.spinner("Bypassing YouTube... Aguarde."):
                output_dir = "downloads"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Configurações com Cookies e Disfarce de Cliente
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'cookiefile': 'cookies.txt',  # Usa o arquivo que você subiu
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'ios', 'web'],
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
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extrai informações e faz o download
                    info = ydl.extract_info(url, download=True)
                    temp_filename = ydl.prepare_filename(info)
                    
                    # Garante que a extensão final seja .mp3 após o processamento do FFmpeg
                    base, _ = os.path.splitext(temp_filename)
                    final_filename = base + ".mp3"

                # Verifica se o arquivo existe e oferece para baixar
                if os.path.exists(final_filename):
                    with open(final_filename, "rb") as f:
                        st.success(f"✅ Sucesso: {info['title']}")
                        st.audio(f.read(), format="audio/mp3")
                        st.download_button(
                            label="CLIQUE PARA BAIXAR O MP3",
                            data=f,
                            file_name=f"{info['title']}.mp3",
                            mime="audio/mpeg"
                        )
                    
                    # Limpa o arquivo do servidor após o download
                    os.remove(final_filename)
                else:
                    st.error("Erro técnico: O arquivo MP3 não foi localizado após a conversão.")

        except Exception as e:
            st.error(f"Erro ao processar: {str(e)}")
            st.warning("Se o erro persistir, verifique se o seu arquivo cookies.txt está atualizado no GitHub.")
    else:
        st.warning("Por favor, cole um link válido.")

st.markdown("---")
st.caption("Uso privado - Desenvolvedor HyperCam")
