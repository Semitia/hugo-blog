---
title: 《Dive into Deep Learning》笔记
date: 2026-02-21
description: A note for learning embedded linux development.
summary: A note for learning embedded linux development. The used development board is N32G0 of *Nationstech*
tags:
  - linux
---

> [《动手学深度学习》 — 动手学深度学习 2.0.0 documentation](https://zh.d2l.ai/)

环境配置
`torch==1.12.0`
`torchvision==0.13.0`
`conda`可以管理`cuda`，直接打包下载
```bash
conda install pytorch==1.12.0 torchvision==0.13.0 cudatoolkit=11.6 -c pytorch -c conda-forge
```
验证功能
```bash
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA是否可用: {torch.cuda.is_available()}'); print(f'显卡名称: {torch.cuda.get_device_name(0)}' if torch.cuda.is_available() else '未发现GPU')"
```

*dive into deep learning* 库
```bash
pip install d2l==0.17.6
```
