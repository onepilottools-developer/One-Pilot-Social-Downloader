import streamlit as st
import yt_dlp
import os
import tempfile

# Page Branding & UI
st.set_page_config(page_title="One Pilot Social Downloader", page_icon="🚀", layout="wide")

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
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Social Media Video Downloader")
st.write("Bahi, apna pasandida video link paste karen aur download button dabayein.")

# Input Section
url = st.text_input("Enter Video Link (YouTube, Shorts, etc.):", placeholder="https://www.youtube.com/...")
quality_choice = st.selectbox("Video Quality Select Karen:", ["Best Quality", "720p (HD)", "360p (Fast)"])

if st.button("GET VIDEO"):
    if url:
        try:
            with st.spinner("Bahi wait karen, video process ho rahi hai..."):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    
                    # Quality Logic
                    format_opt = 'best'
                    if quality_choice == "720p (HD)":
                        format_opt = 'best[height<=720]'
                    elif quality_choice == "360p (Fast)":
                        format_opt = 'best[height<=360]'

                    # YT-DLP Options with Anti-Block
                    ydl_opts = {
                        'format': format_opt,
                        'outtmpl': f'{tmp_dir}/%(title)s.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        'referer': 'https://www.google.com/',
                    }

                    # Check if cookies file exists
                    if os.path.exists("cookies.txt"):
                        ydl_opts['cookiefile'] = 'cookies.txt'

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        video_title = info.get('title', 'Social_Video')
                        file_path = ydl.prepare_filename(info)

                        with open(file_path, "rb") as f:
                            st.success(f"✅ Tayyar hai: {video_title}")
                            st.download_button(
                                label="📥 DOWNLOAD NOW",
                                data=f,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4"
                            )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            if "403" in str(e):
                st.info("Bahi, lagta hai YouTube ne block kiya hai. 'cookies.txt' file GitHub par upload karna lazmi hai.")
    else:
        st.warning("Pehle link toh dalen bahi!")

st.divider()
st.caption("Powered by One Pilot Tools - Multan, Pakistan")
