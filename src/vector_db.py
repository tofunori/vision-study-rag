import chromadb
import os
import numpy as np
from typing import List, Dict, Any

class VectorDatabase:
    def __init__(self, db_path="./chroma_db"):
        """Initialize the vector database.
        
        Args:
            db_path (str): Path to the database directory
        """
        # Create directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=db_path)
        
    def create_collection(self, collection_name: str):
        """Create a new collection.
        
        Args:
            collection_name (str): Name of the collection
        """
        try:
            self.client.get_or_create_collection(collection_name)
            return True
        except Exception as e:
            raise Exception(f"Error creating collection: {str(e)}")
    
    def list_collections(self) -> List[str]:
        """List all available collections.
        
        Returns:
            List of collection names
        """
        try:
            collections = self.client.list_collections()
            return [collection.name for collection in collections]
        except Exception as e:
            print(f"Error listing collections: {str(e)}")
            return []
    
    def add_document(self, collection_name: str, embedding: np.ndarray, metadata: Dict[str, Any]):
        """Add a document to the collection.
        
        Args:
            collection_name (str): Name of the collection
            embedding (np.ndarray): Document embedding
            metadata (dict): Document metadata
        """
        try:
            collection = self.client.get_or_create_collection(collection_name)
            
            # Convert embeddings to the format expected by ChromaDB
            # ChromaDB expects a 1D array, but ColPali returns 2D embeddings (tokens x dim)
            # We'll use max pooling to get a single representation
            if len(embedding.shape) > 1:
                # Apply max pooling across token dimension
                pooled_embedding = np.max(embedding, axis=0)
            else:
                pooled_embedding = embedding
            
            # Generate a unique ID
            doc_id = f"{metadata.get('filename', 'doc')}_{metadata.get('page', '0')}_{os.urandom(4).hex()}"
            
            # Add document to collection
            collection.add(
                ids=[doc_id],
                embeddings=[pooled_embedding.tolist()],
                metadatas=[metadata]
            )
            
            return True
        
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    def search(self, collection_name: str, query_embedding: np.ndarray, n_results: int = 3):
        """Search for similar documents.
        
        Args:
            collection_name (str): Name of the collection
            query_embedding (np.ndarray): Query embedding
            n_results (int): Number of results to return
            
        Returns:
            List of results with metadata
        """
        try:
            collection = self.client.get_collection(collection_name)
            
            # Apply max pooling across token dimension for query embedding
            if len(query_embedding.shape) > 1:
                pooled_query = np.max(query_embedding, axis=0)
            else:
                pooled_query = query_embedding
            
            # Search for similar documents
            results = collection.query(
                query_embeddings=[pooled_query.tolist()],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "score": results["distances"][0][i] if "distances" in results else 0,
                    "metadata": results["metadatas"][0][i]
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []
