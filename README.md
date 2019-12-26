# SOWN Node Flashing Scripts
This repository contains scripts (typically Python) for flashing various devices that can be deployed as SOWN(at)Home nodes.  Below are instructions on how to make use of these scripts.

## AR150
1. Bring up the wired interface on your computer on the IP address **192.168.1.2** with a subnet mask of **255.255.255.0**.
2. Plug in a network cable between your computer and the node.  It should not matter which interface Ethernet socket but the **WAN** socket is technically the more appropriate choice. 
3. Run the ar150.py script specifying the , using the command below, substituting the variables shown in capitals:
```
./ar150.py /PATH/TO/FIRMWARE/IMAGE.bin
```
4. Hold down the **reset** button and plug in the power lead to the node.
5. Wait for the script to display **Starting HTTPD...** and then release the reset button.
6. Wait for the script to display **==== NEXT NODE PLEASE! ====** indicating the flashing has been successful. Then unplug the node. 
