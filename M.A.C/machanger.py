import subprocess
import re
from optparse import OptionParser

def get_args():
    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify the interface ,use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify the new mac ,use --help for more info")
    return options

def mac_changer(interface,new_mac):
    print("[+] changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_add_search_result:
        return mac_add_search_result.group(0)
    else:
        print("[-] couldnt read MAC Address.")
        exit()

options = get_args()
current_mac = get_current_mac(options.interface)
print("Current MAC Add = " + str(current_mac))
mac_changer(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else :
    print("[-] MAC Address did not get changed.")

