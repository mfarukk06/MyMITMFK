import scapy.all as scapy
from scapy_http import http

def listenPackets(interface):
    scapy.sniff(iface=interface,store=False,prn=analyzePackets)
    #prn= callback function

def analyzePackets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)


listenPackets("eth0")