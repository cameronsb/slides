# Slideshow Collection

A collection of interactive presentations with AI-generated narration.

## Current Presentations

### 1. Engineering Organization Improvement
A strategic approach to implementing systematic workflow improvements in engineering organizations through discovery, piloting, and adoption phases.

## Features

- 🔊 High-quality AI narration (OpenAI TTS)
- ⚡ Adjustable playback speed (0.5x - 3.0x)
- 🎮 Keyboard navigation (arrow keys, spacebar for play/pause)
- 📝 Speaker notes with detailed scripts
- 🔄 Auto-advance to next slide after audio completion
- 📱 Responsive design for all devices

## Usage

Visit the collection at: [cameronsb.github.io/slides](https://cameronsb.github.io/slides)

### Controls

- **Arrow Keys**: Navigate between slides
- **Spacebar**: Play/pause audio
- **S**: Toggle speaker notes
- **Speed Slider**: Adjust narration speed

## Local Development

1. Clone the repository
2. Run a local server:
   ```bash
   python3 -m http.server 8000
   ```
3. Open http://localhost:8000 in your browser

## Adding New Slideshows

1. Create a new directory for your slideshow
2. Copy the template from an existing slideshow
3. Update the content and generate audio files
4. Add an entry to the main index.html

## Audio Generation

To generate audio files for a slideshow:

1. Navigate to the slideshow directory
2. Run the generation script:
   ```bash
   python generate_slideshow_audio.py
   ```

## Technologies

- Pure HTML/CSS/JavaScript (no dependencies)
- OpenAI Text-to-Speech API for narration
- GitHub Pages for hosting