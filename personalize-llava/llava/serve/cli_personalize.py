import os
os.environ["CUDA_VISIBLE_DEVICES"] = "7"
import argparse
import torch

from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.conversation import conv_templates, SeparatorStyle
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path

from PIL import Image

import requests
from PIL import Image
from io import BytesIO
from transformers import TextStreamer
import readline

def load_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image

face_prefix = "<image>\nThis is {name}.\n<image>\nAnswer the following question based on the image:\n{question}"
def main(args):
    # Model
    disable_torch_init()
    readline.parse_and_bind("")

    model_name = get_model_name_from_path(args.model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(args.model_path, args.model_base, model_name, args.load_8bit, args.load_4bit, device=args.device)

    if "llama-2" in model_name.lower():
        conv_mode = "llava_llama_2"
    elif "mistral" in model_name.lower():
        conv_mode = "mistral_instruct"
    elif "v1.6-34b" in model_name.lower():
        conv_mode = "chatml_direct"
    elif "v1" in model_name.lower():
        conv_mode = "llava_v1"
    elif "mpt" in model_name.lower():
        conv_mode = "mpt"
    else:
        conv_mode = "llava_v0"

    if args.conv_mode is not None and conv_mode != args.conv_mode:
        print('[WARNING] the auto inferred conversation mode is {}, while `--conv-mode` is {}, using {}'.format(conv_mode, args.conv_mode, args.conv_mode))
    else:
        args.conv_mode = conv_mode
    #
    # conv = conv_templates[args.conv_mode].copy()
    # if "mpt" in model_name.lower():
    #     roles = ('user', 'assistant')
    # else:
    #     roles = conv.roles
    #
    # image = load_image(args.image_file)
    # image_size = image.size
    # # Similar operation in model_worker.py
    # image_tensor = process_images([image], image_processor, model.config)
    # if type(image_tensor) is list:
    #     image_tensor = [image.to(model.device, dtype=torch.float16) for image in image_tensor]
    # else:
    #     image_tensor = image_tensor.to(model.device, dtype=torch.float16)

    while True:
        conv = conv_templates[args.conv_mode].copy()
        if "mpt" in model_name.lower():
            roles = ('user', 'assistant')
        else:
            roles = conv.roles

        try:
            img_name = input("Enter image path (or 'q' to quit): ")
            if img_name.lower() == 'q':
                break
            face_name = input("Enter face path (or 'q' to quit): ")
            if face_name.lower() == 'q':
                break
            name = input(f"name: ")
            question = input(f"question: ")
        except EOFError:
            question = ""
        if not question:
            print("exit...")
            break
        # ++++++++++++++<DEBUG>+++++++++++++++
        # name = "Bobby"
        # question = "What is Bobby wearing?"
        # face_name = "debug/personalize/coco-face/000000327481/0.jpg"
        # img_name = "debug/personalize/coco-person/000000327481/0.jpg"

        print(f"{roles[1]}: ", end="")

        image = load_image(img_name)
        face_image = load_image(face_name)
        image_size = image.size
        face_image_size = face_image.size
        # Similar operation in model_worker.py
        image_tensor = process_images([face_image, image], image_processor, model.config)
        if type(image_tensor) is list:
            image_tensor = [image.to(model.device, dtype=torch.float16) for image in image_tensor]
        else:
            image_tensor = image_tensor.to(model.device, dtype=torch.float16)
        # image_tensor, face_image_tensor = image_tensor[0], image_tensor[1]
        # first message
        # if model.config.mm_use_im_start_end:
        #     inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + inp
        # else:
        inp = face_prefix.format(name=name, question=question)
        image = None

        conv.append_message(conv.roles[0], inp)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)
        stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
        keywords = [stop_str]
        streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                images=image_tensor,
                image_sizes=[face_image_size, image_size],
                do_sample=True if args.temperature > 0 else False,
                temperature=args.temperature,
                max_new_tokens=args.max_new_tokens,
                streamer=streamer,
                use_cache=True)

        outputs = tokenizer.decode(output_ids[0]).strip()
        conv.messages[-1][-1] = outputs
        print(outputs)
        if args.debug:
            print("\n", {"prompt": prompt, "outputs": outputs}, "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="facebook/opt-350m")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--conv-mode", type=str, default=None)
    parser.add_argument("--temperature", type=float, default=0.5)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    main(args)
