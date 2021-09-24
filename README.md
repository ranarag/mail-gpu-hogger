# mail-gpu-hogger
An application to mail the user(s) hogging gpu memory

## Requirements

[1] [nvitop](https://github.com/XuehaiPan/nvitop)


# NOTE

Before running the script please change the following global variables with the ones in <>:
1. SERVER_NAME <your server name>
2. AUTHOR <your name>
3. AUTH_MAIL <your mail address>

This is script was created to be run on GPU servers inside IIT Kharagpur. Hence the smtp server is hardcoded to that of IIT Kharagpur.
In order to use it for GPU serves elsewhere, you will have to change the smtp address in line 71 of the code.
