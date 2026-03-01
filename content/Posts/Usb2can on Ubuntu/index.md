---
title: usb2can on Ubuntu
date: 2025-01-14
description: Simple usage of usb2can on Ubuntu
summary: Simple usage of usb2can on Ubuntu
tags: ["embedded", "linux", "can"]
---

![IMG-20250114171043624.webp](/img/Posts/Linux/Usb2can%20on%20Ubuntu/IMG-20250114171043624.webp)

## I. Install Necessary Packages

### Python-can

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
pip3 install python-can
```

After successfully installing the `python-can` library, a warning about the script path may appear, prompting us to add environment variables.
Add the statement to `.bashrc` and source it.

```bash
export PATH=$PATH:/home/semitia/.local/bin
```

### can-utils tools

```bash
sudo apt-get install can-utils
```

## II. Test CAN to USB Device

### 1. Check USB Device

Use the `lsusb` command to check if the system recognizes your USB device:

```bash
lsusb
```

### 2. Check Network Interface

Use the `ip link` command to check if a CAN network interface exists in the system:

```bash
ip link
```

Look for an interface like `can0`. If it exists, it means the system has recognized your CAN device and created the corresponding network interface.

### 3. Use dmesg to View System Logs

You can use the `dmesg` command to view system logs and understand the detailed information when the device is connected:

```bash
dmesg | grep can
```

### 4. Configure and Start CAN Interface

If the device has been detected, you can use the following command to configure and start the CAN interface (assuming the device name is `can0`):

```bash
sudo ip link set can0 up type can bitrate 1000000
```

### 6. Send/Receive Test

Use the `candump` command to listen for messages on the CAN bus:

```bash
candump can0
```

If the CAN device and connection are normal, you should be able to see messages transmitted on the bus.
If there are two devices, you can use the `cansend` command to send messages via another device:

```bash
cansend can1 123#12345678
```

This will send 4 bytes of data with ID `0x123`. The reception effect is as follows.

```bash
  can0  123   [4]  12 34 56 78
```

### 7. Check Device Status

Display detailed status information of the CAN interface, including configuration and error statistics.

```bash
ip -details link show can0
```

## III. Use Python-can Library

```python
import can
import time
import threading

# Set CAN interface configuration
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

# Define messages to send
messages = [
    "Hello from CAN0!",
    "Greetings from CAN1!",
    "CAN is fun!",
    "Let's communicate!"
]

def can_sender(bus, msg_id, message):
    data = [ord(c) for c in message]  # Convert string to byte array
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
    # Create CAN bus objects
    can0 = can.Bus(**can0_config)
    can1 = can.Bus(**can1_config)

    # Start receiver threads
    receiver_thread_0 = threading.Thread(target=can_receiver, args=(can0,))
    receiver_thread_1 = threading.Thread(target=can_receiver, args=(can1,))
    receiver_thread_0.start()
    receiver_thread_1.start()

    # Send messages
    for message in messages:
        can_sender(can0, 0x100, message)
        time.sleep(1)  # Sleep for a while to avoid send conflicts
        can_sender(can1, 0x200, message)
        time.sleep(1)

    # Allow some time to receive messages
    time.sleep(5)

    # Close CAN bus
    can0.shutdown()
    can1.shutdown()
    return

if __name__ == "__main__":
    main()
```

## IV. Close Device

```bash
    sudo ip link set can0 down
    sudo ip link set can1 down
```

## links

[Updater - CANable](https://canable.io/updater/canable1.html)

[A great open source usb-can project for stm32, canable and PCAN firmware - CSDN Blog](https://blog.csdn.net/karaxiaoyu/article/details/117491396)

[rbei-etas/busmaster: BUSMASTER is an Open Source Software tool to simulate, analyze and test data bus systems such as CAN. BUSMASTER was conceptualized, designed and implemented by Robert Bosch Engineering and Business Solutions (RBEI). Presently it is a joint project of RBEI and ETAS GmbH. (github.com)](https://github.com/rbei-etas/busmaster)

[cangaroo - GitCode](https://gitcode.com/gh_mirrors/ca/cangaroo/overview?utm_source=artical_gitcode&index=bottom&type=card&webUrl&isLogin=1)

[Makerbase CANable V2.0 Usage on Window System_canable 2.0-CSDN Blog](https://blog.csdn.net/gjy_skyblue/article/details/131323729?ops_request_misc=%7B%22request%5Fid%22%3A%22172377706316800172550675%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fblog.%22%7D&request_id=172377706316800172550675&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-2-131323729-null-null.nonecase&utm_term=canable&spm=1018.2226.3001.4450)



### CANable updater

#### linux

```bash
sudo nano /etc/udev/rules.d/48-stm-dfu.rules
# Add
SUBSYSTEMS=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="df11", MODE:="0666"
sudo udevadm control --reload-rules
sudo udevadm trigger
```
