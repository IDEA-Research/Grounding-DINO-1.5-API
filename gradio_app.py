import os 
import argparse
from typing import Dict, List
from gdino import GroundingDINOAPIWrapper, visualize
import gradio as gr
import numpy as np
import cv2
def arg_parse():
    parser = argparse.ArgumentParser(description="Gradio Demo for T-Rex2")
    parser.add_argument(
        "--token",
        type=str,
        help="This token is only for gradio space. Please do not take it away for your own purpose!",
    )
    args = parser.parse_args()
    return args

def resize_image_with_aspect_ratio(image: np.ndarray, min_size: int = 800, max_size: int = 1333) -> np.ndarray:
    h, w = image.shape[:2]
    aspect_ratio = w / h

    # Determine the scaling factor based on the constraints
    if h < w:
        new_height = min_size
        new_width = int(new_height * aspect_ratio)
        if new_width > max_size:
            new_width = max_size
            new_height = int(new_width / aspect_ratio)
    else:
        new_width = min_size
        new_height = int(new_width / aspect_ratio)
        if new_height > max_size:
            new_height = max_size
            new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_image

def inference(image, prompt: str, return_mask: bool = False, return_score: bool = False) -> gr.Image:
    # shrink image first to save computation
    if return_mask:
        image = resize_image_with_aspect_ratio(image, min_size=600, max_size=1000)
    prompts = dict(image=image, prompt=prompt)
    results = gdino.inference(prompts, return_mask=return_mask)
    image_pil = visualize(image, results, return_mask=return_mask, draw_score=return_score)
    return image_pil

args = arg_parse()
gdino = GroundingDINOAPIWrapper(args.token)

if  __name__ == "__main__":
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="Input Image")
            with gr.Column():
                output_image = gr.Image(label="Output Image")
        with  gr.Row():
            return_mask = gr.Checkbox(label="Return Mask")
            return_score = gr.Checkbox(label="Return Score")
            prompt = gr.Textbox(label="Prompt", placeholder="e.g., person.pigeon.tree")
            run = gr.Button(value="Run")
        with gr.Row():
            gr.Examples(
                examples=[
                    ['asset/demo.jpg', 'person . pigeon . tree'],
                    ['asset/demo2.jpeg', 'wireless walkie-talkie . life jacket . atlantic cod . man . vehicle . accessory . cell phone .'],
                    ['asset/demo3.jpeg', 'wine rack . bottle . basket'],
                    ['asset/demo4.jpeg', 'Mosque. golden dome. smaller domes. minarets. arched windows. white facade. cars. electrical lines. streetlights. trees. pedestrians. blue sky. shadows'],
                    ['asset/demo5.jpeg', 'stately building. columns. sculptures. Spanish flag. clouds. blue sky. street. taxis. van. city bus. traffic lights. street lamps. road markings. pedestrians. sidewalk. traffic sign. palm trees']
                ],
                inputs=[input_image, prompt],
            )
        run.click(inference, inputs=[input_image, prompt, return_mask, return_score], outputs=output_image)
    demo.launch(debug=True)