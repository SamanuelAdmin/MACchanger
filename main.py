import sys
import interfaces
import time
from datetime import datetime


PARAM_SYMBOL = '-'

def getValueFromArgs(args: list, name) -> None|str:
    name = PARAM_SYMBOL + name.lower()

    if name in args:
        try: return args[ args.index(name) + 1 ] if args[ args.index(name) + 1 ][0] != PARAM_SYMBOL else ""
        except: return ""

    return None

def show():
    ifaces = interfaces.all()

    if len(ifaces) == 0:
        print('Cannot find any interfaces.')
        sys.exit(0)

    for ifaceId in range(len(ifaces.keys())):
        print(f'[{ifaceId + 1}] {ifaces[ list( ifaces.keys() )[ifaceId] ]}')

    sys.exit(0)


def main(*args):
    delay = getValueFromArgs(*args, 'd') # time in seconds
    if not delay or delay == "": delay = 10
    delay = int(delay)

    if getValueFromArgs(*args, 'show') is not None: show()

    choocenIfaceName = getValueFromArgs(*args, 'i')

    if choocenIfaceName == "" or choocenIfaceName is None:
        print(f'Please choose an interface via "{PARAM_SYMBOL}i" argument.')
        sys.exit(0)

    allIfaces =  interfaces.all()
    if choocenIfaceName not in allIfaces:
        print('Invalid interface name.')
        sys.exit(0)

    choosenInterface = interfaces.all()[choocenIfaceName]

    print(f'Choose interface: {choosenInterface}')
    print(f'Changing with delay {delay}.')

    while True:
        randomMac = interfaces.getRandomMac()

        print(f'[{str(datetime.now())[:-7]}] Setting new mac {randomMac} for "{choosenInterface.name}"')
        interfaces.setInterfaceMac(choosenInterface, randomMac)

        print('Checking... ', end='')

        allIfaces = interfaces.all()
        if choocenIfaceName not in allIfaces:
            print(f'Something went wrong. Cannot find interface "{choocenIfaceName}".')
            sys.exit(1)

        choosenInterface = interfaces.all()[choocenIfaceName]

        if choosenInterface.mac == randomMac:
            print('Correct.')
        else:
            print(f'Incorrect. Mac: {choosenInterface.mac}')


        time.sleep(delay)





if __name__ == '__main__':
    try: main(sys.argv)
    except KeyboardInterrupt: sys.exit(0)