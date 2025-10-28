# modules/processing/ocr_processor.py
"""
OCR Processor - Extracts text and UI elements from screenshots
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import json

def preprocess_image_for_ocr(image_path: str) -> np.ndarray:
    """
    Preprocess image for better OCR results
    
    Args:
        image_path: Path to screenshot
    
    Returns:
        Preprocessed image as numpy array
    """
    # Read image
    img = cv2.imread(str(image_path))
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Noise removal
    gray = cv2.medianBlur(gray, 3)
    
    return gray

def extract_text_from_screenshot(screenshot_path: str) -> Dict[str, Any]:
    """
    Extract text and metadata from a single screenshot
    
    Args:
        screenshot_path: Path to screenshot file
    
    Returns:
        Dictionary with extracted text and metadata
    """
    try:
        # Preprocess image
        processed_img = preprocess_image_for_ocr(screenshot_path)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(processed_img)
        
        # Extract detailed data (words with positions)
        data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)
        
        # Filter out empty text
        words_with_positions = []
        for i, word in enumerate(data['text']):
            if word.strip():
                words_with_positions.append({
                    'text': word,
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'confidence': data['conf'][i]
                })
        
        # Detect UI elements (buttons, input fields) based on text patterns
        ui_elements = detect_ui_elements(words_with_positions)
        
        return {
            'file': str(screenshot_path),
            'text': text.strip(),
            'word_count': len(text.split()),
            'words_with_positions': words_with_positions[:50],  # Limit to 50 for JSON size
            'ui_elements': ui_elements,
            'success': True
        }
    
    except Exception as e:
        return {
            'file': str(screenshot_path),
            'error': str(e),
            'success': False
        }

def detect_ui_elements(words_with_positions: List[Dict]) -> List[Dict]:
    """
    Detect potential UI elements from OCR data
    
    Args:
        words_with_positions: List of words with position data
    
    Returns:
        List of detected UI elements
    """
    ui_elements = []
    
    # Common UI element keywords
    button_keywords = ['button', 'click', 'submit', 'ok', 'cancel', 'save', 'delete', 'add', 'remove']
    input_keywords = ['enter', 'input', 'type', 'search', 'text', 'field']
    
    for word_data in words_with_positions:
        word_lower = word_data['text'].lower()
        
        # Detect buttons
        if any(keyword in word_lower for keyword in button_keywords):
            ui_elements.append({
                'type': 'button',
                'text': word_data['text'],
                'position': {
                    'x': word_data['x'],
                    'y': word_data['y']
                }
            })
        
        # Detect input fields
        elif any(keyword in word_lower for keyword in input_keywords):
            ui_elements.append({
                'type': 'input',
                'text': word_data['text'],
                'position': {
                    'x': word_data['x'],
                    'y': word_data['y']
                }
            })
    
    return ui_elements

def extract_text_from_screenshots(screenshot_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Extract text from multiple screenshots
    
    Args:
        screenshot_paths: List of screenshot file paths
    
    Returns:
        List of OCR results for each screenshot
    """
    results = []
    
    for i, path in enumerate(screenshot_paths):
        print(f"   Processing screenshot {i+1}/{len(screenshot_paths)}...", end='\r')
        result = extract_text_from_screenshot(path)
        results.append(result)
    
    print(f"   Processed {len(screenshot_paths)} screenshots    ")
    
    return results

def get_combined_text(ocr_results: List[Dict]) -> str:
    """
    Combine all extracted text from multiple screenshots
    
    Args:
        ocr_results: List of OCR results
    
    Returns:
        Combined text string
    """
    all_text = []
    for result in ocr_results:
        if result.get('success') and result.get('text'):
            all_text.append(result['text'])
    
    return '\n\n'.join(all_text)