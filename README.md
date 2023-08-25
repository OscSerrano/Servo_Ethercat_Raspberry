# Servo_Ethercat_Raspberry
Python program for controling a servomotor with a Raspberry and Canopen over Ethercat (CoE).
This program uses IgH EtherCAT Master implementation for linux 2.6 or newer.

## Requirements
### Install dependencies
sudo apt install git gcc bc bison flex libssl-dev automake autoconf libtool linux-source libncurses5-dev python3 python3-pip udev

### Update kernel and download kernel source
sudo apt update
sudo apt upǵrade
sudo reboot

sudo wget https://raw.githubusercontent.com/RPi-Distro/rpi-source/master/rpi-source -O /usr/local/bin/rpi-source && sudo chmod +x /usr/local/bin/rpi-source && /usr/local/bin/rpi-source -q --tag-update

rpi-source

### Install the IgH EtherCAT Master
git clone https://gitlab.com/etherlab.org/ethercat.git
cd ethercat/ 
./bootstrap 
./configure --sysconfdir=/etc
make all modules
sudo make modules_install install
sudo depmod

### Configure the ethercat master
Use ifconfig to find and copy the interface MAC adress in...

sudo nano /etc/ethercat.conf      # For systemd based distro
sudo nano /etc/sysconfig/ethercat # For init.d based distro

Fill MASTER0_DEVICE with eth0 MAC address
Fill DEVICE_MODULES with "generic"

If any file exist then do next and try again.
sudo ln -s /opt/etherlab/etc/init.d/ethercat /etc/init.d/ethercat
sudo mkdir /etc/sysconfig
sudo cp /opt/etherlab/etc/sysconfig/ethercat /etc/sysconfig/ethercat

### Start and grant access to Ethercat service  
sudo systemctl enable ethercat.service
sudo systemctl start ethercat.service
sudo systemctl status ethercat.service
sudo chmod 666 /dev/EtherCAT0



