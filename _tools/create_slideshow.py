#!/usr/bin/env python3
"""
Create a new slideshow from input content.

This script helps you:
1. Read input from various sources (text file, markdown, etc.)
2. Transform it into slideshow JSON using an LLM prompt
3. Generate the HTML slideshow
4. Optionally generate audio files

Usage:
    python create_slideshow.py --input notes.txt --name "my-presentation"
    python create_slideshow.py --input notes.txt --name "my-presentation" --generate-audio
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime

def read_input_file(file_path):
    """Read content from input file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

def read_prompt_template():
    """Read the transformation prompt template."""
    prompt_path = Path(__file__).parent.parent / '_prompts' / 'transform_to_slides.md'
    with open(prompt_path, 'r') as f:
        return f.read()

def transform_content_to_json(input_content):
    """
    Transform input content to slideshow JSON.
    
    In a real implementation, this would call an LLM API.
    For now, we'll create a sample structure that shows what would be generated.
    """
    # This is where you would:
    # 1. Load the prompt template
    # 2. Replace {{INPUT_CONTENT}} with actual content
    # 3. Call LLM API (OpenAI, Claude, etc.)
    # 4. Parse the JSON response
    
    print("\n📝 Analyzing content and generating slideshow structure...")
    print("ℹ️  Note: This is a demo. In production, this would use an LLM to transform your content.")
    
    # For demo purposes, create a sample structure
    sample_json = {
        "metadata": {
            "title": "Transformed Presentation",
            "subtitle": "Generated from your input content",
            "author": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": "Strategy",
            "duration": "8 min",
            "voice": "shimmer",
            "hasAudio": False,
            "titleScript": "Welcome! This presentation was generated from your input content."
        },
        "slides": [
            {
                "id": 1,
                "type": "content",
                "title": "Key Insights from Your Content",
                "content": [
                    "First key point extracted from input",
                    "Second important observation",
                    "Third critical element"
                ],
                "script": "Let's explore the key insights from your content. [This would be generated based on your actual input]"
            },
            {
                "id": 2,
                "type": "content", 
                "title": "The Core Challenge",
                "content": [
                    "Main challenge identified",
                    "Contributing factors",
                    "Impact on stakeholders"
                ],
                "script": "The challenge we're addressing is significant. [LLM would expand on this based on your content]"
            },
            {
                "id": 3,
                "type": "content",
                "title": "Proposed Solution",
                "content": [
                    "Solution approach",
                    "Key benefits",
                    "Implementation strategy"
                ],
                "script": "Here's how we can address this challenge effectively. [Detailed explanation would go here]"
            },
            {
                "id": 4,
                "type": "conclusion",
                "title": "Next Steps",
                "subtitle": "Moving forward together",
                "content": [
                    "Immediate action items",
                    "Timeline for implementation",
                    "Success metrics"
                ],
                "script": "To make this a reality, here are our concrete next steps. [Call to action based on content]"
            }
        ]
    }
    
    # Add a snippet of the actual input to show it was processed
    if len(input_content) > 100:
        snippet = input_content[:100] + "..."
    else:
        snippet = input_content
    
    sample_json["metadata"]["titleScript"] = f"This presentation explores: {snippet}"
    
    return sample_json

def create_slideshow_directory(name):
    """Create directory structure for new slideshow."""
    base_path = Path(__file__).parent.parent
    slideshow_path = base_path / name
    
    if slideshow_path.exists():
        response = input(f"\n⚠️  Directory '{name}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
        shutil.rmtree(slideshow_path)
    
    slideshow_path.mkdir()
    return slideshow_path

def generate_html(slideshow_data, slideshow_path):
    """Generate HTML file from slideshow data and template."""
    template_path = Path(__file__).parent.parent / '_templates' / 'slideshow_template.html'
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Replace placeholders
    html_content = template.replace('{{TITLE}}', slideshow_data['metadata']['title'])
    html_content = html_content.replace('{{SLIDESHOW_DATA}}', json.dumps(slideshow_data, indent=2))
    
    # Write HTML file
    output_path = slideshow_path / 'index.html'
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    return output_path

def save_json_data(slideshow_data, slideshow_path):
    """Save slideshow data as JSON for later editing."""
    json_path = slideshow_path / 'slideshow_data.json'
    with open(json_path, 'w') as f:
        json.dump(slideshow_data, f, indent=2)
    return json_path

def update_main_index(name, slideshow_data):
    """Add new slideshow to main index.html."""
    print("\n📋 To add this slideshow to the main index:")
    print(f"   1. Edit index.html")
    print(f"   2. Add a new card for '{name}' in the slideshows-grid")
    print(f"   3. Use title: {slideshow_data['metadata']['title']}")
    print(f"   4. Use {len(slideshow_data['slides'])} slides count")

def main():
    parser = argparse.ArgumentParser(description='Create a new slideshow from input content')
    parser.add_argument('--input', '-i', required=True, help='Input file path')
    parser.add_argument('--name', '-n', required=True, help='Slideshow directory name (use-kebab-case)')
    parser.add_argument('--generate-audio', '-a', action='store_true', help='Generate audio files after creation')
    parser.add_argument('--preview', '-p', action='store_true', help='Open preview after creation')
    
    args = parser.parse_args()
    
    # Validate name format
    if ' ' in args.name or args.name != args.name.lower():
        print("❌ Error: Slideshow name should be lowercase with hyphens (e.g., 'my-presentation')")
        sys.exit(1)
    
    print(f"🚀 Creating slideshow: {args.name}")
    
    # Step 1: Read input content
    print(f"\n📖 Reading input from: {args.input}")
    input_content = read_input_file(args.input)
    print(f"   ✓ Read {len(input_content)} characters")
    
    # Step 2: Transform content to slideshow JSON
    slideshow_data = transform_content_to_json(input_content)
    print(f"   ✓ Generated {len(slideshow_data['slides'])} slides")
    
    # Step 3: Create directory structure
    print(f"\n📁 Creating slideshow directory: {args.name}/")
    slideshow_path = create_slideshow_directory(args.name)
    
    # Step 4: Generate HTML
    print("\n🎨 Generating HTML slideshow...")
    html_path = generate_html(slideshow_data, slideshow_path)
    print(f"   ✓ Created: {html_path}")
    
    # Step 5: Save JSON data
    json_path = save_json_data(slideshow_data, slideshow_path)
    print(f"   ✓ Saved data: {json_path}")
    
    # Step 6: Update main index
    update_main_index(args.name, slideshow_data)
    
    # Step 7: Generate audio if requested
    if args.generate_audio:
        print("\n🎙️  Generating audio files...")
        audio_script = Path(__file__).parent / 'generate_audio.py'
        os.system(f'cd "{slideshow_path}" && python "{audio_script}"')
    
    # Step 8: Preview if requested
    if args.preview:
        print(f"\n🌐 Opening preview...")
        os.system(f'cd "{slideshow_path}" && python ../../preview_slideshow.py')
    
    print(f"\n✅ Slideshow created successfully!")
    print(f"\n📝 Next steps:")
    print(f"   1. Review and edit: {json_path}")
    print(f"   2. Generate audio: cd {args.name} && python ../_tools/generate_audio.py")
    print(f"   3. Preview locally: cd {args.name} && python ../preview_slideshow.py")
    print(f"   4. Add to main index.html")
    print(f"   5. Commit and push to GitHub")

if __name__ == '__main__':
    main()