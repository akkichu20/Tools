#!usr/bin/env python

import scapy.all as scapy
import optparse

def scan(ip):   #Function that broadcasts ARP request and store details of responding systems
   arp_req = scapy.ARP(pdst=ip)
   broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
   packet = broadcast/arp_req 
   answered_list = scapy.srp(packet,timeout=1,verbose=False)[0]  #srp() sends custom ether frames
   clients_list = []
   for content in answered_list:
        client_dict = {"IP":content[1].psrc,"MAC":content[1].hwsrc}
        clients_list.append(client_dict)
   return clients_list


def net_scan_output(answer):    # Function to print the IP and MAC addresses
   print("\nIP\t\t\tMAC ADDRESS")
   print("-----------------------------------------------")
   for content in answer:
       print(content["IP"] +"\t\t" + content["MAC"])
   


def parser_func():   # Function to include command-line argumments and errors
      parser=optparse.OptionParser()
      parser.add_option("-t","--target",dest="ip",help="target IP range ")
      (values,arguments) = parser.parse_args()
      if not values.ip:
          parser.error("[-] Enter the IP range to searched")
      else:
          return values.ip

ip_input = parser_func()
output_dict = scan(ip_input)
net_scan_output(output_dict)
