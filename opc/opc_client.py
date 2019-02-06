from lib.OpenOPC import *
import lib.OpenOPC as OpenOPC

if __name__ == '__main__':
    opc = OpenOPC.open_client('172.31.22.0')
    print "hello"
    print opc.servers()

