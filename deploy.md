# 🚀 Deploy Poke Clean to Railway

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `poke-clean`
3. Description: `🧠 Clean & Simple Poke AI Assistant`
4. Make it Public
5. Click "Create repository"

## Step 2: Push Code

```bash
cd /Users/CEF/Downloads/poke-clean
git remote set-url origin https://github.com/YOUR_USERNAME/poke-clean.git
git push -u origin poke-clean
```

## Step 3: Deploy to Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `poke-clean` repository
5. Select the `poke-clean` branch
6. Add Environment Variable:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
7. Click Deploy!

## Step 4: Test

Your app will be live at: `https://your-app.up.railway.app`

## Files Ready for Deployment:

✅ `app.py` - Flask app with real OpenAI integration
✅ `requirements.txt` - Dependencies (Flask + OpenAI)
✅ `Procfile` - Railway deployment config
✅ `templates/chat.html` - iMessage-style UI
✅ `.gitignore` - Clean git history
✅ `README.md` - Setup instructions

**This is a clean, simple version that just works! 🎯**
