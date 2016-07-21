import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ftplib import FTP
import os
import StringIO
import time

src_ftp_server = "91.121.154.65"
src_username = "suonialba"
src_password = "src_password"
src_work_dir = "suoni_allalba"

rc_ftp_server = "192.240.97.69"
rc_username = "cmusumec"
rc_password = "rc_password"
rc_work_dir = "/media/Trasmissioni/Suoni_Alba"

filename = "suoni_allalba"

logs = []


def handle_binary(more_data):
    sio.write(more_data)


def logger(log_msg):
    log = "[" + time.strftime("%H.%M.%S") + "] " + log_msg
    print log
    logs.append(log)

src_ftp = FTP(src_ftp_server, src_username, src_password)
logger("connection established with FTP server " + src_ftp_server + ".")
src_ftp.cwd(src_work_dir)
logger("directory changed to " + src_work_dir + ".")
rc_ftp = FTP(rc_ftp_server, rc_username, rc_password)
logger("connection established with FTP server " + rc_ftp_server + ".")
rc_ftp.cwd(rc_work_dir)
logger("directory changed to " + rc_work_dir + ".")

for i in range(1, 4):
    sio = StringIO.StringIO()
    msg = "RETR " + filename + str(i) + ".mp3 | Size (MB): " + \
          str(round(src_ftp.size(filename + str(i) + ".mp3") / 1E6, 3)) + " ... "
    logger(msg)
    src_ftp.retrbinary("RETR " + filename + str(i) + ".mp3", callback=handle_binary)
    msg += "[DONE]"
    logger(msg)
    sio.seek(0)  # set the composed file at the beginning position before uploading it
    msg = "STOR " + filename + str(i) + ".mp3 ... "
    logger(msg)
    rc_ftp.storbinary("STOR " + filename + str(i) + ".mp3", sio)
    msg += "[DONE]"
    logger(msg)

src_ftp.quit()
rc_ftp.quit()

logger("writing logs.")
today = time.strftime("%d.%m.%Y-%H.%M.%S")
log_file = open(os.path.expanduser('~') + "/suoni_all_alba_" + today + ".log", "w")
log_file.write("\n".join(logs))
log_file.close()

logger("sending e-mail.")
from_address = "radiocriluge@criluge.net"
to_address = "crew@criluge.it"
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = "Suoni All\'Alba - responso caricamento (" + today + ")"

body = "\n".join(logs)
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_address, "password")
text = msg.as_string()
server.sendmail(from_address, to_address, text)
server.quit()
