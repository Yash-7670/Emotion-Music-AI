import numpy as np
import librosa
import joblib

# Load the trained audio emotion model
model = joblib.load("models/audio_model.pkl")

# Extract features from audio signal
def extract_features(signal, sample_rate):
    mfccs = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return mfccs_processed.reshape(1, -1)

# Predict emotion from live mic input
def predict_audio_emotion_live(audio, sample_rate):  
    try:
        features = extract_features(audio, sample_rate)
        prediction = model.predict(features)
        return prediction[0]
    except Exception as e:
        print("Audio prediction error:", e)
        return "neutral"
