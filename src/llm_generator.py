import os
import requests
from typing import List, Dict, Any

def generate_response(query: str, results: List[Dict[str, Any]], use_ollama: bool = True) -> str:
    """Generate a response using either Ollama (local) or OpenAI.
    
    Args:
        query (str): The user's query
        results (list): The retrieved documents with metadata
        use_ollama (bool): Whether to use Ollama or OpenAI
        
    Returns:
        str: The generated response
    """
    if use_ollama:
        return generate_response_ollama(query, results)
    else:
        return generate_response_openai(query, results)

def generate_response_ollama(query: str, results: List[Dict[str, Any]]) -> str:
    """Generate a response using Ollama (local LLM).
    
    Args:
        query (str): The user's query
        results (list): The retrieved documents with metadata
        
    Returns:
        str: The generated response
    """
    try:
        # Get Ollama model name from env
        model = os.environ.get("OLLAMA_MODEL", "llama3.2-vision")
        
        # Prepare images for Ollama
        images = []
        for result in results:
            if "image" in result.get("metadata", {}):
                image_data = result["metadata"]["image"]
                images.append(image_data)
        
        # Prepare prompt for Ollama
        prompt = f"Please answer the following question using only the information visible in the provided images. Question: {query}"
        
        # Make request to Ollama API
        ollama_url = "http://localhost:11434/api/chat"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": images
                }
            ],
            "stream": False
        }
        
        response = requests.post(ollama_url, json=payload)
        
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return f"Error generating response: {response.text}"
    
    except Exception as e:
        return f"Error generating response with Ollama: {str(e)}"

def generate_response_openai(query: str, results: List[Dict[str, Any]]) -> str:
    """Generate a response using OpenAI API.
    
    Args:
        query (str): The user's query
        results (list): The retrieved documents with metadata
        
    Returns:
        str: The generated response
    """
    try:
        from openai import OpenAI
        
        # Get API key from env
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return "Error: OpenAI API key not found in environment variables"
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Prepare images
        image_content = []
        for result in results:
            if "image" in result.get("metadata", {}):
                image_data = result["metadata"]["image"]
                image_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                })
        
        # Prepare full content
        content = [
            {"type": "text", "text": f"Please answer the following question based only on the information visible in the provided document images: {query}"}
        ] + image_content
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4-vision-preview"
            messages=[{
                "role": "user",
                "content": content
            }],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating response with OpenAI: {str(e)}"
