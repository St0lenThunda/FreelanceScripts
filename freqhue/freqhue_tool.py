# FreqHue: Synesthetic Sound Visualizer
# This script creates a Streamlit app that visualizes sound as color and provides an interactive piano keyboard.
# It uses sounddevice for audio playback, aubio for pitch detection, and numpy/colorsys for math and color mapping.

import streamlit as st
import numpy as np
import sounddevice as sd
import aubio
import colorsys
import time
import warnings
from scipy.signal import resample

# ----- Constants -----
# Define the white and black keys for a single octave piano
WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']  # White keys in order
BLACK_KEYS = ['C#', 'D#', '', 'F#', 'G#', 'A#', '']  # Black keys, '' for missing black keys
# ALL_KEYS is a list of dicts for each note, with a flag for white/black
ALL_KEYS = [
    {'note': 'C', 'is_white': True},
    {'note': 'C#', 'is_white': False},
    {'note': 'D', 'is_white': True},
    {'note': 'D#', 'is_white': False},
    {'note': 'E', 'is_white': True},
    {'note': 'F', 'is_white': True},
    {'note': 'F#', 'is_white': False},
    {'note': 'G', 'is_white': True},
    {'note': 'G#', 'is_white': False},
    {'note': 'A', 'is_white': True},
    {'note': 'A#', 'is_white': False},
    {'note': 'B', 'is_white': True},
]
# NOTE_RATIOS maps note names to their semitone offset from A (A=0)
NOTE_RATIOS = {
    'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5, 'F': -4, 'F#': -3, 'G': -2, 'G#': -1, 'A': 0, 'A#': 1, 'B': 2
}
SAMPLE_RATE = 44100  # Standard audio sample rate in Hz
BUFFER_SIZE = 1024   # Buffer size for audio input/output

# ----- Session State -----
# Store the base tuning (A=432 or 440 Hz) in Streamlit session state
if 'base_tuning' not in st.session_state:
    st.session_state['base_tuning'] = 432

# ----- Helper Functions -----
def get_freq(note: str, base_freq=432):
    """
    Calculate the frequency of a note given its name and a base frequency (A=base_freq).
    Math:
    - Each semitone is a ratio of 2^(1/12).
    - The offset from A is NOTE_RATIOS[note].
    - freq = base_freq * 2^(semitone/12)
    """
    semitone = NOTE_RATIOS.get(note, 0)  # Offset from A
    return base_freq * (2 ** (semitone / 12))

def freq_to_color(freq, base_freq):
    """
    Map a frequency to a color using HSV color space.
    Math:
    - hue = log2(freq / base_freq) % 1.0 (wraps every octave)
    - colorsys.hsv_to_rgb(hue, 1, 1) gives a bright color for each hue
    - Output is formatted as a hex string
    """
    if freq <= 0:
        return "#000000"
    hue = (np.log2(freq / base_freq)) % 1.0  # Map frequency to hue (0-1)
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # Full saturation and value
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def play_note(freq):
    """
    Play a sine wave at the given frequency for a short duration.
    Handles output device sample rate mismatches by resampling if needed.
    Math explanation:
    - t: time array, linspace from 0 to duration, with SAMPLE_RATE * duration samples.
      (t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False))
    - tone: sine wave, amplitude 1, at frequency 'freq'.
      (tone = np.sin(freq * 2 * pi * t))
    - If the output device's sample rate does not match SAMPLE_RATE, resample the tone to match.
    """
    duration = 0.5  # seconds
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(freq * 2 * np.pi * t)
    try:
        # Use the selected output device if available
        if 'selected_output_device' in globals() and selected_output_device is not None:
            output_device_idx = next((i for i, d in enumerate(all_devices) if d['name'] == selected_output_device and d['max_output_channels'] > 0), None)
        else:
            output_device_idx = sd.default.device[1] if isinstance(sd.default.device, (list, tuple)) else sd.default.device
        device_info = sd.query_devices(output_device_idx, 'output')
        device_rate = int(device_info['default_samplerate'])
        st.sidebar.markdown(f"**[DEBUG] Output Device:** {device_info['name']}")
        st.sidebar.markdown(f"**[DEBUG] Device Sample Rate:** {device_rate}")
        st.sidebar.markdown(f"**[DEBUG] Requested Sample Rate:** {SAMPLE_RATE}")
        if device_rate != SAMPLE_RATE:
            st.sidebar.warning(f"Output device does not support {SAMPLE_RATE} Hz. Using {device_rate} Hz instead.")
            new_len = int(len(tone) * device_rate / SAMPLE_RATE)
            tone = resample(tone, new_len)
            sd.play(tone.astype(np.float32), device_rate, device=output_device_idx)
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sd.play(tone.astype(np.float32), SAMPLE_RATE, device=output_device_idx)
        sd.wait()
    except Exception as e:
        st.sidebar.error(f"Audio playback error: {e}")
        import traceback
        st.sidebar.code(traceback.format_exc())

def detect_pitch(pitch_obj):
    """
    Detect the pitch from the microphone using aubio.
    - Records 1 second of audio at SAMPLE_RATE.
    - Uses aubio's pitch detection to estimate the frequency.
    """
    duration = 2.0  # seconds
    try:
        # Check for available input devices
        input_devices = [d for d in sd.query_devices() if d['max_input_channels'] > 0]
        if not input_devices:
            st.error("No input audio device found. Please connect a microphone.")
            return 0
        # Use default input device
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recording = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()
        samples = np.squeeze(recording)
        return pitch_obj(samples)[0]
    except Exception as e:
        st.error(f"Audio input error: {e}")
        return 0

# ----- Streamlit UI -----
# App title and description
st.title("🎹 FreqHue – Synesthetic Sound Visualizer")
st.caption("Visualize sound through color, tuned to the frequency of your choice.")

# --- Input Mode Selection ---
input_mode = st.selectbox("Choose input mode", ["On-Screen Keyboard", "Microphone Pitch Detection"])

if input_mode == "Microphone Pitch Detection":
    st.markdown("#### 🎤 Microphone Pitch Detection")
    # List available input devices for mic pitch detection
    # Show all input devices with their index, name, and host API for easier identification
    all_devices = sd.query_devices()
    input_devices = [d for d in all_devices if d['max_input_channels'] > 0]
    input_device_names = [f"{i}: {d['name']} (API: {sd.query_hostapis()[d['hostapi']]['name']})" for i, d in enumerate(all_devices) if d['max_input_channels'] > 0]
    if not input_devices:
        st.warning("No input audio devices found. Please connect a microphone.")
        selected_input_device = None
    else:
        selected_input_idx = st.selectbox("Select input device for mic detection", list(range(len(input_device_names))), format_func=lambda i: input_device_names[i])
        selected_input_device = input_devices[selected_input_idx]['name']
        # Show a table of all input devices for reference
        # st.sidebar.markdown("#### Input Device List")
        # for idx, d in enumerate(input_devices):
        #     st.sidebar.markdown(f"**{idx}**: {d['name']} (API: {sd.query_hostapis()[d['hostapi']]['name']}) | Channels: {d['max_input_channels']}")
    # Tuning and pitch detection controls
    col1, col2 = st.columns(2)
    with col1:
        # Choose tuning (A=432 or 440 Hz)
        tuning = st.radio("Choose tuning", [432, 440], horizontal=True)
        st.session_state['base_tuning'] = tuning
    with col2:
        # Button to detect pitch from mic
        if st.button("🎤 Detect Pitch from Mic"):
            if selected_input_device is None:
                st.error("No input device available for pitch detection.")
            else:
                pitch_o = aubio.pitch("yin", BUFFER_SIZE, BUFFER_SIZE // 2, SAMPLE_RATE)
                pitch_o.set_unit("Hz")
                pitch_o.set_silence(-40)
                # Set the input device for sounddevice
                try:
                    sd.default.device = (None, sd.query_devices().index(next(d for d in sd.query_devices() if d['name'] == selected_input_device)))
                except Exception as e:
                    st.error(f"Could not set input device: {e}")
                detected = detect_pitch(pitch_o)
                color = freq_to_color(detected, tuning)
                st.markdown(f"**Detected Frequency:** `{detected:.2f} Hz`")
                st.markdown(f"<div style='width:100%;height:100px;background-color:{color};'></div>", unsafe_allow_html=True)

elif input_mode == "On-Screen Keyboard":
    st.markdown("#### 🎼 On-Screen Keyboard")
    # --- Visually accurate piano keyboard using only Streamlit buttons for interaction ---
    # Use the global WHITE_KEYS and BLACK_KEYS for consistency
    white_key_notes = WHITE_KEYS
    black_key_notes = BLACK_KEYS
    # White keys in a row (7 columns)
    white_cols = st.columns(7)
    note_pressed = None
    for i, note in enumerate(white_key_notes):
        with white_cols[i]:
            if st.button(note, key=f"white_{note}"):
                note_pressed = note
    # Black keys overlay: use empty columns for spacing, only render black keys above the correct white keys
    black_cols = st.columns(7)
    black_key_map = [(0, 'C#'), (1, 'D#'), (3, 'F#'), (4, 'G#'), (5, 'A#')]
    for i, note in black_key_map:
        with black_cols[i]:
            st.markdown('<div style="height: -20px;"></div>', unsafe_allow_html=True)
            if st.button(note, key=f"black_{note}"):
                note_pressed = note
            st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
    # Display color output and debug info in the sidebar
    if note_pressed:
        freq = get_freq(note_pressed, st.session_state['base_tuning'])
        play_note(freq)
        color = freq_to_color(freq, st.session_state['base_tuning'])
        with st.sidebar:
            st.markdown(f"<div style='width:100%;height:100px;background-color:{color};'></div>", unsafe_allow_html=True)
            st.markdown(f"**Note:** `{note_pressed}`")
            st.markdown(f"**Frequency:** `{freq:.2f} Hz`")
            st.markdown(f"**Color:** `{color}`")

# --- Output Device Selection ---
# List all output devices with their index, name, and host API
all_devices = sd.query_devices()
output_devices = [d for d in all_devices if d['max_output_channels'] > 0]
output_device_names = [f"{i}: {d['name']} (API: {sd.query_hostapis()[d['hostapi']]['name']})" for i, d in enumerate(all_devices) if d['max_output_channels'] > 0]
if not output_devices:
    st.sidebar.warning("No output audio devices found. Please connect speakers or headphones.")
    selected_output_device = None
else:
    # Try to default to internal speakers if present, else first output device
    default_idx = 0
    for idx, d in enumerate(output_devices):
        if 'speaker' in d['name'].lower() or 'output' in d['name'].lower() or 'internal' in d['name'].lower():
            default_idx = idx
            break
    # selected_output_idx = st.sidebar.selectbox("Select output device for sound playback", list(range(len(output_device_names))), format_func=lambda i: output_device_names[i], index=default_idx)
    # selected_output_device = output_devices[selected_output_idx]['name']
    # # Show a table of all output devices for reference
    # st.sidebar.markdown("#### Output Device List")
    # for idx, d in enumerate(output_devices):
    #     st.sidebar.markdown(f"**{idx}**: {d['name']} (API: {sd.query_hostapis()[d['hostapi']]['name']}) | Channels: {d['max_output_channels']}")
