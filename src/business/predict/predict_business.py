from abc import ABC, abstractmethod
from PIL import Image
import torch
from typing import Tuple, List

class PredictBusiness(ABC):
    @staticmethod
    def get_instance():
        from src.business.predict.predict_business_impl import PredictBusinessImpl
        return PredictBusinessImpl()

    @abstractmethod
    def loaded_device(self) -> torch.device:
        pass

    @abstractmethod
    def loaded_model(self, device: torch.device) -> torch.nn.Module:
        pass

    @abstractmethod
    def predict(self, image_bytes: bytes) -> Tuple[float, str, Image.Image]:
        pass