import os.path
from transformers import pipeline
from transformers import ViTForImageClassification, ViTImageProcessor
import json
from PIL import Image
import torch


class ViT:
    def __init__(self):
        self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
        self.processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")

        with open(r"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/a_dummy/imagenet-simple-labels.json", "r") as f:
            class_labels = json.load(f)
            self.class_labels = list(class_labels.values())
            print(type(self.class_labels), len(self.class_labels))

    def load_image(self, im_path):
        # Load your image
        image = Image.open(im_path)
        return image

    def predict_label(self, image):
        # Preprocess the image and generate predictions
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        # Get the predicted class
        predicted_class = torch.argmax(logits).item()
        predicted_class_name = self.class_labels[predicted_class - 1]
        print(predicted_class_name)


class ZeroClassifier:
    def __init__(self):
        self.checkpoint = "openai/clip-vit-large-patch14"
        self.detector = pipeline(model=self.checkpoint, task="zero-shot-image-classification", device="cuda")
        with open(r"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/a_dummy/imagenet-simple-labels.json", "r") as f:
            class_labels = json.load(f)
            self.class_labels = list(class_labels.values())

    def load_image(self, im_path):
        # Load your image
        image = Image.open(im_path)
        return image

    def predict_label(self, image):
        obj_name = self.detector(image, candidate_labels=self.class_labels)
        max_label = max(obj_name, key=lambda x: x['score'])
        return max_label['label'], max_label['score']


def main():
    source = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_objects"
    vit = ZeroClassifier()
    for i in range(1, 15):
        im_path = os.path.join(source, f"obj_top_{i}.png")
        # vit = ViT()

        image = vit.load_image(im_path)
        obj_name, _ = vit.predict_label(image)
        print(obj_name)


if __name__ == '__main__':
    main()
