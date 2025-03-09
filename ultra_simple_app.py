import streamlit as st

# Configure page
st.set_page_config(page_title="Vision Study RAG", page_icon="📚")

# Main title
st.title("📚 Vision Study RAG")
st.write("A vision-based RAG system for studying PDFs with charts and images")

# Simple UI for collection creation
collection_name = st.text_input("Create a Collection:")
if st.button("Create Collection"):
    if collection_name:
        st.success(f"Collection '{collection_name}' created!")

# Basic uploader
if st.checkbox("Upload PDFs"):
    st.file_uploader("Choose PDF files", accept_multiple_files=True, type=['pdf'])
    if st.button("Process Files"):
        st.info("Files would be processed here (demo only).")

# Simple query interface
if st.checkbox("Query Documents"):
    query = st.text_input("Enter your question:")
    if st.button("Search"):
        st.write(f"Searching for: {query}")
        st.write("This is a placeholder response.")

# Footer
st.markdown("---")
st.write("Made with Streamlit. [GitHub Repository](https://github.com/tofunori/vision-study-rag)")
