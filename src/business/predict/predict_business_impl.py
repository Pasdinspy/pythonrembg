from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import io
from torchvision import datasets
from typing import Tuple
from src.business.image.image_business import ImageBusiness
from src.business.predict.predict_business import PredictBusiness

class PredictBusinessImpl(PredictBusiness):
    def __init__(self):
        self.image_business = ImageBusiness.get_instance()

    def loaded_device(self) -> torch.device:
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def loaded_model(self, device: torch.device) -> torch.nn.Module:
        try:
            model = models.efficientnet_v2_m(pretrained=False, num_classes=2)
            model.load_state_dict(torch.load('efficientnet_model.pth'))
            model = model.to(device)
            print("Le modèle a été chargé avec succès.")
            return model
        except FileNotFoundError:
            print("Erreur : Le fichier 'efficientnet_model.pth' est introuvable. Veuillez entraîner le modèle.")
            raise
        except Exception as e:
            print(f"Erreur lors du chargement du modèle : {e}")
            raise

    def predict(self, image_bytes: bytes) -> Tuple[float, str, Image.Image]:
        device = self.loaded_device()
        model = self.loaded_model(device)
        image = Image.open(io.BytesIO(image_bytes))
        image = self.image_business.remove_background(image)
        image = self.image_business.auto_crop(image)
        image = self.image_business.auto_redim(image)
        
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
        image_tensor = transform(image).unsqueeze(0).to(device)
    
        model.eval()
        with torch.no_grad():
            output = model(image_tensor)
            _, predicted = torch.max(output, 1)
            probabilities = torch.nn.functional.softmax(output, dim=1)

        probabilities_list = probabilities.squeeze(0).tolist()
        class_id = predicted.item()
    
        train_dataset = datasets.ImageFolder(root='data/train', transform=transform)
        class_name = train_dataset.classes[class_id]
    
        return probabilities_list[class_id], class_name, image