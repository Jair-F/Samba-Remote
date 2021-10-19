# Samba-Remote

## Install Requirements(Client)
### **Client needs Python>=3.x**
Maybe you want to install the requirements in a virtual environment 
- `mkdir env`
- `python -m virtualenv ./env`. 
- On Windows: `env/Scripts/activate.bat` - On Linux: `source ./env/bin/activate`
- And then install the requrements by executing: `pip install -r requrements.txt`

## Install Server
### **Server can only run on a Linux-Based OS and needs Python>=3.9**
### The automatic startup at the boot supports only systemd - not init...
Open a Terminal in the Samba-Remote folder
<br>
Run `chmod +x install_server.sh && ./install_server.sh`

## Uninstall Server
Open a Terminal in the Samba-Remote folder
<br>
Run `chmod +x uninstall_server.sh && ./uninstall_server.sh`

## Client executeable
**This will make a single executeable binary file of the client python script**
- Install pyinstaller: `pip install pyinstaller`
- run in the Samba-Remote directory: `pyinstaller -F -i "icon1.ico" client-gui.py`
- Your executeable will be in the newly created directory `dist`

**You cant create an executeable for example on Windows for Linux. You need an instance of the OS, on which the executeable should run afterwards!**