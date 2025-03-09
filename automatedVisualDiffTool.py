import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageChops

def pdf_to_images(pdf_path, output_folder):
    """ Convert a PDF into images, one per page. """
    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"page_{i+1}.png")
        img.save(img_path, "PNG")
        image_paths.append(img_path)

    return image_paths

def compare_images(img1_path, img2_path, diff_output_path):
    """ Compare two images and save differences. """
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    if img1.shape != img2.shape:
        print(f"Size mismatch: {img1_path} vs {img2_path}")
        return False

    # Compute absolute difference
    diff = cv2.absdiff(img1, img2)
    
    # Use a higher threshold value to detect more significant differences
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

    # Convert to BGR (color) for marking differences
    diff_colored = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)

    # Highlight differences with bright yellow to make it more visible
    diff_colored[thresh > 0] = [0, 255, 255]  # Yellow highlights differences

    # Adding a border (outline) around the differences to make them stand out more
    kernel = np.ones((5,5), np.uint8)
    border = cv2.dilate(thresh, kernel, iterations=1)

    # Apply the border on the diff image
    diff_colored[border > 0] = [255, 0, 0]  # Blue outline around the differences

    # Blend the diff image with the original image to keep details and enhance readability
    alpha = 0.6  # Control blending of original and diff image
    diff_blended = cv2.addWeighted(cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR), alpha, diff_colored, 1 - alpha, 0)

    # Save the final diff image
    cv2.imwrite(diff_output_path, diff_blended)
    return True

def compare_pdfs(pdf1, pdf2, output_folder):
    """ Full PDF comparison pipeline. """
    os.makedirs(output_folder, exist_ok=True)

    # Create subdirectories for pdf1 and pdf2
    pdf1_folder = os.path.join(output_folder, "pdf1")
    pdf2_folder = os.path.join(output_folder, "pdf2")
    os.makedirs(pdf1_folder, exist_ok=True)
    os.makedirs(pdf2_folder, exist_ok=True)

    # Convert PDFs to images
    pdf1_images = pdf_to_images(pdf1, pdf1_folder)
    pdf2_images = pdf_to_images(pdf2, pdf2_folder)

    if len(pdf1_images) != len(pdf2_images):
        print("PDFs have different page counts!")
        return

    # Compare each corresponding page
    for i in range(len(pdf1_images)):
        diff_output = f"{output_folder}/diff_page_{i+1}.png"
        compare_images(pdf1_images[i], pdf2_images[i], diff_output)
        print(f"Page {i+1} comparison saved at {diff_output}")

# Example Usage
pdf1_path = "/Users/kavyagarikapati/Desktop/Docs/coverLettermastercard.pdf"
pdf2_path = "/Users/kavyagarikapati/Desktop/Docs/CoverLetter Global Relay.pdf"
output_dir = "/Users/kavyagarikapati/Desktop/Docs/comparison_results"
compare_pdfs(pdf1_path, pdf2_path, output_dir)
