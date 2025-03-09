# Vision Study RAG

A vision-based RAG (Retrieval-Augmented Generation) system for studying PDFs with charts and images, using the ColPali vision language model.

## Features (Coming Soon)

- PDF processing with visual awareness of images, charts, and tables
- No OCR required - works directly with the visual content
- Vector storage using ChromaDB (local, free, open-source)
- Simple and intuitive web interface
- Compatible with Ollama for completely local LLM generation

## Important: Python 3.13 Compatibility Notice

The repository is being updated to work with Python 3.13. Some dependencies need adaptation to work correctly with this version.

## Quick Start (Simplified Version)

1. Clone this repository
   ```bash
   git clone https://github.com/tofunori/vision-study-rag.git
   cd vision-study-rag
   ```

2. Run the simplified setup script
   ```bash
   setup_simplified.bat
   ```

3. Run the application
   ```bash
   run_app.bat
   ```

4. Open your browser at `http://localhost:8501`

## Development Status

This project is under active development. The current version includes:
- Basic Streamlit interface
- Simplified setup for Python 3.13
- Roadmap for full implementation

Future updates will add:
- Full ColPali integration
- Vector database connectivity
- PDF processing
- LLM integration with Ollama

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
