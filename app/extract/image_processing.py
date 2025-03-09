from pdf2image import convert_from_path
import cv2
import numpy as np

POPPLER_PATH = r'C:\Users\MuhammadNAAL\AppData\Local\Programs\poppler-24.08.0\Library\bin'
SAVE_IMG_PATH = r'D:\Personal\vidavox_test_de\tmp'

def pdf_to_image(filename: str):
    """Wrapper for convert PDF to Pillow Image function"""
    print('converting pdf to image')
    return convert_from_path(pdf_path=filename, poppler_path=POPPLER_PATH)

def sort_contours(contours):
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    # centers = [ ( x + int(0.5*w), y + int(0.5*h) ) for x, y, w, h in boundingBoxes ]
    contours, boundingBoxes = zip(*sorted(zip(contours, boundingBoxes), key=lambda b: 10*b[1][0] + b[1][1]))
    
    return contours

def contour_numbering(image, cnt, i):
    # compute the center of the contour area
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the countour number on the image
    cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
        1.0, (0, 0, 255), 2)
    
    return image

def preprocess_image(image):
    """Enhance the image for better OCR accuracy."""
    print('preprocessing image')

    image = np.array(image) # Convert PIL image to NumPy array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV) # Binarization

    kernel = np.ones((5,5))
    dilated = cv2.dilate(thresh, kernel, iterations = 5) # Dilation

    print('detecting contour')
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Contours
    contours = sort_contours(contours)

    # DRAWING CONTOUR
    for i, cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)
        if w*h > 5100: # Filter out small contours
            segmented = cv2.rectangle(gray,(x,y),(x+w,y+h),(0,0,0),2)
            # segmented = contour_numbering(segmented, cnt, i)

    _, result = cv2.threshold(segmented, 230, 255, cv2.THRESH_BINARY) # Binarization
    segments = [ result[y:y+h, x:x+w] for x, y, w, h in [ cv2.boundingRect(cnt) for cnt in contours ] if w*h > 5100 ] # Mutilate the result image into segments

    return result, segments

def save_image(filename, image, multiple=False):
    print('saving image')
    if multiple:
        for i, img in enumerate(image):
            cv2.imwrite(f'{SAVE_IMG_PATH}\\{filename}-{i+1}.png', img)

    else:
        cv2.imwrite(f'{SAVE_IMG_PATH}\\{filename}.png', image)

# Example usage:
# text_from_image = extract_text_from_image("research_paper.png")
# text_from_pdf = extract_text_from_pdf("research_paper.pdf")
# print(text_from_pdf)

if __name__ == '__main__':
    images = pdf_to_image('D:\\Personal\\vidavox_test_de\\AR for improved learnability.pdf')
    for i, image in enumerate(images):
        print('='*30)
        print(i)
        image = np.array(image)
        processed_image = preprocess_image(image)
        cv2.imwrite(f'{SAVE_IMG_PATH}\\zz.png', processed_image)