#!/usr/bin/env python3
"""
Generate MP3 audio files for slideshow from JSON data.

This script:
1. Reads slideshow_data.json in the current directory
2. Extracts all speaker scripts
3. Generates MP3 files using OpenAI TTS
4. Updates the JSON to mark audio as generated

Usage:
    cd slideshow-directory
    python ../_tools/generate_audio.py
"""

import os
import json
import time
from pathlib import Path
import urllib.request
import urllib.error

def get_api_key():
    """Get API key from the absolute path."""
    key_file_path = '/Users/cam/keys/openai-key.js'
    
    try:
        with open(key_file_path, 'r') as f:
            content = f.read()
        
        # Extract the API key from the JS export
        import re
        match = re.search(r'OPENAI_API_KEY\s*=\s*["\'](.*?)["\']', content)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("Could not find OPENAI_API_KEY in key file")
    except FileNotFoundError:
        raise ValueError(f"Key file not found at {key_file_path}")
    except Exception as e:
        raise ValueError(f"Error reading key file: {e}")

def load_slideshow_data():
    """Load slideshow data from JSON file."""
    json_path = Path('slideshow_data.json')
    
    if not json_path.exists():
        raise FileNotFoundError("slideshow_data.json not found. Run this script from the slideshow directory.")
    
    with open(json_path, 'r') as f:
        return json.load(f)

def extract_scripts(slideshow_data):
    """Extract all scripts from slideshow data."""
    scripts = []
    
    # Title slide script
    title_script = slideshow_data['metadata'].get('titleScript', 
        f"Welcome to {slideshow_data['metadata']['title']}. {slideshow_data['metadata'].get('subtitle', '')}")
    
    scripts.append({
        'id': 'slide-0',
        'text': title_script
    })
    
    # Content slides scripts
    for i, slide in enumerate(slideshow_data['slides']):
        script_text = slide.get('script', f"Slide {i + 1}: {slide.get('title', 'No title')}")
        scripts.append({
            'id': f'slide-{i + 1}',
            'text': script_text
        })
    
    return scripts

def generate_audio(text, voice='shimmer'):
    """Generate audio using OpenAI TTS API."""
    api_key = get_api_key()
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data_json = json.dumps({
        'model': 'tts-1',
        'input': text,
        'voice': voice
    }).encode('utf-8')
    
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

def update_slideshow_metadata(slideshow_data):
    """Update slideshow metadata to indicate audio has been generated."""
    slideshow_data['metadata']['hasAudio'] = True
    slideshow_data['metadata']['audioGeneratedAt'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    
    with open('slideshow_data.json', 'w') as f:
        json.dump(slideshow_data, f, indent=2)

def update_html_file(slideshow_data):
    """Update the HTML file with the new slideshow data."""
    html_path = Path('index.html')
    
    if not html_path.exists():
        print("⚠️  Warning: index.html not found. Audio files generated but HTML not updated.")
        return
    
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    # Find and replace the slideshowData
    import re
    pattern = r'let slideshowData = {.*?};'
    replacement = f'let slideshowData = {json.dumps(slideshow_data, indent=8)};'
    
    # Adjust indentation for the replacement
    replacement_lines = replacement.split('\n')
    replacement_lines = [replacement_lines[0]] + ['        ' + line for line in replacement_lines[1:]]
    replacement = '\n'.join(replacement_lines)
    
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    with open(html_path, 'w') as f:
        f.write(html_content)

def main():
    """Main function to generate all audio files."""
    print("🎙️  Generating audio files for slideshow...\n")
    
    try:
        # Load slideshow data
        slideshow_data = load_slideshow_data()
        voice = slideshow_data['metadata'].get('voice', 'shimmer')
        
        print(f"📚 Loaded slideshow: {slideshow_data['metadata']['title']}")
        print(f"🎤 Using voice: {voice}\n")
        
        # Create audio directory
        audio_dir = Path('slideshow_audio')
        audio_dir.mkdir(exist_ok=True)
        
        # Extract scripts
        scripts = extract_scripts(slideshow_data)
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
                audio_data = generate_audio(script['text'], voice)
                
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
        
        # Update metadata
        update_slideshow_metadata(slideshow_data)
        update_html_file(slideshow_data)
        
        # Generate manifest file
        manifest = {
            'voice': voice,
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
        print(f"✨ Slideshow data updated with hasAudio: true")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    # Try to load API key
    try:
        get_api_key()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nExpected key file at: /Users/cam/keys/openai-key.js")
        exit(1)
    
    exit(main())