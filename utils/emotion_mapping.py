def get_mood_variations(emotion):
    emotion = emotion.lower()
    mapping = {
        "happy": ["happy", "jolly", "cheerful", "party"],
        "sad": ["sad", "calm", "soothing", "healing"],
        "angry": ["angry", "peaceful", "relaxing", "neutral"],
        "fear": ["fear", "brave", "uplifting"],
        "surprise": ["surprise", "exciting", "upbeat"],
        "neutral": ["neutral", "balanced", "chill"],
        "disgust": ["disgust", "refreshing", "hopeful"]
    }
    return mapping.get(emotion, [emotion])
