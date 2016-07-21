import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

get_date = ["date", "+%d-%m-%Y"]
proc = subprocess.Popen(get_date, stdout=subprocess.PIPE)

output_path = '/home/rbmondom/development/logs/sar/'
filename = proc.stdout.read().replace('\n', '') + '.log'

create_empty_file = ["touch", output_path + filename]
subprocess.call(create_empty_file)

get_sar_log = ['sar', '-q', '-f']
sar_output = subprocess.Popen(get_sar_log, stdout=subprocess.PIPE).stdout.read()

log = open(output_path + filename, 'w')
log.write(sar_output)

from_address = "radiocriluge@criluge.net"
to_address = "team@criluge.net"
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = "MondoMobileWeb - Workload CPU"

body = sar_output
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_address, "password")
text = msg.as_string()
server.sendmail(from_address, to_address, text)
server.quit()
