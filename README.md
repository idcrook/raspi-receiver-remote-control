raspi-receiver-remote-control
=============================

Control some features of a home audio stereo receiver using Raspberry Pi and IR LED as an IR remote

**UPDATE** 2019-Sep-08: Update for Raspbian Buster

Software and System Configuration
---------------------------------

See [INSTALL.md](doc/INSTALL.md). [LIRC](http://www.lirc.org/) config, system packages, and system config is handled.

Hardware
--------

See [TRANSMITTER.md](design/TRANSMITTER.md) for a discussion of the transmitter circuit and [PARTS.md](design/PARTS.md) for the components used.

Home Automation
---------------

Original motivation for this project was to be able to control a Sony stereo receiver located across the house connected to a Raspberry Pi. There was a need for a lazy, push-button way to turn on receiver and switch to the Raspberry Pi-powered source comfortably from my computer across the room. This project has elements completed for that goal, but hasn't got around to making the "smart home" compatible code components yet.

### Homebridge or MQTT, or both, or none?

I use the excellent [shairport-sync](https://github.com/mikebrady/shairport-sync) project to fill house with sound using many Raspberry Pi's as Airplay receivers. It has added MQTT support for both track metadata and remote controls (for the Airplay source)

-	[shairport-sync-mqtt-display](https://github.com/idcrook/shairport-sync-mqtt-display)

I also use the [homebridge](https://github.com/nfarina/homebridge) project that provides support of multiple "unsupported" home automation projects into HomeKit. A while ago made it so I could turn on and off using Siri in this [blog post](https://idcrook.github.io/siri-shortcut-controlled-ir-remote-for-home-receiver-using-a-raspberry-pi/).

Some IR RC commands for other remotes : https://github.com/idcrook/homespun_lirc_codes
