Install this on Raspbian
========================

Clone the git repo
------------------

```
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/idcrook/raspi-receiver-remote-control.git
cd ~/projects/raspi-receiver-remote-control
```

Install some packages and configure Raspbian
--------------------------------------------

Instructions on how to do pathced builds

https://github.com/AnaviTechnology/anavi-docs/blob/master/anavi-infrared-phat/anavi-infrared-phat.md#setting-up-lirc https://www.raspberrypi.org/forums/viewtopic.php?t=235256

```shell
# sudo apt-get install -y lirc
# will use a patched version now
sudo apt install ./liblirc0_0.10.1-5.2_armhf.deb ./liblircclient0_0.10.1-5.2_armhf.deb ./lirc_0.10.1-5.2_armhf.deb \
# (will fail)
cat conf/snippet-config.txt | sudo tee -a /boot/config.txt
#sudo cp -v conf/udev.rules.txt /etc/udev/rules.d/71-lirc.rules
sudo mv /etc/lirc/lirc_options.conf.dist /etc/lirc/lirc_options.conf
sudo mv /etc/lirc/lircd.conf.dist /etc/lirc/lircd.conf
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist

sudo vi /etc/lirc/lirc_options.conf

sudo systemctl status lircd
sudo systemctl start lircd
sudo systemctl enable lircd

sudo reboot

cd ~/projects/raspi-receiver-remote-control
sudo apt install -y --allow-downgrades ./liblirc0_0.10.1-5.2_armhf.deb ./liblircclient0_0.10.1-5.2_armhf.deb ./lirc_0.10.1-5.2_armhf.deb

sudo systemctl status lircd
journalctl -f -u lircd
```

in `lirc_options.conf`

```
driver          = default
#device          = /dev/lirc0
device          = /dev/lird-tx
```

Did not end up using this : [lirc_rpi got replaced by gpio-ir and gpio-ir-tx, how do I upgrade?](https://github.com/raspberrypi/linux/issues/2993#issuecomment-497420228)

HARDWARE
--------

Assumes IR LED is connected to BCM 22 output. Unplug Pi and wire up NPN transistor amplifier circuit.

Configure LIRC for remote
-------------------------

Assuming the IR LED circuit is wired up, power up Pi.

```
sudo journalctl -u lircd
sudo service lircd stop
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf \
        /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist

cd ~/projects/raspi-receiver-remote-control
sudo cp -v conf/RM-AAU190.lircd.conf /etc/lirc/lircd.conf.d/
sudo service lircd restart
sudo journalctl -u lircd

irsend LIST RM-AAU190 ""

irsend SEND_ONCE RM-AAU190 SA-CD/CD
irsend SEND_ONCE RM-AAU190 VOLUME_UP
irsend --count=2 SEND_ONCE RM-AAU190 VOLUME_UP
irsend SEND_ONCE RM-AAU190 POWER
```

Troubleshooting
---------------

### do the GPIO devices get created?

```
sudo cat /sys/kernel/debug/gpio
```

```
gpiochip0: GPIOs 0-53, parent: platform/3f200000.gpio, pinctrl-bcm2835:
 gpio-22  (                    |gpio-ir-transmitter@) out lo
 gpio-23  (                    |ir-receiver@17      ) in  hi IRQ
 ...
```

### hardware does not support sending

```
$ irsend SEND_ONCE RM-AAU190 SA-CD/CD
```

```
hardware does not support sending Error running command: Input/output error
```

in `lirc_options.conf`

```
driver = default
```

if driver is `devinput` we cannot use to send IR.
