import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

def describe_image(image_path):
    try:
        print("[INFO] Loading model and processor...")
        
        # Load processor & model for BLIP-2
        processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b", 
            torch_dtype=torch.float16  # Recommended for BLIP-2 models
        )

        # Use GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        # Load and preprocess image
        print("[INFO] Processing image...")
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)

        # Generate caption
        print("[INFO] Generating description...")
        generated_ids = model.generate(**inputs)
        caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        return f"Image Description: {caption}"

    except FileNotFoundError:
        return "[ERROR] Image file not found. Check the path!"
    except Exception as e:
        return f"[ERROR] An error occurred: {str(e)}"

# Example Usage
if __name__ == "__main__":
    image_path = r"D:\Python Projects 2025\images\Supercar_Lineup_(18092106572).jpg"
    result = describe_image(image_path)
    print(result)
