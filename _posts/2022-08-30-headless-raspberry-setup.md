---
layout: post
title:  "Headless installation of Ubuntu on Rasbperry"
author: jose
categories: [ Servers, Raspberry Pi, Tutorial ]
featured: false
hidden: false
comments: false
share: false
image: assets/images/raspberry-pi-modelos.png
use_math: false
time_read: 1
---

This tutorial aims to be a fast* tutorial for installing Ubuntu Server into a Raspberry Pi and accessing it via ssh. First, download the image from [here](https://cdimage.ubuntu.com/releases/22.04.1/release/ubuntu-22.04.1-preinstalled-server-arm64+raspi.img.xz). Then, using [Balena Etcher](https://www.balena.io/etcher/){:target="_blank"} boot the image into a USB. The process is simple, just follow the steps of the program.

Now, the configuration part. Access your bootable USB. In my case I accessed it via the bash command line with `cd /Volumes/system-boot` but you can access it in any other ways. In order to enable SSH on the first boot, you need to create a file called `ssh` with nothing on it. But, to be able to connect to the Raspberry you also need it to be connected to a wifi. By default, it doesn't connect to any wifi, just to the ethernet in case it is plugged. So you need to modify the `network-config` file. At the end of the file you can see something like this
```
version: 2
ethernets:
  eth0:
    dhcp4: true
    optional: true
```
After that there are many commented lines. You need to uncomment and modify those lines. The first you need to do is to add your wifi\*\*. For that, after `access-points` include the SSID which is the name of the wifi, and the password of that wifi:
```
access-points:
  <SSID>:
    password: "<password>"
```
Be sure to maintain those commas and remove any other wifis from there. 

Finally, insert the SD card, start your raspberry and you are free to go. Connect to your Raspberry Pi using the command `ssh ubuntu@<raspberry IP>`\*\*\*, enter the default password "ubuntu". You will be asked to change the default password and voilà, you have a server.

*For a more detailed explanation you can go to the official [Ubuntu page](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#3-wifi-or-ethernet){:target="_blank"}. And for more details on how netplan and their config files work you can go to [their reference.](https://netplan.io/reference/#dhcp-overrides){:target="_blank"}

**If you have a Mac and an iPhone you can create a wifi hotspot from the iPhone's internet. That way you can access your Raspberry anywhere. [Here](https://www.howtogeek.com/214053/how-to-turn-your-mac-into-a-wi-fi-hotspot/){:target="_blank"} you have a tutorial for creating the hotspot. One more thing, use the channel 1, otherwise the Raspberry Pi won't be able to connect to that frequency.

***To find the assigned IP yourself you can try nmaping several IPs in the range to see which one has the 22 port open. You can also follow [this tutorial for MacOS](https://osxdaily.com/2016/11/03/view-lan-device-ip-address-arp/){:target="_blank"} or any other you find. 