# Servo_Ethercat_Raspberry
## General description
Python program for controling a servomotor with a Raspberry and Canopen over Ethercat (CoE).

Deployed with:
+ Raspbian operative system
+ IgH EtherCAT Master implementation for linux 2.6 or newer.
+ Python 3 with sys and subprocess libraries.
+ SDO comunication with slaves (No PDO. Only SDO).

## Requirements
### Install dependencies
```shell
sudo apt install git gcc bc bison flex libssl-dev automake autoconf libtool linux-source libncurses5-dev python3 python3-pip udev
```

### Update kernel and download kernel source
```shell
sudo apt update
sudo apt upǵrade
sudo reboot

sudo wget https://raw.githubusercontent.com/RPi-Distro/rpi-source/master/rpi-source -O /usr/local/bin/rpi-source && sudo chmod +x /usr/local/bin/rpi-source && /usr/local/bin/rpi-source -q --tag-update

rpi-source

```

### Install the IgH EtherCAT Master
```shell
git clone https://gitlab.com/etherlab.org/ethercat.git
cd ethercat/ 
./bootstrap 
./configure --sysconfdir=/etc
make all modules
sudo make modules_install install
sudo depmod
```

### Configure the ethercat master
> [!IMPORTANT]
> Use `ifconfig` to find and copy the interface MAC adress to use later.
```shell
sudo nano /etc/ethercat.conf      # For systemd based distro
sudo nano /etc/sysconfig/ethercat # For init.d based distro
```
> [!NOTE]
> You can edit both files so don't worry.

Do the next modification to the opened file:
```
MASTER0_DEVICE= "your eth0 MAC address"
DEVICE_MODULES= "generic"
```

> [!NOTE]
> If any file exist then do next and try again.
```shell
sudo ln -s /opt/etherlab/etc/init.d/ethercat /etc/init.d/ethercat
sudo mkdir /etc/sysconfig
sudo cp /opt/etherlab/etc/sysconfig/ethercat /etc/sysconfig/ethercat
```

### Grant users access to ethercat
```shell
sudo nano /etc/udev/rules.d/99-EtherCAT.rules
```
Type in: 
```
KERNEL=="EtherCAT[0-9]*", MODE="0664", GROUP="users"
```
Exit the file.
> [!WARNING]
> Necessary step, not doing it will result in the need of using sudo.
> And even with it the program might not work at all.

### Start Ethercat service  
```shell
sudo systemctl enable ethercat.service
sudo systemctl start ethercat.service
sudo systemctl status ethercat.service
```
> The last command is to check if the service started correctly (Not necessary).

## Program use
### Run the program
Open a terminal console where the python program is.
Then type in:
```shell
python3 Servo_CoE.py
```

### Input modes
At the beginning, the program will ask for one of these inputs
+ `vel` Control the velocity.
+ `pa ` Control the position(encoder absolute value) and velocity. This mode uses a buffer in the drive to save a list of all given positions and go to them one by one.
+ `pai` Control the position(encoder absolute value) and velocity. This mode changes target position when input a new position.
+ `pr ` Control the position(by adding values) and velocity. This mode saves the positions in the buffer, but instead of going to the specified position, it adds up the given value to actual position (does every sum one by one).
+ `pri` Control the position(by adding values) and velocity. This mode instantly adds up the last value given to set the new target position.

### Input values
> Next one aplies for all modes

First input value is the slave's `id` (its position within the ehtercat network).
> [!NOTE]
> If you don't know the servo id or the slaves connected, at init, the program shows all the connected slaves with id, alias, state and name.

> Next one is for velocity mode

Apart from `id`, the only other value required is `velocity`. In my case it can be a number between -20_000 and 20_000 rpm.
> [!IMPORTANT]
> Read your own device manual to get correct values.

> Next one is for position mode

The second value required is the position value (I used degrees), in my program it can be a number between -77_309_411 and 77_309_411 degrees.
> (my encoder manages from -2_147_483_647 to 2_147_483_647 reference units).

In position mode, the third and last value is velocity, but in this case it can only be a number between -6_000 and 6_000 rpm (again, check device manual to get right values).
> [!IMPORTANT]
> Read your own device manual to get correct values.
