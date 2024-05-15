# Grounding DINO 1.5 API

Grounding DINO 1.5 is our most powerful open-world object detection model series. The project provides **examples** for using the models, which are hosted on [DeepDataSpace](https://deepdataspace.com/home).


We provide Grounding DINO 1.5 with two models for different scenarios:

- **Grounding DINO 1.5 Pro** — our most capable model for open-set object detection. It encompasses a wide range of detection scenarios, including but not limited to long-tailed object detection, dense object detection, and long caption phrase grounding, etc.

- **Grounding DINO 1.5 Edge** — our most efficient model for edge computing scenarios. It strives for fast and reliable detection while maintaining low latency and reduced power consumption.


## State-of-the-Art Zero-Shot Transfer Performance

Grounding DINO 1.5 sets new records on several academic benchmarks. Grounding DINO 1.5 Pro achieves a 54.3 AP on the COCO detection zero-shot transfer benchmark and simultaneously achieves a 55.7 AP and a 47.6 AP on the LVIS-minival and LVIS-val zero-shot transfer benchmarks, respectively. We compare the zero-shot performance of Grounding DINO 1.5 Pro and Grounding DINO in Figure 1. 

![alt text](asset/zeroshot.png)

## Usage


### 1. Install

```bash
pip install dds-cloudapi-sdk
```

### 2. Request API from DeepDataSpace

Refer to the DeepDataSpace for API keys: https://deepdataspace.com/request_api


### 3. Runing demo

```bash
export DDS_API="your_api"
python demo/demo.py
```


## Related Project
[Grounding DINO](https://github.com/IDEA-Research/GroundingDINO): A strongr open-set object detection model.

[T-Rex/T-Rex2](https://github.com/IDEA-Research/t-rex): supporting both text and visual prompts for open-set object detection.

