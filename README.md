A simple project for tracking CTA train arrivals with the limitations of the BBC micro:bit device.
To setup:
    - Plug in a BCC micro:bit device to your computer. 
        - If you're on Windows, go to device manager, inspect your USB devices, and grab the COM port the micro:bit is connected to.
        - If you're on Linux, scan /dev/tty for the micro:bit device.
        - Replace the segment in "microprocessor_interface.py" that defines a serial connection with the information you've gathered.
    - Flash "receiver_main.py" to that micro:bit device, and unplug it.
    - In the same port, plug in a new micro:bit device - this will be your static sending device, and will not be unplugged.
    - Run "microprocessor_interface.py". The rest is automatic!

    
