# FreqHue – Synesthetic Sound Visualizer

> ## Purpose 
> FreqHue is an interactive Streamlit app that visualizes sound as color and provides a playable piano keyboard. It supports real-time pitch detection from a microphone, audio file uploads, and YouTube audio analysis, mapping detected frequencies to vibrant colors. The tool is designed for musicians, educators, creators, and anyone interested in the intersection of sound and color.
>
> Key Features:
> - On-screen piano keyboard with color feedback
> - Microphone pitch detection and visualization
> - Audio file and YouTube pitch/color analysis
> - Sequence recording, playback, and color bar visualization
> - Robust device selection and progress indicators

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/St0lenThunda/FreelanceScripts.git
   cd FreelanceScripts/freqhue
   ```
2. **Install dependencies:**
   ```bash
   pip install streamlit sounddevice aubio numpy soundfile yt-dlp scipy
   ```
   - On Linux/WSL, also install FFmpeg:
     ```bash
     sudo apt update && sudo apt install ffmpeg
     ```

## Usage

Run the app with Streamlit:
```bash
streamlit run freqhue_tool.py
```

## Use Cases

- **Music Education:** Visualize the relationship between pitch and color for music students.
- **Ear Training:** Practice pitch recognition and see instant color feedback.
- **Audio Analysis:** Analyze melodies or songs from files or YouTube and see their color sequence.
- **Accessibility:** Provide a synesthetic experience for users with hearing or visual differences.
- **Creative Inspiration:** Use color-mapped melodies for art, design, or multimedia projects.

## Input Modes

- **On-Screen Keyboard:** Play notes, record sequences, and visualize colors.
- **Microphone Pitch Detection:** Select your microphone, detect pitch, and visualize.
- **Audio File/YouTube:** Upload a file or enter a YouTube URL to analyze and visualize pitch/color sequences.

## Troubleshooting

- If you see errors about FFmpeg or yt-dlp, ensure they are installed and accessible in your environment.
- For WSL users, make sure temp directories and FFmpeg paths are set for Linux, not Windows.
- If you encounter device errors, check your system's audio settings and permissions.

## License
MIT License

## Author
St0lenThunda

---
FreqHue is part of the FreelanceScripts toolkit.
