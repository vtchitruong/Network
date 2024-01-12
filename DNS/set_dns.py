import subprocess
import os

# Cloudflare DNS, Google DNS, Open DNS
my_dns = {'Cloudflare DNS': ('1.1.1.1', '1.0.0.1'),
          'Google DNS': ('8.8.8.8', '8.8.4.4'),
          'Open DNS': ('208.67.222.222', '208.67.220.220')}


def show_dns_list():
    for i, (key, value) in enumerate(my_dns.items(), start=1):
        print(f'{i}. {key}: {value[0]}, {value[1]}')


def change_dns(opt):
    # Spawn a process and get the string of all interfaces
    interface_string = subprocess.check_output('netsh interface show interface').decode('utf-8')

    # Split the string into lines
    interface_list = interface_string.splitlines()

    # Get the line in which the interface is connected
    connected_interface = [itf for itf in interface_list if 'Connected' in itf]

    # Get the name of the interface
    interface_name = ''
    if connected_interface:
        interface_name = connected_interface[0]
        interface_name = interface_name.replace('Enabled', '')
        interface_name = interface_name.replace('Connected', '')
        interface_name = interface_name.replace('Dedicated', '')    
        interface_name = interface_name.strip()

    ## Get the DNS depends on the user's input option
    preferred_dns = ''
    alternate_dns = ''
    for i, (key, value) in enumerate(my_dns.items()):
        if i == opt - 1:
            preferred_dns = value[0]
            alternate_dns = value[1]
            break

    # Set DNS
    os.system(f'netsh interface ip set dns name="{interface_name}" static {preferred_dns}')
    os.system(f'netsh interface ip add dns name="{interface_name}" {alternate_dns} index=2')

    print('Your DNS has been changed successfully.')


if __name__ == '__main__':
    show_dns_list()

    option = int(input('Enter your choice: '))

    if option < 1 or option > len(my_dns):
        print('Your choice is wrong. Please choose a number from the above list.')
    else:
        change_dns(option)