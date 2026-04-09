import fitz  # PyMuPDF
import os
import json

def extract_knowledge_base(pdf_path, output_image_dir):
    """
    Extracts text and renders full pages as images for vision processing.
    """
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)

    doc = fitz.open(pdf_path)
    knowledge_chunks = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        chunk = {
            "source": os.path.basename(pdf_path),
            "page": page_num + 1,
            "text": text.strip(),
            "images": []
        }
        
        pix = page.get_pixmap(dpi=100)
        base_name = os.path.basename(pdf_path).replace('.pdf', '')
        image_filename = f"{base_name}_page_{page_num+1}.png"
        image_filepath = os.path.join(output_image_dir, image_filename)
        
        pix.save(image_filepath)
        chunk["images"].append(image_filepath)
            
        knowledge_chunks.append(chunk)
        print(f"Processed {base_name} Page {page_num + 1} - Rendered image and extracted text.")

    return knowledge_chunks

if __name__ == "__main__":
    files_to_process = [
        "files/owner-manual.pdf",
        "files/selection-chart.pdf",
        "files/quick-start-guide.pdf"
    ]
    
    image_output = "extracted_assets"
    all_knowledge = []
    
    print("Starting extraction engine...")
    for file in files_to_process:
        if os.path.exists(file):
            chunks = extract_knowledge_base(file, image_output)
            all_knowledge.extend(chunks)
        
    # NEW: Save the extracted text so the agent can read it!
    with open("knowledge.json", "w") as f:
        json.dump(all_knowledge, f, indent=4)
        
    print("Extraction complete. Saved text to 'knowledge.json' and images to 'extracted_assets/'.")
