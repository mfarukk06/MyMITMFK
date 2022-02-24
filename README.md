This tool used as Man-In-The-Middle Attack Framework. With this tool, you can capture packets from the target machine. Also, you can capture your target's HTTP sites usernames and passwords.

USAGE : 1-) python3 python3 my_arp_poisoning.py -t 10.0.2.15(Target's IP address) -g 10.0.2.1(Target's gateway IP address)
        2-) python3 my_packet_listener.py
        
Explanation: In 1st step, we are Arp Spoofing target's machine and gateway to become the Man in the middle. In 2nd step, we are capturing and filtering packets to capture login credentials and etc.
