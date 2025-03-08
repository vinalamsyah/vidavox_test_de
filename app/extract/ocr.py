import pytesseract
import pandas as pd
import image_processing as ip

def extract_text_from_pdf(pdf_path):
    """Extract text from a multi-page scanned PDF."""
    images = ip.pdf_to_image(pdf_path) # Convert PDF pages to images
    extracted_text = ""
    dict_like = {
        'page': [],
        'number': [],
        'text': []
    }
    
    for i, image in enumerate(images):
        processed_image, segments = ip.preprocess_image(image) # Image Pre-processing

        # SAVING IMAGE
        ip.save_image(f'{i}-0', processed_image)
        ip.save_image(f'{i}', segments, multiple=True)

        # OCR
        tmp = [ pytesseract.image_to_string(sgmt, lang='eng', config='--psm 1').strip() for sgmt in segments ]
        extracted_text += f"\n--- Page {i+1} ---\n{'\n---\n'.join(tmp)}\n"

        dict_like['page'] += [ i for x in range(len(tmp)) ]
        dict_like['number'] += [ x for x in range(len(tmp)) ]
        dict_like['text'] += tmp

    return dict_like, extracted_text


def save_text_to_file(text, output_path):
    """Save extracted text to a .txt file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Text successfully saved to {output_path}")


if __name__ == '__main__':
    pdf_path = r'D:\Personal\vidavox_test_de\AR for improved learnability.pdf'
    output_path = r'D:\Personal\vidavox_test_de\result.txt'

    data, text = extract_text_from_pdf(pdf_path)
    df = pd.DataFrame(data)
    df.to_csv('test.csv', sep=';')
    save_text_to_file(text, output_path)