# Agentic RAG - Production-Grade AI System

A **production-grade Agentic Retrieval-Augmented Generation (RAG)** system implementing the 12-step workflow with LangChain and LangGraph.

## 🌟 Overview

This is a complete, production-ready RAG system with specialized AI agents at each stage. The system uses **intelligent decision-making** at every step, resulting in higher quality responses than traditional RAG systems.

### 🎯 What Makes It "Agentic"?

Unlike traditional RAG that follows a fixed pipeline, this system:
- **Thinks**: Each agent actively analyzes and makes decisions
- **Adapts**: Routes differently based on query needs  
- **Evaluates**: Self-assesses quality and retries if needed
- **Learns**: Iteratively improves responses

## 🏗️ Architecture

The system follows a 12-step workflow with multiple decision points:

1. **Query Rewriting** - Optimize user queries for better retrieval
2. **Information Need Assessment** - Decide if external data is needed
3. **Source Selection** - Choose the best information source
4. **Context Retrieval** - Fetch relevant information
5. **Answer Generation** - Create comprehensive responses
6. **Answer Evaluation** - Validate response quality
7. **Iterative Refinement** - Retry if quality is insufficient

### Workflow Diagram

```
START → Query Rewriter → Needs More Info? 
           ↓                    ↓
       (No Info)          Source Selector
           ↓                    ↓
    Answer Generator ← Retriever
           ↓
    Answer Evaluator
           ↓
    Relevant? → YES → END
           ↓
          NO (Max retries?) → Retry from Start
```

## 📁 Project Structure (Production-Ready)

```
AGENTIC-RAG/
│
├── src/                            # Application source code
│   │
│   ├── core/                       # ⭐ Core utilities (centralized)
│   │   ├── __init__.py            # Clean exports
│   │   ├── config.py              # Settings & environment vars
│   │   ├── logger.py              # Logging utilities
│   │   ├── constants.py           # Application constants
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── message_filter.py      # Message filtering for context
│   │
│   ├── agents/                     # AI Agents (LLM-powered)
│   │   ├── __init__.py
│   │   ├── query_rewriter.py       # Steps 1–2: Query optimization
│   │   ├── needs_more_info.py      # Steps 3–4: Retrieval decision
│   │   ├── source_selector.py      # Steps 5–6: Source routing
│   │   ├── answer_generator.py     # Steps 8–9: Response generation
│   │   └── answer_evaluator.py     # Steps 10–12: Quality evaluation
│   │
│   ├── schemas/                    # ⭐ Pydantic models (reorganized)
│   │   ├── __init__.py            # Clean exports
│   │   ├── request.py             # Request models (QueryRequest, etc.)
│   │   ├── response.py            # Response models (QueryResponse, etc.)
│   │   ├── agent_io.py            # Agent I/O schemas
│   │   └── api.py                 # Backward compatibility
│   │
│   ├── api/                        # FastAPI REST API
│   │   ├── __init__.py
│   │   ├── router.py              # Main API router
│   │   ├── dependencies.py        # Shared dependencies
│   │   └── v1/                    # API v1 endpoints
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── query.py           # Query endpoints
│   │       ├── session.py         # Session management
│   │       └── documents.py       # Document operations
│   │
│   ├── graph/                      # LangGraph workflow
│   │   ├── __init__.py
│   │   ├── state.py               # State schema
│   │   └── rag_graph.py           # Agentic RAG workflow
│   │
│   ├── memory/                     # Session persistence
│   │   ├── __init__.py
│   │   └── database.py            # MongoDB checkpointer
│   │
│   ├── session/                    # Session management
│   │   ├── __init__.py
│   │   └── manager.py             # Session lifecycle
│   │
│   ├── retrieval/                  # Knowledge access layer
│   │   ├── __init__.py
│   │   ├── vector_store.py        # Chroma/FAISS/Pinecone
│   │   ├── tools.py               # External tools & APIs
│   │   └── web_search.py          # Internet search
│   │
│   ├── llms/                       # LLM wrappers
│   │   ├── __init__.py
│   │   └── model.py               # Groq/OpenAI LLMs
│   │
│   ├── prompts/                    # Prompt templates
│   │   ├── __init__.py
│   │   ├── rewrite_prompt.py
│   │   ├── retrieval_prompt.py
│   │   └── evaluation_prompt.py
│   │
│   ├── app.py                      # FastAPI application factory
│   │
│   ├── config/                     # ⚠️ DEPRECATED (backward compatibility)
│   └── utils/                      # ⚠️ DEPRECATED (backward compatibility)
│
├── data/                           # Local data storage
│   ├── documents/                  # Source documents
│   ├── chroma/                     # Vector database
│   └── embeddings/                 # Embeddings cache
│
├── logs/                           # Application logs
│   └── agentic_rag_*.log          # Timestamped log files
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_agents.py
│   └── test_graph.py
│
├── main.py                         # Server entry point
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example                    # Environment template
├── .gitignore
└── LICENSE
```

### 🎯 Key Structural Improvements

- ✅ **`src/core/`** - Centralized configuration, logging, constants, and utilities
- ✅ **`src/schemas/`** - Separated into `request.py`, `response.py`, `agent_io.py`
- ✅ **`src/api/`** - Full REST API with FastAPI
- ✅ **`src/memory/`** - MongoDB session persistence
- ✅ **`src/session/`** - Session management utilities
- ✅ **Production-ready** - Follows industry best practices

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API key (free) or OpenAI API key
- (Optional) Tavily API key for web search

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Agentic-Rag
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (faster)
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure:
   ```env
   # LLM Configuration (using Groq - FREE!)
   GROQ_API_KEY=your_groq_api_key_here
   LLM_MODEL=llama-3.3-70b-versatile
   LLM_TEMPERATURE=0.4
   
   # Vector Store (uses free local embeddings)
   VECTOR_STORE_TYPE=chroma
   CHROMA_PERSIST_DIR=./data/chroma
   
   # Optional: Web Search
   TAVILY_API_KEY=your_tavily_key_here
   ```

5. **Verify setup**
   ```bash
   python setup.py
   ```

### Usage

#### Start the API Server

```bash
python main.py
```

The server will start and display:
```
============================================================
🚀 Starting Agentic RAG API Server...
============================================================
📍 Server will bind to: 127.0.0.1:8000

🌐 Access the API at:
   • http://localhost:8000/
   • http://127.0.0.1:8000/

📚 API Documentation:
   • Swagger UI: http://localhost:8000/docs
   • ReDoc:      http://localhost:8000/redoc

💚 Health Check: http://localhost:8000/health
============================================================
```

### Method 1: API Upload (Recommended)

Upload documents via the API:

```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@mydocument.txt"

# Or use the Swagger UI at http://localhost:8000/docs
```

### Method 2: Direct File Placement

1. Place your text documents in `data/documents/`
2. The system will automatically index them on first query

**Incremental Indexing** (Production Feature):
- System tracks which files are already indexed
- Only processes NEW or MODIFIED documents
- Much faster when adding documents incrementally
- Metadata stored in `data/chroma/indexed_files.json`

**Supported Formats:**
- `.txt` - Plain text files
- More formats can be added (PDF, DOCX, etc.
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'

# Create a new session
curl -X POST http://localhost:8000/api/v1/session

# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.txt"
```

**Python Client Example:**

```python
import requests

# Query the system
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={"query": "Explain Python decorators"}
)
print(response.json())
```

## 📚 Adding Your Documents

1. Place your text documents in `data/documents/`
2. Run the indexing command:
   ```bash
   python main.py --index
   ```
   Or type `index` in interactive mode

**Incremental Indexing** (Production Feature):
- System tracks which files are already indexed
- Only processes NEW or MODIFIED documents
- Much faster when adding documents incrementally
- Metadata stored in `data/chroma/indexed_files.json`

Supported formats: `.txt` (more formats can be added)

## 🔧 Configuration
 (using Groq - FREE)
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.4

# Vector Store (uses free local HuggingFace embeddings)
VECTOR_STORE_TYPE=chroma
CHROMA_PERSIST_DIR=./data/chroma
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# RAG Parameters
MAX_ITERATIONS=3
RETRIEVAL_TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Logging (saves to logs/agentic_rag_TIMESTAMP.log)
LOG_LEVEL=INFO

# Optional: Web Search
TAVILY_API_KEY=your_tavily_key
SERPAPI_API_KEY=your_serpapi
RETRIEVAL_TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Optional: Web Search
TAVILY_API_KEY=your_tavily_key
```

### Customizing Agents

Each agent can be customized by modifying its corresponding file in `src/agents/`:

- **Query Rewriter**: Adjust rewriting strategy in `src/agents/query_rewriter.py`
- **Source Selector**: Modify source selection logic in `src/agents/source_selector.py`
- **Answer Evaluator**: Change evaluation criteria in `src/agents/answer_evaluator.py`

### Modifying Prompts

All prompts are in `src/prompts/`. Edit them to change agent behavior:

- `src/prompts/rewrite_prompt.py`
- `src/prompts/retrieval_prompt.py`
- `src/prompts/evaluation_prompt.py`

## 🧪 Testing

Run tests:

```bash
pytest tests/
```

- **Self-Evaluation**: Quality assessment and automatic retry mechanism
- **Adaptive Source Selection**: Chooses best information source dynamically

### 🔍 Multiple Information Sources

- **Vector Database**: ChromaDB for document retrieval (with incremental indexing)
- **External Tools/APIs**: Calculator, datetime, and custom tools
- **Web Search**: Real-time internet information (Tavily/SerpAPI)

### 🌐 Production-Ready API

- **FastAPI Framework**: Modern, high-performance REST API
- **OpenAPI/Swagger**: Auto-generated interactive documentation
- **Session Management**: MongoDB-based conversation persistence
- **Health Checks**: Built-in monitoring endpoints
- **CORS Support**: Configurable cross-origin access
- **Versioned API**: `/api/v1/` structure for future expansion

### 📊 Production Features

- **FREE to Use**: Uses Groq API (free) + local embeddings (no OpenAI costs)
- **Incremental Indexing**: Only processes new/modified documents
- **Session Persistence**: MongoDB checkpointer for conversation history
- **Timestamped Logging**: Each run creates separate log file in `logs/`
- **Centralized Configuration**: All settings in `src/core/`
- **Clean Architecture**: Separation of concerns with clear module boundaries
- **Structured Logging**: Comprehensive logging for debugging
- **Configurable Parameters**: Easy customization via environment variables
- **Error Handling**: Graceful degradation and informative errors
- **Modular Design**: Easy to extend and maintain
- **Type Hints**: Full type annotations throughout
- **Comprehensive Documentation**: Docstrings in every module
- **Production Structure**: Follows industry best practicesmbeddings (no OpenAI costs)
- **Incremental Indexing**: Only processes new/modified documents
- **Timestamped Logging**: Each run creates separate log file in `logs/`
- **Absolute Imports**: Clean, direct imports (no relative imports)
- **Structured Logging**: Comprehensive logging for debugging
- **Configurable Parameters**: Easy customization via environment variables
- **Error Handling**: Graceful degradation and informative errors
- **Modular Design**: Easy to extend and maintain
- **Type Hints**: Full type annotations throughout
- **Comprehensive Documentation**: Docstrings in every moduleor debugging
- **Configurable Parameters**: Easy customization via environment variables
- **Error Handling**: Graceful degradation and informative errors
- **Modular Design**: Easy to extend and maintain

## 🛠️ Advanced Usage

### Adding Custom Tools

Edit `src/retrieval/tools.py`:

```python
def _my_custom_tool(self, query: str) -> str:
    """Your custom tool logic."""
    return "Tool result"

# Register in __init__
self.available_tools["my_tool"] = self._my_custom_tool
```

### Using Different Vector Stores

Configure in `.env`:

```env
VECTOR_STORE_TYPE=faiss  # or pinecone
### Complete 12-Step Workflow:

1. **Query Rewriting (Steps 1-2)**: Optimizes user query for better retrieval
2. **Needs More Info (Steps 3-4)**: Decides if retrieval is needed or direct answer
3. **Source Selection (Steps 5-6)**: Chooses best source (vector DB, tools, web)
4. **Context Retrieval (Step 7)**: Fetches relevant information
5. **Answer Generation (Steps 8-9)**: Creates response with context
6. **Answer Evaluation (Steps 10-12)**: Validates quality, retries if needed

### Intelligent Routing:

```
Query → Rewrite → Need Info?
                      ├─ NO → Direct Answer → END
                      └─ YES → Select Source → Retrieve → Generate → Evaluate
                                                                         ├─ GOOD → END
                                                                         └─ BAD → RETRY (max 3)
```

### Example Queries:

**Simple Math (No Retrieval)**:
```bash
python main.py -q "What is 2 + 2?"
# Ou� Technologies Used

**Core Functionality:**
- [x] Complete 12-step agentic workflow
- [x] 5 specialized agents implemented
- [x] 3 retrieval sources (vector DB, tools, web)
- [x] LangGraph state management with conditional routing
- [x] FREE to use (Groq + local embeddings)
- [x] Incremental document indexing

**API & Architecture:**
- [x] FastAPI REST API with versioning
- [x] OpenAPI/Swagger documentation
- [x] Session management (MongoDB)
- [x] Health check endpoints
- [x] Production-ready structure (`src/core/`)
- [x] Separated schemas (request/response/agent_io)

**Code Quality:**
- [x] Timestamped logging for each run
- [x] Centralized configuration
- [x] Absolute imports (no relative imports)
- [x] Comprehensive error handling
- [x] Environment-based configuration
- [x] Full type hints and docstrings
- [x] Custom exception classes
- [x] Message filtering utilities

**Developer Experience:**
- [x] Test suite included
- [x] Sample documents provided
- [x] `.env.example` template
- [x] Comprehensive README
- [x] Clear file structure
- [ ] Rate limiting and authentication
- [ ] Containerization (Docker/Kubernetes)
- [ ] CI/CD pipelineector DB, tools, web)
- [x] LangGraph state management with conditional routing
- [x] FREE to use (Groq + local embeddings)
- [x] Incremental document indexing
- [x] Timestamped logging for each run
- [x] Absolute imports (no relative imports)
- [x] Comprehensive error handling
- [x] CLI interface (interactive + single query)
- [x] Environment-based configuration
- [x] Full type hints and docstrings
- [x] Test suite included
- [x] Sample documents provided

## 🚧 Future Enhancements

Potential improvements:
- [ ] Add streaming responses
- [ ] Implement conversation memory
- [ ] Support PDF and DOCX documents
- [ ] Add FastAPI REST API
- [ ] Implement re-ranking for better retrieval
- [ ] Add monitoring dashboard
- [ ] Support more LLM providers
- [ ] Multi-language support

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Groq](https://groq.com/) for fast, free LLM inference
**Document Query (Vector DB)**:
```bash
python main.py -q "What is machine learning?"
# Uses: vector_database → retrieves from indexed documents
```

**Real-time Info (Web Search)**:
```bash
python main.py -q "Who is the current PM of India?"
# Uses: web_search → fetches current information
```

1. **User submits a query** → System initializes the workflow
2. **Query Rewriter Agent** → Optimizes the query for retrieval
3. **Needs Info Agent** → Decides if external information is required
4. **If Yes** → Source Selector Agent chooses best source (DB/API/Web)
5. **Retriever** → Fetches relevant context from selected source
6. **Answer Generator** → Creates response using context
7. **Answer Evaluator** → Checks quality and relevance
8. **If Poor Quality** → Retry from step 2 (up to MAX_ITERATIONS)
9. **Return Final Answer** → User receives the response

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

See LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Inspired by advanced RAG architectures and agentic AI systems

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Happy Building! 🚀**