from PIL import Image
from typing import Dict
from rembg import remove
import numpy as np
import cv2
from skimage.feature import graycomatrix, graycoprops
from scipy.stats import kurtosis, skew
from src.business.image.image_business import ImageBusiness

class ImageBusinessImpl(ImageBusiness):

    def remove_background(self, image: Image.Image) -> Image.Image:
        # Retirer le fond d'une image
        image = image.convert("RGB")
        return remove(image)

    def auto_crop(self, image: Image.Image) -> Image.Image:
        # Centrer et recadrer une image
        image_array = np.array(image.convert("RGBA"))
        pixel_transparent = image_array[:, :, 3]
        pixels = np.where(pixel_transparent > 0)
        top = np.min(pixels[0])
        bottom = np.max(pixels[0])
        left = np.min(pixels[1])
        right = np.max(pixels[1])
        return image.crop((left, top, right + 1, bottom + 1))

    def auto_redim(self, image: Image.Image) -> Image.Image:
        # Redimensionner l'image
        image = image.convert("RGB")
        return image.resize((224, 224))

    def auto_morpho(self, image: Image.Image) -> Image.Image:
        # Appliquer une transformation morphologique
        image = image.convert("RGB")
        image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        _, image = cv2.threshold(image, 130, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

    def analyze_texture(self, image: Image.Image) -> Dict[str, float]:
        # Analyse des textures
        image_array = np.array(image.convert("RGB"))
        gris = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        distances = [1]
        angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
        glcm = graycomatrix(gris, distances, angles, symmetric=True, normed=True)
        textures = {
            'contraste': float(graycoprops(glcm, 'contrast').mean()),
            'dissimilarite': float(graycoprops(glcm, 'dissimilarity').mean()),
            'homogeneite': float(graycoprops(glcm, 'homogeneity').mean()),
            'energie': float(graycoprops(glcm, 'energy').mean()),
            'correlation': float(graycoprops(glcm, 'correlation').mean()),
            'asm': float(graycoprops(glcm, 'ASM').mean()),
            'moyenne': float(np.mean(gris)),
            'ecart_type': float(np.std(gris)),
            'asymetrie': float(skew(gris.flatten())),
            'aplatissement': float(kurtosis(gris.flatten())),
            'entropie': float(-np.sum(np.multiply(glcm, np.log2(glcm + np.finfo(float).eps))).mean())
        }
        return textures
