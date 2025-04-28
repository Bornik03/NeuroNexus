import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image

print("Loading pre-trained models --->")
vit_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

resnet_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def caption_with_pretrained_model(image_path):
    img = Image.open(image_path).convert('RGB')
    pixel_values = image_processor(images=img, return_tensors="pt").pixel_values
    
    output_ids = vit_model.generate(pixel_values, max_length=16, num_beams=4)
    caption = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    
    return caption

def extract_features_and_caption(image_path):
    print("\nExtracting features using ResNet50 --->")
    
    img = keras_image.load_img(image_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    features = resnet_model.predict(x)
    print(f"Features shape: {features.shape}")
    
    print("Generating caption --->")
    caption = caption_with_pretrained_model(image_path)
    
    print(f"\n🖼️  Image Caption: {caption}")
    
    return features, caption

if __name__ == "__main__":
    image_path = r"C:\Users\borni\Downloads\WhatsApp Image 2025-04-28 at 11.28.04_a390eb0b.jpg"
    
    features, caption = extract_features_and_caption(image_path)
