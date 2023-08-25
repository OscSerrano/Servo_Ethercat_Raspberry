# Servo_Ethercat_Raspberry
## General description
Python program for controling a servomotor with a Raspberry and Canopen over Ethercat (CoE).

Deployed with:
+ Raspbian operative system
+ IgH EtherCAT Master implementation for linux 2.6 or newer.
+ Python 3 with sys and subprocess libraries.
+ SDO comunication with slaves (No PDO, SDO only).

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

If any file exist then do next and try again.
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

### Start Ethercat service  
```shell
sudo systemctl enable ethercat.service
sudo systemctl start ethercat.service
sudo systemctl status ethercat.service
```


