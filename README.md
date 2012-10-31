Not sure about a license yet...thinking about it.
=================================================
<p align="center">
  <img src="https://raw.github.com/dandroid88/webmote/master/server/webmote_django/static/remote.png"/>
  <img src="https://raw.github.com/dandroid88/webmote/master/server/webmote_django/static/record.png"/>
</p>

This project aims to allow any type of device to be controlled by a common web interface (IR, X10, etc.).

The original project is located at https://github.com/azylman/webmote and was written by Daniel Myers, Alex Wilson, and Alex Zylman. This rewrite serves to improve extensibility by using a plugin architechture with a minimal core and plugins for features or protocols.


Goals:
------
* Extensible - plugins for new protocols and functionality  
* Mobile web interface - works on any browser on any platform  
* Simple enough for my parents (old) to setup  
* (eventually) Serve media connected to the server, upload to, download to, etc (this is more of a long term goal...)  


Core:
-----------------
A set of superclasses (and associated methods) for the plugins to expand on.


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
* How to install dependencies for plugins  
* Manage USB port changes manually  
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
* X10  
  * Basics can be found here: http://www.arduino.cc/en/Tutorial/x10  
  * Pins in sketch:  
    * zero crossing - 12
    * data tx - 13
    * data rx - 1 (rx isn't actually used at the moment)
  * Download the X10 library and put it in the arduino libraries folder 
    * on ubuntu 12.10 - /usr/share/arduino/libraries
    * will probably need to be root to copy to this directory
  * Flash Sketch
    * Open X10\_transceiver.pde via arduino (found in webmote/modules/X10/X10\_tranceiver)
    * Click 'upload' - circle with right arrow

* IR
  * Basic can be found at http://www.arcfn.com/2009/08/multi-protocol-infrared-remote-library.html
  * Pins in sketch:
    * Recieve - 11
    * IR - 3
    * Button - 8
    * Status - 13
  * Download the library and put it in the arduino libraries folder
    * available at https://github.com/shirriff/Arduino-IRremote
    * on ubuntu 12.10 - /usr/share/arduino/libraries
    * will probably need to be root to copy to this directory
  * Flash Sketch
    * Open IR\_transceiver.pde via arduino (found in webmote/modules/IR/IR\_tranceiver)
    * Click 'upload' - circle with right arrow

Run (development server):
-------------------------
```bash
./run
```

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/c6a7739f49d37ca82a30b8c7debe7609 "githalytics.com")](http://githalytics.com/dandroid88/webmote)
