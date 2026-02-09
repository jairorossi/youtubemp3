import streamlit as st
import yt_dlp
import os
import shutil

# Configuração da página e estilo
st.set_page_config(page_title="HyperCam MP3", page_icon="🎵", layout="centered")

# CSS para deixar a interface com a cara dos seus projetos (Escuro/Moderno)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1f6aa5; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 HyperCam MP3 Downloader")
st.write("Versão Web para amigos - Converta vídeos para MP3 online.")

# Entrada da URL
url = st.text_input("", placeholder="Cole o link do YouTube aqui...")

# Qualidade do áudio
quality_map = {"Baixa (128kbps)": "128", "Média (192kbps)": "192", "Alta (320kbps)": "320"}
quality_choice = st.select_slider("Qualidade do Áudio", options=list(quality_map.keys()), value="Média (192kbps)")

if st.button("GERAR MP3"):
    if url:
        try:
            with st.spinner("Processando... Isso pode levar alguns segundos."):
                output_dir = "temp_downloads"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Opções com a SOLUÇÃO 1 (Disfarce de Cliente)
                ydl_opts = {
                    'format': 'bestaudio/best',
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
                    info = ydl.extract_info(url, download=True)
                    # O yt-dlp às vezes mantém a extensão original no nome do arquivo interno
                    temp_filename = ydl.prepare_filename(info)
                    base, _ = os.path.splitext(temp_filename)
                    final_filename = base + ".mp3"

                # Oferece o download para o usuário
                if os.path.exists(final_filename):
                    with open(final_filename, "rb") as f:
                        st.success(f"✅ Concluído: {info['title']}")
                        st.audio(f.read(), format="audio/mp3")
                        st.download_button(
                            label="BAIXAR ARQUIVO MP3",
                            data=f,
                            file_name=f"{info['title']}.mp3",
                            mime="audio/mpeg"
                        )
                    
                    # Limpeza para não encher o servidor
                    os.remove(final_filename)
                else:
                    st.error("Erro: O arquivo MP3 não foi geratedo corretamente.")

        except Exception as e:
            st.error(f"Erro ao processar: {str(e)}")
            st.info("Dica: Se o erro 403 persistir, o YouTube pode ter bloqueado o IP do servidor temporariamente.")
    else:
        st.warning("Insira uma URL válida.")

st.markdown("---")
st.caption("Desenvolvido para a comunidade HyperCam.")
