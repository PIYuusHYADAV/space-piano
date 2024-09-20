from PIL import Image
import numpy as np
from pyo import *
import time

# Load image
img = Image.open('Screenshot 2024-09-19 233907.png').convert('L')
pixels = np.array(img)

# Image size
width, height = img.size

# Define piano frequencies for a melodic range (C4 to B4)
piano_frequencies = [
    261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 554.37, 587.33, 659.25, 698.46
]

# Initialize Pyo server
s = Server().boot()
s.start()

# Background sound
background = Sine(freq=440, mul=0.05).out()  # Soft background sound

# Scan the image row by row
for y in range(height):
    row = pixels[y]
    
    # For each pixel in the row, generate sound
    for x in range(width):
        intensity = row[x]

        # Detect "stars" based on intensity
        if intensity > 15:
            note_index = int(np.clip(intensity / 255 * (len(piano_frequencies) - 1), 0, len(piano_frequencies) - 1))
            frequency = float(piano_frequencies[note_index])  # Ensure it's a float
            amplitude = float(intensity) / 255  # Ensure it's a float

            # Create an envelope for smoother sound
            env = Adsr(attack=0.02, decay=0.1, sustain=0.5, release=0.2, mul=amplitude).play()

            # Create a chord with slight detuning
            root = Sine(freq=frequency, mul=env).out()
            third = Sine(freq=frequency * 1.25, mul=env * 0.7).out()
            fifth = Sine(freq=frequency * 1.5, mul=env * 0.5).out()

            # Play melodic note with slight delay
            if x % 5 == 0:
                melodic_note = Sine(freq=frequency * 1.5 + np.random.uniform(-2, 2), mul=env * 0.3).out()
                time.sleep(0.04)  # Slight delay for rhythm
            
            time.sleep(0.2)  # Delay to allow notes to resonate
            
        # Handle low intensity regions
        else:
            low_frequency = 110.0  # Frequency for low-intensity regions (A2)
            low_amplitude = float(0.1 * (intensity / 255))  # Ensure it's a float
            
            low_sound = Sine(freq=low_frequency, mul=low_amplitude).out()
            time.sleep(0.2)  # Slight delay to allow the low sound to resonate
            low_sound.stop()  # Stop the low sound immediately after playing
            
# Stop the server after scanning the image
s.stop()