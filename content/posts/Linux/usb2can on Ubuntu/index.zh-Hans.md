---
title: usb2can on Ubuntu
date: 2025-01-14
description: Simple usage of usb2can on Ubuntu
summary: Simple usage of usb2can on Ubuntu
tags: ["embedded", "linux", "can"]
---
![IMG-20250114171043624.jpg]
## 一、安装必要的软件包

### Python-can

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
pip3 install python-can
```

成功安装`python-can`库后，可能出现关于脚本路径的警告，提示我们添加环境变量。
在`.bashrc`添加语句并source

```bash
export PATH=$PATH:/home/semitia/.local/bin
```

### can-utils工具

```bash
sudo apt-get install can-utils
```

## 二、测试CAN转USB设备

### 1. 检查USB设备

使用`lsusb`命令查看系统是否识别到你的USB设备：

```bash
lsusb
```

### 2. 检查网络接口

使用`ip link`命令查看系统中是否存在CAN网络接口：

```bash
ip link
```

查找类似`can0`的接口。如果存在，则表示系统已经识别到你的CAN设备并创建了相应的网络接口。

### 3. 使用dmesg查看系统日志

可以使用`dmesg`命令查看系统日志，了解设备连接时的详细信息：

```bash
dmesg | grep can
```

### 4. 配置和启动CAN接口

如果已经检测到设备，可以使用以下命令配置和启动CAN接口（假设设备名为`can0`）：

```bash
sudo ip link set can0 up type can bitrate 1000000
```

### 6. 收发测试

使用`candump`命令监听CAN总线上的消息：

```bash
candump can0
```

若CAN设备和连接正常，则能够看到总线上传输的消息。
如果有两个设备，可以使用`cansend`命令通过另一个设备发送消息：

```bash
cansend can1 123#12345678
```

这将发送4个字节数据，ID为`0x123`，接收效果如下。

```bash
  can0  123   [4]  12 34 56 78
```

### 7. 检查设备状态

显示CAN接口的详细状态信息，包括配置和错误统计数据。

```bash
ip -details link show can0
```

## 三、使用Python-can库

```python
import can
import time
import threading

# 设置CAN接口的配置
can0_config = {
    'interface': 'socketcan',
    'channel': 'can0',
    'bitrate': 500000
}

can1_config = {
    'interface': 'socketcan',
    'channel': 'can1',
    'bitrate': 500000
}

# 定义要发送的消息
messages = [
    "Hello from CAN0!",
    "Greetings from CAN1!",
    "CAN is fun!",
    "Let's communicate!"
]

def can_sender(bus, msg_id, message):
    data = [ord(c) for c in message]  # 将字符串转换为字节数组
    msg = can.Message(arbitration_id=msg_id, data=data[:8], is_extended_id=False)
    try:
        bus.send(msg)
        print(f"Message sent on {bus.channel_info}: ID={msg_id} Data={message}")
    except can.CanError:
        print("Message NOT sent")

def can_receiver(bus):
    while True:
        msg = bus.recv()
        if msg:
            received_message = ''.join(chr(byte) for byte in msg.data)
            print(f"Message received on {bus.channel_info}: {received_message}")

def main():
    # 创建CAN总线对象
    can0 = can.Bus(**can0_config)
    can1 = can.Bus(**can1_config)

    # 启动接收线程
    receiver_thread_0 = threading.Thread(target=can_receiver, args=(can0,))
    receiver_thread_1 = threading.Thread(target=can_receiver, args=(can1,))
    receiver_thread_0.start()
    receiver_thread_1.start()

    # 发送消息
    for message in messages:
        can_sender(can0, 0x100, message)
        time.sleep(1)  # 休息一段时间以避免发送冲突
        can_sender(can1, 0x200, message)
        time.sleep(1)

    # 允许一些时间来接收消息
    time.sleep(5)

    # 关闭CAN总线
    can0.shutdown()
    can1.shutdown()
    return

if __name__ == "__main__":
    main()
```

## 四、关闭设备

```bash
    sudo ip link set can0 down
    sudo ip link set can1 down
```

## links

[Updater - CANable](https://canable.io/updater/canable1.html)

[扒一个超棒的stm32的开源usb-can项目，canable及PCAN固件-CSDN博客](https://blog.csdn.net/karaxiaoyu/article/details/117491396)

[rbei-etas/busmaster: BUSMASTER is an Open Source Software tool to simulate, analyze and test data bus systems such as CAN. BUSMASTER was conceptualized, designed and implemented by Robert Bosch Engineering and Business Solutions (RBEI). Presently it is a joint project of RBEI and ETAS GmbH. (github.com)](https://github.com/rbei-etas/busmaster)

[cangaroo - GitCode](https://gitcode.com/gh_mirrors/ca/cangaroo/overview?utm_source=artical_gitcode&index=bottom&type=card&webUrl&isLogin=1)

[Makerbase CANable V2.0在Window系统使用_canable 2.0-CSDN博客](https://blog.csdn.net/gjy_skyblue/article/details/131323729?ops_request_misc=%7B%22request%5Fid%22%3A%22172377706316800172550675%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fblog.%22%7D&request_id=172377706316800172550675&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-2-131323729-null-null.nonecase&utm_term=canable&spm=1018.2226.3001.4450)



### CANable updater

#### linux

```bash
sudo nano /etc/udev/rules.d/48-stm-dfu.rules
# 添加
SUBSYSTEMS=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="df11", MODE:="0666"
sudo udevadm control --reload-rules
sudo udevadm trigger
```
