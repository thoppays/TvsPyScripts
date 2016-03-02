    ############# Application #7 - Config File Comparator #############
    
#This program will:
# * Connect to a router via Telnet and it will compare the running-config file to the startup-config file on that device (this can be usually done with: show archive config differences)
# * Compare a locally stored config file (.txt) with the running-config file or startup-config file running on a router.
#Please see the "Python File Operations" section in the course for a recap of the necessary concepts.
#Don't forget to configure Telnet access on the router!

#username teopy privilege 15 password 0 python
#line vty 0 4
# privilege level 15
# login local
# transport input telnet ssh



#The first part of the program is very similar to Application #2 in the course.

import telnetlib
import os.path
import subprocess
import time
import sys



def ip_validity():
    global ip_address
    
    #Checking IP validity
    while True:
        ip_address = raw_input("Enter an IP address: ")
        
        #Checking octets            
        a = ip_address.split('.')
                    
        if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
            break
        
        else:
            print "\nThe IP address is INVALID! Please retry!\n"
            continue
    


def file_validity():
    while True:
        cfg_file = raw_input("Enter config file name and extension: ")
        
        #Changing exception message
        if os.path.isfile(cfg_file) == True:
            print "\nFile was found...\n"
            break
        
        else:
            print "\nFile %s does not exist! Please check and try again!\n" % cfg_file
            continue
        


def telnet(command):
    #Connecting to router via Telnet
    #Define telnet parameters
    username = 'teopy'
    password = 'python'
    
    #Specify the Telnet port (default is 23, anyway)
    port = 23
    
    #Specify the connection timeout in seconds for blocking operations, like the connection attempt
    connection_timeout = 5
    
    #Specify a timeout in seconds. Read until the string is found or until the timout has passed
    reading_timeout = 5
    
    #Logging into device
    connection = telnetlib.Telnet(ip_address, port, connection_timeout)
    
    #Waiting to be asked for an username
    router_output = connection.read_until("Username:", reading_timeout)
    #Enter the username when asked and a "\n" for Enter
    connection.write(username + "\n")
    
    #Waiting to be asked for a password
    router_output = connection.read_until("Password:", reading_timeout)
    #Enter the password when asked and a "\n" for Enter
    connection.write(password + "\n")
    time.sleep(1)	
    
    #Setting terminal length for the entire output - disabling pagination
    connection.write("terminal length 0\n")
    time.sleep(1)
    
    #Entering global config mode
    connection.write("\n")
    connection.write(command + "\n")
    time.sleep(5)
    
    router_output = connection.read_very_eager()
    #print router_output
        
    #Closing the connection
    connection.close()
    
    return router_output

################## USER MENU #################
try:
    #Entering user option
    while True:
        print "\nUse this tool to:\n1 - Compare running-config with startup-config\n2 - Compare running-config with local file\n3 - Compare startup-config with local file\ne - Exit program\n"
        
        user_option = raw_input("Enter your choice: ")
        
        if user_option == "1":
            ###Checking IP validity first###
            ip_validity()
            
            print "\nPlease wait while the config file is being analyzed...\n"
            
            output_run = telnet("show running-config")
            output_start = telnet("show startup-config")
            
            #print output_run
            #print output_start
            
            ###Creating and writing the command output to files###
            file_run = open("file_run.txt", "w")
            
            print >>file_run, output_run
            
            file_start = open("file_start.txt", "w")
            
            print >>file_start, output_start
            
            #Closing both files after writing
            file_run.close()
            file_start.close()
            
            ###Comparing the contents of the files and saving the differences to a new file###
            ###First, reading the lines in each file and storing them as elements of a list###
            
            file_run = open("file_run.txt", "r")
           
            file_start = open("file_start.txt", "r")
            
            list_run = file_run.readlines()
            #print list_run
            
            list_start = file_start.readlines()
            #print list_start
            
            #Closing both files after reading
            file_run.close()
            file_start.close()
            
            ###Secondly, filtering the elements at the beginning of each file/list, because we are interested in only the lines starting from "version 12.4" up to the end###
            #This is done by finding out the index of the element that contains "version" and deleting all the elements at indexes lower than this index
            #The deletion process is done by slicing the first elements in the list, up to the index of the element containing "version" and replacing that slice with, basically, nothing
            
            for index, element in enumerate(list_run):
                if "version " in element and "!\r\n" == list_run[list_run.index(element) - 1]:
                    list_run[0:list_run.index(element)] = []
                    
            #print list_run
            
            for index, element in enumerate(list_start):
                if "version " in element and "!\r\n" == list_start[list_start.index(element) - 1]:
                    list_start[0:list_start.index(element)] = []
                    
            #print list_start  
               
            ###Finally, comparing the elements in both lists and exporting the differences to a new file###
            #Inside the file, the following rules apply:
            #A "+" sign means the line is present in the RUNNING-CONFIG but not in the STARTUP-CONFIG
            #A "-" sign means the line is present in the STARTUP-CONFIG but not in the RUNNING-CONFIG
            
            file_diff = open("file_diff.txt", "w")
      
            #Finding lines in the running-config which are not present in the startup-config            
            run_diff = [x for x in list_run if x not in list_start]
            #print run_diff
            
            #Printing the lines to the file_diff.txt file
            for line in run_diff:
                print >>file_diff, "+" + line
                
            #Finding lines in the startup-config which are not present in the running-config  
            start_diff = [x for x in list_start if x not in list_run]
            #print start_diff
            
            #Printing the lines to the file_diff.txt file
            for line in start_diff:
                print >>file_diff, "-" + line
            
            file_diff.close()

        elif user_option == "2":
            #Having the code from option "1" as a guideline, you should be able to compare the running-config with a local config file
            #Write the code and test it...
            pass
            
        elif user_option == "3":
            #Having the code from option "1" as a guideline, you should be able to compare the startup-config with a local config file
            #Write the code and test it...
            pass
            
        else:
            print "Exiting... See ya...\n\n"
            sys.exit()

except KeyboardInterrupt:
    print "\n\nProgram aborted by user. Exiting...\n"
    sys.exit()         

#End of program










