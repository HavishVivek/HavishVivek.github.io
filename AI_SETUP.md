# AI Chat Setup Guide

This guide explains how to set up the AI-powered chat that knows all your blog content.

## Overview

The chat system uses a knowledge base extracted from your blog HTML files. It can:
1. Search through all your blog content
2. Answer questions based on your actual blog posts
3. Use AI (OpenAI) for intelligent responses (optional)

## Step 1: Extract Blog Content

First, extract content from all your blog HTML files:

```bash
# Install required Python packages
pip install -r requirements.txt

# Extract blog content
python extract_blog_content.py
```

This will create:
- `knowledge_base.json` - Full structured data from all blogs
- `blog_chunks.json` - Text chunks for embedding generation

## Step 2: Create Embeddings (Optional but Recommended)

For better search and AI integration, create embeddings:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Create embeddings
python create_embeddings.py
```

This will create:
- `blog_embeddings.json` - Vector embeddings (for server-side use)
- `blog_search_index.json` - Lightweight search index (for client-side)

**Note:** You can get an OpenAI API key from https://platform.openai.com/api-keys

## Step 3: Deploy Files

Make sure these files are accessible on your website:
- `knowledge_base.json` - Required for basic search
- `blog_search_index.json` - Optional, improves search
- `chat.html` - The chat interface

## Step 4: Configure AI API (Optional)

For AI-powered responses, you have two options:

### Option A: Client-Side OpenAI (Not Recommended for Production)

Add this to `chat.html` before the closing `</script>` tag:

```javascript
// WARNING: This exposes your API key in the browser
// Only use for development/testing
window.OPENAI_API_KEY = "your-api-key-here";
```

### Option B: Server-Side API (Recommended)

Create a backend API endpoint that:
1. Receives the user's question
2. Searches your knowledge base/embeddings
3. Calls OpenAI API with context
4. Returns the response

Then update `chat.html`:

```javascript
window.AI_API_ENDPOINT = "https://your-api.com/chat";
```

## How It Works

1. **Knowledge Base Loading**: On page load, `chat.html` loads `knowledge_base.json`
2. **Search**: When a user asks a question, it searches through all blog content
3. **Response Generation**:
   - If AI API is configured: Uses AI with blog context for intelligent responses
   - Otherwise: Uses keyword matching and returns relevant blog excerpts

## File Structure

```
.
├── extract_blog_content.py    # Extracts content from HTML
├── create_embeddings.py       # Creates embeddings (optional)
├── requirements.txt           # Python dependencies
├── knowledge_base.json        # Extracted blog content (auto-generated)
├── blog_chunks.json           # Text chunks (auto-generated)
├── blog_embeddings.json       # Vector embeddings (auto-generated)
├── blog_search_index.json     # Search index (auto-generated)
└── chat.html                  # Chat interface
```

## Updating the Knowledge Base

When you add new blog posts:

1. Run `python extract_blog_content.py` again
2. (Optional) Run `python create_embeddings.py` to update embeddings
3. Upload the updated JSON files to your website

## Troubleshooting

### Knowledge base not loading
- Check browser console for errors
- Ensure `knowledge_base.json` is in the same directory as `chat.html`
- Check file permissions

### AI responses not working
- Verify API key is set correctly
- Check browser console for API errors
- Ensure CORS is configured if using a custom API endpoint

### Search not finding content
- Run `extract_blog_content.py` again to regenerate knowledge base
- Check that blog HTML files are in expected locations
- Verify blog HTML structure is correct

## Security Notes

⚠️ **Never commit API keys to version control!**

- Use environment variables for API keys
- For production, always use a server-side API
- Client-side API keys can be exposed in browser source code

## Next Steps

1. Extract your blog content: `python extract_blog_content.py`
2. Test the chat interface - it should work with basic search
3. (Optional) Set up embeddings and AI API for better responses
4. Customize the chat interface styling if needed

## Support

If you encounter issues:
1. Check the browser console for errors
2. Verify all JSON files are generated correctly
3. Test with a simple question first
4. Review the knowledge base JSON structure








