---
title: notes of 《Dive into Deep Learning》
date: 2026-02-21
description: Notes for learning Dive into Deep Learning.
summary: Notes for learning Dive into Deep Learning.
tags:
  - deep learning
  - pytorch
---

> [Dive into Deep Learning — Dive into Deep Learning 2.0.0 documentation](https://zh.d2l.ai/)

Environment Configuration
`torch==1.12.0`
`torchvision==0.13.0`
`conda` can manage `cuda`, download directly as a package

```bash
conda install pytorch==1.12.0 torchvision==0.13.0 cudatoolkit=11.6 -c pytorch -c conda-forge
```

Verify Functionality

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'Is CUDA available: {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0)}' if torch.cuda.is_available() else 'No GPU found')"
```

*dive into deep learning* library

```bash
pip install d2l==0.17.6
```
