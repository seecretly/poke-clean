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

def get_demo_response(message):
    """Generate intelligent demo responses without OpenAI API"""
    message_lower = message.lower().strip()
    
    # Greetings
    if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey', 'sup', 'yo']):
        return """Hey there! 👋 I'm Poke from The Interaction Company!

I'm your AI assistant designed to be incredibly helpful and proactive. I can help you with:

📧 **Email Management** - Search, compose, and organize your Gmail
📅 **Calendar Scheduling** - Create events, find meeting times, manage your schedule  
🌐 **Web Research** - Browse the internet and find exactly what you need
🔗 **Smart Integrations** - Connect with Notion, Linear, and other tools
💭 **Proactive Assistance** - I remember your preferences and suggest next steps

What would you like to accomplish today? I'm here to make your life more efficient! 🚀"""

    # Email questions
    elif any(word in message_lower for word in ['email', 'gmail', 'inbox', 'mail']):
        return """Perfect! Email is one of my superpowers! 📧

I'm designed to revolutionize how you handle email:

• **Smart Search** - Find any email instantly, even with vague descriptions
• **Intelligent Composition** - Write emails in your perfect tone and style
• **Proactive Organization** - Clean up, prioritize, and manage your inbox
• **Draft Review** - I always show you drafts before sending anything
• **Context Awareness** - Remember previous conversations and your preferences

I can help you search for specific emails, compose new messages, or organize your inbox. What email task can I tackle for you?"""

    # Calendar questions  
    elif any(word in message_lower for word in ['calendar', 'schedule', 'meeting', 'event']):
        return """Excellent! Calendar management is another area where I excel! 📅

I can help you with:

• **Smart Scheduling** - Find optimal meeting times across multiple calendars
• **Event Intelligence** - Create detailed events with all the right information  
• **Coordination Master** - Handle complex scheduling with multiple participants
• **Availability Expert** - Check when you're free for weeks ahead
• **Meeting Optimization** - Suggest the best times based on your patterns

What's on your scheduling agenda? I can check your availability, create events, or help coordinate meetings!"""

    # General capabilities
    else:
        return f"""I received your message: "{message}"

I'm Poke, your intelligent AI assistant from The Interaction Company! I'm designed to be proactive, efficient, and incredibly helpful.

Here's what I can help you with:
• 📧 Email management and organization
• 📅 Calendar scheduling and coordination
• 🔍 Research and information gathering  
• 🔗 Integration with your favorite tools
• 💭 Proactive suggestions and task management

I'm built to understand your goals and help you accomplish them efficiently. What would you like to work on together?

*Note: I'm currently running in demo mode. For full AI capabilities, an OpenAI API key is needed.*"""

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
            # Demo mode - intelligent responses without API
            return jsonify({
                'response': get_demo_response(message),
                'timestamp': str(uuid.uuid4())
            })
        
        # Call OpenAI with Poke system prompt
        try:
            print(f"🤖 Calling OpenAI with message: {message}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Much cheaper than gpt-4
                messages=[
                    {"role": "system", "content": POKE_SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,  # Reduced to save costs
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
        'service': 'Poke Clean - UPDATED VERSION',
        'version': '2.0.0',
        'openai_api_key': api_key_status,
        'demo_mode': 'Available',
        'last_updated': '2025-09-18'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting Poke Clean on port {port}")
    print(f"🔑 OpenAI API Key: {'✅ Set' if OPENAI_API_KEY and OPENAI_API_KEY != 'sk-proj-demo-key' else '❌ Missing'}")
    app.run(host='0.0.0.0', port=port, debug=True)
