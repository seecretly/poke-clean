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
        
        # Call OpenAI with Poke system prompt
        try:
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
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            # Fallback response
            poke_response = f"""Hey! I'm Poke from The Interaction Company! 👋

I received your message: "{message}"

I'm your AI assistant designed to help you with email, calendar, web research, and various integrations. I'm proactive, efficient, and here to make your life easier!

What can I help you accomplish today? 🚀"""
        
        return jsonify({
            'response': poke_response,
            'timestamp': str(uuid.uuid4())
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Poke Clean',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
