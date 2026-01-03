from huggingface_hub import Padding
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class Librarian:
    def __init__(self):
        self.model_id = "openai/clip-vit-base-patch32"
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.labels = ["sunset", "waterfall", "mountain", "forest", "ocean", "cityscape", "night", "snowy"]

        print(f"Librarian loading {self.model_id} on {self.device}")
        self.model = CLIPModel.from_pretrained(self.model_id).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.model_id, use_fast=True)

    def analyze_image(self, image_path: str, threshold: float = 0.15):
        """Analyzes an image and returns a list of valid labels."""

        try:
            image = Image.open(image_path)
            inputs = self.processor(
                text = self.labels,
                images = image,
                return_tensors="pt",
                padding=True
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probs = outputs.logits_per_image.softmax(dim=1).cpu().numpy()[0]

            detected = [
                self.labels[i] for i, prob in enumerate(probs) if prob > threshold
            ]
            return detected
        except Exception as e:
            print(f"Librarian Error: {e}")
            return []

librarian = Librarian()