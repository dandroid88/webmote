<p align="center">
  <img src="https://raw.github.com/dandroid88/webmote/master/server/webmote_django/static/remote.png"/>
  <img src="https://raw.github.com/dandroid88/webmote/master/server/webmote_django/static/record.png"/>
</p>
<p>
  <a href="https://plus.google.com/photos/114801052085717416954/albums/5244814407639128177">More Screenshots</a>
</p>

The original project is located at https://github.com/azylman/webmote and was written by Daniel Myers, Alex Wilson, and Alex Zylman. This rewrite serves to improve extensibility by using a plugin architecture with a minimal core and plugins for features or protocols.

High Level Concept: 
-------------------
This project aims to allow any type of device to be controlled by a common web interface (IR, X10, etc.).

How It Works:  
-------------
* Devices - these are things like your TV, Stereo, Light, etc.  
* Actions - these are things you do to your devices like, turning them on/off, changing channels, etc.
* Transcievers - for the devices that need them (so far IR and X10), these are pieces of hardware that transmit/recieve data between the server running Webmote and your devices.  
    * These are built with arduinos connected to the server via USB that then have additional circuitry for IR, X10, etc.  
* Remotes - there are both custom (user defined) and default (all available actions for a device) remotes that allow a user to trigger actions.  
    * For custom remotes, users can pick where buttons should be placed, what actions they should trigger, what they should look like etc.  
    * One motivation for this project was the numerous remotes I had to control my entertainment system.  With custom remotes a user can make a remote that has actions from any device or macros.  In other words, a remote might be named "Watch TV".  That remote might have a button like "Watch Cable" that turns on the TV, cable box, and stereo and also changes them to the correct inputs.  There might also be a button called "ESPN" or "CNN" which will automatically navigate you to the channels without having to remember channel numbers (phew...).  
* There are already a few different plugins for example XBMC control and Scheduling which allows you to schedule things like your lights to go on or off at a given time throughout the week.  


Goals:
------
* Extensible - plugins for new protocols and functionality  
* Mobile web interface - works on any browser on any platform  
* Simple enough for my parents (old) to setup  
* (eventually) Serve media connected to the server, upload to, download to, etc (this is more of a long term goal...)  


Core:
-----------------
A set of abstract base classes (and associated methods) for the plugins to expand on.


Plugins:
-------------------
A set of subclasses, files and routines that expand the functionality of webmote.  
The format is as follows:  

A top level directory containing at least:  
* templates (directory)  
    * html files containing pages specific to the plugin  
* static    (directory)  
    * images, javascript, etc.  
* models.py  
* urls.py  
* views.py  
* \_\_init\_\_.py  
* info.json  
    * authors  
    * version  
    * name  
    * url  


Tasks:
------
* Need to implement a method for installing plugin dependencies  
* Need to implement a method or plugin for managing USB port changes manually, or better yet automatically  
* Secondary:  
    * Remote/Local Media player  
    * In browser file browser  
    * Mobile playback  
    * Local playback  
 

Setup Server:
-------------
```bash
#install virtualenv, pip
sudo apt-get install python-virtualenv python-pip
cd webmote
./install
```

Setup Transceivers:
-------------------
### X10  
* Basics can be found here: http://www.arduino.cc/en/Tutorial/x10  
* Pins in sketch:  
    * Zero Crossing - 12
    * Data TX - 13
    * Data RX - 1 (rx isn't actually used at the moment)
* Download the X10 library and put it in the arduino libraries folder 
    * on ubuntu 12.10 - /usr/share/arduino/libraries
    * will probably need to be root to copy to this directory
* Flash Sketch
    * Open X10\_transceiver.pde via arduino (found in webmote/modules/X10/X10\_tranceiver)
    * Click 'upload' - circle with right arrow

<p align="center">
    <img src="https://raw.github.com/dandroid88/webmote/master/modules/X10/X10_transceiver/Arduino---PSC05.png"/>
</p>



### IR
* Basics can be found at http://www.arcfn.com/2009/08/multi-protocol-infrared-remote-library.html
* Pins in sketch:
    * Recieve - 11
    * IR - 3
    * Status - 13
* Download the library and put it in the arduino libraries folder
    * available at https://github.com/shirriff/Arduino-IRremote
    * on ubuntu 12.10 - /usr/share/arduino/libraries
    * will probably need to be root to copy to this directory
* Flash Sketch
    * Open IR\_transceiver.pde via arduino (found in webmote/modules/IR/IR\_tranceiver)
    * Click 'upload' - circle with right arrow

<p align="center">
  <img src="https://raw.github.com/dandroid88/webmote/master/modules/IR/IR_transceiver/Webmote---Infrared-Transceiver.png"/>
</p>


* One thing to note is that by default, arduinos are reset when a serial connection is initiated (which webmote does from time to time...) which can cause problems with commands being lost while the arduino is in its reset sequence.
    * You are experiencing this if:
        * When sending a command your tx/rx lights are active (you are talking to the device correctly) AND
        * The console or logfile does not have a message saying "Failed to play" AND
        * When sending a command nothing happens
    * The simplest fix is placing a small capacitor (2.2 uF works for me) between "reset" and "3v3"

Run (development server):
-------------------------
```bash
./run
```

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/c6a7739f49d37ca82a30b8c7debe7609 "githalytics.com")](http://githalytics.com/dandroid88/webmote)
