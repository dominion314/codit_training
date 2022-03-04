from typing import Protocol

allowed = "['tcp:80,tcp:443', 'icmp']"
   
    list = allowed.split(',')

    # Clean data
    new_list = []
    
    for item in list:
        data = item.strip().replace("'",'').replace("[", "").replace("]", '')
        new_list.append(data)

    # Structure data with dictionaries
    values = []

    tcp_ports = {
                "protocol": "tcp",
                "ports": []
                }
    udp_ports = {
                "protocol": "upd",
                "ports": []
                }
    icmp = {
            "protocol": "icmp",
            "ports": []
            }
    icmp_used = False


    #Create loop to iterate through all tcp, udp, icmp values and append the port numbers
    for item in new_list:
        if item == 'icmp':
            icmp_used = True
        else:
            data = item.split(':')

            protocol = data[0]
            
            try:
                port = data[1]
                if protocol == 'tcp':
                    tcp_ports['ports'].append(port)
                elif protocol == 'udp':
                    udp_ports['ports'].append(port)
            except:
                pass

    if tcp_ports['ports'] != []: #if tcp ports doesnt equal an empty list
        values.append(tcp_ports) #we will append values for tcp ports
    if udp_ports['ports'] != []: #same for UDP, just need to iterate over this. 
        values.append(udp_ports)
    if icmp_used != False: #If icmp doesnt equal false, we will append ICMP.
        values.append(icmp)

print(values)