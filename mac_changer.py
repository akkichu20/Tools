#!usr/bin/env python

#Run it using python and python3
#Do not enter interfaces without any MAC Address

import subprocess
import optparse
import re

def parser_func():          # Function that allows to include options and arguments
   parser = optparse.OptionParser()
   parser.add_option("-i","--interface",dest = "interface",help = "Interface to change MAC Address")
   parser.add_option("-m","--mac",dest = "new_mac",help = "new MAC Address")
   (values,arguments) =  parser.parse_args()
   if not values.interface and not values.new_mac:
       parser.error("[-] Please enter interface and MAC address.\nUse --help for more information")
   elif not values.interface:	
       parser.error("[-] Please specifiy the interface.\nUse --help for more information.")
   elif not values.new_mac:
       parser.error("[-] Please specify the new MAC Address.\nUse --help for more information")
   else :
       return values 

def mac_changer(interface , mac_addr):     # Function that allows to run terminal commands
  print("[+] Changing MAC ADDRESS of " + interface + " to " + mac_addr + "....") 
  subprocess.call("ifconfig " + interface +" down",shell=True)
  subprocess.call("ifconfig " + interface + " hw ether " + mac_addr,shell=True)
  subprocess.call("ifconfig " + interface + " up",shell=True)

def get_current_mac(interface):           # Function that prints current MAC Address
  ifconfig_result = subprocess.check_output(["ifconfig",interface]) # Has b' printed before output when run in python3
  mac_addr_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w\:\w\w",ifconfig_result)
  return mac_addr_result.group(0)


values = parser_func()
current_mac = get_current_mac(values.interface)
print("\nCurrent MAC Address: " + current_mac)
mac_changer(values.interface,values.new_mac)
current_mac = get_current_mac(values.interface)
if current_mac == values.new_mac:
   print("[+] MAC address successfully changed to " + current_mac)
else:
   print("[-] MAC address change unsuccessfull")
