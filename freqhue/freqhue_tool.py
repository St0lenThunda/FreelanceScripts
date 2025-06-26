import pygame
import numpy as np
import sounddevice as sd
import aubio
import colorsys

# --- Settings ---
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
KEY_WIDTH = 60
WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTE_FREQS = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 432.00,
    'B': 493.88,
}

# --- Init Pygame ---
pygame.init()
WIDTH, HEIGHT = len(WHITE_KEYS) * KEY_WIDTH, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎹 432Hz Light Piano")

font = pygame.font.SysFont(None, 24)

# --- Helper Functions ---
def freq_to_color(freq):
    if freq <= 0: return (0, 0, 0)
    hue = (np.log2(freq / 432.0)) % 1.0
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return tuple(int(c * 255) for c in rgb)

def draw_keyboard():
    for i, key in enumerate(WHITE_KEYS):
        rect = pygame.Rect(i * KEY_WIDTH, 0, KEY_WIDTH, HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        txt = font.render(key, True, (0, 0, 0))
        screen.blit(txt, (i * KEY_WIDTH + 20, HEIGHT - 30))

def play_note(freq):
    duration = 0.3  # seconds
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(freq * t * 2 * np.pi)
    audio = tone.astype(np.float32)
    sd.play(audio, SAMPLE_RATE)

def mic_input_visualizer(pitch_o):
    def callback(indata, frames, time, status):
        samples = np.frombuffer(indata, dtype=np.float32)
        freq = pitch_o(samples)[0]
        if freq > 20:
            color = freq_to_color(freq)
            screen.fill(color)
            draw_keyboard()
            pygame.display.flip()
    return callback

# --- Main Loop ---
pitch_o = aubio.pitch("yin", BUFFER_SIZE, BUFFER_SIZE // 2, SAMPLE_RATE)
pitch_o.set_unit("Hz")
pitch_o.set_silence(-40)
stream = sd.InputStream(callback=mic_input_visualizer(pitch_o),
                        channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE)
stream.start()

running = True
while running:
    screen.fill((0, 0, 0))
    draw_keyboard()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            key_index = x // KEY_WIDTH
            if 0 <= key_index < len(WHITE_KEYS):
                note = WHITE_KEYS[key_index]
                freq = NOTE_FREQS[note]
                color = freq_to_color(freq)
                screen.fill(color)
                draw_keyboard()
                pygame.display.flip()
                play_note(freq)

pygame.quit()
stream.stop()
