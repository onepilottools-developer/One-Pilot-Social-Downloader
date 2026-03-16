import streamlit as st
import yt_dlp
import os
import tempfile

# 1. Page Configuration
st.set_page_config(page_title="One Pilot Social Downloader", page_icon="🚀", layout="wide")

# 2. Custom White UI Styling
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        background-color: #FF0000; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #cc0000; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 One Pilot Social Downloader")
st.write("YouTube, Shorts, Instagram ya Facebook ka link paste karen.")

# 3. User Inputs
url = st.text_input("Paste Video Link Here:", placeholder="https://www.youtube.com/...")
option = st.selectbox("Download Type & Quality:", [
    "Video - Best Quality", 
    "Video - 720p (HD)", 
    "Video - 360p (Fast)",
    "Audio Only (MP3)"
])

if st.button("GET FILE"):
    if url:
        try:
            with st.spinner("Bahi process ho raha hai, thora intezar karen..."):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    
                    # 4. Flexible Format Logic
                    if option == "Video - 720p (HD)":
                        format_opt = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
                    elif option == "Video - 360p (Fast)":
                        format_opt = 'bestvideo[height<=360]+bestaudio/best[height<=360]/best'
                    elif option == "Audio Only (MP3)":
                        format_opt = 'bestaudio/best'
                    else:
                        format_opt = 'bestvideo+bestaudio/best'

                    # 5. Advanced Options with Anti-Block & Cookies
                    ydl_opts = {
                        'format': format_opt,
                        'outtmpl': f'{tmp_dir}/%(title)s.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        'referer': 'https://www.google.com/',
                        'merge_output_format': 'mp4' if "Video" in option else None,
                    }

                    # Post-processor for MP3
                    if option == "Audio Only (MP3)":
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]

                    # Check for cookies.txt
                    if os.path.exists("cookies.txt"):
                        ydl_opts['cookiefile'] = 'cookies.txt'

                    # 6. Execution
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        
                        # Audio extension fix
                        if option == "Audio Only (MP3)":
                            file_path = os.path.splitext(file_path)[0] + ".mp3"

                        # 7. Final Download Button
                        with open(file_path, "rb") as f:
                            st.success(f"✅ Ready: {info.get('title', 'File')}")
                            st.download_button(
                                label="📥 CLICK TO DOWNLOAD NOW",
                                data=f,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4" if "Video" in option else "audio/mpeg"
                            )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Bahi, agar error aye toh check karen link sahi hai ya 'cookies.txt' updated hai.")
    else:
        st.warning("Pehle link toh dalen bahi!")

st.divider()
st.caption("Powered by One Pilot Tools - Multan, Pakistan")
