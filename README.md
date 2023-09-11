# Servo_Ethercat_Raspberry
## General description
Python program for controling a servomotor with a Raspberry and Canopen over Ethercat (CoE).

Deployed with:
+ Raspbian operative system
+ IgH EtherCAT Master implementation for linux 2.6 or newer.
+ Python 3 with sys and subprocess libraries.
+ SDO comunication with slaves (No PDO. Only SDO).

## Requirements
### Update system
```shell
sudo apt update
sudo apt upgrade
sudo reboot
```

### Install dependencies
```shell
sudo apt install git gcc bc bison flex libssl-dev automake autoconf libtool linux-source libncurses5-dev python3 python3-pip udev
```

### Download and update kernel source
```shell
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

> [!WARNING]
> If ```./configure --sysconfdir=/etc``` throws 'kernel not available for 8139too driver'.
>
> Then try with ```./configure --sysconfdir=/etc --enable-generic --disable-8139too``` and continue from there.

### Configure the ethercat master
> [!IMPORTANT]
> Use `ifconfig` or `ip a` to find and copy the interface MAC adress to use later.
```shell
sudo nano /etc/ethercat.conf      # For systemd based distro
sudo nano /etc/sysconfig/ethercat # For init.d based distro
```
> [!NOTE]
> Edit both files.

Do the next modification to the opened file:
```
MASTER0_DEVICE= "your eth0 MAC address"
DEVICE_MODULES= "generic"
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

Apart from `id`, the only other value required is `velocity`. In my case it can be a number between -5_000 and 5_000 rpm.
> [!IMPORTANT]
> Read your own device manual to get correct values.

> Last ones are for position mode

Apart from `id`, the second value required is the `position` value.
> [!NOTE]
> My encoder manages between -77_309_411 and 77_309_411 degrees (360 is a turn).
> 
> And that's equivalent to between -2_147_483_647 to 2_147_483_647 reference units (10_000 is a turn).
>
> At this moment the position input is in degrees.

The third and last value is `velocity`, wich has the same limits as in velocity mode (-5_000 and 5_000 rpm).
> [!IMPORTANT]
> Please, read your own device manual to get correct values.
