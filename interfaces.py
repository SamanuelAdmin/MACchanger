import subprocess
import psutil
import re
from faker import Faker


fake = Faker()


class Interface:
    def __init__(self, name, mac, localIp):
        self.name = name
        self.mac = mac
        self.localIp = localIp

    def __str__(self):
        return f'{self.name} -> {self.mac} [{self.localIp}]'


def isValidMac(mac: str) -> bool:
    mac = mac.replace('-', ':').lower()
    return re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac)




def all():
    result = {}

    for ifaceName, ifaceInfo in psutil.net_if_addrs().items():
        ifaceMac = ifaceInfo[0].address.replace('-', ':')
        ifaceIp = ifaceInfo[1].address

        if not isValidMac(ifaceMac): continue

        result[ifaceName] = Interface(ifaceName, ifaceMac, ifaceIp)

    return result

def getRandomMac() -> str: return fake.mac_address()

def setInterfaceMac(self, iface, mac, port=None): # from https://github.com/feross/SpoofMAC/blob/master/spoofmac/interface.py#L110
    subprocess.call(f"ip link set {iface} down".split())
    subprocess.call(f"ip link set {iface} address {mac}".split())
    subprocess.call(f"ip link set {iface} up".split())



def test():
    for iface in psutil.net_if_addrs().items():
        print(iface)

if __name__ == '__main__': test()