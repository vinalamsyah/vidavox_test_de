import pytesseract
from img2table.document import Image
from io import BytesIO
from img2table.ocr import TesseractOCR

def extract_text(layouts):
    """Extract text from a multi-page scanned PDF."""
    text_format = ""
    tabular_format = []
    
    for i, layout in enumerate(layouts):
        print('OCRing')
        # OCR
        tmp = [ pytesseract.image_to_string(sgmt, lang='eng', config='--psm 1').strip() for sgmt in layout['segments'] ]
       
        text_format += f"\n--- Page {i+1} ---\n{'\n---\n'.join(tmp)}\n"
        tabular_format += [ 
            {'pagenumber': i+1, 'ordernumber': j+1, 'textvalue': text} 
            for j, text in enumerate(tmp)
        ]

    return tabular_format, text_format


def extract_table(images):
    """extracting tables"""

    # image = np.array(image) # Convert PIL image to NumPy array
    ocr = TesseractOCR()
    result = []

    for i, img in enumerate(images):
        binary_img = BytesIO()
        img.save(binary_img, format='PNG')
        source = Image(binary_img)
        tables = source.extract_tables(ocr=ocr, borderless_tables=True)
        result += [
            {'pagenumber': i+1, 'tablejson': tbl.df.to_json(), 'tableraw': tbl.df.to_dict(orient='index')} 
            for tbl in tables 
        ]

    return result



def save_text_to_file(text: str, output_path: str):
    """Save extracted text to a .txt file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Text successfully saved to {output_path}")


if __name__ == '__main__':
    # import pandas as pd
    import sys

    sys.path.append(r'D:\Personal\vidavox_test_de\app')
    from extract import image_processing as ip

    pdf_path = r'D:\Personal\vidavox_test_de\input\AR for improved learnability.pdf'
    output_path = r'D:\Personal\vidavox_test_de\result.txt'

    doc = ip.pdf_to_image(pdf_path)
    tables = extract_table(doc)
    print(tables)
    # df.to_csv('test.csv', sep=';')
    # save_text_to_file(text, output_path)