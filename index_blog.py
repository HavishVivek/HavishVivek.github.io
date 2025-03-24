# app.py - Main application file

import os
import yaml
import markdown
from bs4 import BeautifulSoup
import pickle
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify, render_template
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global variables for models
embedding_model = None
llm_model = None
llm_tokenizer = None
blog_index = {}

def extract_jekyll_content(blog_dir):
    """Extract content from Jekyll blog posts"""
    blog_data = []
    
    logger.info(f"Extracting content from {blog_dir}")
    
    for root, _, files in os.walk(blog_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split front matter and content
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            front_matter = yaml.safe_load(parts[1])
                            main_content = parts[2]
                            
                            # Convert markdown to plain text
                            html = markdown.markdown(main_content)
                            text = BeautifulSoup(html, 'html.parser').get_text()
                            
                            blog_data.append({
                                'title': front_matter.get('title', ''),
                                'date': front_matter.get('date', ''),
                                'content': text,
                                'slug': os.path.splitext(file)[0],
                                'categories': front_matter.get('categories', []),
                                'tags': front_matter.get('tags', [])
                            })
                            logger.info(f"Processed: {front_matter.get('title', '')}")
                except Exception as e:
                    logger.error(f"Error processing {filepath}: {e}")
    
    logger.info(f"Extracted {len(blog_data)} blog posts")
    return blog_data

def initialize_models():
    """Initialize and load all required models"""
    global embedding_model, llm_model, llm_tokenizer, blog_index
    
    # Check if we have a saved index
    if os.path.exists('blog_index.pkl'):
        logger.info("Loading existing blog index")
        with open('blog_index.pkl', 'rb') as f:
            blog_index = pickle.load(f)
    else:
        logger.info("Creating new blog index")
        # Load sentence transformer model for embeddings
        logger.info("Loading embedding model")
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Process blogs
        blogs = extract_jekyll_content('_posts')
        
        # Create embeddings and index
        for blog in blogs:
            # Skip blogs without titles
            if not blog['title']:
                continue
                
            # Create embedding for the blog content
            embedding = embedding_model.encode(blog['content'])
            
            # Store in the index with the blog title as the key
            blog_title = blog['title'].lower()
            blog_index[blog_title] = {
                'title': blog['title'],
                'content': blog['content'],
                'embedding': embedding,
                'categories': blog.get('categories', []),
                'tags': blog.get('tags', [])
            }
        
        # Save the index to disk
        with open('blog_index.pkl', 'wb') as f:
            pickle.dump(blog_index, f)
    
    # Load language model
    logger.info("Loading language model")
    model_name = "deepseek-ai/deepseek-coder-7b-instruct"
    
    llm_tokenizer = AutoTokenizer.from_pretrained(model_name)
    llm_model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    logger.info("All models initialized successfully")

def chunk_blog_content(content, max_chunk_size=500, overlap=50):
    """Split blog content into manageable chunks"""
    words = content.split()
    chunks = []
    
    for i in range(0, len(words), max_chunk_size - overlap):
        chunk = ' '.join(words[i:i + max_chunk_size])
        chunks.append(chunk)
    
    return chunks

def find_blog_by_name(query):
    """Find a blog by name in the query"""
    query_lower = query.lower()
    
    # Try exact matching first
    for blog_title in blog_index:
        if blog_title in query_lower:
            return blog_index[blog_title]
    
    # Try fuzzy matching if no exact match
    best_match = None
    highest_score = 0
    
    for blog_title in blog_index:
        # Simple word overlap score
        title_words = set(blog_title.split())
        query_words = set(query_lower.split())
        overlap = len(title_words.intersection(query_words))
        
        if overlap > highest_score:
            highest_score = overlap
            best_match = blog_index[blog_title]
    
    # Return the best match if it has at least one word overlap
    if highest_score > 0:
        return best_match
    
    return None

def answer_blog_query(user_query):
    """Generate an answer to a user query about a blog"""
    # Find the blog
    blog_found = find_blog_by_name(user_query)
    
    if not blog_found:
        return "I couldn't find a blog with that name in my database. Could you specify which blog you're asking about?"
    
    # Chunk the content if needed
    blog_content = blog_found['content']
    if len(blog_content) > 4000:  # Arbitrary threshold
        chunks = chunk_blog_content(blog_content)
        blog_content = chunks[0]  # Use the first chunk for now
    
    # Construct prompt with blog content for context
    prompt = f"""
You are an AI assistant that helps answer questions about blog posts.

Blog Title: {blog_found['title']}

Blog Content: 
{blog_content[:4000]}  # Limit content size to fit model context

Question: {user_query}

Please answer the question based on the blog content above. Be concise and accurate.
"""
    
    # Generate response
    inputs = llm_tokenizer(prompt, return_tensors="pt").to(llm_model.device)
    with torch.no_grad():
        outputs = llm_model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True
        )
    
    response = llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the answer part (after the prompt)
    try:
        answer = response.split("Please answer the question based on the blog content above.")[1].strip()
    except IndexError:
        # If splitting fails, return the whole response
        answer = response
    
    return answer

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle user queries and generate responses"""
    user_query = request.json.get('query', '')
    
    if not user_query:
        return jsonify({'response': 'Please enter a question.'})
    
    try:
        response = answer_blog_query(user_query)
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return jsonify({'response': f"Sorry, I encountered an error: {str(e)}"})

@app.route('/list_blogs')
def list_blogs():
    """Return a list of all available blogs"""
    blog_titles = [blog_index[key]['title'] for key in blog_index]
    return jsonify({'blogs': sorted(blog_titles)})

def create_templates_directory():
    """Create the templates directory and index.html file if they don't exist"""
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    index_html = """<!DOCTYPE html>
<html>
<head>
    <title>Blog Chat Assistant</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            line-height: 1.6;
        }
        h1 { 
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        #chat-container { 
            height: 400px; 
            border: 1px solid #ccc; 
            border-radius: 5px;
            overflow-y: auto; 
            padding: 15px; 
            margin-bottom: 15px; 
            background: #f9f9f9;
        }
        .user-message {
            background: #e1f5fe;
            padding: 8px 12px;
            border-radius: 15px;
            margin-bottom: 10px;
            max-width: 80%;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background: #f0f0f0;
            padding: 8px 12px;
            border-radius: 15px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        #user-input { 
            width: 75%; 
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }
        button { 
            padding: 10px 15px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        #blog-list {
            margin-top: 20px;
            border-top: 1px solid #eee;
            padding-top: 15px;
        }
        #blog-list h3 {
            margin-bottom: 10px;
        }
        #blogs {
            columns: 2;
            list-style-type: none;
            padding: 0;
        }
        #blogs li {
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 3px;
        }
        #blogs li:hover {
            background: #f0f0f0;
        }
        .loading { 
            color: #888; 
            font-style: italic; 
        }
    </style>
</head>
<body>
    <h1>Blog Chat Assistant</h1>
    <p>Ask questions about any blog post on this site. Example: "What is the main topic of the blog titled [blog name]?"</p>
    <div id="chat-container"></div>
    <div style="display: flex; gap: 10px;">
        <input type="text" id="user-input" placeholder="Ask about a blog...">
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <div id="blog-list">
        <h3>Available Blogs</h3>
        <ul id="blogs"></ul>
    </div>

    <script>
        // Load available blogs when page loads
        window.onload = function() {
            fetch('/list_blogs')
                .then(response => response.json())
                .then(data => {
                    const blogsList = document.getElementById('blogs');
                    data.blogs.forEach(blog => {
                        const li = document.createElement('li');
                        li.textContent = blog;
                        li.onclick = function() {
                            document.getElementById('user-input').value = 
                                `Tell me about the blog "${blog}"`;
                        };
                        blogsList.appendChild(li);
                    });
                });
        };
        
        function sendMessage() {
            const userInput = document.getElementById('user-input');
            const chatContainer = document.getElementById('chat-container');
            
            if (!userInput.value.trim()) return;
            
            // Add user message to chat
            const userMessage = document.createElement('div');
            userMessage.className = 'user-message';
            userMessage.textContent = userInput.value;
            chatContainer.appendChild(userMessage);
            
            // Add loading message
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'bot-message loading';
            loadingMessage.textContent = 'Thinking...';
            chatContainer.appendChild(loadingMessage);
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            // Send to backend
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: userInput.value
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Remove loading message
                chatContainer.removeChild(loadingMessage);
                
                // Add bot response to chat
                const botMessage = document.createElement('div');
                botMessage.className = 'bot-message';
                botMessage.textContent = data.response;
                chatContainer.appendChild(botMessage);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            })
            .catch(error => {
                // Remove loading message
                chatContainer.removeChild(loadingMessage);
                
                // Add error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'bot-message';
                errorMessage.textContent = 'Sorry, there was an error processing your request.';
                chatContainer.appendChild(errorMessage);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });
            
            userInput.value = '';
        }
        
        // Allow Enter key to send message
        document.getElementById('user-input').addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""
    
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    
    logger.info("Created templates directory and index.html")

if __name__ == '__main__':
    # Create the templates directory if it doesn't exist
    create_templates_directory()
    
    # Initialize models
    initialize_models()
    
    # Start the Flask server
    app.run(debug=True, host='0.0.0.0', port=5001)