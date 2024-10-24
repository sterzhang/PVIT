import json
import os
import argparse
from PIL import Image
import torch
from torchvision.ops import box_convert
from tqdm import tqdm
from groundingdino.util.inference import load_model, load_image, predict

def main(input_file, image_dir, output_file, start_line, end_line, person_output_dir):
    """
    Processes images from a JSONL file, performs model inference, crops detected persons, 
    and saves the results in JSONL format where the 'image' field contains the cropped person's path.
    """
    # Ensure person output directory exists
    os.makedirs(person_output_dir, exist_ok=True)

    # Load model
    model = load_model(
        "./GroundingDINO/groundingdino/config/GroundingDINO_SwinB_cfg.py",
        "./weights/groundingdino_swinb_cogcoor.pth"
    )

    # Inference configuration
    text_prompt = "person"
    box_threshold = 0.35
    text_threshold = 0.25

    with open(output_file, 'a') as outfile, open(input_file, 'r') as infile:
        lines = infile.readlines()
        for i, line in enumerate(tqdm(lines, desc="Person Extraction and Cropping")):
            if i < start_line: continue
            if i >= end_line: break

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            image_name = data.get('image')
            if not image_name: continue

            image_path = os.path.join(image_dir, image_name)

            try:
                image_source, image = load_image(image_path)
                boxes, logits, phrases = predict(
                    model=model,
                    image=image,
                    caption=text_prompt,
                    box_threshold=box_threshold,
                    text_threshold=text_threshold
                )
            except FileNotFoundError:
                print(f"Error processing {image_path}")
                continue

            if len(boxes) < 2: continue

            # Crop and save the detected persons, then update the JSONL output
            base_image_name = os.path.splitext(image_name)[0]
            cropped_image_paths = crop_and_save_person(image_path, boxes, person_output_dir, base_image_name)

            # Write results with the cropped image paths to the output JSONL
            for cropped_image_path in cropped_image_paths:
                result = {
                    'image': cropped_image_path  # Store the path relative to person_output_dir
                }
                outfile.write(json.dumps(result) + '\n')

    print(f'Results saved to {output_file}')

def crop_and_save_person(image_path, boxes, person_output_dir, image_name):
    """
    Crops detected bounding boxes from the image and saves them as separate files.
    Returns a list of the saved file paths relative to person_output_dir.
    """
    cropped_image_paths = []
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            boxes = torch.tensor(boxes) * torch.tensor([width, height, width, height])
            xyxy_boxes = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()

            for idx, box in enumerate(xyxy_boxes):
                left, top, right, bottom = box
                cropped_img = img.crop((left, top, right, bottom))

                # Create a folder named after the base image name
                image_folder = os.path.join(person_output_dir, image_name)
                os.makedirs(image_folder, exist_ok=True)

                # Save each cropped image
                output_file_name = f"{idx}.jpg"
                output_file_path = os.path.join(image_folder, output_file_name)
                cropped_img.save(output_file_path)

                # Store the relative path to the cropped image
                relative_path = os.path.relpath(output_file_path, person_output_dir)
                cropped_image_paths.append(relative_path)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

    return cropped_image_paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images, annotate bounding boxes, crop, and save persons")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSONL file")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing the images")
    parser.add_argument("--output_file", type=str, required=True, help="Path to the output JSONL file")
    parser.add_argument("--start_line", type=int, default=0, help="Starting line number to process")
    parser.add_argument("--end_line", type=int, default=999999999, help="Ending line number to process")
    parser.add_argument("--person_output_dir", type=str, required=True, help="Directory to save cropped person images")
    args = parser.parse_args()

    main(args.input_file, args.image_dir, args.output_file, args.start_line, args.end_line, args.person_output_dir)
