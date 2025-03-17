from pdf2image import convert_from_path
import cv2
import numpy as np

POPPLER_PATH = r'C:\Users\MuhammadNAAL\AppData\Local\Programs\poppler-24.08.0\Library\bin'
COLOR_CODE = {
    'r': (255,0,0),
    'g': (0,255,0),
    'b': (0,0,255),
    'w': (255,255,255),
    '0': (0,0,0)
}

def pdf_to_image(filename: str):
    """Wrapper function for converting PDF to Pillow Image"""
    print('converting pdf to image')
    return convert_from_path(pdf_path=filename, poppler_path=POPPLER_PATH)

def _sort_contours(contours):
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    # centers = [ ( x + int(0.5*w), y + int(0.5*h) ) for x, y, w, h in boundingBoxes ]
    contours, boundingBoxes = zip(*sorted(zip(contours, boundingBoxes), key=lambda b: 10*b[1][0] + b[1][1]))
    
    return contours

def _draw_contours(base_image, output_image=None, line_color='r', line_width=1, min_w=0, min_h=0, min_area=0, is_numbered=False):
    if output_image is None:
        output_image = base_image.copy()

    contours, _ = cv2.findContours(base_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Contours
    contours = _sort_contours(contours)

    for i, cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)
        if w > min_w and h > min_h and w*h > min_area: # Filter out small contours
            output_image = cv2.rectangle(output_image, (x,y), (x+w,y+h), COLOR_CODE[line_color], line_width)
        if is_numbered:
            output_image = _contour_numbering(output_image, cnt, i)
    
    return output_image, contours

def _contour_numbering(image, cnt, i):
    # compute the center of the contour area
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the countour number on the image
    cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
        1.0, (0, 0, 255), 2)
    
    return image

def layouting(image):
    """Enhance the image for better OCR accuracy."""
    print('preprocessing image')

    image = np.array(image) # Convert PIL image to NumPy array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV) # Binarization

    kernel = np.ones((7,7))
    dilated = cv2.dilate(thresh, kernel, iterations = 5) # Dilation

    print('detecting contour')
    temp, _ = _draw_contours(dilated, line_color='w', line_width=-1) # First Contour
    final, contours = _draw_contours(temp, output_image=gray.copy(), line_color='0', line_width=2) #Second Contour

    _, result = cv2.threshold(final, 230, 255, cv2.THRESH_BINARY) # Binarization
    segments = [ result[y:y+h, x:x+w] for x, y, w, h in [ cv2.boundingRect(cnt) for cnt in contours ] ] # Mutilate the result image into segments

    return { 'full': result, 'segments': segments }

def image_clipping(image):
    print('preprocessing image')

    image = np.array(image) # Convert PIL image to NumPy array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV) # Binarization

    # kernel = np.ones((5,5))
    # dilated = cv2.dilate(thresh, kernel, iterations = 1) # Dilation

    print('detecting contour')
    tmp, _ = _draw_contours(thresh, line_color='w', line_width=-1, min_h=50, min_area=5100) # First Contour
    final, contours = _draw_contours(tmp, output_image=image.copy(), line_color='r', line_width=2, min_h=50, min_area=5100) # Second Contour

    result = final
    clips = [ image[y:y+h, x:x+w] for x, y, w, h in [ cv2.boundingRect(cnt) for cnt in contours ] if h > 50 and w*h > 5100 ] # Mutilate the result image into segments

    return clips


if __name__ == '__main__':
    import sys

    sys.path.append(r'D:\Personal\vidavox_test_de\app')
    from load.local import save_images, save_layouts

    images = pdf_to_image('D:\\Personal\\vidavox_test_de\\input\\AR for improved learnability.pdf')
    for i, image in enumerate(images):
        print('='*30)
        print(i)
        image = np.array(image)
        processed_image, segments = image_clipping(image)
        if processed_image is not None:
            # cv2.imwrite(f'{SAVE_IMG_PATH}\\{i}.png', processed_image)
            save_images(i,segments,multiple=True)
            save_images(f'{i}-0', processed_image)