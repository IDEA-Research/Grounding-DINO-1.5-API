<h1 align="center">Grounding DINO 1.5</h2>

<div align=center>

  **IDEA Research's Most Capable Open-World Object Detection Model Series.** 
  The project provides **examples** for using the models, which are hosted on [DeepDataSpace](https://deepdataspace.com/home).

  **[IDEA-CVR, IDEA-Research](https://github.com/IDEA-Research)** 

</div>

<div align=center>

[![arXiv preprint](https://img.shields.io/badge/arxiv_2403.14610-blue%3Flog%3Darxiv)](https://arxiv.org/pdf/2403.14610.pdf)   [![Homepage](https://img.shields.io/badge/homepage-visit-blue)](https://deepdataspace.com/home) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FIDEA-Research%2FGrounding-DINO-1.5-API&count_bg=%2390E1ED&title_bg=%23EB7373&icon=&icon_color=%23E9BABA&title=VISITORS&edge_flat=true)](https://hits.seeyoufarm.com) [![Static Badge](https://img.shields.io/badge/Try_Demo!-blue?logo=chainguard&logoColor=green)](https://deepdataspace.com/playground/grounding_dino)
</div>

[![Video Name](asset/video_cover.jpg)](https://github.com/Mountchicken/DeepStudio/assets/65173622/7f5fcb50-b41d-4a0f-b07e-0dfbf3f1118b)


## Contents
- [Grounding DINO 1.5](#grounding-dino-15)
  - [Contents](#contents)
  - [Introduction](#introduction)
  - [Model Framework](#model-framework)
  - [Performance](#performance)
    - [Side-by-Side Performance Comparison with Grounding DINO](#side-by-side-performance-comparison-with-grounding-dino)
    - [Zero-Shot Transfer Results of Grounding DINO 1.5 Pro](#zero-shot-transfer-results-of-grounding-dino-15-pro)
    - [Fine-tuning Results on Downstream Datasets](#fine-tuning-results-on-downstream-datasets)
  - [API Usage](#api-usage)
    - [1. Installation](#1-installation)
    - [2. Request API from DeepDataSpace](#2-request-api-from-deepdataspace)
    - [3. Runing demo code](#3-runing-demo-code)
    - [4. Online Grdio demo](#4-online-grdio-demo)
  - [Related Work](#related-work)
  - [BibTeX](#bibtex)

## Introduction

We introduce Grounding DINO 1.5, a suite of advanced open-set object detection models developed by [IDEA Research](https://github.com/IDEA-Research), which aims to advanced the "Edge" of open-set object detection. The suite encompasses two models:

- **Grounding DINO 1.5 Pro:** Our most **capable** model for open-set object detection, which is designed for stronger generalization capability across a wide range of scenarios.

- **Grounding DINO 1.5 Edge:** Our most **efficient** model for edge computing scenarios, which is optimized for faster speed demanded in many applications requiring edge deployment.

<p align="left"><em>Note: We use "edge" for its dual meaning both as in <b>pushing the boundaries</b> and as in <b>running on edge devices</b>.</em></p>


## Model Framework

The overall framework of Grounding DINO 1.5 is as the following image:

<div align="center">
  <img src="./asset/gd1.5_overall_framework.png" width="80%">
</div>

Grounding DINO 1.5 Pro preserves the core architecture of Grounding DINO which employs a deep early fusion architecture.

## Performance

### Side-by-Side Performance Comparison with Grounding DINO

<div align="center">
  <img src="./asset/zeroshot.png" width="80%">
</div>

### Zero-Shot Transfer Results of Grounding DINO 1.5 Pro

<table align="center">
<thead>
  <tr>
    <th>Model</th>
    <th>COCO <br><sup><sup>(AP box)</sup></sup></th>
    <th>LVIS-minival <br><sup><sup>(AP all)</sup></sup></th>
    <th>LVIS-minival <br><sup><sup>(AP rare)</sup></sup></th>
    <th>LVIS-val <br><sup><sup>(AP all)</sup></sup></th>
    <th>LVIS-val <br><sup><sup>(AP rare)</sup></sup></th>
    <th>ODinW35 <br><sup><sup>(AP avg)</sup></sup></th>
    <th>ODinW13 <br><sup><sup>(AP avg)</sup></sup></th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td>Other Best<br>Open-Set Model</td>
    <td>53.4<br><sup><sup>(OmDet-Turbo)</sup></sup></td>
    <td>47.6<br><sup><sup>(T-Rex2 visual)</sup></sup></td>
    <td>45.4<br><sup><sup>(T-Rex2 visual)</sup></sup></td>
    <td>45.3<br><sup><sup>(T-Rex2 visual)</sup></sup></td>
    <td>43.8<br><sup><sup>(T-Rex2 visual)</sup></sup></td>
    <td>30.1<br><sup><sup>(OmDet-Turbo)</sup></sup></td>
    <td><b>59.8</b><br><sup><sup>(APE-B)</sup></sup></td>
  </tr>
  <tr>
    <td>DetCLIPv3</td>
    <td> - </td>
    <td>48.8</td>
    <td>49.9</td>
    <td>41.4</td>
    <td>41.4</td>
    <td> - </td>
    <td> - </td>
  </tr>
  <tr>
    <td>Grounding DINO</td>
    <td>52.5</td>
    <td>27.4</td>
    <td>18.1</td>
    <td> - </td>
    <td> - </td>
    <td> 26.1 </td>
    <td> 56.9 </td>
  </tr>
  <tr>
    <td>T-Rex2 (text)</td>
    <td>52.2</td>
    <td>54.9</td>
    <td>49.2</td>
    <td> 45.8 </td>
    <td> 42.7 </td>
    <td> 22.0 </td>
    <td> - </td>
  </tr>
  <tr>
    <td><b>Grounding DINO 1.5 Pro</b></td>
    <td><b>54.3</b></td>
    <td><b>55.7</b></td>
    <td><b>56.1</b></td>
    <td><b>47.6</b></td>
    <td><b>44.6</b></td>
    <td><b>30.2</b></td>
    <td>58.7</td>
  </tr>
</tbody>
</table>

- Grounding DINO 1.5 Pro achieves **SOTA** performance on COCO, LVIS-minival, LVIS-val, and ODinW35 **zero-shot** transfer benchmarks.

### Fine-tuning Results on Downstream Datasets

<table align="center">
<thead>
  <tr>
    <th>Model</th>
    <th>LVIS-minival <br><sup><sup>(AP all)</sup></sup></th>
    <th>LVIS-minival <br><sup><sup>(AP rare)</sup></sup></th>
    <th>LVIS-val <br><sup><sup>(AP all)</sup></sup></th>
    <th>LVIS-val <br><sup><sup>(AP rare)</sup></sup></th>
    <th>ODinW35 <br><sup><sup>(AP avg)</sup></sup></th>
    <th>ODinW13 <br><sup><sup>(AP avg)</sup></sup></th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td>DetCLIPv2</td>
    <td>58.3</td>
    <td>60.1</td>
    <td>53.1</td>
    <td> 49.0 </td>
    <td> - </td>
    <td> 70.4 </td>
  </tr>
  <tr>
    <td>DetCLIPv3</td>
    <td> - </td>
    <td>60.5</td>
    <td>60.7</td>
    <td>-</td>
    <td>-</td>
    <td> 72.1 </td>
  </tr>
  <tr>
    <td>DetCLIPv3 †</td>
    <td>60.8</td>
    <td>56.7</td>
    <td>54.1</td>
    <td>45.8</td>
    <td> - </td>
    <td> - </td>
  </tr>
  <tr>
    <td>Grounding DINO 1.5 Pro (zero-shot)</td>
    <td>55.7</td>
    <td>56.1</td>
    <td>47.6</td>
    <td>44.6</td>
    <td>30.2</td>
    <td>58.7</td>
  </tr>
  <tr>
    <td><b>Grounding DINO 1.5 Pro</b></td>
    <td><b>68.1</b></td>
    <td><b>68.7</b></td>
    <td><b>63.5</b></td>
    <td><b>64.0</b></td>
    <td><b>70.6</b></td>
    <td><b>72.4</b></td>
  </tr>
</tbody>
</table>

- † indicates results of fine-tuning with LVIS base categories only.

## API Usage
### 1. Installation

```bash
pip install -v -e .
```

### 2. Request API from DeepDataSpace

Refer to the DeepDataSpace for API keys: https://deepdataspace.com/request_api


### 3. Runing demo code

```bash
python demo/demo.py --token <API_TOKEN>
```

### 4. Online Grdio demo
```bash
python gradio_app.py --token <API_TOKEN>
```

## Related Work
- [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO): Strong open-set object detection model.
- [Grounded-Segment-Anything](https://github.com/IDEA-Research/Grounded-Segment-Anything): Open-set detection and segmentation model by combining Grounding DINO with SAM.
- [T-Rex/T-Rex2](https://github.com/IDEA-Research/t-rex): Generic open-set detection model supporting both text and visual prompts.

## BibTeX

If you find our work helpful for your research, please consider citing the following BibTeX entry.

```BibTeX

```