from abc import ABC, abstractmethod
from PIL import Image
from typing import Dict

class ImageBusiness(ABC):
    @staticmethod
    def get_instance():
        from src.business.image.image_business_impl import ImageBusinessImpl
        return ImageBusinessImpl()
    
    @abstractmethod
    def remove_background(self, image: Image.Image) -> Image.Image:
        pass

    @abstractmethod
    def auto_crop(self, image: Image.Image) -> Image.Image:
        pass

    @abstractmethod
    def auto_redim(self, image: Image.Image) -> Image.Image:
        pass

    @abstractmethod
    def auto_morpho(self, image: Image.Image) -> Image.Image:
        pass

    @abstractmethod
    def analyze_texture(self, image: Image.Image) -> Dict[str, float]:
        pass