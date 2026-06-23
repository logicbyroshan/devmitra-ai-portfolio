import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

def compress_image_to_webp(image_field, quality=80):
    """
    Compresses an image to WebP format if it's an image and not already a compressed WebP/SVG.
    """
    if not image_field or not image_field.name:
        return

    # Check extension
    filename = image_field.name
    ext = os.path.splitext(filename)[1].lower()
    
    # Don't convert SVGs or PDFs
    if ext in ['.svg', '.pdf', '.webp']:
        return

    try:
        # Open image using Pillow
        image = Image.open(image_field)
        
        # Convert to RGB if needed (e.g. RGBA for PNGs)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create a white background instead of black for transparency
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1]) # 3 is the alpha channel
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Save to BytesIO
        output = BytesIO()
        image.save(output, format='WEBP', quality=quality, method=4)
        output.seek(0)
        
        # Replace the file in the field with the new webp file
        new_filename = os.path.splitext(os.path.basename(filename))[0] + '.webp'
        image_field.save(new_filename, ContentFile(output.read()), save=False)
        
    except Exception as e:
        # If Pillow can't process it, just leave it as is
        print(f"Error compressing image: {e}")
