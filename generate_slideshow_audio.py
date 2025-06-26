#!/usr/bin/env python3
"""
Generate MP3 audio files for engineering slideshow using OpenAI TTS API.

Usage:
    export OPENAI_API_KEY="your-api-key-here"
    python generate_slideshow_audio.py
"""

import os
import json
import re
import time
from pathlib import Path
import urllib.request
import urllib.error

def extract_slideshow_scripts():
    """Extract all scripts from the slideshow HTML file."""
    with open('engineering_slideshow.html', 'r') as f:
        html_content = f.read()

    # Extract slideshowData JavaScript object
    match = re.search(r'const slideshowData = ({[\s\S]*?});', html_content)
    if not match:
        raise ValueError("Could not find slideshowData in HTML")

    # Parse the JavaScript object (simplified approach)
    slideshow_data_str = match.group(1)

    scripts = []

    # Title slide script
    scripts.append({
        'id': 'slide-0',
        'text': "Welcome! This presentation outlines a systematic approach to improving our engineering organization. We'll cover the current challenges and propose a structured framework for implementing AI-powered workflow improvements."
    })

    # Extract script content using regex
    script_matches = re.findall(r'"script":\s*"([^"]+)"', slideshow_data_str)

    for i, script_text in enumerate(script_matches):
        scripts.append({
            'id': f'slide-{i + 1}',
            'text': script_text
        })

    return scripts

def get_api_key():
    """Get API key from the absolute path."""
    key_file_path = '/Users/cam/keys/openai-key.js'
    
    try:
        with open(key_file_path, 'r') as f:
            content = f.read()
        
        # Extract the API key from the JS export
        match = re.search(r'OPENAI_API_KEY\s*=\s*["\'](.*?)["\']', content)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("Could not find OPENAI_API_KEY in key file")
    except FileNotFoundError:
        raise ValueError(f"Key file not found at {key_file_path}")
    except Exception as e:
        raise ValueError(f"Error reading key file: {e}")

def generate_audio(text, voice='shimmer'):
    """Generate audio using OpenAI TTS API."""
    api_key = get_api_key()

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'tts-1',
        'input': text,
        'voice': voice
    }

    data_json = json.dumps(data).encode('utf-8')
    
    request = urllib.request.Request(
        'https://api.openai.com/v1/audio/speech',
        data=data_json,
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            if response.status != 200:
                error_data = response.read().decode('utf-8')
                raise Exception(f"API error {response.status}: {error_data}")
            return response.read()
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        raise Exception(f"API error {e.code}: {error_data}")

def main():
    """Main function to generate all audio files."""
    print("🎙️  Generating audio files for engineering slideshow...\n")

    # Create audio directory
    audio_dir = Path('slideshow_audio')
    audio_dir.mkdir(exist_ok=True)

    try:
        # Extract scripts
        scripts = extract_slideshow_scripts()
        print(f"📝 Found {len(scripts)} scripts to convert\n")

        # Process each script
        for i, script in enumerate(scripts):
            filename = audio_dir / f"{script['id']}.mp3"

            print(f"[{i + 1}/{len(scripts)}] Generating {script['id']}...")

            if filename.exists():
                print(f"   ✓ Already exists, skipping")
                continue

            try:
                # Generate audio
                audio_data = generate_audio(script['text'])

                # Save to file
                with open(filename, 'wb') as f:
                    f.write(audio_data)

                print(f"   ✓ Generated successfully")

                # Add delay to avoid rate limiting (except for last item)
                if i < len(scripts) - 1:
                    time.sleep(1)

            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue

        # Generate manifest file
        manifest = {
            'voice': 'shimmer',
            'model': 'tts-1',
            'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'files': [
                {
                    'id': s['id'],
                    'filename': f"{s['id']}.mp3",
                    'textLength': len(s['text'])
                }
                for s in scripts
            ]
        }

        with open(audio_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"\n✅ All audio files generated successfully!")
        print(f"📁 Audio files saved to: {audio_dir}")
        print(f"📋 Manifest file created: {audio_dir}/manifest.json")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0

if __name__ == '__main__':
    # Try to load API key from file
    try:
        get_api_key()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nExpected key file at: /Users/cam/keys/openai-key.js")
        print("The file should contain:")
        print('  export const OPENAI_API_KEY = "your-api-key-here";')
        exit(1)

    exit(main())