import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk


# Path to Tesseract executable (update the path if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\inesb\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Step 1: Detect blue regions and save the blue mask
def extract_and_save_blue_mask(image_path, output_path="blue_mask.png"):
    image = cv2.imread(image_path)

    # Convert to HSV and detect blue regions
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Save the blue mask
    cv2.imwrite(output_path, blue_mask)
    return output_path

# Step 2: Preprocess the blue mask image for OCR
def preprocess_image_for_ocr(image_path):
    img = Image.open(image_path)

    # Resize the image for better OCR accuracy
    img_resized = img.resize((img.width * 4, img.height * 4), Image.LANCZOS)

    # Convert to grayscale
    img_gray = img_resized.convert('L')

    # Ensure all text is black
    img_black_text = img_gray.point(lambda p: 0 if p < 128 else 255)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img_black_text)
    img_enhanced = enhancer.enhance(20.0)

    # Sharpen the image
    img_sharpened = img_enhanced.filter(ImageFilter.SHARPEN)

    # Apply median filter to reduce noise
    img_filtered = img_sharpened.filter(ImageFilter.MedianFilter(size=3))

    # Binarize the image using Otsu's method
    img_array = np.array(img_filtered)
    _, img_thresh = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Dilation to enhance text features
    kernel = np.ones((2, 2), np.uint8)
    img_dilated = cv2.dilate(img_thresh, kernel, iterations=1)

    # Convert back to a PIL image
    return Image.fromarray(img_dilated)

# Step 3: Extract text from the processed image using Tesseract OCR
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='eng+fra')
    return text

# Step 4: Clean the extracted text using NLP techniques
def clean_extracted_text(text):
    # Find the first occurrence of 'https' and keep the text starting from that point
    https_index = text.find('https')
    if https_index != -1:
        text = text[https_index:]

    # Remove all spaces from the text to make it a single line
    cleaned_text = text.replace(' ', '').replace('\n', '')

    return cleaned_text

# Example usage
    # if __name__ == '__main__':
    # Step 1: Extract and save the blue mask
    #original_image_path = 'C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\screenshots\\last_screenshot.png'  # Path to your original image
   #blue_mask_path = extract_and_save_blue_mask(original_image_path)

    # Step 2: Preprocess the blue mask image for OCR
    #preprocessed_image = preprocess_image_for_ocr(blue_mask_path)

    # Step 3: Extract text from the preprocessed image
    #extracted_text = extract_text_from_image(preprocessed_image)

    # Step 4: Clean and format the extracted text
    #cleaned_text = clean_extracted_text(extracted_text)

    # Output the results
    #print("Cleaned Text:\n", cleaned_text)
