# Vision Study RAG

A vision-based RAG (Retrieval-Augmented Generation) system for studying PDFs with charts and images, using the ColPali vision language model.

## Features

- PDF processing with visual awareness of images, charts, and tables
- No OCR required - works directly with the visual content
- Vector storage using ChromaDB (local, free, open-source)
- Simple and intuitive web interface
- Compatible with Ollama for completely local LLM generation

## Installation

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) (optional, for local LLM generation)

### Setup

1. Clone this repository
   ```bash
   git clone https://github.com/tofunori/vision-study-rag.git
   cd vision-study-rag
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. (Optional) If using Ollama, make sure it's installed and running

## Usage

1. Start the application
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:8501`

3. Upload your PDFs and start querying!

## Configuration

You can configure the application by editing the `.env` file or setting environment variables:

```
# Model selection
COLPALI_MODEL=vidore/colqwen2-v1.0

# LLM Configuration
USE_OLLAMA=true  # Set to false to use OpenAI
OLLAMA_MODEL=llama3.2-vision  # Only if USE_OLLAMA=true
OPENAI_API_KEY=  # Only if USE_OLLAMA=false

# Database settings
CHROMA_DB_PATH=./chroma_db
```

## How It Works

1. **PDF Processing**: PDFs are converted to images page by page
2. **Embedding Generation**: ColPali processes these images to create multi-vector embeddings
3. **Vector Storage**: Embeddings are stored in a local ChromaDB database
4. **Query Processing**: Your questions are converted to embeddings and used to retrieve the most relevant PDF pages
5. **Response Generation**: Retrieved pages are sent to Ollama or OpenAI for final answer generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
