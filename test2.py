import streamlit as st

video_file = open('defend1.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes, start_time=0)