from nvitop import host, Device, HostProcess, GpuProcess, NA
import smtplib
from email.message import EmailMessage
import getpass
import pwd

SERVER_NAME = "DEVI"
AUTHOR = 'ANURAG ROY'
AUTH_MAIL = 'anurag_roy@iitkgp.ac.in'

class Mailer(object):
    def __init__(self, server_addr, from_addr, username, password):
        self.server_addr = server_addr
        self.from_addr = from_addr
        self.username = username
        self.password = password
    
    def connect(self):
        self.s = smtplib.SMTP(self.server_addr)
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo()
        self.s.login(self.username, self.password)
    def disconnect(self):
        self.s.quit()
        
    def send_msg(self, to_addr, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        self.s.send_message(msg)



def get_user_info_dict():
    username_dict = {}
    with open('/etc/passwd', 'r') as fid:
        for line in fid:
            line = line.strip().split(',')
            if len(line) != 2:
                continue
            uname_name = line[0].strip().split(":") 
            username = uname_name[0].strip()
            name = uname_name[-1]
            mail_addr = line[1].split(':')[0].strip()
            username_dict[username] = (name, mail_addr)
    
    return username_dict 

# taken from https://stackoverflow.com/questions/5327707/how-could-i-get-the-user-name-from-a-process-id-in-python-on-linux/5328008
UID   = 1
EUID  = 2

def owner(pid):
    '''Return username of UID of process pid'''
    for ln in open('/proc/%d/status' % pid):
        if ln.startswith('Uid:'):
            uid = int(ln.split()[UID])
            return pwd.getpwuid(uid).pw_name


def find_and_send():
    global SERVER_NAME
    global AUTHOR
    global AUTH_MAIL
    password =getpass.getpass()
    user_info_dict = get_user_info_dict()

    mailer = Mailer('iitkgpmail.iitkgp.ac.in:587', AUTH_MAIL, AUTH_MAIL, password)
    mailer.connect()
    for i in range(Device.count()):
        device = Device(i)
        process_dict = device.processes()
        for pid, proc in process_dict.items():
            if proc.host.status() == 'sleeping':
                uname = owner(pid)
                try:
                    name, mail_id = user_info_dict[uname]
                except:
                    continue
                message = "Dear {name}, \n \n Please kill idle process with id {pid} occupying GPU {gpuid} and make gpu memory free for others"\
                    " \n\n\n Thanks and regards, \n {author}".format(name=name, pid=pid, gpuid=i, author=AUTHOR)
                subject = "KILL IDLE GPU PROCESS in {}".format(SERVER_NAME)
                print("SENT TO {uname} {name} {mail_id} {pid}".format(uname=uname, name=name, mail_id=mail_id, pid=pid))
                mailer.send_msg(mail_id, subject, message)
    mailer.disconnect()



find_and_send()

