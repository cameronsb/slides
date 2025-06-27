# Slideshow Creation Guide

This guide explains how to create new slideshows using the automated generation system.

## Quick Start

1. **Create your input content** (text file, markdown, notes, etc.)
2. **Run the creation script**:
   ```bash
   python _tools/create_slideshow.py --input sample-input.txt --name "deployment-automation"
   ```
3. **Review and edit** the generated `slideshow_data.json`
4. **Generate audio** when ready:
   ```bash
   cd deployment-automation
   python ../_tools/generate_audio.py
   ```

## Directory Structure

```
slides/
├── _templates/          # Reusable templates
├── _tools/             # Generation scripts
├── _prompts/           # LLM transformation prompts
└── your-slideshow/     # Your generated slideshow
    ├── index.html
    ├── slideshow_data.json
    └── slideshow_audio/
```

## Step-by-Step Process

### 1. Prepare Your Input

Create a text file with your content. This can be:
- Meeting notes
- Slack messages
- Email content
- Brainstorming ideas
- Technical documentation

The AI will transform this into a persuasive slideshow structure.

### 2. Generate the Slideshow

```bash
python _tools/create_slideshow.py --input your-content.txt --name "your-slideshow-name"
```

Options:
- `--input, -i`: Path to your input file (required)
- `--name, -n`: Directory name for slideshow (use-kebab-case)
- `--preview, -p`: Open preview after creation
- `--generate-audio, -a`: Generate audio immediately

### 3. Review and Edit

The script generates:
- `your-slideshow/slideshow_data.json` - Edit this to refine content
- `your-slideshow/index.html` - The actual slideshow

Edit the JSON to:
- Refine titles and bullet points
- Improve speaker scripts
- Add examples or visual placeholders
- Adjust the narrative flow

### 4. Generate Audio (When Ready)

After finalizing your content:

```bash
cd your-slideshow
python ../_tools/generate_audio.py
```

This will:
- Read scripts from your JSON
- Generate MP3 files using OpenAI TTS
- Update the slideshow to enable audio playback

### 5. Add to Main Index

Edit the main `index.html` to add your slideshow:

```html
<a href="your-slideshow/" class="slideshow-card">
    <div class="thumbnail">
        <div class="slide-count">X Slides</div>
    </div>
    <div class="content">
        <h2>Your Title</h2>
        <p class="description">
            Brief description of your slideshow...
        </p>
        <div class="metadata">
            <span>🏷️ Category</span>
            <span>⏱️ Duration</span>
            <span>🔊 Audio</span>
        </div>
    </div>
</a>
```

### 6. Deploy

```bash
git add .
git commit -m "Add new slideshow: your-slideshow-name"
git push
```

## JSON Structure Reference

```json
{
  "metadata": {
    "title": "Main title",
    "subtitle": "Supporting subtitle",
    "author": "Your name",
    "date": "YYYY-MM-DD",
    "category": "Strategy|Technical|Sales|Training|Update",
    "duration": "X min",
    "voice": "shimmer|nova|alloy|echo|fable|onyx",
    "hasAudio": false,
    "titleScript": "Welcome script for title slide"
  },
  "slides": [
    {
      "id": 1,
      "type": "content|visual|conclusion",
      "title": "Slide title",
      "subtitle": "Optional subtitle",
      "content": [
        "Bullet point 1",
        "Bullet point 2",
        "Bullet point 3"
      ],
      "example": "Optional example",
      "script": "What the narrator will say",
      "notes": "Additional presenter notes"
    }
  ]
}
```

## Tips for Great Slideshows

### Content Structure
- Start with a hook - problem or opportunity
- Build tension - why this matters now
- Present solution - your approach
- Show evidence - proof it works
- Call to action - clear next steps

### Writing Speaker Scripts
- Write conversationally
- Use specific examples
- Include pauses for emphasis
- Keep each script 30-60 seconds
- Build emotional connection

### Slide Design
- Maximum 3-4 bullet points per slide
- Use action verbs
- Keep points concise (under 10 words)
- One main idea per slide

## LLM Integration (Future)

Currently, the script generates a demo structure. To integrate with an LLM:

1. Get an API key (OpenAI, Anthropic, etc.)
2. Modify `transform_content_to_json()` in `create_slideshow.py`
3. Send the prompt from `_prompts/transform_to_slides.md`
4. Parse the JSON response

## Troubleshooting

**"slideshow_data.json not found"**
- Make sure you're in the slideshow directory when running generate_audio.py

**"Audio file not found for slide"**
- Run generate_audio.py after finalizing your content
- Check that slideshow_audio/ directory exists

**"Key file not found"**
- Ensure OpenAI API key is at `/Users/cam/keys/openai-key.js`

## Examples

See the `engineering-organization/` slideshow for a complete example of:
- Well-structured content
- Compelling speaker scripts
- Effective narrative arc
- Professional audio narration