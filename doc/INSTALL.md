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

https://github.com/AnaviTechnology/anavi-docs/blob/master/anavi-infrared-phat/anavi-infrared-phat.md#setting-up-lirc

https://www.raspberrypi.org/forums/viewtopic.php?t=235256

[lirc_rpi got replaced by gpio-ir and gpio-ir-tx, how do I upgrade?](https://github.com/raspberrypi/linux/issues/2993#issuecomment-497420228)

```shell
# sudo apt-get install -y lirc
# will use a patched version now
sudo apt install ./liblirc0_0.10.1-5.2_armhf.deb ./liblircclient0_0.10.1-5.2_armhf.deb ./lirc_0.10.1-5.2_armhf.deb \
# ./liblirc-client0_0.10.1-5.2_armhf.deb
# (will fail)
cat conf/snippet-config.txt | sudo tee -a /boot/config.txt
#sudo cp -v conf/udev.rules.txt /etc/udev/rules.d/71-lirc.rules
sudo mv /etc/lirc/lirc_options.conf.dist /etc/lirc/lirc_options.conf
sudo mv /etc/lirc/lircd.conf.dist /etc/lirc/lircd.conf
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist

sudo vi /etc/lirc/lirc_options.conf

sudo systemctl status lircd
sudo systemctl restart lircd

journalctl -f -u lircd
```

in `lirc_options.conf`

```
driver          = default
device          = /dev/lirc0
#device          = /dev/lird-tx
```

HARDWARE
--------

Assumes IR LED is connected to BCM 22 output. Unplug Pi and wire up NPN transistor amplifier circuit.

Configure LIRC
--------------

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

#sudo cp -v conf/irsend /usr/local/bin/irsend
#sudo chmod +x /usr/local/bin/irsend
#which irsend
# /usr/local/bin/irsend
irsend SEND_ONCE RM-AAU190 SA-CD/CD
irsend SEND_ONCE RM-AAU190 VOLUME_UP
irsend --count=2 SEND_ONCE RM-AAU190 VOLUME_UP
irsend SEND_ONCE RM-AAU190 POWER

irsend LIST RM-AAU190 ""
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
```

```
$ irsend SEND_ONCE RM-AAU190 SA-CD/CD

hardware does not support sending
Error running command: Input/output error
```

need to run this command and steps after

```
sudo /usr/share/lirc/lirc-old2new
```
