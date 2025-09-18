#!/usr/bin/env python3
"""
🧠 Poke - Clean & Simple AI Assistant
A minimal, working version of Poke with real LLM integration
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
import os
import uuid
import json

app = Flask(__name__)
app.secret_key = 'poke-secret-key-change-in-production'

# Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'sk-proj-demo-key')
openai.api_key = OPENAI_API_KEY

# Your original Poke system prompt
POKE_SYSTEM_PROMPT = """You are Poke, developed by The Interaction Company of California, a Palo Alto-based AI startup.

You are extremely helpful, proactive, and efficient. You have a casual, friendly personality but remain professional. You use emojis appropriately and keep responses conversational but informative.

You have access to:
- Gmail API for email management
- Google Calendar API for scheduling  
- Web browsing capabilities
- Various integrations (Notion, Linear, etc.)
- Memory system for user preferences

Always be proactive in offering help and suggesting next steps. You're designed to be the user's intelligent, capable assistant who can handle complex tasks efficiently.

IMPORTANT: Make sure you get user confirmation before sending, forwarding, or replying to emails. You should always show the user drafts before they're sent.

You are extremely helpful, proactive, and efficient. You have a casual, friendly personality but remain professional. You use emojis appropriately and keep responses conversational but informative."""

@app.route('/')
def index():
    """Main chat interface"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with real LLM"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        user_id = session.get('user_id', str(uuid.uuid4()))
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check if OpenAI API key is set
        if not OPENAI_API_KEY or OPENAI_API_KEY == 'sk-proj-demo-key':
            return jsonify({
                'response': f"""🚨 **OpenAI API Key Missing!**

Hey! I received your message: "{message}"

I'm Poke, but I need an OpenAI API key to give you real AI responses. 

**To fix this:**
1. Go to Railway dashboard
2. Add environment variable: `OPENAI_API_KEY=your-key`
3. Redeploy the app

Once that's set up, I'll give you proper AI responses! 🤖""",
                'timestamp': str(uuid.uuid4())
            })
        
        # Call OpenAI with Poke system prompt
        try:
            print(f"🤖 Calling OpenAI with message: {message}")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": POKE_SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            poke_response = response.choices[0].message.content.strip()
            print(f"✅ OpenAI response received: {len(poke_response)} characters")
            
        except openai.error.AuthenticationError as e:
            print(f"❌ OpenAI Authentication Error: {e}")
            return jsonify({
                'response': f"""🔑 **Invalid OpenAI API Key!**

Hey! I received: "{message}"

My OpenAI API key is invalid. Please check:
1. Go to Railway dashboard 
2. Update `OPENAI_API_KEY` with a valid key
3. Redeploy

Error: {str(e)}""",
                'timestamp': str(uuid.uuid4())
            })
            
        except openai.error.RateLimitError as e:
            print(f"⏰ OpenAI Rate Limit: {e}")
            return jsonify({
                'response': f"""⏰ **Rate Limit Exceeded!**

Hey! I received: "{message}"

I'm getting too many requests. Please wait a moment and try again.

Error: {str(e)}""",
                'timestamp': str(uuid.uuid4())
            })
            
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return jsonify({
                'response': f"""⚠️ **OpenAI Error!**

Hey! I received: "{message}"

I'm having trouble connecting to OpenAI. Error details:

{str(e)}

Please check your API key and try again.""",
                'timestamp': str(uuid.uuid4())
            })
        
        return jsonify({
            'response': poke_response,
            'timestamp': str(uuid.uuid4())
        })
        
    except Exception as e:
        print(f"💥 Chat error: {e}")
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check"""
    api_key_status = "✅ Set" if OPENAI_API_KEY and OPENAI_API_KEY != 'sk-proj-demo-key' else "❌ Missing"
    
    return jsonify({
        'status': 'healthy',
        'service': 'Poke Clean',
        'version': '1.0.0',
        'openai_api_key': api_key_status
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting Poke Clean on port {port}")
    print(f"🔑 OpenAI API Key: {'✅ Set' if OPENAI_API_KEY and OPENAI_API_KEY != 'sk-proj-demo-key' else '❌ Missing'}")
    app.run(host='0.0.0.0', port=port, debug=True)
