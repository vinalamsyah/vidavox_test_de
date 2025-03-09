import pytesseract
from . import image_processing as ip

def extract_text_from_pdf(pdf_path: str):
    """Extract text from a multi-page scanned PDF."""
    images = ip.pdf_to_image(pdf_path) # Convert PDF pages to images
    text_format = ""
    tabular_format = []
    
    for i, image in enumerate(images):
        processed_image, segments = ip.preprocess_image(image) # Image Pre-processing

        # SAVING IMAGE
        ip.save_image(f'{i}-0', processed_image)
        ip.save_image(f'{i}', segments, multiple=True)

        print('OCRing')
        # OCR
        tmp = [ pytesseract.image_to_string(sgmt, lang='eng', config='--psm 1').strip() for sgmt in segments ]
       
        text_format += f"\n--- Page {i+1} ---\n{'\n---\n'.join(tmp)}\n"
        tabular_format += [ 
            {'pagenumber': i+1, 'ordernumber': j+1, 'textvalue': text} 
            for j, text in enumerate(tmp)
        ]

    return tabular_format, text_format


def save_text_to_file(text: str, output_path: str):
    """Save extracted text to a .txt file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Text successfully saved to {output_path}")


if __name__ == '__main__':
    import pandas as pd

    pdf_path = r'D:\Personal\vidavox_test_de\AR for improved learnability.pdf'
    output_path = r'D:\Personal\vidavox_test_de\result.txt'

    data, text = extract_text_from_pdf(pdf_path)
    df = pd.DataFrame(data)
    df.to_csv('test.csv', sep=';')
    save_text_to_file(text, output_path)