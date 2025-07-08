import requests

def get_user_country():
    """
    Get user's country code (like 'IN', 'US') using IP geolocation.
    Fallback to 'IN' if it fails.
    """
    try:
        response = requests.get("https://ipinfo.io", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("country", "IN")
    except Exception as e:
        print(f"🌐 Location detection failed: {e}")
    
    return "IN"  # Default to India if error
