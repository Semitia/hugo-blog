---

title: "Embedded Development on Linux"

date: 2025-01-14

description: "A note for learning embedded linux development."

summary: "A note for learning embedded linux development. The used development board is N32G0 of *Nationstech*"

tags: ["embedded", "linux"]

---

This is a note for learning embedded linux development. The used development board is N32G0 of *Nationstech*

## Reference Links

- [Nationstech Developer Community](https://www.nationstech.com/developer/)
- [野火 tutorial for embedded linux development](https://doc.embedfire.com/linux/imx6/linux_base/zh/latest/README.html)

## Environment Config

- [Nationstech Tutorial]()

### VsCode

#### Clangd

> To understand your source code, clangd needs to know your build flags.
> (This is just a fact of life in C++, source files are not self-contained).
> 
> By default, clangd will assume your code is built as `clang some_file.cc`,
> and you’ll probably get spurious errors about missing `#include`d files, etc.

For this project , we use **bear** tool to generate **compile_commands.json**.

- **确保 Bear 已安装** 
  
  `sudo apt-get install bear`

- **导航到项目根目录** 确保您在项目的根目录下：
  
  `cd ~/SumResearch_2024/Repository/Nations.N32G030_Library.1.1.0`

- **使用 Bear 生成 `compile_commands.json` 文件** 
  
  `bear -- make -C projects/n32g030_EVAL/gripper/GCC clean `
  
  `bear -- make -C projects/n32g030_EVAL/gripper/GCC`

### GCC

- [Arm GNU Toolchain Downloads – Arm Developer](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
1. **Choose the right version**：

![](/home/semitia/.config/marktext/images/2024-07-12-12-08-52-image.png)

2. **unpack the file**：

```bash
tar -xf arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi.tar.xz
```

这将会在当前目录下解压出一个名为 `arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi` 的文件夹。

3. **选择安装位置**：
   将解压后的工具链移动到适当的位置，比如 `/opt` 目录下

```bash
sudo mv arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi /opt
```

4. **设置环境变量**：

```bash
echo 'export PATH="/opt/arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

5. **验证安装**：
    Create a C file and run command below to confirm the installation of GCC.

```bash
arm-none-eabi-gcc -o output_file source_file.c
```

Expect output:

### .NET6

- [Download .NET 6.0 (Linux, macOS, and Windows)](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)

When firstly opened a project with extension **EIDE**, it would warn that:

>  Not found [.NET6 runtime](https://dotnet.microsoft.com/en-us/download/dotnet/6.0 "https://dotnet.microsoft.com/en-us/download/dotnet/6.0") on your pc, please install it !

Directly click the official link and follow the guide then we can download the correct version.

### Jlink

- [J-Link Software and Documentation Pack](https://www.segger.com/downloads/jlink/)

We can directly download the **.deb** pack or others.

After download, use command below to vertify

```bash
JLinkExe --version
```

expect output:

```bash
SEGGER J-Link Commander V7.96s (Compiled Jul  4 2024 18:19:44)
DLL version V7.96s, compiled Jul  4 2024 18:19:18
```

#### Connect To Board

```bash
Connecting to target via SWD
Found SW-DP with ID 0x0BB11477
DPv0 detected
CoreSight SoC-400 or earlier
Scanning AP map to find all available APs
AP[1]: Stopped AP scan as end of AP map has been reached
AP[0]: AHB-AP (IDR: 0x04770021)
Iterating through AP map to find AHB-AP to use
AP[0]: Core found
AP[0]: AHB-AP ROM base: 0xE00FF000
CPUID register: 0x410CC200. Implementer code: 0x41 (ARM)
Found Cortex-M0 r0p0, Little endian.
FPUnit: 4 code (BP) slots and 0 literal slots
CoreSight components:
ROMTbl[0] @ E00FF000
[0][0]: E000E000 CID B105E00D PID 000BB008 SCS
[0][1]: E0001000 CID B105E00D PID 000BB00A DWT
[0][2]: E0002000 CID B105E00D PID 000BB00B FPB
Memory zones:
  Zone: "Default" Description: Default access mode
Cortex-M0 identified.
```

```bash
sudo JLinkGDBServer -device N32G030C8 -if SWD -speed 4000
```

```bash
Connecting to J-Link...
J-Link is connected.
Firmware: J-Link ARM-OB STM32 compiled Aug 22 2012 19:52:04
Hardware: V7.00
S/N: 20090928
Feature(s): RDI,FlashDL,FlashBP,JFlash,GDB
Checking target voltage...
Target voltage: 3.30 V
Listening on TCP/IP port 2331
Connecting to target...
Halting core...
Connected to target
Waiting for GDB connection...
```

Then we can use DEBUG in VsCode. It may meet report an error:

![截图 2024-07-13 21-26-31.png](/home/semitia/图片/截图/截图%202024-07-13%2021-26-31.png)

That means the lack of libncursesw.

```bash
sudo apt-get update
sudo apt-get install libncursesw5
sudo apt-get install libncurses5
```

### Armcc

Armcc is included in DS-5, however, **Arm DS-5** has been superseded by **Arm Development Studio**. Evaluation **licenses** are only available for the latest version of Arm DS. 

- [Linux下armcc和arm-linux交叉编译环境的配置_Linux编程_Linux公社-Linux系统门户网站](https://www.linuxidc.com/Linux/2014-02/97346.htm)

- [Arm Development Studio](https://developer.arm.com/Tools%20and%20Software/Arm%20Development%20Studio#Software-Download)

![](/home/semitia/.config/marktext/images/2024-07-12-12-24-02-image.png)

```bash
To start using Arm Development Studio 2024.0 either:
- Create a suite sub-shell using /opt/arm/developmentstudio-2024.0/bin/suite_exec <shell>
- Launch GUI tools via their desktop menu entries

The Release notes for the product can be found here: file:///opt/arm/developmentstudio-2024.0/sw/info/readme.html
```

### VOFA+

Download the software directly from on official website.

- [VOFA+](https://www.vofa.plus/)

After installation, double-clicking the software icon does not start the program normally. Run it in terminal, it would repot the error:

> vofa+: error while loading shared libraries: libcrypto.so.1.1: cannot open shared object file: No such file or directory

Before **UBUNTU22.04**, we may can install it directly

```bash
sudo apt install libssl1.1
```

After 22.04, we can't find the package because libssl1.1 may have been replaced by libssl3.

Luckily, I found **libssl1.1** in my system:

```bash
find / -name "libcrypto.so*"
# OUTPUT: /opt/QQ/resources/app/avsdk/libcrypto.so.1.1
```

So we can make symbolic link:

```bash
sudo ln -s /opt/QQ/resources/app/avsdk/libcrypto.so.1.1 /usr/lib/libcrypto.so.1.1
```

If we can't find libssl1.1, we can download **QQ-linux** or download it **manually** (for reference only).

1. **下载 OpenSSL 1.1 源码**
   
   `wget https://www.openssl.org/source/openssl-1.1.1k.tar.gz tar -zxvf openssl-1.1.1k.tar.gz cd openssl-1.1.1k`

2. **配置和安装**
   
   使用自定义前缀安装到特定路径以避免与系统版本冲突：
   
   `./config --prefix=/usr/local/openssl-1.1 --openssldir=/usr/local/openssl-1.1 make sudo make install`

3. **配置动态链接库路径**
   
   将新安装的 OpenSSL 库路径添加到系统库路径中：
   
   `echo "/usr/local/openssl-1.1/lib" | sudo tee /etc/ld.so.conf.d/openssl-1.1.conf sudo ldconfig`

#### 确认安装是否成功

1. **验证 OpenSSL 版本**
   
   通过指定路径运行新安装的 OpenSSL 来确认版本：
   
   `/usr/local/openssl-1.1/bin/openssl version`

2. **检查库文件**
   
   确认新库文件存在于指定路径：
   
   `ls /usr/local/openssl-1.1/lib`
   
   

### ttyUSB

ttyUSB cannot be used directly In **Ubuntu22.04**.

Check the state of the USB device

```bash
sudo dmesg | grep tty
# output 
[    0.068371] printk: console [tty0] enabled
[  555.498168] usb 3-3.3: ch341-uart converter now attached to ttyUSB0
[  556.189007] usb 3-3.3: usbfs: interface 0 claimed by ch341 while 'brltty' sets config #1
[  556.189756] ch341-uart ttyUSB0: ch341-uart converter now disconnected from ttyUSB0
```

It indicates that **brltty** has taken control of the CH341 device.

We can uninstall it directly:

```bash
sudo apt-get remove --purge brltty
```

Then **reboot** Ubuntu and check the USB again:

```bash
[    0.066547] printk: console [tty0] enabled
[    4.535503] usb 3-3.3: ch341-uart converter now attached to ttyUSB03
# OR: ls /dev/ttyUSB*
```

## Environment Configuration Test

### GCC

With the help of VsCode extension **EIDE**, it's convient to use gcc to compile chips of *Cortex-M4* series. However, it doesn't support *Cortex-M0* series.

![IMG-20250123185742358.webp](/img/Posts/Linux/Embedded%20Linux%20Development/IMG-20250123185742358.webp)

![IMG-20250123185748430.webp](/img/Posts/Linux/Embedded%20Linux%20Development/IMG-20250123185748430.webp)
#### N32 G4x

```bash
[ INFO ] start outputting files ...

>> output hex file              [done]

file path: "build/N32G45x_GCC/N32G45xDemo.hex"

>> output bin file              [done]

file path: "build/N32G45x_GCC/N32G45xDemo.bin"

[ DONE ] build successfully !, elapsed time 0:0:0
```

#### N32 G0x

### Armcc

#### compile


![IMG-20250121233152772.webp](/img/Posts/Linux/Embedded%20Linux%20Development/IMG-20250121233152772.webp)