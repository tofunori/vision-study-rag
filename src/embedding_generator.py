import torch
from transformers.utils.import_utils import is_flash_attn_2_available
from colpali_engine.models import ColQwen2, ColQwen2Processor
from typing import List
from PIL import Image

def get_device():
    """Get appropriate device for running the model."""
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"  # For Apple Silicon
    else:
        return "cpu"

def load_model(model_name="vidore/colqwen2-v1.0"):
    """Load ColPali model and processor.
    
    Args:
        model_name (str): HuggingFace model name
        
    Returns:
        tuple: (model, processor)
    """
    device_map = get_device()
    
    # Load model with appropriate settings
    model = ColQwen2.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map=device_map,
        attn_implementation="flash_attention_2" if is_flash_attn_2_available() else None,
    ).eval()
    
    # Load processor
    processor = ColQwen2Processor.from_pretrained(model_name)
    
    return model, processor

def generate_embeddings(model, processor, images: List[Image.Image]):
    """Generate embeddings for a list of images.
    
    Args:
        model: ColPali model
        processor: ColPali processor
        images: List of PIL Image objects
        
    Returns:
        List of embeddings, one per image
    """
    # Process images
    batch_images = processor.process_images(images).to(model.device)
    
    # Generate embeddings
    with torch.no_grad():
        embeddings = model(**batch_images)
    
    # Convert to CPU and standard format
    return [emb.cpu().numpy() for emb in embeddings]

def generate_query_embedding(model, processor, query: str):
    """Generate embedding for a query string.
    
    Args:
        model: ColPali model
        processor: ColPali processor
        query: Query string
        
    Returns:
        Query embedding
    """
    # Process query
    batch_query = processor.process_queries([query]).to(model.device)
    
    # Generate embedding
    with torch.no_grad():
        query_embedding = model(**batch_query)
    
    # Convert to CPU and standard format
    return query_embedding[0].cpu().numpy()
