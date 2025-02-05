import urllib
import torch
from PIL import Image
from torchvision import transforms, datasets
import torchvision.models as models
import torch.optim as optim
 
# Charger le modèle efficientnet_b7 sans poids pré-entraînés
model = models.efficientnet_v2_m(pretrained=False, num_classes=2)
 
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
 
train_dataset = datasets.ImageFolder(root='data/train', transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)
 
criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
 
for epoch in range(100):  # Nombre d'époques
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
       
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
 
        running_loss += loss.item()
    print(f"Époque {epoch+1}, Perte : {running_loss / len(train_loader)}")
 
# Sauvegarder les poids
torch.save(model.state_dict(), 'efficientnet_model.pth')