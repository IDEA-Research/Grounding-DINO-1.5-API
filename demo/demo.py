import argparse
import os
from gdino import GroundingDINOAPIWrapper, visualize
from PIL import Image
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(description="Interactive Inference")
    parser.add_argument(
        "--token",
        type=str,
        help="The token for T-Rex2 API. We are now opening free API access to T-Rex2",
    )
    parser.add_argument(
        "--box_threshold", type=float, default=0.3, help="The threshold for box score"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    gdino = GroundingDINOAPIWrapper(args.token)
    prompts = dict(image='asset/demo.jpg', prompt='person.pigeon.tree')
    results = gdino.inference(prompts)
    # now visualize the results
    image_pil = Image.open(prompts['image'])
    image_pil = visualize(image_pil, results)
    # dump the image to the disk
    image_pil.save('asset/demo_output.jpg')
