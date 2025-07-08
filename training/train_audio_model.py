import os
import librosa
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Path to TESS dataset
dataset_path = "dataset/TESS"
features = []
labels = []

# Process audio files
for folder in os.listdir(dataset_path):
    emotion_label = folder.split('_')[-1].lower()  # e.g., YAF_happy → happy
    folder_path = os.path.join(dataset_path, folder)

    for file in os.listdir(folder_path):
        if file.endswith('.wav'):
            file_path = os.path.join(folder_path, file)
            try:
                y, sr = librosa.load(file_path, duration=3, offset=0.5)
                mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
                mfccs_scaled = np.mean(mfccs.T, axis=0)
                features.append(mfccs_scaled)
                labels.append(emotion_label)
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

# Convert to arrays
X = np.array(features)
y = LabelEncoder().fit_transform(labels)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"✅ Audio model accuracy: {accuracy:.2f}")

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/audio_model.pkl")
print("✅ Audio emotion model saved at models/audio_model.pkl")
