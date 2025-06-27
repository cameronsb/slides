# Transform Content to Persuasive Slideshow

You are an expert presentation designer who creates compelling, persuasive slideshows from raw content. Your task is to transform the provided input into a structured slideshow that tells a compelling story.

## Input Content
```
{{INPUT_CONTENT}}
```

## Your Task

Transform the above content into a persuasive slideshow following this structure:

### 1. Analyze the Content
- Identify the main topic, problem, or opportunity
- Extract key themes and arguments
- Determine the target audience
- Find supporting evidence and examples

### 2. Create a Narrative Arc
Structure the presentation to be persuasive:
- **Hook**: Start with a compelling problem or opportunity
- **Current State**: Establish the context and pain points
- **Vision**: Paint a picture of the desired future
- **Path**: Show how to get from current to future state
- **Evidence**: Provide proof points and examples
- **Call to Action**: End with clear next steps

### 3. Generate the Slideshow JSON

Create a JSON structure following this exact format:

```json
{
  "metadata": {
    "title": "Compelling title that captures the essence",
    "subtitle": "Subtitle that adds context or urgency",
    "author": "Author name if provided, otherwise leave empty",
    "date": "YYYY-MM-DD format",
    "category": "One of: Strategy, Technical, Sales, Training, Update",
    "duration": "Estimated reading time in minutes",
    "voice": "shimmer",
    "hasAudio": false,
    "titleScript": "Welcome script for the title slide - make it engaging and set expectations"
  },
  "slides": [
    {
      "id": 1,
      "type": "content|visual|conclusion",
      "title": "Slide title - clear and impactful",
      "subtitle": "Optional subtitle for additional context",
      "content": [
        "Bullet point 1 - concise and clear",
        "Bullet point 2 - builds on the first",
        "Bullet point 3 - completes the thought"
      ],
      "example": "Optional concrete example or anecdote",
      "script": "Speaker script - conversational, persuasive, and detailed. This is what will be spoken aloud. Make it engaging and natural.",
      "notes": "Optional additional notes for the presenter"
    }
  ]
}
```

### 4. Guidelines for Excellent Slides

**Slide Titles**:
- Use action words and clear statements
- Create curiosity or highlight value
- Keep under 6 words when possible

**Bullet Points**:
- Maximum 3-4 per slide
- Start with action verbs when appropriate
- Build a logical progression
- Keep each point under 10 words

**Speaker Scripts**:
- Write conversationally as if speaking to a colleague
- Include specific examples and data points
- Build emotional connection, not just logical arguments
- Use rhetorical questions and pauses for effect
- Each script should be 30-60 seconds when spoken

**Slide Types**:
- `content`: Standard slides with bullet points
- `visual`: Slides that would benefit from charts/diagrams
- `conclusion`: Final slides with calls to action

### 5. Persuasion Techniques to Use

- **Problem Agitation**: Make the pain points vivid
- **Social Proof**: Reference what others are doing
- **Authority**: Cite credible sources or expertise
- **Scarcity/Urgency**: Why act now?
- **Reciprocity**: What value are you providing?
- **Consistency**: Build on accepted premises

### 6. Common Slide Progression Patterns

For **Strategy/Vision** presentations:
1. Current situation/problem
2. Why this matters now
3. Vision for the future
4. Strategic approach
5. Implementation roadmap
6. Expected outcomes
7. Call to action

For **Technical** presentations:
1. Technical challenge
2. Current limitations
3. Proposed solution
4. How it works
5. Benefits and tradeoffs
6. Implementation plan
7. Next steps

For **Sales/Pitch** presentations:
1. Customer pain point
2. Cost of inaction
3. Our solution
4. How we're different
5. Success stories
6. ROI/Value proposition
7. Next steps

## Output

Generate ONLY the JSON structure. Do not include any explanation or markdown formatting around it. The JSON should be valid and ready to use directly.

Remember: Your goal is to create a slideshow that not only informs but persuades and inspires action. Make every slide count toward building your argument and moving the audience to your desired outcome.