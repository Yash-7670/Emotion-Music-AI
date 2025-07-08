import sounddevice as sd
import numpy as np

print("🎤 Scanning input devices using WASAPI (Windows)...\n")

# Find WASAPI hostapi index
wasapi_index = None
for i, hostapi in enumerate(sd.query_hostapis()):
    if 'wasapi' in hostapi['name'].lower():
        wasapi_index = i
        break

if wasapi_index is None:
    print("❌ WASAPI not available on this system.")
    exit()

# Get WASAPI input devices
devices = sd.query_devices()
wasapi_input_devices = [
    (i, d['name']) for i, d in enumerate(devices)
    if d['hostapi'] == wasapi_index and d['max_input_channels'] > 0
]

if not wasapi_input_devices:
    print("❌ No input devices found under WASAPI.")
    exit()

print("✅ Available WASAPI input devices:")
for i, name in wasapi_input_devices:
    print(f"[{i}] {name}")

# Pick your known mic index
device_index = 16  # Your Realtek Mic

# Try common sample rates
sample_rates_to_try = [48000, 44100, 32000, 16000, 11025, 8000]
working_rate = None

print(f"\n🎤 Trying to find working sample rate for device [{device_index}]...")

for rate in sample_rates_to_try:
    try:
        duration = 2
        print(f"🔍 Trying sample rate: {rate} Hz")
        audio = sd.rec(int(duration * rate), samplerate=rate,
                       channels=1, dtype='float32', device=device_index)
        sd.wait()
        audio = np.nan_to_num(audio.flatten())
        peak = np.max(np.abs(audio))
        if peak < 1e-5:
            print("⚠️  Silent signal")
        else:
            print(f"✅ Success! Sample rate = {rate} Hz, Peak = {peak:.4f}")
            working_rate = rate
            break
    except Exception as e:
        print(f"❌ Failed at {rate} Hz: {e}")

if working_rate:
    print(f"\n🎉 Your working mic setup → Device Index: {device_index}, Sample Rate: {working_rate} Hz")
else:
    print("❌ Could not find any working sample rate for this mic.")
