# Install this on Raspbian

## Clone the git repo

```
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/idcrook/raspi-receiver-remote-control.git
cd ~/projects/raspi-receiver-remote-control
```

## Install some packages and configure Raspbian


```shell
sudo apt-get install -y lirc
cat conf/snippet-config.txt | sudo tee -a /boot/config.txt
sudo cp -v conf/hardware.conf /etc/lirc/hardware.conf
sudo poweroff
```

## HARDWARE

Assumes IR LED is connected to BCM 22 output.
Unplug Pi and wire up NPN transistor amplifier circuit.


## Configure LIRC

Assuming the IR LED circuit is wired up, power up Pi.

```
sudo journalctl -u lircd
sudo service lircd stop
sudo /usr/share/lirc/lirc-old2new
sudo rm /etc/lirc/lircd.conf.d/lirc-old.conf
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf \
        /etc/lirc/lircd.conf.d/devinput.lircd.dist
cd ~/projects/raspi-receiver-remote-control
sudo cp -v conf/RM-AAU190.lircd.conf /etc/lirc/lircd.conf.d/
sudo service lircd restart
sudo journalctl -u lircd
irsend SEND_ONCE RM-AAU190 SA-CD/CD
irsend SEND_ONCE RM-AAU190 VOLUME_UP
irsend --count=2 SEND_ONCE RM-AAU190 VOLUME_UP
irsend SEND_ONCE RM-AAU190 POWER
```

## Troubleshooting

```
$ irsend SEND_ONCE RM-AAU190 SA-CD/CD

hardware does not support sending
Error running command: Input/output error
```

need to run this command and steps after

```
sudo /usr/share/lirc/lirc-old2new
```
