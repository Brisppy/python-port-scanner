# Import the required modules
import ipaddress
import socket
import struct

print('''
  _____           _    _____                 
 |  __ \         | |  / ____|                
 | |__) |__  _ __| |_| (___   ___ __ _ _ __  
 |  ___/ _ \| '__| __|\___ \ / __/ _` | '_ \ 
 | |  | (_) | |  | |_ ____) | (_| (_| | | | |
 |_|   \___/|_|   \__|_____/ \___\__,_|_| |_|
                            ''')

# Default values
network_address = ['127.0.0.0/29']
ip_list = ['127.0.0.1', '127.0.0.2', '127.0.0.3', '127.0.0.4']
port_list = [80, 443]
reserved_addresses = ['127.0.0.2', '127.0.0.3']


# Tests to see if the address is valid
# Expects an IP address as an input
# Returns True if the address is a valid IP address
# There are no bad inputs as this is intended for errorchecking
def test_ip(ip):
    while True:
        try:
            ipaddress.ip_network(ip)  # Tests if the address is an IP
        except ValueError:  # Checks to see if the IP is a proper value
            print('Invalid address(es).')
            break
        return True


# Generates an address range
# Expects two variables: two ip addresses, separated with a dash (-), and the
# type of list
# Returns a list of addresses
# Bad inputs are anything which is not two valid ip addresses separated with a
# dash (-)
# If bad inputs are used, error checking prints the error and returns to the
# menu
def address_range(address_range, list_type):
    global network_address
    fandl = address_range.split('-')
    # Splits the input into two variables using the dash as a delimeter
    try:
        a = fandl[1]
    except(IndexError):
        print('Incorrect delimiter.')
        return
    start_ip = fandl[0]  # Assigns a variable to the first value
    end_ip = fandl[1]  # Assigns a variable to the second value
    if test_ip(start_ip) and test_ip(end_ip):  # Tests both IPs
        start_ip = struct.unpack('>I', socket.inet_aton(start_ip))[0]
        # Converts the first IP address to a C struct
        end_ip = struct.unpack('>I', socket.inet_aton(end_ip))[0]
        # Converts the last IP address to a C struct
        if list_type:
            network_address.append(address_range)
            # Appends the new range to the list of ranges
        return ([
            socket.inet_ntoa(struct.pack('>I', ip))
            for ip in range(start_ip, (end_ip + 1))])


# Generates a port range
# Expects two ports (numbers), separated with a dash (-)
# Returns a list of ports
# Bad inputs are anything which is not two numbers separated with a dash (-)
# If bad inputs are used, error checking prints the error and returns to the
# menu
def port_range(port_range):
    sande = port_range.split('-')
    # Splits the input into two variables using the dash as a delimeter
    try:
        a = sande[1]
    except(IndexError):
        print('Incorrect delimiter.')
        return
    start_port = sande[0]  # Assigns a variable to the first value
    end_port = sande[1]  # Assigns a variable to the second value
    if int(start_port) > int(end_port):
        # Checks if the start port comes before the last port
        print("First port larger than last port.")
        return
    return range(int(start_port), int(end_port) + 1)


# Gets the network address from the user and turns it into a list
# Called by the menu - expects no input
def ass_get_range():
    global ip_list
    global network_address
    choice = 1
    print('''
            0: Exit
            1: Input network
            2: Input range of addresses
            3: Input individual addresses ''')
    while choice:
        choice = input("Enter your command: ")
        # Takes the choice from the user and calls the appropriate function
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        if int(choice) == 0:
            break
        elif int(choice) == 1:
            ip = input(
                'Input the network address in CIDR notation (IP/Mask): ')
            if test_ip(ip):  # Checks to see if the address is valid
                network_address.append(ip)
                for i in ipaddress.ip_network(ip).hosts():
                    # Iterates through each host IP address in the network
                    if struct.unpack(
                            '>I', socket.inet_aton(str(i)))[0] % 2 != 0:
                        # Checks to see if the address is odd
                        if i not in ip_list:
                            # Appends every host IP in the range to a list
                            ip_list.append(str(i))
        elif int(choice) == 2:
            temp_list = address_range(input(
                'Input first IP, then second separated by a dash (-): '), 1)
            if temp_list is None:
                return
            for i in temp_list:
                if i not in ip_list:
                    ip_list.append(i)
        elif int(choice) == 3:
            while True:
                ip = input('Input IP address (0 to exit): ')
                if ip == '0':  # Breaks if it is the exit character
                        break
                elif test_ip(ip):  # Tests to see if the ip is valid
                    if ip in ip_list:
                        # Checks to see if the ip is already present
                        print('IP already present.')
                    else:
                        network_address.append(ip)
                        # Appends the IP to the list of ranges
                        ip_list.append(ip)
                        # Appends the ip to the ip list
        break


# Reserves the specified addresses
# Called by the menu - expects no input
def reserve_addresses():
    global reserved_addresses
    choice = 1
    print('''
            0: Exit
            1: Input range of addresses
            2: Input individual addresses ''')
    while choice:
        choice = input("Enter your command: ")
        # Takes the choice from the user and calls the appropriate function
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        if int(choice) == 0:
            break  # Breaks if the choice is the exit character
        elif int(choice) == 1:
            temp_list = address_range(input(
                'Input first IP, then second separated by a dash (-): '), 0)
            if temp_list is None:
                return
            for i in temp_list:
                if i not in reserved_addresses:
                    reserved_addresses.append(i)
        elif int(choice) == 2:
            while True:
                ip = input('Input IP address to reserve (0 to exit): ')
                if ip == '0':  # Breaks if it is the exit character
                    break
                elif test_ip(ip):  # Tests to see if the ip is valid
                    if ip in reserved_addresses:
                        # Checks to see if the ip is already reserved
                        print('IP already reserved.')
                    else:
                        reserved_addresses.append(ip)
                        # Adds the ip to the list of reserved addresses
        break


# Gets IP addresses from the user to be removed from the reserved list
# Called by the menu - expects no input
def release_addresses():
    global reserved_addresses
    choice = 1
    print('''
            0: Exit
            1: Release range of addresses
            2: Release individual addresses ''')
    while choice:
        choice = input("Enter your command: ")
        # Takes the choice from the user and calls the appropriate function
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        if int(choice) == 0:
            break
        elif int(choice) == 1:
            temp_list = address_range(input(
                'Input first IP, then second separated by a dash (-): '), 0)
            if temp_list is None:
                return
            for i in temp_list:
                if i in reserved_addresses:
                    # Removes the selected addresses from the reserved
                    # addresses list
                    reserved_addresses.remove(i)
        elif int(choice) == 2:
            while True:
                ip = input('Input IP address to release (0 to exit): ')
                if ip == '0':
                    break
                elif test_ip(ip):  # Tests the IP address
                    if ip not in reserved_addresses:
                        # Checks to see if the IP is present in
                        # reserved_addresses
                        print('IP not present.')
                    else:
                        reserved_addresses.remove(ip)
                        # Removes the address from the list
        break


# Gets the ports which are to be scanned from the user
# Called by the menu - expects no input
def get_ports():
    global port_list
    global start_port
    global end_port
    choice = 1
    print('''
            0: Exit
            1: Input range of ports
            2: Input individual ports ''')
    while choice:
        choice = input("Enter your command: ")
        # Takes the choice from the user and calls the appropriate function
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        if int(choice) == 1:
            temp_list = port_range(input(
                'Input first port, then second separated by a dash (-): '))
            if temp_list is None:
                return
            for i in temp_list:
                # Appends the ports to the list of ports
                port_list.append(i)
        if int(choice) == 2:
            while True:
                port = input('Input port to scan. (0 to exit): ')
                try:
                    value = int(port)
                    # Tests to see if port is an integer
                except(TypeError, ValueError):
                    # If a TypeError or ValueError occurs, restart the loop
                    print('Invalid port.')
                    continue
                if int(port) == 0:
                    # If the port is 0, exit
                    break
                elif port in port_list:
                    # Checks to see if the port is already in the list
                    print('Port already present.')
                elif int(port) < 0 or int(port) > 65535:
                    # Checks to see if the port is valid
                    print('Invalid port.')
                else:
                    if int(port) not in port_list:
                        port_list.append(int(port))
                        # Appends the port to the list
        break


# Removes ports from the list
# Called by the menu - expects no input
def remove_ports():
    global port_list
    choice = 1
    print('''
            0: Exit
            1: Remove range of ports
            2: Remove individual ports ''')
    while choice:
        choice = input("Enter your command: ")
        # Takes the choice from the user and calls the appropriate function
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        if int(choice) == 1:
            temp_list = port_range(input(
                'Input first port, then second separated by a dash (-): '))
            if temp_list is None:
                return
            for i in temp_list:
                if i in port_list:
                    port_list.remove(i)
                    # Removes the ports from the list of ports
        elif int(choice) == 2:
            while True:
                port = input('Input port to remove. (0 to exit): ')
                try:
                    value = int(port)
                    # Tests to see if port is an integer
                except(TypeError, ValueError):
                    # If a TypeError or ValueError occurs, restart the loop
                    print('Invalid port.')
                    continue
                if int(port) == 0:
                    # If the port is 0, exit
                    break
                elif int(port) < 0 or int(port) > 65535:
                    # Checks to see if the port is valid
                    print('Invalid port.')
                elif int(port) not in port_list:
                    # Checks if the port is present or not
                    print('Port not present.')
                else:
                    port_list.remove(int(port))  # Removes the specified port
        break


# Scans ports in each IP address
# Called by the menu - expects no input
def scan_ports():
    scan_ip_list = ip_list
    for a in reserved_addresses:
        if a in scan_ip_list:
            # Duplicates the ip_list and removes the reserved addresses from it
            scan_ip_list.remove(a)
    socket.setdefaulttimeout(0.01)  # Sets timeout for the connections
    count = 0
    scans = 0
    scan_length = (len(scan_ip_list) * len(port_list))
    print('Scanning ports...')
    for a in scan_ip_list:
        # Iterates through every ip in scan_ip_list
        for port in port_list:
            # Iterates through every port in port_list
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Defines sock as a socket function
            result = sock.connect_ex((a, int(port)))
            # Defines result as a socket result
            if result == 0:
                # Prints that the port is open using result
                print('{}:          '.format(a), 'Port {} Open'.format(port))
                count += 1
            scans += 1
            # Prints the current progress
            print(scans, '/', (scan_length),
                  ' | {}% complete.'.format(round(100 * scans / (len(
                      scan_ip_list) * len(port_list)))), sep='', end='\r')
            sock.close()  # Closes the socket
    print('\n{}'.format(scans), 'ports were scanned.', count,
          'ports were open.')


# Prints assigned values
# Called by the menu - expects no input
def print_values():
    # Prints all of the necessary variables with formatting
    print('IP Addresses in network', network_address, '\n\n', ip_list)
    print('Reserved addresses\n', reserved_addresses)
    print('Ports\n', port_list)


# Clear the selected dataset
# Called by the menu - expects no input
def clear_values():
    global network_address
    global ip_list
    global port_list
    global reserved_addresses
    choice = 1
    print('''
            0: Exit
            1: Clear IP range
            2: Clear reserved addresses
            3: Clear ports
            4: Clear all''')
    while choice:
        choice = input("Enter your command: ")
        # Takes the choice from the user and calls the appropriate function
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        if int(choice) == 0:
            break
        elif int(choice) == 1:
            # Clears the network addresses and ip list
            network_address = []
            ip_list = []
            print('IP range cleared.')
        elif int(choice) == 2:
            # Clears the reserved addresses
            reserved_addresses = []
            print('Reserved addresses cleared.')
        elif int(choice) == 3:
            # Clears the list of ports
            port_list = []
            print('Ports cleared.')
        elif int(choice) == 4:
            # Clears all of the values
            network_address = []
            ip_list = []
            reserved_addresses = []
            port_list = []
            print('All values cleared.')
        break


# Menu for the program
# Used to select options within the functions
def menu():
    choice = 1
    while choice:
        print('\nCurrent network address is:', network_address, '''
        0: Exit
        1: Input IP range
        2: Reserve addresses
        3: Release addresses
        4: Input ports
        5: Remove ports
        6: Scan ports
        7: View values
        8: Clear set of values
        ''')
        choice = input('Enter your command: ')  # Takes user selection
        try:
            value = int(choice)
            # Tests to see if input is an integer
        except(TypeError, ValueError):
            # If a TypeError or ValueError occurs, restart the loop
            continue
        # Checks what the user input, and runs the specified function.
        if int(choice) == 0:
            break
        elif int(choice) == 1:
            # ass_get_range is the assessment version, get_range is non-ass
            ass_get_range()
        elif int(choice) == 2:
            reserve_addresses()
        elif int(choice) == 3:
            release_addresses()
        elif int(choice) == 4:
            get_ports()
        elif int(choice) == 5:
            remove_ports()
        elif int(choice) == 6:
            scan_ports()
        elif int(choice) == 7:
            print_values()
        elif int(choice) == 8:
            clear_values()


# Calls the menu when the program is run
menu()
