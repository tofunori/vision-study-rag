import streamlit as st
import os
import base64
import torch
from io import BytesIO
from PIL import Image
import tempfile
from dotenv import load_dotenv

from src.pdf_processor import convert_pdf_to_images
from src.embedding_generator import load_model, generate_embeddings, generate_query_embedding
from src.vector_db import VectorDatabase
from src.llm_generator import generate_response

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Vision Study RAG", page_icon="📚", layout="wide")

# Initialize session state
if 'model' not in st.session_state:
    with st.spinner("Loading ColPali model..."):
        model, processor = load_model(os.environ.get("COLPALI_MODEL", "vidore/colqwen2-v1.0"))
        st.session_state.model = model
        st.session_state.processor = processor

# Initialize vector database
if 'vector_db' not in st.session_state:
    db_path = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
    st.session_state.vector_db = VectorDatabase(db_path)

# App title
st.title("📚 Vision Study RAG")
st.write("A vision-based RAG system for studying PDFs with charts and images")

# Sidebar for collections management
st.sidebar.title("Collections")

# Create or select collection
collections = st.session_state.vector_db.list_collections()
selected_collection = st.sidebar.selectbox(
    "Select Collection", 
    options=["Create New Collection"] + collections,
    index=0
)

if selected_collection == "Create New Collection":
    new_collection = st.sidebar.text_input("Enter Collection Name")
    if st.sidebar.button("Create Collection") and new_collection:
        st.session_state.vector_db.create_collection(new_collection)
        st.sidebar.success(f"Collection '{new_collection}' created!")
        st.experimental_rerun()
    working_collection = None
else:
    working_collection = selected_collection
    st.sidebar.success(f"Using collection: {working_collection}")

# Create tabs
tab1, tab2 = st.tabs(["📄 Upload Documents", "🔍 Query Documents"])

# Tab 1: Upload Documents
with tab1:
    if working_collection:
        st.header("Upload PDFs to Collection")
        uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type=['pdf'])
        
        if uploaded_files and st.button("Process Documents"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_files = len(uploaded_files)
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    temp_path = tmp.name
                
                # Convert PDF to images
                try:
                    images = convert_pdf_to_images(temp_path)
                    
                    # Generate embeddings for each page
                    for page_idx, image in enumerate(images):
                        status_text.text(f"Processing {uploaded_file.name}, page {page_idx+1}/{len(images)}...")
                        
                        # Convert to PIL Image if needed
                        if not isinstance(image, Image.Image):
                            image = Image.fromarray(image)
                        
                        # Generate embedding
                        embedding = generate_embeddings(
                            st.session_state.model, 
                            st.session_state.processor,
                            [image]
                        )[0]
                        
                        # Encode image for storage
                        buffered = BytesIO()
                        image.save(buffered, format="JPEG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        # Store in vector database
                        metadata = {
                            "filename": uploaded_file.name,
                            "page": page_idx + 1,
                            "image": img_str
                        }
                        
                        st.session_state.vector_db.add_document(
                            working_collection,
                            embedding,
                            metadata
                        )
                        
                    # Clean up temp file
                    os.unlink(temp_path)
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                # Update progress
                progress_bar.progress((i + 1) / total_files)
            
            status_text.text("Processing complete!")
            st.success(f"All documents processed and added to {working_collection}!")
    else:
        st.info("Please select or create a collection first.")

# Tab 2: Query Documents
with tab2:
    if working_collection:
        st.header("Ask Questions About Your Documents")
        
        query = st.text_input("Enter your question")
        num_results = st.slider("Number of relevant pages to retrieve", 1, 5, 3)
        use_ollama = os.environ.get("USE_OLLAMA", "true").lower() == "true"
        
        if st.button("Search") and query:
            with st.spinner("Processing query..."):
                # Generate query embedding
                query_embedding = generate_query_embedding(
                    st.session_state.model,
                    st.session_state.processor,
                    query
                )
                
                # Search for similar documents
                results = st.session_state.vector_db.search(
                    working_collection,
                    query_embedding,
                    num_results
                )
                
                if results:
                    # Display results
                    st.subheader("Retrieved Documents")
                    for i, result in enumerate(results):
                        with st.expander(f"Document: {result['metadata']['filename']} (Page {result['metadata']['page']})"):
                            # Decode and display image
                            img_data = base64.b64decode(result['metadata']['image'])
                            img = Image.open(BytesIO(img_data))
                            st.image(img, caption=f"Page {result['metadata']['page']} from {result['metadata']['filename']}")
                    
                    # Generate response
                    st.subheader("Answer")
                    with st.spinner("Generating answer..."):
                        answer = generate_response(query, results, use_ollama)
                        st.write(answer)
                else:
                    st.warning("No relevant documents found.")
    else:
        st.info("Please select or create a collection first.")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using ColPali, ChromaDB, and Streamlit. "
    "[GitHub Repository](https://github.com/tofunori/vision-study-rag)"
)