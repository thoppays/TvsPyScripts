    ############# Application #6 - Basic Network Sniffer #############
    
#In Scapy, we will use the sniff() function to capture network packets.
#To see a list of what commands Scapy has available, run the lsc() function.
#Run the ls() command to see ALL the supported protocols.
#Run the ls(protocol) command to see the fields and default values for any protocol.
#See packet layers with the .summary() function.
#See packet contents with the .show() function.
#Dig into a specific packet layer using a list index: pkts[3][2].summary()...
#...the first index chooses the packet out of the pkts list, the second index chooses the layer for that specific packet.
#Using the .command() packet method will return a string of the command necessary to recreate that sniffed packet.

#To see the list of optional arguments for the sniff() function:
'''
>>> print sniff.__doc__
Sniff packets
sniff([count=0,] [prn=None,] [store=1,] [offline=None,] [lfilter=None,] + L2ListenSocket args) -> list of packets

  count: number of packets to capture. 0 means infinity
  store: wether to store sniffed packets or discard them
    prn: function to apply to each packet. If something is returned,
         it is displayed. Ex:
         ex: prn = lambda x: x.summary()
lfilter: python function applied to each packet to determine
         if further action may be done
         ex: lfilter = lambda x: x.haslayer(Padding)
offline: pcap file to read packets from, instead of sniffing them
timeout: stop sniffing after a given time (default: None)
L2socket: use the provided L2socket
opened_socket: provide an object ready to use .recv() on
stop_filter: python function applied to each packet to determine
             if we have to stop the capture after this packet
             ex: stop_filter = lambda x: x.haslayer(TCP)
'''



#Importing the necessary modules

import logging
import subprocess

#This will suppress all messages that have a lower level of seriousness than error messages, while running or loading Scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)


try:
    from scapy.all import *

except ImportError:
    print "Scapy package for Python is not installed on your system."
    print "Get it from https://pypi.python.org/pypi/scapy and try again."
    sys.exit()
    


# Asking the user for some parameters: interface on which to sniff, the number of packets to sniff,
# the time interval to sniff, the protocol

# Making the necessary configurations

print "\n! Make sure to run this program as ROOT !\n"

# Setting network interface in promiscuous mode
# Wikipedia: In computer networking, promiscuous mode or "promisc mode"[1] is a mode for a wired network interface controller (NIC) or wireless network interface controller (WNIC)...
# ...that causes the controller to pass all traffic it receives to the central processing unit (CPU) rather than passing only the frames that the controller is intended to receive.
# This mode is normally used for packet sniffing that takes place on a router or on a computer connected to a hub.

# Also, when using our setup (VirtualBox-to-GNS3), you should go to the Settings section for the virtual machine you are using...
# ...select the adapter that connects to the GNS3 network and set Promiscuous Mode: Allow All

net_iface = raw_input("* Enter the interface on which to run the sniffer (like 'eth1'): ")

subprocess.call(["ifconfig", net_iface, "promisc"], stdout=None, stderr=None, shell=False)

print "\nInterface %s was set to PROMISC mode." % net_iface
print

# Asking the user for the number of packets to sniff (the "count" parameter)
pkt_to_sniff = raw_input("Enter the number of packets to capture (0 is infinity): ")

# Considering the case when the user enters 0 (infinity)
if int(pkt_to_sniff) != 0:
    print "\nThe program will capture %d packets." % int(pkt_to_sniff)
    print
elif int(pkt_to_sniff) == 0:
    print "\nThe program will capture packets until the timeout expires."
    print


#Asking the user for the time interval to sniff (the "timeout" parameter)
time_to_sniff = raw_input("* Enter the number of seconds to run the capture: ")

#Handling the value entered by the user
if int(time_to_sniff) != 0:
    print "\nThe program will capture packets for %d seconds." % int(time_to_sniff)
    print
    
    
#Asking the user for any protocol filter he might want to apply to the sniffing process
#For this example I chose three protocols: ARP, BOOTP, ICMP
#You can customize this to add your own desired protocols
proto_sniff = raw_input("* Enter the protocol to filter by (arp|bootp|icmp|0 is all): ")

#Considering the case when the user enters 0 (all)
if (proto_sniff == "arp") or (proto_sniff == "bootp") or (proto_sniff == "icmp"):
    print "\nThe program will capture only %s packets." % proto_sniff.upper()
    print
elif int(proto_sniff) == 0:
    print "\nThe program will capture all protocols."
    print


#Creating an external file for packet logging
file_name = raw_input("* Please give a name to the log file: ")
sniffer_log = open(file_name, "w")


#Initializing the packet counter
packet_no = 0

# This is the function that will be applied to each captured packet
# The function will extract some parameters from the packet and then log each packet to an external file
def packet_log(pkt):
    #The packet index
    global packet_no
    
    # Filtering the packets based on the protocol. Using the lower() method to ignore the case when searching for the protocol in the packet.    
    if proto_sniff.lower() in pkt[0][1].summary().lower():
        packet_no = packet_no + 1
        #Writing the data for each packet to the external file
        print >>sniffer_log, "Packet " + str(packet_no) + ": " + "SMAC: " + pkt[0].src + " DMAC: " + pkt[0].dst
    

print "\n* Starting the capture... Waiting for %s seconds..." % time_to_sniff

#Running the sniffing process
pkt = sniff(iface=net_iface, count=int(pkt_to_sniff), timeout=int(time_to_sniff), prn=packet_log)

#print pkt.show()

#Printing the closing message
print "\n* The timeout of %s seconds has passed." % time_to_sniff
print "* Please check the %s file to see the captured packets.\n" % file_name


#Closing the log file
sniffer_log.close()

#End of program. Feel free to modify it, test it, add new protocols to sniff and improve de code whenever you feel the need to.






























