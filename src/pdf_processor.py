import pypdfium2 as pdfium
import numpy as np
from PIL import Image

def convert_pdf_to_images(pdf_path, dpi=300):
    """Convert PDF file to a list of images (one per page).
    
    Args:
        pdf_path (str): Path to the PDF file
        dpi (int): DPI for rendering (higher means better quality but larger images)
        
    Returns:
        list: List of PIL Image objects, one per page
    """
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        page_count = len(pdf)
        
        images = []
        for page_idx in range(page_count):
            # Load the page
            page = pdf[page_idx]
            
            # Render the page
            bitmap = page.render(
                scale=dpi/72,  # 72 DPI is the PDF standard
                rotation=0,
                crop=(0, 0, 0, 0)
            )
            
            # Convert to numpy array
            image_data = np.frombuffer(bitmap.raw_data, dtype=np.uint8)
            image_data = image_data.reshape(bitmap.height, bitmap.width, 4)  # RGBA
            
            # Convert to RGB (dropping alpha channel) and to PIL Image
            image = Image.fromarray(image_data[:, :, :3])
            images.append(image)
        
        return images
    
    except Exception as e:
        raise Exception(f"Error converting PDF to images: {str(e)}")
