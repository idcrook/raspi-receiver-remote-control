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

[lirc_rpi got replaced by gpio-ir and gpio-ir-tx, how do I upgrade?](https://github.com/raspberrypi/linux/issues/2993#issuecomment-497420228)

```shell
sudo apt-get install -y lirc
cat conf/snippet-config.txt | sudo tee -a /boot/config.txt
sudo cp -v conf/udev.rules.txt /etc/udev/rules.d/71-lirc.rules

sudo cp -v /etc/lirc/lirc_options.conf /etc/lirc/lirc_tx_options.conf
sudo vi /etc/lirc/lirc_tx_options.conf
systemctl cat lircd | sudo tee /etc/systemd/system/lircd-tx.service
sudo vi /etc/systemd/system/lircd-tx.service
# ExecStart=/usr/sbin/lircd --nodaemon --options-file /etc/lirc/lirc_tx_options.conf
systemctl cat lircd.socket | sudo tee /etc/systemd/system/lircd-tx.socket
sudo vi /etc/systemd/system/lircd-tx.socket
# see conf/lircd-tx.socket
sudo systemctl daemon-reload
sudo systemctl start lircd-tx
sudo systemctl enable lircd-tx
sudo systemctl status lircd-tx

```

in `lirc_tx_options.conf`

```
driver          = default
device          = /dev/lirc-tx
output          = /var/run/lirc/lircd-tx
pidfile         = /var/run/lirc/lircd-tx.pid
listen         = 0.0.0.0:8765
#connect        = 127.0.0.1:8766
```

HARDWARE
--------

Assumes IR LED is connected to BCM 22 output. Unplug Pi and wire up NPN transistor amplifier circuit.

Configure LIRC
--------------

Assuming the IR LED circuit is wired up, power up Pi.

```
sudo journalctl -u lircd
sudo journalctl -u lircd-tx
sudo service lircd stop
sudo service lircd-tx stop
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf \
        /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist

cd ~/projects/raspi-receiver-remote-control
sudo cp -v conf/RM-AAU190.lircd.conf /etc/lirc/lircd.conf.d/
sudo service lircd-tx restart
sudo journalctl -u lircd-tx

sudo cp -v conf/irsend /usr/local/bin/irsend
sudo chmod +x /usr/local/bin/irsend
which irsend
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
