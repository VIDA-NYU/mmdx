import numpy as np
from PIL import Image
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast


# TODO: consider using larger models such as openai/clip-vit-large-patch14
DEFAULT_MODEL_ID = "openai/clip-vit-base-patch32"


class ClipModel:
    def __init__(self, model_id=DEFAULT_MODEL_ID) -> None:
        self.tokenizer: CLIPTokenizerFast = CLIPTokenizerFast.from_pretrained(model_id)
        self.model: CLIPModel = CLIPModel.from_pretrained(model_id)
        self.processor: CLIPProcessor = CLIPProcessor.from_pretrained(model_id)

    def embed_text(self, query: str) -> np.ndarray:
        inputs = self.tokenizer([query], padding=True, return_tensors="pt")
        text_features = self.model.get_text_features(**inputs)
        return text_features.detach().numpy()[0]

    def embed_image(self, image: Image) -> np.ndarray:
        pixel_values = self.processor(images=image, return_tensors="pt")["pixel_values"]
        emb_tensor = self.model.get_image_features(pixel_values)
        return emb_tensor.detach().numpy()[0]

    def embed_image_path(self, image_path: str) -> np.ndarray:
        return self.embed_image(Image.open(image_path))
