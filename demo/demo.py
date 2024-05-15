import os

from dds_cloudapi_sdk import Config
from dds_cloudapi_sdk import Client
from dds_cloudapi_sdk import DetectionTask
from dds_cloudapi_sdk import TextPrompt
from dds_cloudapi_sdk import DetectionModel
from dds_cloudapi_sdk import DetectionTarget

# Step 1: initialize the config
token = os.getenv("DDS_API")
config = Config(token)

# Step 2: initialize the client
client = Client(config)

# Step 3: run the task by DetectionTask class
image_url = "https://algosplt.oss-cn-shenzhen.aliyuncs.com/test_files/tasks/detection/iron_man.jpg"
# if you are processing local image file, upload them to DDS server to get the image url
# image_url = client.upload_file("/path/to/your/prompt/image.png")

task = DetectionTask(
    image_url=image_url,
    prompts=[TextPrompt(text="iron man")],
    targets=[DetectionTarget.Mask, DetectionTarget.BBox],  # detect both bbox and mask
    model=DetectionModel.GDino1_5_Pro,  # detect with GroundingDino-1.5-Pro model.
    # Available models: []
)

client.run_task(task)
result = task.result

print(result.mask_url)

objects = result.objects  # the list of detected objects
for idx, obj in enumerate(objects):
    print(obj.score)  # 0.42

    print(obj.category)  # "iron man"

    print(obj.bbox)  # [635.0, 458.0, 704.0, 508.0]

    print(
        obj.mask.counts
    )  # RLE compressed to string, ]o`f08fa14M3L2O2M2O1O1O1O1N2O1N2O1N2N3M2O3L3M3N2M2N3N1N2O...

    # convert the RLE format to RGBA image
    mask_image = task.rle2rgba(obj.mask)
    print(mask_image.size)  # (1600, 1170)

    # save the image to file
    mask_image.save(f"mask_{idx}.png")

    break
