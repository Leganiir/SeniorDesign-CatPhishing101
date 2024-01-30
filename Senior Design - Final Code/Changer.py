import seniordesigncode

def receive(content, header):
    domain = header.split("@")[1]
    seniordesigncode.receive(content, domain)  
