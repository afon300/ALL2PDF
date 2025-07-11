import os
from PIL import Image

# A list of common image file extensions to look for.
SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tiff']

def convert_image_to_pdf(image_path: str, pdf_path: str):
    """
    Converts a single image file to a PDF file.

    Args:
        image_path (str): The full path to the source image file.
        pdf_path (str): The full path where the converted PDF will be saved.
    """
    try:
        # Open the image using the Pillow library
        image = Image.open(image_path)

        # Convert the image to RGB mode if it has an alpha channel (like RGBA in PNGs)
        # The PDF format does not support transparency well.
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Save the image as a PDF
        image.save(pdf_path, "PDF", resolution=100.0)
        print(f"✅ Successfully converted '{os.path.basename(image_path)}' to PDF.")
    
    except FileNotFoundError:
        print(f"❌ Error: The file '{os.path.basename(image_path)}' was not found.")
    except Exception as e:
        print(f"❌ Error converting '{os.path.basename(image_path)}': {e}")


def create_output_directory(base_path: str, folder_name: str = "converted_pdfs") -> str:
    """
    Creates a new directory if it does not already exist.

    Args:
        base_path (str): The parent path where the new folder will be created.
        folder_name (str): The name of the new folder.

    Returns:
        str: The full path to the created directory.
    """
    # Join the base path and the new folder name to create the full path
    directory_path = os.path.join(base_path, folder_name)
    
    try:
        # Create the directory. The `exist_ok=True` argument prevents an error
        # if the directory already exists.
        os.makedirs(directory_path, exist_ok=True)
        return directory_path
    except OSError as e:
        print(f"❌ Error creating directory '{directory_path}': {e}")
        return None


def process_files_at_root(drive_path: str):
    """
    Finds all images at the root of the given path, converts them to PDF,
    and saves them in a new directory.

    Args:
        drive_path (str): The path to the root of the drive (e.g., a USB stick).
    """
    print(f"🔍 Scanning directory: {drive_path}")

    # 1. Create the output directory for the PDFs
    output_dir = create_output_directory(drive_path, "PDF_Conversions")
    if not output_dir:
        print("Could not create an output directory. Aborting.")
        return
    
    print(f"📄 Converted files will be saved in: '{output_dir}'")
    
    # 2. Get a list of all items at the root of the drive path
    try:
        all_items = os.listdir(drive_path)
    except FileNotFoundError:
        print(f"❌ Error: The path '{drive_path}' does not exist.")
        return
        
    image_files_found = 0

    # 3. Loop through all items to find image files
    for item_name in all_items:
        # Get the full path of the item
        item_path = os.path.join(drive_path, item_name)
        
        # Check if it's a file and if the extension is in our supported list
        is_image = any(item_name.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS)

        if os.path.isfile(item_path) and is_image:
            image_files_found += 1
            # Create the name for the new PDF file
            file_name_without_ext = os.path.splitext(item_name)[0]
            pdf_filename = f"{file_name_without_ext}.pdf"
            pdf_output_path = os.path.join(output_dir, pdf_filename)
            
            # 4. Convert the found image to PDF
            convert_image_to_pdf(item_path, pdf_output_path)

    if image_files_found == 0:
        print("\nNo supported image files found at the root of the specified path.")
    else:
        print(f"\n✨ Process finished. Found and processed {image_files_found} image(s).")