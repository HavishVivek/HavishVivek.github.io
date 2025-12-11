# AI Chatbot Architecture Explanation

## Important: The Model is NOT Being Trained

The AI model is **NOT being trained**. Instead, it uses **pre-trained models** that have already been trained on large datasets. Your blog content is used as **context** to help the AI answer questions, not to train it.

## How It Works

### 1. **Blog Content Extraction** (`extract_blog_content.py`)

**Source of Blogs:**
- The system looks for HTML files matching these patterns:
  - `blog-*.html` (e.g., `blog-raspberrypi.html`, `blog-arduino.html`)
  - `blog/*.html` (files in the `blog/` directory)
- It skips `blog.html` (the listing page)

**What Gets Extracted:**
- Title, headings (h1-h6)
- Paragraphs
- Code blocks
- Tags/categories
- Full text content

**Output:**
- Creates `knowledge_base.json` - a structured JSON file with all blog content
- Creates `blog_chunks.json` - text chunks suitable for embedding (optional)

### 2. **Optional: FAISS Index Creation** (`create_faiss_index.py`)

**Purpose:** Creates a fast semantic search index for better blog retrieval

**Process:**
- Loads `knowledge_base.json`
- Uses pre-trained embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Creates vector embeddings for each blog post
- Builds a FAISS index for fast similarity search

**Output:**
- `blog_index.faiss` - FAISS vector index
- `blog_texts.json` - Blog metadata matching the index

### 3. **Chatbot Runtime** (`chatbot.py`)

**Pre-trained Models Used:**

1. **Embedding Model** (for finding relevant blogs):
   - Model: `sentence-transformers/all-MiniLM-L6-v2`
   - Purpose: Converts text to vectors for semantic search
   - Already trained on millions of text examples

2. **Text Generation Model** (for answering questions):
   - Model: `gpt2` (from Hugging Face)
   - Purpose: Generates text responses
   - Already trained on large text corpus

**How Questions Are Answered:**

1. **User asks a question** → Frontend sends POST to `/ask` endpoint

2. **Find relevant blog:**
   - If FAISS is available: Uses semantic search to find the most relevant blog
   - If FAISS is not available: Uses keyword matching in `knowledge_base.json`

3. **Generate response:**
   - Takes the relevant blog content
   - Creates a prompt: "Answer based on this blog: [blog content] User: [question] AI:"
   - Uses the pre-trained GPT-2 model to generate a response
   - Returns the answer to the user

## Data Flow Diagram

```
Blog HTML Files (blog-*.html, blog/*.html)
    ↓
extract_blog_content.py
    ↓
knowledge_base.json
    ↓
create_faiss_index.py (optional)
    ↓
blog_index.faiss + blog_texts.json
    ↓
chatbot.py (runtime)
    ↓
User Question → Find Relevant Blog → Generate Answer
```

## Key Points

1. **No Training Happens**: The models are pre-trained and downloaded from Hugging Face
2. **Blogs as Context**: Your blog content is used as context/prompt, not training data
3. **Lazy Loading**: Models are loaded only when first needed (prevents startup crashes)
4. **Fallback System**: Works with or without FAISS - falls back to keyword search if FAISS unavailable

## To Add New Blogs

1. Add new HTML files matching `blog-*.html` pattern or put them in `blog/` directory
2. Run `python extract_blog_content.py` to update `knowledge_base.json`
3. (Optional) Run `python create_faiss_index.py` to update the FAISS index
4. Restart the Flask server

## Model Files Location

- Models are downloaded automatically from Hugging Face on first use
- They're cached in `~/.cache/huggingface/` directory
- No need to manually download or train anything










