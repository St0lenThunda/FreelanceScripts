#!/usr/bin/env python3
"""
This script creates a Streamlit app that visualizes sound as color and provides an interactive piano keyboard.
It uses sounddevice for audio playback, aubio for pitch detection, and numpy/colorsys for math and color mapping.

Key Features:
- Visualizes sound as color using frequency-to-hue mapping
- Interactive on-screen piano keyboard with recording/playback
- Microphone pitch detection with device selection
- Audio file and YouTube URL input support
- Progress bars for long-running analysis
- Robust input/output device management
- Customizable tuning (A=432 or 440 Hz)
- Color bar visualization of note sequences
- Cross-platform compatibility (Linux/WSL/Windows)
"""
# TODO: onscreen keyboard updated to look like piano
# TODO: Audio Input/Outputs must be tested on different computers
# TODO: Separate the onscreen recorder interface from the file uploader

import streamlit as st
import numpy as np
import sounddevice as sd
import aubio
import colorsys
import time
import warnings
from scipy.signal import resample
import io
import tempfile
import os
try:
    import yt_dlp
except ImportError:
    yt_dlp = None
import soundfile as sf

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

# --- Input/Output Device Discovery and Session State ---
def get_device_list(kind='input'):
    """
    Returns a list of dicts for input or output devices, each with:
    - 'index': device index
    - 'name': device name
    - 'api': host API name
    - 'channels': max_input_channels or max_output_channels
    """
    input_desc = ['mic', 'microphone', 'input']
    all_devs = sd.query_devices()
    hostapis = sd.query_hostapis()
    devs = []
    for i, d in enumerate(all_devs):
        api = hostapis[d['hostapi']]['name']
        name = d['name']
        if kind == 'input' and d['max_input_channels'] > 0 and any(x in name.lower() for x in input_desc):
            devs.append({
                'index': i,
                'name': name,
                'api': api,
                'channels': d['max_input_channels'],
                'str': f"{i}: {name} (API: {api})"
            })
        elif kind == 'output' and d['max_output_channels'] > 0 and not any(x in name.lower() for x in input_desc):
            devs.append({
                'index': i,
                'name': name,
                'api': api,
                'channels': d['max_output_channels'],
                'str': f"{i}: {name} (API: {api})"
            })
    return devs

if 'input_devices' not in st.session_state:
    st.session_state['input_devices'] = get_device_list('input')
if 'output_devices' not in st.session_state:
    st.session_state['output_devices'] = get_device_list('output')

input_devices = st.session_state['input_devices']
output_devices = st.session_state['output_devices']


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
    Uses the selected output device from session state.
    """
    duration = 1.5  # 1.5 seconds
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(freq * 2 * np.pi * t)
    try:
        # Use the selected output device index from session state
        if 'selected_output_idx' in st.session_state and st.session_state['selected_output_idx'] is not None:
            output_device_idx = output_devices[st.session_state['selected_output_idx']]['index']
        else:
            output_device_idx = sd.default.device[1] if isinstance(sd.default.device, (list, tuple)) else sd.default.device
        device_info = sd.query_devices(output_device_idx, 'output')
        device_rate = int(device_info['default_samplerate'])
        st.sidebar.markdown(f"**[INFO] Output Device:** {device_info['name']}")
        st.sidebar.markdown(f"**[INFO] Device Sample Rate:** {device_rate}")
        st.sidebar.markdown(f"**[INFO] Requested Sample Rate:** {SAMPLE_RATE}")
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

def render_device_info_html(devices, title):
    html = """
    <details>
      <summary><strong>""" + title + """ Devices</strong></summary>
    """ 
    for d in devices:
        html += f"<p>{d['index']}: {d['name']} (API: {d['api']}, Channels: {d['channels']})</p><br />"
    html += """
    </details>
    """
    return html
    
def detect_pitch(pitch_obj, input_device_idx=None):
    """
    Detect the pitch from the microphone using aubio.
    - Records 1 second of audio at SAMPLE_RATE.
    - Uses aubio's pitch detection to estimate the frequency.
    Uses the selected input device index if provided.
    """
    duration = 1.0  # seconds
    try:
        if input_device_idx is None:
            st.error("No input device selected for pitch detection.")
            return 0
        # Use the selected input device
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recording = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1, dtype='float32', device=input_device_idx)
            sd.wait()
        samples = np.squeeze(recording)
        return pitch_obj(samples)[0]
    except Exception as e:
        st.error(f"Audio input error: {e}")
        return 0
  # --- Audio Processing Utility ---
def process_audio_samples(samples, sr, show_progress=True):
    """
    Process audio samples to extract a sequence of detected pitches (as frequencies) and durations.
    Returns a list of (note_label, duration) tuples.
    If show_progress is True, displays a Streamlit progress bar.
    """
    win_s = 2048
    hop_s = 512
    pitch_o = aubio.pitch("yin", win_s, hop_s, sr)
    pitch_o.set_unit("Hz")
    pitch_o.set_silence(-40)
    n_frames = int((len(samples) - hop_s) / hop_s)
    notes = []
    last_pitch = None
    last_time = 0
    min_note_duration = 0.1  # seconds
    progress_bar = st.progress(0) if show_progress else None
    for i in range(n_frames):
        start = i * hop_s
        end = start + hop_s
        if end > len(samples):
            break
        frame = samples[start:end]
        pitch = float(pitch_o(frame)[0])
        t = start / sr
        if pitch > 0:
            note_label = f"{pitch:.2f}Hz"
            if last_pitch is None:
                last_pitch = note_label
                last_time = t
            elif abs(pitch - float(last_pitch.replace('Hz',''))) > 1.0:
                dur = t - last_time
                if dur >= min_note_duration:
                    notes.append((last_pitch, dur))
                last_pitch = note_label
                last_time = t
        if progress_bar and i % 10 == 0:
            progress_bar.progress(i / n_frames)
    # Add last note
    if last_pitch is not None and (len(samples)/sr - last_time) >= min_note_duration:
        notes.append((last_pitch, len(samples)/sr - last_time))
    if progress_bar:
        progress_bar.progress(1.0)
        progress_bar.empty()
    return notes

# --- Recording and Sequence Visualization Utilities ---
def recording_controls():
    col_rec, col_play, col_clear = st.columns([1,1,1])
    with col_rec:
        if not st.session_state.get('recording', False):
            if st.button('🎬 Start Recording'):
                st.session_state['recording'] = True
                st.session_state['note_sequence'] = []
                st.session_state['last_note_time'] = time.time()
        else:
            if st.button('⏹️ Stop Recording'):
                st.session_state['recording'] = False
                st.session_state['last_note_time'] = None
    with col_play:
        if st.button('▶️ Play Sequence') and st.session_state.get('note_sequence'):
            for note, dur in st.session_state['note_sequence']:
                freq = get_freq(note, st.session_state['base_tuning'])
                play_note(freq)
                time.sleep(dur)
    with col_clear:
        if st.button('🗑️ Clear Sequence'):
            st.session_state['note_sequence'] = []

def record_note(note):
    now = time.time()
    if st.session_state.get('recording', False):
        if st.session_state.get('last_note_time') is not None:
            dur = now - st.session_state['last_note_time']
            st.session_state['note_sequence'].append((note, dur))
        st.session_state['last_note_time'] = now

def sequence_color_bar():
    if st.session_state.get('note_sequence'):
        notes, durs = zip(*st.session_state['note_sequence'])
        total = sum(durs)
        colors = [freq_to_color(get_freq(n, st.session_state['base_tuning']), st.session_state['base_tuning']) for n in notes]
        bar_html = "<div style='display:flex;width:100%;height:40px;border-radius:8px;overflow:hidden;'>"
        for i, (c, d) in enumerate(zip(colors, durs)):
            width = int(100 * d / total)
            if i < len(colors)-1:
                next_c = colors[i+1]
                bar_html += f"<div style='flex:0 0 {width}%;background:linear-gradient(to right, {c}, {next_c});'></div>"
            else:
                bar_html += f"<div style='flex:0 0 {width}%;background:{c};'></div>"
        bar_html += "</div>"
        st.markdown(bar_html, unsafe_allow_html=True)

# ----- Streamlit UI -----
# App title and description
st.title("🎹 FreqHue – Synesthetic Sound Visualizer")
st.caption("Visualize sound through color, tuned to the frequency of your choice.")

# --- Input Mode Selection ---
input_mode = st.selectbox("Choose input mode", ["On-Screen Keyboard", "Microphone Pitch Detection", "Audio File/YouTube"])

if input_mode == "Microphone Pitch Detection":
    st.markdown("#### 🎤 Microphone Pitch Detection")
    # Use input_devices and input_device_str from session state
    input_devices = st.session_state['input_devices']
    input_device_str = [d['str'] for d in input_devices]
    if not input_devices:
        st.warning("No input audio devices found. Please connect a microphone.")
        selected_input_device = None
        selected_input_idx = None
    else:
        selected_input_idx = st.selectbox("Select input device for mic detection", list(range(len(input_device_str))), format_func=lambda i: input_device_str[i])
        selected_input_device = input_devices[selected_input_idx]['name']
        st.session_state['selected_input_idx'] = selected_input_idx
        st.sidebar.markdown(f"**[INFO] Input Device:** {selected_input_device}")
    # Tuning and pitch detection control===
    col1, col2 = st.columns(2)
    with col1:
        # Choose tuning (A=432 or 440 Hz)
        tuning = st.radio("Choose tuning", [432, 440], horizontal=True)
        st.session_state['base_tuning'] = tuning
    with col2:
        # Button to detect pitch from mic
        if st.button("🎤 Detect Pitch from Mic"):
            if selected_input_device is None or selected_input_idx is None:
                st.error("No input device available for pitch detection.")
            else:
                pitch_o = aubio.pitch("yin", BUFFER_SIZE, BUFFER_SIZE // 2, SAMPLE_RATE)
                pitch_o.set_unit("Hz")
                pitch_o.set_silence(-40)
                input_device_idx = input_devices[selected_input_idx]['index']
                st.session_state['selected_input_idx'] = selected_input_idx
                detected = detect_pitch(pitch_o, input_device_idx)
                color = freq_to_color(detected, tuning)
                # Record detected note (as frequency string for uniqueness)
                note_label = f"{detected:.2f}Hz"
                record_note(note_label)
                st.markdown(f"**Detected Frequency:** `{detected:.2f} Hz`")
                st.markdown(f"<div style='width:100%;height:100px;background-color:{color};'></div>", unsafe_allow_html=True)
    sequence_color_bar()

elif input_mode == "On-Screen Keyboard":
    st.markdown("#### 🎼 On-Screen Keyboard")
    recording_controls()
    # White keys in a row (7 columns)
    white_cols = st.columns(7)
    note_pressed = None
    for i, note in enumerate(WHITE_KEYS):
        with white_cols[i]:
            if st.button(note, key=f"white_{note}"):
                note_pressed = note
    # Black keys overlay: use empty columns for spacing, only render black keys above the correct white keys
    black_cols = st.columns(7)
    for i, note in enumerate(BLACK_KEYS):
        if note:
            with black_cols[i]:
                st.markdown('<div style="height: -20px;"></div>', unsafe_allow_html=True)
                if st.button(note, key=f"black_{note}"):
                    note_pressed = note
                st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
    if note_pressed:
        freq = get_freq(note_pressed, st.session_state['base_tuning'])
        play_note(freq)
        color = freq_to_color(freq, st.session_state['base_tuning'])
        record_note(note_pressed)
        with st.sidebar:
            st.markdown(f"<div style='width:100%;height:100px;background-color:{color};'></div>", unsafe_allow_html=True)
            st.markdown(f"**Note:** `{note_pressed}`")
            st.markdown(f"**Frequency:** `{freq:.2f} Hz`")
            st.markdown(f"**Color:** `{color}`")
    sequence_color_bar()

elif input_mode == "Audio File/YouTube":
    st.markdown("#### 📁 Audio File or YouTube URL")
    recording_controls()
    audio_file = st.file_uploader("Upload audio file (wav/mp3/flac)", type=["wav", "mp3", "flac"])
    yt_url = st.text_input("Or enter a YouTube URL to analyze audio:")
    samples = None
    sr = SAMPLE_RATE
    if audio_file is not None:
        # Read audio file
        try:
            data, sr = sf.read(audio_file)
            if data.ndim > 1:
                data = data[:,0]  # Use first channel
            samples = data.astype(np.float32)
        except Exception as e:
            st.error(f"Could not read audio file: {e}")
        if samples is not None:
            st.success(f"Loaded audio, sample rate: {sr}, duration: {len(samples)/sr:.2f}s")
            # Extract sequence with progress
            sequence = process_audio_samples(samples, sr, show_progress=True)
            st.session_state['note_sequence'] = sequence
            st.session_state['recording'] = False
            st.session_state['last_note_time'] = None
            sequence_color_bar()
            if st.button('▶️ Play Sequence', key='play_sequence_audiofile') and sequence:
                for note, dur in sequence:
                    try:
                        freq = float(note.replace('Hz',''))
                    except:
                        freq = 0
                    if freq > 0:
                        play_note(freq)
                    time.sleep(dur)
    elif yt_url:
        if yt_dlp is None:
            st.error("yt-dlp is not installed. Please install it to use YouTube audio.")
        else:
            ffmpeg_path = '/usr/bin/ffmpeg'  # Linux default
            if not os.path.exists(ffmpeg_path):
                st.warning("FFmpeg not found at /usr/bin/ffmpeg. Please install ffmpeg in your Linux environment.")
            with st.spinner("Downloading audio from YouTube..."):
                # Always use a Linux-side temp dir for WSL compatibility
                with tempfile.TemporaryDirectory(dir="/tmp") as tmpdir:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(tmpdir, '%(id)s.%(ext)s'),
                        'quiet': True,
                        'no_warnings': True,
                        'ffmpeg_location': ffmpeg_path,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'wav',
                            'preferredquality': '192',
                        }],
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(yt_url, download=True)
                        wav_filename = os.path.join(tmpdir, f"{info['id']}.wav")
                        try:
                            data, sr = sf.read(wav_filename)
                            if data.ndim > 1:
                                data = data[:,0]
                            samples = data.astype(np.float32)
                        except Exception as e:
                            st.error(f"Could not read downloaded audio: {e}")
        if samples is not None:
            st.success(f"Loaded audio, sample rate: {sr}, duration: {len(samples)/sr:.2f}s")
            # Extract sequence with progress
            sequence = process_audio_samples(samples, sr, show_progress=True)
            st.session_state['note_sequence'] = sequence
            st.session_state['recording'] = False
            st.session_state['last_note_time'] = None
            sequence_color_bar()
            if st.button('▶️ Play Sequence', key='play_sequence_youtube') and sequence:
                for note, dur in sequence:
                    try:
                        freq = float(note.replace('Hz',''))
                    except:
                        freq = 0
                    if freq > 0:
                        play_note(freq)
                    time.sleep(dur)
  
# Use only the output_devices and output_device_str from session state
output_device_str = [d['str'] for d in output_devices]
if not output_devices:
    st.sidebar.warning("No output audio devices found. Please connect speakers or headphones.")
    selected_output_device = None
    st.session_state['selected_output_idx'] = None
else:
    # Try to default to internal speakers if present, else first output device
    default_idx = 0
    keywords = ['speaker', 'output', 'internal']
    for idx, d in enumerate(output_devices):
        if any(k in d['name'].lower() for k in keywords):
            default_idx = idx
            break
    selected_output_idx = st.sidebar.selectbox("Select output device for sound playback", list(range(len(output_device_str))), format_func=lambda i: output_device_str[i], index=default_idx)
    selected_output_device = output_devices[selected_output_idx]['name']
    st.session_state['selected_output_idx'] = selected_output_idx

# At the end of the script, add device discovery info to the sidebar
with st.sidebar:
    st.markdown('---')
    st.markdown(render_device_info_html(input_devices, "Input"), unsafe_allow_html=True)
    st.markdown(render_device_info_html(output_devices, "Output"), unsafe_allow_html=True)
