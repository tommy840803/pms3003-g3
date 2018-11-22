# pms3003-g3
The version to support to read pm data from pms3003 g3 sensor with python3 on Raspberry Pi3

# install and run

Download g3.py and install python modules

    sudo apt-get install python3-pip python3-serial

Check your Raspberry Pi3 enable uart interface

    sudo vim /boot/config/

Insert the command below

    enable_uart = 1
    
Check your tty device "ttyS0" should appear

    ls /dev/tty*

And give a try

    python3 g3.py


# Output

python3 g3.py
[2, 8, 5, 2, 8, 5]

[pm1_cf, pm10_cf, pm2.5_cf, pm1, pm10, pm2.5]

First three data (pmX_cf, cf=1) is the to value is a TSI For standard data.

Last three is reading to the value of value is an atmosphere as the standard.

