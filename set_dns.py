import subprocess
import os

# spawn a process and get the string of all interfaces
interface_string = subprocess.check_output('netsh interface show interface').decode('utf-8')

# split the string into lines
interface_list = interface_string.splitlines()

# get the line in which the interface is connected
connected_interface = [itf for itf in interface_list if 'Connected' in itf]

# get the name of the interface
interface_name = ''
if connected_interface:
    interface_name = connected_interface[0]
    interface_name = interface_name.replace('Enabled', '')
    interface_name = interface_name.replace('Connected', '')
    interface_name = interface_name.replace('Dedicated', '')    
    interface_name = interface_name.strip()

# Cloudflare DNS, Google DNS, Open DNS
dns_list = [('1.1.1.1', '1.0.0.1'), ('8.8.8.8', '8.8.4.4'), ('208.67.222.222', '208.67.220.220')]

# Set DNS
os.system(f'netsh interface ip set dns name="{interface_name}" static {dns_list[1][0]}')
os.system(f'netsh interface ip add dns name="{interface_name}" {dns_list[1][1]} index=2')

