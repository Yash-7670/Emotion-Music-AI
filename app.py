import streamlit as st
import cv2
import numpy as np
import sounddevice as sd
import time

from utils.camera_face_predict import detect_emotion_from_frame
from utils.extract_audio_features import predict_audio_emotion_live
from utils.spotify_api import get_spotify_songs, get_user_location_name
from utils.emotion_mapping import get_mood_variations

# Config
st.set_page_config(page_title="🎭 EmoTune AI", page_icon="🎶", layout="wide")

# Sidebar
with st.sidebar:
    location = get_user_location_name()
    st.markdown(f"📍 **Location:** :green[{location}]")
    st.markdown("### 🎙️ Input Method")
    method = st.radio("Choose Input", ["Webcam", "Mic"])

# Title
st.markdown("<h1 style='text-align:center;'>🎭 EmoTune AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Real-time Emotion Detection + Music to Match or Improve Your Mood</p>", unsafe_allow_html=True)

# UI Layout
col1, col2, col3 = st.columns([1, 8, 1])
placeholder_frame = st.empty()
emotion_box = st.empty()
song_block = st.container()

emoji_map = {
    "happy": "😄", "sad": "😢", "angry": "😠",
    "surprise": "😲", "fear": "😨", "disgust": "🤢", "neutral": "😐"
}

if method == "Webcam":
    if "cam_running" not in st.session_state:
        st.session_state.cam_running = False

    start = col1.button("📸 Start Webcam")
    stop = col3.button("⛔ Stop Webcam")

    if start:
        st.session_state.cam_running = True
    if stop:
        st.session_state.cam_running = False

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    last_emotion = None
    cooldown = 5
    last_time = 0

    while st.session_state.cam_running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Unable to access webcam.")
            break

        emotion, annotated = detect_emotion_from_frame(frame)
        placeholder_frame.image(annotated, channels="RGB", width=520)

        if emotion and emotion != last_emotion and (time.time() - last_time > cooldown):
            last_emotion = emotion
            last_time = time.time()

            emoji = emoji_map.get(emotion, "🎭")
            emotion_box.success(f"{emoji} Emotion Detected: **{emotion.upper()}**")

            songs = get_spotify_songs(emotion, location)
            with song_block:
                st.markdown("### 🎶 Songs for Your Mood:")
                cols = st.columns(2)
                for i, song in enumerate(songs):
                    with cols[i % 2]:
                        st.image(song["album_cover"], width=180)
                        st.markdown(f"**{song['title']}**")
                        st.markdown(f"👤 {song['artist']}")
                        if song.get("preview_url"):
                            st.audio(song["preview_url"], format="audio/mp3")
                        else:
                            st.markdown(f"[▶️ Play on Spotify]({song['url']})", unsafe_allow_html=True)
                        st.markdown("---")
        time.sleep(0.1)
    cap.release()

elif method == "Mic":
    if "mic_on" not in st.session_state:
        st.session_state.mic_on = False

    start = col1.button("🎙️ Start Mic")
    stop = col3.button("⛔ Stop Mic")

    if start:
        st.session_state.mic_on = True
    if stop:
        st.session_state.mic_on = False

    waveform = st.empty()
    last_emotion = None
    cooldown = 6
    last_time = 0

    while st.session_state.mic_on:
        fs = 48000
        duration = 2
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32', device=16)
        sd.wait()
        waveform.line_chart(audio.flatten())

        try:
            emotion = predict_audio_emotion_live(audio, fs)

        except Exception as e:
            st.error(f"❌ Audio error: {e}")
            break

        if emotion and emotion != last_emotion and (time.time() - last_time > cooldown):
            last_emotion = emotion
            last_time = time.time()

            emoji = emoji_map.get(emotion, "🎭")
            emotion_box.success(f"{emoji} Emotion Detected: **{emotion.upper()}**")

            songs = get_spotify_songs(emotion, location)
            with song_block:
                st.markdown("### 🎶 Songs for Your Mood:")
                cols = st.columns(2)
                for i, song in enumerate(songs):
                    with cols[i % 2]:
                        st.image(song["album_cover"], width=180)
                        st.markdown(f"**{song['title']}**")
                        st.markdown(f"👤 {song['artist']}")
                        if song.get("preview_url"):
                            st.audio(song["preview_url"], format="audio/mp3")
                        else:
                            st.markdown(f"[▶️ Play on Spotify]({song['url']})", unsafe_allow_html=True)
                        st.markdown("---")
        time.sleep(0.1)
