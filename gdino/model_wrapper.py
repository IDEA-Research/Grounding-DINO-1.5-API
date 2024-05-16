import tempfile
from typing import Dict, List, Union
import numpy as np
from dds_cloudapi_sdk import (
    DetectionTask,
    Client,
    Config,
    TextPrompt,
    DetectionModel,
    DetectionTarget,
)
from PIL import Image
import concurrent.futures

class GroundingDINOAPIWrapper:
    """API wrapper for Grounding DINO 1.5

    Args:
        token (str): The token for Grounding DINO 1.5 API. We are now opening free API access to Grounding DINO 1.5. For
            educators, students, and researchers, we offer an API with extensive usage times to
            support your educational and research endeavors. You can get free API token at here:
            https://deepdataspace.com/request_api

    """

    def __init__(self, token: str):
        self.client = Client(Config(token=token))

    def inference(self, prompt: Dict, return_mask:bool=False):
        """Main inference function of Grounding DINO 1.5. We take batch as input and
        each image is a dict. N. We do not support batch inference for now.

        Args:
            prompts (dict): Annotations with the following keys:
                - "image" (str): Path to image. E.g. "test1.jpg",
                - "prompt" (str): Text prompt sepearted by '.' E.g. 'cate1 . cate2 . cate3'
            return_mask (bool): Whether to return mask. Defaults to False.

        Returns:
            (Dict): Detection results in dict format with keys::
                - "scores": (List[float]): A list of scores for each object in the batch
                - "labels": (List[int]): A list of labels for each object in the batch
                - "boxes": (List[List[int]]): A list of boxes for each object in the batch,
                     in format [xmin, ymin, xmax, ymax]
                - "masks": (List[np.ndarray]): A list of segmentations for each object in the batch
        """
        # construct input prompts
        image=self.get_image_url(prompt["image"]),
        task=DetectionTask(
            image_url=image[0],
            prompts=[TextPrompt(text=prompt['prompt'])],
            targets=[DetectionTarget.Mask, DetectionTarget.BBox] if return_mask else [DetectionTarget.BBox],
            model=DetectionModel.GDino1_5_Pro,
        )
        self.client.run_task(task)
        result = task.result
        return self.postprocess(result, task, return_mask)


    def postprocess(self, result, task, return_mask):
        """Postprocess the result from the API call

        Args:
            result (TaskResult): Task result with the following keys:
                - objects (List[DetectionObject]): Each DetectionObject has the following keys:
                    - bbox (List[float]): Box in xyxy format
                    - category (str): Detection category
                    - score (float): Detection score
                    - mask (DetectionObjectMask): Use mask.counts to parse RLE mask 
            task (DetectionTask): The task object
            return_mask (bool): Whether to return mask

        Returns:
            (Dict): Return dict in format:
                {
                    "scores": (List[float]): A list of scores for each object
                    "categorys": (List[str]): A list of categorys for each object
                    "boxes": (List[List[int]]): A list of boxes for each object
                    "masks": (List[PIL.Image]): A list of masks in the format of PIL.Image
                }
        """
        def process_object_with_mask(object):
            box = object.bbox
            score = object.score
            category = object.category
            mask = task.rle2rgba(object.mask)
            return box, score, category, mask
        
        def process_object_without_mask(object):
            box = object.bbox
            score = object.score
            category = object.category
            mask = None
            return box, score, category, mask
        
        boxes, scores, categorys, masks = [], [], [], []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if return_mask:
                process_object = process_object_with_mask
            else:
                process_object = process_object_without_mask
            futures = [executor.submit(process_object, obj) for obj in result.objects]
            for future in concurrent.futures.as_completed(futures):
                box, score, category, mask = future.result()
                boxes.append(box)
                scores.append(score)
                categorys.append(category)
                if mask is not None:
                    masks.append(mask)

        return dict(boxes=boxes, categorys=categorys, scores=scores, masks=masks)

    def get_image_url(self, image: Union[str, np.ndarray]):
        """Upload Image to server and return the url

        Args:
            image (Union[str, np.ndarray]): The image to upload. Can be a file path or np.ndarray.
                If it is a np.ndarray, it will be saved to a temporary file.

        Returns:
            str: The url of the image
        """
        if isinstance(image, str):
            url = self.client.upload_file(image)
        else:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".png") as tmp_file:
                # image is in numpy format, convert to PIL Image
                image = Image.fromarray(image)
                image.save(tmp_file, format="PNG")
                tmp_file_path = tmp_file.name
                url = self.client.upload_file(tmp_file_path)
        return url