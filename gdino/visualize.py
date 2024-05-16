from typing import Dict

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random


def draw_mask(mask, draw, random_color=True):
    """Draws a mask with a specified color on an image.

    Args:
        mask (np.array): Binary mask as a NumPy array.
        draw (ImageDraw.Draw): ImageDraw object to draw on the image.
        random_color (bool): Whether to use a random color for the mask.
    """
    if random_color:
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            153,
        )
    else:
        color = (30, 144, 255, 153)

    nonzero_coords = np.transpose(np.nonzero(mask))
    
    for coord in nonzero_coords:
        draw.point(coord[::-1], fill=color)

def visualize(image_pil: Image,
              result: Dict,
              draw_width: float = 6.0,
              return_mask=True,
              draw_score=True) -> Image:
    """Plot bounding boxes and labels on an image.

    Args:
        image_pil (PIL.Image): The input image as a PIL Image object.
        result (Dict[str, Union[torch.Tensor, List[torch.Tensor]]]): The target dictionary containing
            the bounding boxes and labels. The keys are:
                - boxes (List[int]): A list of bounding boxes in shape (N, 4), [x1, y1, x2, y2] format.
                - scores (List[float]): A list of scores for each bounding box. shape (N)
                - categorys (List[str]): A list of categorys for each object
                - masks (List[PIL.Image]): A list of masks in the format of PIL.Image
        draw_score (bool): Draw score on the image. Defaults to False.

    Returns:
        PIL.Image: The input image with plotted bounding boxes, labels, and masks.
    """
    # Get the bounding boxes and labels from the target dictionary
    boxes = result["boxes"]
    scores = result["scores"]
    categorys = result["categorys"]
    masks = result.get("masks", [])

    # Find all unique categories and build a cate2color dictionary
    cate2color = {}
    unique_categorys = set(categorys)
    for cate in unique_categorys:
        cate2color[cate] = tuple(np.random.randint(0, 255, size=3).tolist())

    # Create a PIL ImageDraw object to draw on the input image
    if isinstance(image_pil, np.ndarray):
        image_pil = Image.fromarray(image_pil)
    draw = ImageDraw.Draw(image_pil)
    
    # Create a new binary mask image with the same size as the input image
    mask = Image.new("L", image_pil.size, 0)
    # Create a PIL ImageDraw object to draw on the mask image
    mask_draw = ImageDraw.Draw(mask)

    # Draw boxes, labels, and masks for each box and label in the target dictionary
    for box, score, category in zip(boxes, scores, categorys):
        # Extract the box coordinates
        x0, y0, x1, y1 = box
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        color = cate2color[category]

        # Draw the box outline on the input image
        draw.rectangle([x0, y0, x1, y1], outline=color, width=int(draw_width))

        # Draw the label and score on the input image
        if draw_score:
            text = f"{category} {score:.2f}"
        else:
            text = f"{category}"
        
        font = ImageFont.load_default()
        if hasattr(font, "getbbox"):
            bbox = draw.textbbox((x0, y0), text, font)
        else:
            w, h = draw.textsize(text, font)
            bbox = (x0, y0, w + x0, y0 + h)
        draw.rectangle(bbox, fill=color)
        draw.text((x0, y0), text, fill="white")

    # Draw the mask on the input image if masks are provided
    if len(masks) > 0 and return_mask:
        size = image_pil.size
        mask_image = Image.new("RGBA", size, color=(0, 0, 0, 0))
        mask_draw = ImageDraw.Draw(mask_image)
        for mask in masks:
            mask = np.array(mask)[:, :, -1]
            draw_mask(mask, mask_draw)

        image_pil = Image.alpha_composite(image_pil.convert("RGBA"), mask_image).convert("RGB")
    return image_pil