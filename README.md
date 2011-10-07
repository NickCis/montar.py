captchatrader
=============

Python bindings for the captchatrader.com API. Submit captcha images, retrieve the text as a string, receive captcha image and submit its result.


Features
--------

* Submit capture images and retrieve the text
* Notify server if text is correct to prevent charging credits on incorrectly detected captchas
* Retrieve amount of credits left
* Get captcha image
* Submit the result of the captcha image getted

Usage
--------

[cisco@localhost montarpy]$ python montar.py -h
Usage: montar.py [options] [ips]
        If the script is run without arguments, the saved ips will be mounted.
        By default, all ips mounted by the script are saved.
        Options:
            -l: lists saved ips and exits
            -n: mount but don't save ips
            -e: edit saved configuration
            -lm: list saved ips and ask what ip to mount
            -u:  lists ips and ask what ip to unmount.
        Valid ip sintaxis:
            <user>@<ip>:<remote mount point>|<local mount point>
            where:
                <user> is the user (default is root)
                <ip> ip, 192.168.1.1 will be used as default.
                    Instead of passing the full ip, only the lasts digits can be passed.
                    Eg: if 69 is passed, 192.168.1.69 will be used
                        if 4.67 is passed, 192.168.4.67 will be used
                        if 160.3.45 is passed, 192.160.3.45 will be used
                        if 200.40.32.4 is passed 200.40.32.4 will be used
            <remove mount point> like in sshfs, / will be used as default
            <local mount point> local folder where to mount.
                %%ip%%  will be replaced by the ip.
                Default local mount point:  ~/ip_%%ip%%
            All [options] are optional.
        Examples:
            python montar.py 69 (192.168.1.69 will mounted in ~/ip_69 as root)
            python montar.py 69 89 (192.168.1.69 and 192.168.1.89 will be mounted in ~/ip_69 ~/ip_89 as root)
            python montar.py (saved ips will be mounted)
            python montar.py 69 -n (192.168.1.69 will be mounted in ~/ip_69 as root without saving the ip)
            python montar.py pepe@4.69 (192.168.4.69 will be mounted in ~/ip_69 as pepe)
            python montar.py 4.69:/asd|~/miFolder/%%ip%% (/asd folder from 192.168.4.69 will be mounted in  ~/miFolder/4_69 as root)
            python montar.py -l (will list saved ips)
            python mountar.py -e (will list saved ips for erasing)
        Config file: ~/.montadorsshfs
        
[cisco@localhost montarpy]$ 


Requirements
------------

* Python 2.6

License
-------

Gnu gpl v 3

Copyright (c) 2011 NickCis

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

