# WMIexec
Set of python scripts which perform different ways of command execution via WMI protocol.

## Usage  

### wmiexec_scheduledjob.py  
Is a python script which authenticates to a remote WMI instance and execute commands via `Win32_Process`.

To run the script:  
```bash
python3 wmiexec_scheduledjob.py -i <ip_address> -u <username> -p <password> -c <command>
```

### wmiexec_win32process.py  
Is a python script which authenticates to a remote WMI instance and execute commands via Scheduled Tasks.  

To run the script:  
```bash
python3 wmiexec_win32process.py -i <ip_address> -u <username> -p <password> -c <command>
```

### webserver_ssl.py  
Is a python script which creates a HTTPS server (with a self-signed SSL certificate). Used to exfiltrate the command's output.  

Before running the HTTP server, make sure to generate the certificates by running:  

```bash
openssl genpkey -algorithm RSA -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

If everything is done correctly, the server will be running without any error:  
```bash
python3 webserver_ssl.py
```

## Demo  

![wmi_in_action](https://github.com/WKL-Sec/wmiexec/assets/97109724/5384a87d-a4b2-432e-9bfe-375a34cf9e7b)

## Credits  
https://github.com/XiaoliChan/wmiexec-RegOut  
https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-scheduledjob  

## Author  
Kleiton Kurti ([@kleiton0x00](https://github.com/kleiton0x00))
