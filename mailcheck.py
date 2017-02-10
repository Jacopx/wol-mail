import poplib
from email import parser
import datetime
import time
from wakeonlan import wol

MAC = ''
user = ''
pwd = ''

isnow = datetime.datetime.now()

fname='WOL_'+ str(isnow.year)+ str(isnow.month) + str(isnow.day) + '.log'
f = open(fname, 'w', 0)

f.write('Start: ' + str(datetime.datetime.now()) + '\n\n')

while 1:
    isnow = datetime.datetime.now()
    # Gmail POP3 Server
    pop_link = poplib.POP3_SSL('pop.gmail.com')
    # Try login
    try:
        pop_link.user(user)
    except:
        f.write('LOGIN ERROR')
    # Try password
    try:
        pop_link.pass_(pwd)
    except:
        f.write('LOGIN ERROR')

    # Get messages from server:
    msg = [pop_link.retr(i) for i in range(1, len(pop_link.list()[1]) + 1)]
    # Concat message pieces:
    msg = ["\n".join(mssg[1]) for mssg in msg]
    msg = [parser.Parser().parsestr(mssg) for mssg in msg]

    # Printing log and cheching MSG syntax
    for msg in msg:
        if msg['subject']=='WOL':
            f.write('WOL --> OK @ {0}:{1} from {2}\n'.format(isnow.hour, isnow.minute, msg['from']))
            wol.send_magic_packet(MAC, ip_address='255.255.255.255', port=9)
        else:
            f.write('WOL --> WRONG @ {0}:{1} from {2}\n'.format(isnow.hour, isnow.minute, msg['from']))

    pop_link.quit()

f.close()
