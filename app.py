"""
Flask Backend API for YouTube Video & Blog Q&A System
Converts terminal Q&A system to REST API for frontend integration
Port: 5001
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from bs4 import BeautifulSoup
import yt_dlp
import os
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
PERSIST_DIRECTORY = "./chroma_db"
EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama2"


class YouTubeQA:
    def __init__(self):
        """Initialize the Q&A system"""
        print("🔧 Initializing AI system...")
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize Ollama
        self.llm = Ollama(model=OLLAMA_MODEL, temperature=0.3)
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        self.vectorstore = None
        self.qa_chain = None
        
        # yt-dlp options
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'json3',
        }
        
        # Load existing database if available
        self.load_database()
        
        print("✅ System ready!\n")
    
    def get_transcript(self, video_url: str):
        """Get transcript and metadata from YouTube video using yt-dlp"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract video info
                info = ydl.extract_info(video_url, download=False)
                
                # Get video metadata
                video_id = info.get('id', '')
                title = info.get('title', 'Unknown Title')
                channel = info.get('uploader', 'Unknown Channel')
                duration = info.get('duration', 0)
                
                # Try to get subtitles
                transcript_text = None
                subtitles = info.get('subtitles', {})
                automatic_captions = info.get('automatic_captions', {})
                
                # Priority: manual subtitles > auto-generated captions
                subtitle_data = None
                
                # Check for manual English subtitles
                if 'en' in subtitles:
                    subtitle_data = subtitles['en']
                # Check for auto-generated English captions
                elif 'en' in automatic_captions:
                    subtitle_data = automatic_captions['en']
                
                if subtitle_data:
                    # Find json3 format
                    for fmt in subtitle_data:
                        if fmt.get('ext') == 'json3':
                            # Download subtitle data
                            subtitle_url = fmt.get('url')
                            if subtitle_url:
                                import urllib.request
                                with urllib.request.urlopen(subtitle_url) as response:
                                    subtitle_json = json.loads(response.read().decode())
                                    
                                    # Parse json3 subtitle format
                                    transcript_text = self.parse_json3_subtitles(subtitle_json)
                                    break
                
                if not transcript_text:
                    return {
                        'success': False,
                        'error': 'No subtitles/captions available for this video'
                    }
                
                metadata = {
                    'video_id': video_id,
                    'url': video_url,
                    'title': title,
                    'channel': channel,
                    'duration': duration,
                    'source': 'youtube'
                }
                
                return {
                    'success': True,
                    'transcript': transcript_text,
                    'metadata': metadata
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def parse_json3_subtitles(self, subtitle_json: dict) -> str:
        """Parse json3 subtitle format and create timestamped transcript"""
        transcript_text = ""
        
        events = subtitle_json.get('events', [])
        
        for event in events:
            # Get start time
            tStartMs = event.get('tStartMs', 0)
            start_seconds = tStartMs / 1000
            minutes = int(start_seconds // 60)
            seconds = int(start_seconds % 60)
            
            # Get text segments
            segs = event.get('segs', [])
            text_parts = []
            
            for seg in segs:
                text = seg.get('utf8', '').strip()
                if text:
                    text_parts.append(text)
            
            if text_parts:
                full_text = ' '.join(text_parts)
                transcript_text += f"[{minutes}:{seconds:02d}] {full_text}\n"
        
        return transcript_text
    
    def learn_from_video(self, video_url: str):
        """Process video and add to knowledge base"""
        # Get transcript
        result = self.get_transcript(video_url)
        
        if not result['success']:
            return result
        
        # Create document
        doc = Document(
            page_content=result['transcript'],
            metadata=result['metadata']
        )
        
        # Split into chunks
        texts = self.text_splitter.split_documents([doc])
        
        # Add to vector store
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=PERSIST_DIRECTORY
            )
        else:
            self.vectorstore.add_documents(texts)
        
        # Persist to disk
        self.vectorstore.persist()
        
        # Setup QA chain
        self.setup_qa_chain()
        
        return {
            'success': True,
            'title': result['metadata']['title'],
            'channel': result['metadata']['channel'],
            'chunks': len(texts)
        }
    
    def extract_blog_content(self, html_content: str):
        """Extract content from HTML"""
        try:
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Try to extract title
            title = None
            if soup.title:
                title = soup.title.string
            elif soup.find('h1'):
                title = soup.find('h1').get_text()
            else:
                title = "Blog Post"
            
            # Extract main content
            # Try to find main content area
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.body
            
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                text = soup.get_text(separator='\n', strip=True)
            
            # Clean up text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            clean_text = '\n'.join(lines)
            
            return {
                'success': True,
                'content': clean_text,
                'title': title
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def learn_from_blog(self, html_content: str, title: str = None, file_path: str = None):
        """Process HTML blog and add to knowledge base"""
        # Extract blog content
        result = self.extract_blog_content(html_content)
        
        if not result['success']:
            return result
        
        blog_title = title or result['title']
        
        # Create document
        doc = Document(
            page_content=result['content'],
            metadata={
                'title': blog_title,
                'source': 'blog',
                'file_path': file_path or 'uploaded',
                'type': 'html_blog'
            }
        )
        
        # Split into chunks
        texts = self.text_splitter.split_documents([doc])
        
        # Add to vector store
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=PERSIST_DIRECTORY
            )
        else:
            self.vectorstore.add_documents(texts)
        
        # Persist to disk
        self.vectorstore.persist()
        
        # Setup QA chain
        self.setup_qa_chain()
        
        return {
            'success': True,
            'title': blog_title,
            'chunks': len(texts)
        }
    
    def setup_qa_chain(self):
        """Setup the question-answering chain"""
        if self.vectorstore is None:
            return
        
        prompt_template = """Use the following context from YouTube video transcripts or blog posts to answer the question.
If you don't know the answer, just say you don't have enough information.

Context:
{context}

Question: {question}

Answer based on the content (include timestamps like [2:34] for videos when relevant):"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def ask(self, question: str, content_reference: str = None, filter_type: str = None):
        """Ask a question about the videos or blogs
        
        Args:
            question: The question to ask
            content_reference: Specific video/blog title to search in
            filter_type: 'video', 'blog', or None for all content
        """
        if self.qa_chain is None:
            return {
                'success': False,
                'error': 'No content learned yet. Please add videos or blogs first.'
            }
        
        try:
            # If content reference provided, search only in that content
            if content_reference:
                specific_title, source_type = self.find_content_by_reference(content_reference)
                if specific_title:
                    return self.ask_about_specific_content(question, specific_title)
                else:
                    return {
                        'success': False,
                        'error': f'Content "{content_reference}" not found'
                    }
            elif filter_type:
                # Filter by content type (video or blog)
                if filter_type == 'video':
                    return self.ask_filtered(question, 'youtube')
                elif filter_type == 'blog':
                    return self.ask_filtered(question, 'blog')
                else:
                    return {
                        'success': False,
                        'error': 'Invalid filter. Use "video" or "blog"'
                    }
            else:
                return self.ask_general(question)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def find_content_by_reference(self, reference: str):
        """Find a video or blog by partial title match. Returns (title, source_type)"""
        if not self.vectorstore:
            return None, None
        
        reference_lower = reference.lower().strip()
        
        # Get all documents and extract unique content
        try:
            docs = self.vectorstore.get()
            content_items = {}
            
            if docs and 'metadatas' in docs:
                for metadata in docs['metadatas']:
                    title = metadata.get('title', '')
                    content_id = metadata.get('video_id') or metadata.get('file_path', '')
                    source = metadata.get('source', 'youtube')
                    
                    if content_id and title and content_id not in content_items:
                        content_items[content_id] = {
                            'title': title,
                            'source': source
                        }
            
            if not content_items:
                return None, None
            
            # Try to find matching content
            # 1. Exact match (case insensitive)
            for content_id, info in content_items.items():
                if reference_lower == info['title'].lower():
                    return info['title'], info['source']
            
            # 2. Check if reference is contained in title
            for content_id, info in content_items.items():
                if reference_lower in info['title'].lower():
                    return info['title'], info['source']
            
            # 3. Check if title is contained in reference (for longer user input)
            for content_id, info in content_items.items():
                if info['title'].lower() in reference_lower:
                    return info['title'], info['source']
            
            # 4. Word matching - find title with most matching words
            reference_words = set(word.lower() for word in reference.split() if len(word) > 2)
            if not reference_words:
                return None, None
            
            best_match = None
            best_source = None
            best_score = 0
            
            for content_id, info in content_items.items():
                title_words = set(word.lower() for word in info['title'].split() if len(word) > 2)
                matches = len(reference_words & title_words)
                
                if matches > best_score:
                    best_score = matches
                    best_match = info['title']
                    best_source = info['source']
            
            # Return if at least 1 significant word matches
            if best_score >= 1:
                return best_match, best_source
            
        except Exception as e:
            print(f"⚠️  Error searching content: {e}")
        
        return None, None
    
    def ask_about_specific_content(self, question: str, content_title: str):
        """Ask a question about specific video or blog"""
        try:
            # Create a filtered retriever for the specific content
            retriever = self.vectorstore.as_retriever(
                search_kwargs={
                    "k": 5,
                    "filter": {"title": content_title}
                }
            )
            
            prompt_template = f"""Use the following context to answer the question.
If you don't know the answer, just say you don't have enough information.

Content: {content_title}

Context:
{{context}}

Question: {{question}}

Answer based ONLY on this specific content (include timestamps like [2:34] for videos when relevant):"""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create temporary QA chain for this specific content
            specific_qa = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            
            result = specific_qa({"query": question})
            
            # Collect sources
            sources = []
            if result.get('source_documents'):
                for doc in result['source_documents']:
                    metadata = doc.metadata
                    source_type = metadata.get('source', 'unknown')
                    
                    sources.append({
                        'title': metadata.get('title', 'Unknown'),
                        'type': 'video' if source_type == 'youtube' else 'blog',
                        'url': metadata.get('url', ''),
                        'channel': metadata.get('channel', ''),
                        'file_path': metadata.get('file_path', '')
                    })
            
            return {
                'success': True,
                'answer': result['result'],
                'sources': sources
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def ask_general(self, question: str):
        """Ask a general question across all videos and blogs"""
        try:
            result = self.qa_chain({"query": question})
            
            # Show sources with titles and types
            sources = []
            for doc in result.get('source_documents', []):
                metadata = doc.metadata
                source_type = metadata.get('source', 'unknown')
                
                sources.append({
                    'title': metadata.get('title', 'Unknown Title'),
                    'type': 'video' if source_type == 'youtube' else 'blog',
                    'url': metadata.get('url', ''),
                    'channel': metadata.get('channel', ''),
                    'file_path': metadata.get('file_path', '')
                })
            
            return {
                'success': True,
                'answer': result['result'],
                'sources': sources
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def ask_filtered(self, question: str, source_type: str):
        """Ask a question filtered by source type (youtube or blog)"""
        try:
            # Create filtered retriever
            retriever = self.vectorstore.as_retriever(
                search_kwargs={
                    "k": 5,
                    "filter": {"source": source_type}
                }
            )
            
            content_name = "videos" if source_type == "youtube" else "blogs"
            
            prompt_template = f"""Use the following context from {content_name} to answer the question.
If you don't know the answer, just say you don't have enough information.

Context:
{{context}}

Question: {{question}}

Answer based on the {content_name}:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create filtered QA chain
            filtered_qa = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            
            result = filtered_qa({"query": question})
            
            # Show sources
            sources = []
            for doc in result.get('source_documents', []):
                metadata = doc.metadata
                
                sources.append({
                    'title': metadata.get('title', 'Unknown Title'),
                    'type': 'video' if source_type == 'youtube' else 'blog',
                    'url': metadata.get('url', ''),
                    'channel': metadata.get('channel', ''),
                    'file_path': metadata.get('file_path', '')
                })
            
            return {
                'success': True,
                'answer': result['result'],
                'sources': sources
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_database(self):
        """Load existing database from disk"""
        if os.path.exists(PERSIST_DIRECTORY):
            try:
                print("📂 Loading existing knowledge base...")
                self.vectorstore = Chroma(
                    persist_directory=PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
                self.setup_qa_chain()
                print("✅ Knowledge base loaded")
            except Exception as e:
                print(f"⚠️  Could not load existing database: {e}")
    
    def list_content(self):
        """List all learned videos and blogs"""
        if not self.vectorstore:
            return {
                'videos': [],
                'blogs': [],
                'total': 0
            }
        
        try:
            docs = self.vectorstore.get()
            content_items = {}
            
            if docs and 'metadatas' in docs:
                for metadata in docs['metadatas']:
                    title = metadata.get('title', 'Unknown')
                    source_type = metadata.get('source', 'unknown')
                    
                    content_id = metadata.get('video_id') or metadata.get('file_path', '')
                    
                    if content_id and content_id not in content_items:
                        if source_type == 'youtube':
                            content_items[content_id] = {
                                'title': title,
                                'type': 'video',
                                'channel': metadata.get('channel', 'Unknown'),
                                'url': metadata.get('url', '')
                            }
                        else:
                            content_items[content_id] = {
                                'title': title,
                                'type': 'blog',
                                'file_path': metadata.get('file_path', '')
                            }
            
            # Separate videos and blogs
            videos = [v for v in content_items.values() if v['type'] == 'video']
            blogs = [v for v in content_items.values() if v['type'] == 'blog']
            
            return {
                'videos': videos,
                'blogs': blogs,
                'total': len(videos) + len(blogs)
            }
        
        except Exception as e:
            return {
                'videos': [],
                'blogs': [],
                'total': 0,
                'error': str(e)
            }


# Initialize the system
print("=" * 70)
print("🚀 Initializing YouTube & Blog Q&A System...")
print("=" * 70)
qa_system = YouTubeQA()


# API Endpoints

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'YouTube & Blog Q&A API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            'GET /': 'API info',
            'GET /api/health': 'Health check',
            'POST /api/learn/video': 'Learn from YouTube video',
            'POST /api/learn/blog': 'Learn from blog HTML',
            'POST /api/ask': 'Ask a question',
            'GET /api/content': 'List all content'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': OLLAMA_MODEL,
        'embeddings': EMBEDDINGS_MODEL,
        'database': 'loaded' if qa_system.vectorstore else 'empty'
    })


@app.route('/api/learn/video', methods=['POST'])
def learn_video():
    """Learn from a YouTube video"""
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({
            'success': False,
            'error': 'No URL provided. Send JSON with "url" field.'
        }), 400
    
    result = qa_system.learn_from_video(data['url'])
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route('/api/learn/blog', methods=['POST'])
def learn_blog():
    """Learn from HTML blog content"""
    data = request.json
    
    if not data or 'html' not in data:
        return jsonify({
            'success': False,
            'error': 'No HTML content provided. Send JSON with "html" field.'
        }), 400
    
    result = qa_system.learn_from_blog(
        data['html'],
        data.get('title'),
        data.get('file_path')
    )
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question
    
    Request body can include:
    - question (required): The question to ask
    - filter (optional): 'video' or 'blog' to filter by type
    - content (optional): Specific content name to search in
    """
    data = request.json
    
    if not data or 'question' not in data:
        return jsonify({
            'success': False,
            'error': 'No question provided. Send JSON with "question" field.'
        }), 400
    
    result = qa_system.ask(
        question=data['question'],
        content_reference=data.get('content'),
        filter_type=data.get('filter')
    )
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route('/api/content', methods=['GET'])
def list_content():
    """List all learned content"""
    content = qa_system.list_content()
    return jsonify(content), 200


if __name__ == '__main__':
    print("=" * 70)
    print("🎉 Flask API Server Starting on Port 5001...")
    print("=" * 70)
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Embeddings: {EMBEDDINGS_MODEL}")
    print("=" * 70)
    print("\n📡 API Endpoints:")
    print("  GET  /                    - API info")
    print("  GET  /api/health          - Health check")
    print("  POST /api/learn/video     - Learn from YouTube video")
    print("  POST /api/learn/blog      - Learn from HTML blog")
    print("  POST /api/ask             - Ask a question")
    print("  GET  /api/content         - List all content")
    print("=" * 70)
    print("\n🌐 Server running at: http://localhost:5001")
    print("🔗 Test it: http://localhost:5001/")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5001)