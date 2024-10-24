import os
import json
import numpy as np
from PIL import Image
import face_recognition
import tqdm
import argparse

def get_face(image_path):
    """
    Detects faces in the given image, adjusts the bounding box if necessary, and returns cropped face images and their coordinates.
    """
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return [], []

    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        print(f"No faces found in image: {image_path}")
        return [], []

    pil_images, coordinates = [], []

    for face_location in face_locations:
        top, right, bottom, left = face_location
        p_distance = bottom - top
        l_distance = right - left
        error = np.abs(p_distance - l_distance)
        
        # Adjust left and right coordinates based on error
        left_adjust = int(np.floor(error / 2))
        right_adjust = int(np.ceil(error / 2))
        
        # Ensure the cropping region is within the image boundaries
        top = max(0, top - 20)
        bottom = min(image.shape[0], bottom + 10)
        left = max(0, left - 15 - left_adjust)
        right = min(image.shape[1], right + 15 + right_adjust)
        
        # Crop the face from the image
        face_image = image[top:bottom, left:right]
        pil_images.append(Image.fromarray(face_image))
        coordinates.append([left, top, right, bottom])
    
    return pil_images, coordinates

def process_faces(input_file, person_dir, face_dir, output_file):
    """
    Processes a JSONL file with bounding box information, extracts faces from images, saves the face images,
    and stores the face image paths in the output JSON file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in tqdm.tqdm(infile, desc="Processing faces"):
            data = json.loads(line)
            image = data.get('image')

            i_path = os.path.join(person_dir, image)
        
            f_path = os.path.join(face_dir, os.path.dirname(image))

            pil_images, coordinates = get_face(i_path)

            # Only save the face if exactly one face was detected
            if len(coordinates) == 1:
                os.makedirs(f_path, exist_ok=True)
                face_image_path = os.path.join(face_dir, image)
                pil_images[0].save(face_image_path)

                # Modify the JSON structure to include the face image path
                data['image'] = face_image_path
                outfile.write(json.dumps(data) + '\n')
            else:
                print(f"Multiple faces found in {i_path}, skipping.")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract faces from images based on bounding box information and store results in output JSONL.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSONL file")
    parser.add_argument("--person_dir", type=str, required=True, help="Directory containing cropped person images")
    parser.add_argument("--face_dir", type=str, required=True, help="Directory to save cropped face images")
    parser.add_argument("--output_file", type=str, required=True, help="Path to save output JSONL with face image paths")
    
    args = parser.parse_args()

    # Process the faces using the provided arguments
    process_faces(args.input_file, args.person_dir, args.face_dir, args.output_file)
