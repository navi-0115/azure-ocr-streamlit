import cv2
import numpy as np


def adjust_gamma(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gamma_corrected = adjust_gamma(gray, gamma=0.3)
    denoised = cv2.fastNlMeansDenoising(gamma_corrected, None, h=10, templateWindowSize=7, searchWindowSize=21)
    adaptive_threshold = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    close_morphed = cv2.morphologyEx(adaptive_threshold, cv2.MORPH_CLOSE, kernel, iterations=1)
    kernel_erosion = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    final_image = cv2.erode(close_morphed, kernel_erosion, iterations=1)

    # Return the final preprocessed image
    return final_image