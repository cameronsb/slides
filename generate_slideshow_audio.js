#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const https = require('https');

// Read the slideshow HTML to extract scripts
async function extractSlideshowScripts() {
    const htmlContent = await fs.readFile('engineering_slideshow.html', 'utf-8');
    
    // Extract slideshowData from the HTML
    const match = htmlContent.match(/const slideshowData = ({[\s\S]*?});/);
    if (!match) {
        throw new Error('Could not find slideshowData in HTML');
    }
    
    // Parse the JavaScript object
    const slideshowDataStr = match[1];
    const slideshowData = eval('(' + slideshowDataStr + ')');
    
    // Prepare scripts array
    const scripts = [];
    
    // Title slide script
    scripts.push({
        id: 'slide-0',
        text: "Welcome! This presentation outlines a systematic approach to improving our engineering organization. We'll cover the current challenges and propose a structured framework for implementing AI-powered workflow improvements."
    });
    
    // Content slides scripts
    slideshowData.slides.forEach((slide, index) => {
        scripts.push({
            id: `slide-${index + 1}`,
            text: slide.script
        });
    });
    
    return scripts;
}

// Make API call to OpenAI TTS
async function generateAudio(text, voice = 'shimmer') {
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (!apiKey) {
        throw new Error('OPENAI_API_KEY environment variable is required');
    }
    
    const data = JSON.stringify({
        model: 'tts-1',
        input: text,
        voice: voice
    });
    
    const options = {
        hostname: 'api.openai.com',
        port: 443,
        path: '/v1/audio/speech',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
            'Content-Length': data.length
        }
    };
    
    return new Promise((resolve, reject) => {
        const chunks = [];
        
        const req = https.request(options, (res) => {
            if (res.statusCode !== 200) {
                let errorBody = '';
                res.on('data', chunk => errorBody += chunk);
                res.on('end', () => {
                    reject(new Error(`API error ${res.statusCode}: ${errorBody}`));
                });
                return;
            }
            
            res.on('data', (chunk) => chunks.push(chunk));
            res.on('end', () => resolve(Buffer.concat(chunks)));
        });
        
        req.on('error', (e) => reject(e));
        req.write(data);
        req.end();
    });
}

// Main function
async function main() {
    try {
        console.log('🎙️  Generating audio files for engineering slideshow...\n');
        
        // Create audio directory
        const audioDir = path.join(__dirname, 'slideshow_audio');
        await fs.mkdir(audioDir, { recursive: true });
        
        // Extract scripts
        const scripts = await extractSlideshowScripts();
        console.log(`📝 Found ${scripts.length} scripts to convert\n`);
        
        // Process each script
        for (let i = 0; i < scripts.length; i++) {
            const script = scripts[i];
            const filename = path.join(audioDir, `${script.id}.mp3`);
            
            console.log(`[${i + 1}/${scripts.length}] Generating ${script.id}...`);
            
            try {
                // Check if file already exists
                await fs.access(filename);
                console.log(`   ✓ Already exists, skipping`);
            } catch {
                // File doesn't exist, generate it
                const audioBuffer = await generateAudio(script.text);
                await fs.writeFile(filename, audioBuffer);
                console.log(`   ✓ Generated successfully`);
                
                // Add delay to avoid rate limiting
                if (i < scripts.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }
        }
        
        console.log('\n✅ All audio files generated successfully!');
        console.log(`📁 Audio files saved to: ${audioDir}`);
        
        // Generate a manifest file for easy reference
        const manifest = {
            voice: 'shimmer',
            model: 'tts-1',
            generated: new Date().toISOString(),
            files: scripts.map(s => ({
                id: s.id,
                filename: `${s.id}.mp3`,
                textLength: s.text.length
            }))
        };
        
        await fs.writeFile(
            path.join(audioDir, 'manifest.json'),
            JSON.stringify(manifest, null, 2)
        );
        
        console.log('📋 Manifest file created: slideshow_audio/manifest.json');
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

// Check for API key
if (!process.env.OPENAI_API_KEY) {
    console.error('❌ Error: OPENAI_API_KEY environment variable is required');
    console.error('\nTo set it temporarily:');
    console.error('  export OPENAI_API_KEY="your-api-key-here"');
    console.error('\nOr create a .env file in this directory with:');
    console.error('  OPENAI_API_KEY=your-api-key-here');
    console.error('\nThen run: node generate_slideshow_audio.js');
    process.exit(1);
}

// Run the script
main();