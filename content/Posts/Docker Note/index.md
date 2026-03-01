---
title: Docker Note
date: 2025-01-21
description: Practical usage of Docker.
summary: Practical usage of Docker.
tags: ["Docker"]
---

![IMG-20250121235045541.webp](/img/Posts/Tools/Docker%20Note/IMG-20250121235045541.webp)

## Installation and Configuration

---

### 1. Install Docker

#### Step 1: Update System Packages

Ensure system packages are up to date:

```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install Docker

Run the following command to install Docker:

```bash
sudo apt install docker.io -y
```

#### Step 3 (Optional): Start and Enable Docker Service

Start Docker and set it to start on boot:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### Step 4: Verify Docker Installation

Run the following command to check Docker version:

```bash
docker --version
```

Output similar to `Docker version xx.xx.xx` indicates successful installation.

### Configure Docker Proxy

Create configuration file and add proxy settings:

1. Create or edit Docker service configuration file:
   
   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d 
   sudo gedit /etc/systemd/system/docker.service.d/http-proxy.conf
   ```

2. Add the following content to `http-proxy.conf` file:
   
   ```bash
   [Service] 
   Environment="HTTP_PROXY=http://127.0.0.1:7890/" 
   Environment="HTTPS_PROXY=http://127.0.0.1:7890/" 
   Environment="NO_PROXY=localhost,127.0.0.1"
   ```

3. Reload system daemon configuration and restart Docker service:
   
   ```bash
   sudo systemctl daemon-reload 
   sudo systemctl restart docker
   ```

### Add User Group

Avoid needing sudo every time you use docker.

[Post-installation steps | Docker Docs](https://docs.docker.com/engine/install/linux-postinstall/)

Username seems to require lowercase.

```bash
alexavier@alexavier:~$ sudo usermod -aG docker Alexavier
usermod: user 'Alexavier' does not exist
alexavier@alexavier:~$ sudo usermod -aG docker alexavier
```

After configuration, it seems you need to restart/re-login for VSCode plugins to work.

## Common Operations

### Pull Image

```bash
docker pull osrf/ros:noetic-desktop-full
```

### View Local Images

```bash
docker images
```

### View Running Containers

```bash
docker ps
```

### View All Containers (Including Stopped)

```bash
docker ps -a
```

### Start Container

If multiple containers share the same image, the read-only part of the image will be shared, **not occupying duplicated space**.

```bash
docker run -it my_noetic:7_26 /bin/bash

docker run -it --network host my_noetic:7_26 /bin/bash

docker run -it --network host -v ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws my_noetic:latest /bin/bash

docker run -it --network host -v ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws -v ~/SumResearch_2024/Repo/RDKx5:/root/RDKx5 arm_noetic:latest

docker run -it --network host -v ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws -v ~/SumResearch_2024/Repo/RDKx5:/root/RDKx5 --privileged --device /dev/ttyUSB0 arm_noetic:latest
```

### Start New Shell Session

Find the running container ID or name, suppose it is my_noetic_container.

```bash
docker exec -it my_noetic_container /bin/bash
```

### Stop Container

```bash
docker kill <container_name_or_id>
```

### Save Container as Image

```bash
docker commit youthful_khayyam airbot_img:latest
```

### View Container Space Usage

```bash
docker system df
```

### View Image Info

```bash
docker inspect b56b435576e8
```

### Local Save and Load Docker Images

Save a Docker image as a file, then load this file elsewhere.

##### Save Image

Use `docker save` command to save the image as a tar file:

```bash
docker save -o my-ubuntu-image.tar my-ubuntu-image
```

##### Load Image

```bash
docker load -i my-ubuntu-image.tar
```

### Delete Image and Container

- **Delete Container**:
  
  ```bash
  docker rm <container_id_or_name>
  ```

- **Delete Image**:
  
  ```bash
  docker rmi <image_id_or_repository:tag>
  ```

### File Operations

#### Copy to Container

```bash
docker cp ~/SumResearch_2024/Repo/Host/ROS1_ws youthful_khayyam:/home/
```

## GUI Configuration

### Host

Install x11

```bash
sudo apt update
sudo apt install xserver-xorg xauth
```

Verify function

```bash
xeyes
```

Grant permissions

```bash
xhost +local:
```



### Container

Recommend using compose to open container, specific content can refer to later sections.

Install x11

```bash
apt update
apt install -y x11-apps
```

Test

```bash
xeyes
```



## Dockerfile

### File Example

Dockerfile is a text file containing a series of instructions to define how to build a Docker image. Suppose you want to create a Docker image containing a basic Ubuntu system, you can create a simple Dockerfile:

```Dockerfile
# Use official Ubuntu image as base image
FROM ubuntu:20.04

# Maintainer info
LABEL maintainer="your_email@example.com"

# Update package list and install some basic tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    git \
    && apt-get clean

# Set working directory
WORKDIR /root

# Copy your system configuration file (Optional)
# COPY my_config_file /root/my_config_file

# Install other software or do other configurations (As needed)
# RUN ...

# Default command
CMD ["bash"]
```

You can add more instructions in Dockerfile according to your needs, such as installing other software, copying files, etc.

### Build Image using Docker

In the directory where Dockerfile is located, open terminal and run the following command to build Docker image:

```bash
docker build -t my-ubuntu-image .
```

Where `my-ubuntu-image` is the name you specify for the image, and `.` indicates Dockerfile is in the current directory.

 

## Docker Compose

Docker Compose uses a YAML file to define and manage multiple containers, thereby simplifying command line operations.

### Old Version Content (Skip for ubuntu 24.04 and later)
#### Installation

[Docker Compose Official Docs](https://docs.docker.com/compose/install/)

[Docker Compose | Runoob Tutorial](https://www.runoob.com/docker/docker-compose.html)

#### Usage

Create a `docker-compose.yml` file in the project root directory and add the following content:

```yaml
version: '3.8'

services:
  arm_noetic:
    image: arm_noetic:latest
    container_name: arm_noetic_container
    network_mode: host
    volumes:
      - ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws
      - ~/SumResearch_2024/Repo/RDKx5:/root/RDKx5
    privileged: true
    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"
    stdin_open: true
    tty: true
```

In this file:

- `version` specifies the Docker Compose file version.
- `services` section defines a service (i.e., container), here named `arm_noetic`.
- `image` specifies the Docker image to use.
- `container_name` specifies a name for the container.
- `network_mode` set to `host`, same as `--network host` parameter.
- `volumes` defines volumes to mount.
- `privileged` set to `true`, giving the container privileges.
- `devices` section specifies devices to share.
- `stdin_open` and `tty` set to `true` to enable interactive mode.

In the directory where `docker-compose.yml` is located, use the following command to start the container in background mode:

```sh
docker-compose up -d
```



### Installation

  When using 24.04, `docker-compose` cannot be used because `docker-compose` 1.x version depends on `distutils`, and `distutils` was removed in Python 3.12. The new version of `docker-compose` has switched to Go implementation (`docker-compose-plugin`) and no longer depends on Python. So use the new version **'docker compose plugin'**
  
```bash
sudo apt remove docker-compose
sudo apt update 
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
sudo chmod a+r /etc/apt/keyrings/docker.gpg 

# Add Docker software source
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 

# Update & Verify
sudo apt update
sudo apt install docker-compose-plugin
docker compose version
```

The new version command has no hyphen in the middle, it is `docker compose`, not `docker-compose`.

Correspondingly, the specific content of compose seems to need slight modification (filename unchanged).

```yml
version: '3.8'

services:
	graspnet:
		image: nvidia/cuda:12.1.0-devel-ubuntu22.04 # Use the image you downloaded
		container_name: graspnet-container
		network_mode: host
		environment:
			- NVIDIA_VISIBLE_DEVICES=all # Show all GPUs (Can specify GPU)
			- NVIDIA_DRIVER_CAPABILITIES=all
			- DISPLAY=${DISPLAY} # Support visualization
			- QT_X11_NO_MITSHM=1 # Prevent Qt error
			- HTTP_PROXY=http://127.0.0.1:7890 # Clash Proxy Port
			- HTTPS_PROXY=http://127.0.0.1:7890
		volumes:
			- ~/graspnet:/workspace # Mount local ~/graspnet to container /workspace
			- /media/user/disk/dataset/graspnet:/workspace/dataset
			- /tmp/.X11-unix:/tmp/.X11-unix # Share X11 Unix socket, support GUI
		privileged: true
		working_dir: /workspace # Default working directory inside container
		stdin_open: true # Support interactive session
		tty: true # Enable terminal
		deploy:
			resources:
				reservations:
					devices:
						- capabilities: [gpu]
```

### Commands
The new version commands also have slight changes, missing the hyphen. Execute in the directory where `docker-compose.yml` is located:

```bash
docker compose up -d
```

**Note**, this method will delete existing containers with the same name and **recreate** the container using the image. If you just want to start a container that **already exists but is in stopped state**, use the following command:

```bash
docker compose start
```

```bash
# Check if container is alive:
docker compose ps
# View real-time logs:
docker compose logs -f
# Stop service:
docker compose down
```

## Use Graphics Card in Container

To support GPU, NVIDIA Container Toolkit needs to be installed.

#### Set NVIDIA Docker Repository

Add NVIDIA's GPG key and repository:

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```

#### Install NVIDIA Container Toolkit

Update package list and install:

```bash
sudo apt update
sudo apt install -y nvidia-docker2
# If download is too slow, can also use proxy
sudo apt -o Acquire::http::Proxy="http://127.0.0.1:7890" \
         -o Acquire::https::Proxy="http://127.0.0.1:7890" install -y nvidia-docker2
```

#### Restart Docker Service

```bash
sudo systemctl restart docker
```

#### Verify NVIDIA Docker Availability

Run the following command to check if GPU can be accessed by Docker:

```bash
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# Monitor GPU usage
sudo apt install gpustat
gpustat --watch
```

If GPU info is displayed, installation is successful.

#### Ubuntu 24.04 Version
Currently (2024.12.15) NVIDIA Container Toolkit does not support ubuntu 24.04 yet, but it can be downloaded, refer to:
> https://www.server-world.info/en/note?os=Ubuntu_24.04&p=nvidia&f=3

Summary:
```bash
# Update dependencies and system
sudo apt update
sudo apt install -y curl apt-transport-https ca-certificates software-properties-common

# Add NVIDIA GPG public key
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-toolkit.gpg

# Add NVIDIA container toolkit source
curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sudo tee /etc/apt/sources.list.d/nvidia-toolkit.list
sudo sed -i -e "s/^deb/deb [signed-by=\/usr\/share\/keyrings\/nvidia-toolkit.gpg]/g" /etc/apt/sources.list.d/nvidia-toolkit.list

# Update package index and install toolkit
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Restart Docker and test
sudo systemctl restart docker
sudo docker run --rm --gpus all nvidia/cuda:12.3.0-runtime-ubuntu22.04 nvidia-smi
```

---

### Pull CUDA 11.8 Image

https://hub.docker.com/r/nvidia/cuda/tags

Select suitable image and run:

```bash
sudo docker pull nvidia/cuda:11.8.0-base-ubuntu22.04
```

---

### Run Container

Start container using CUDA image and verify if CUDA is available:

```bash
docker run --rm --gpus all -it nvidia/cuda:11.8-base-ubuntu22.04 bash
```

Or use compose

```yaml
version: '3.8'

services:
  graspnet:
    image: pytorch/pytorch:2.2.0-cuda11.8-cudnn8-devel # Use the image you downloaded
    container_name: graspnet-container
    network_mode: host
    runtime: nvidia # Enable GPU support (Need to install NVIDIA Container Toolkit)
    environment:
      - NVIDIA_VISIBLE_DEVICES=all # Show all GPUs (Can specify GPU)
      - NVIDIA_DRIVER_CAPABILITIES=all
      - DISPLAY=${DISPLAY}         # Support visualization
      - QT_X11_NO_MITSHM=1         # Prevent Qt error
      - HTTP_PROXY=http://127.0.0.1:7890  # Clash Proxy Port
      - HTTPS_PROXY=http://127.0.0.1:7890
    volumes:
      - ~/graspnet:/workspace      # Mount local ~/graspnet to container /workspace
      - /media/alexavier/8018420DD8B69548/dataset/graspnet:/workspace/dataset 
      - /tmp/.X11-unix:/tmp/.X11-unix # Share X11 Unix socket, support GUI
    privileged: true  
    working_dir: /workspace        # Default working directory inside container
    stdin_open: true               # Support interactive session
    tty: true                      # Enable terminal
```

#### **Verify Environment**:

Run the following command in container:

```bash
nvidia-smi
```

Since nvcc is a tool only available in devel version, `nvcc -V` cannot be used. If you don't need to develop cuda programs and only use it when running programs, you can just use base.



---

## Other Issues

### Git Permission Issues Caused by Shared Volumes (Possible)

Something like this

```bash
❯ git pull
error: unable to create file RDKx5/hand/servo_limit.json: Permission denied
```

Ensure user owns the ownership of the entire Git repository files and directories

```bash
sudo chown -R $USER:$USER ~/SumResearch_2024/Repo
```

### Container Configure Host Proxy

Long-term configuration can be added in compose

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
# test
curl -I https://www.google.com
```

### Vscode Development

#### VSCode Remote - Containers Plugin

#### Modify Shared Directory Permissions

> Unable to write file "/home/semitia/SumResearch_2024/Repo/Host/ROS1_ws/src/hand_control/src/hand_ctrl.py"(NoPermissions (FileSystemError): Error: EACCES: permission denied, open '/home/semitia/SumResearch_2024/Repo/Host/ROS1_ws/src/hand_control/src/hand_ctrl.py')

Modify permissions of the mounted directory on the host machine to make it writable for all users:

```bash
chmod -R 777 ~/SumResearch_2024/Repo/Host/ROS1_ws
```
