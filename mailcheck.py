import poplib
from email import parser
import datetime
import time
from wakeonlan import wol

def main(f, MAC, user, pwd):
    # Writing starting time and divisor
    f.write('Start: ' + str(datetime.datetime.now()) + '\n')
    f.write('----------------------------------------------\n\n')

    # Infinite cycle
    while 1:
        isnow = datetime.datetime.now()
        # Gmail POP3 Server
        pop_link = poplib.POP3_SSL('pop.gmail.com')
        # Try login
        try:
            pop_link.user(user)
        except poplib.socket.error, poplib.error_proto:
            f.write('LOGIN ERROR @ ' + str(datetime.datetime.now()) + '\n')
        # Try password
        try:
            pop_link.pass_(pwd)
        except poplib.socket.error, poplib.error_proto:
            f.write('LOGIN ERROR @ ' + str(datetime.datetime.now()) + '\n')

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
                f.write('WOL --> KO @ {0}:{1} from {2}\n'.format(isnow.hour, isnow.minute, msg['from']))

        pop_link.quit()

# Managing signal KeyboardInterrupt
if __name__ == '__main__':

    # Variables
    MAC = 'AA:BB:CC:DD:EE:FF'
    user = 'jacopx.freenas'
    pwd = 'popolo99'

    # Opening file with date of the day
    isnow = datetime.datetime.now()
    fname='WOL_' + str(isnow.month) + str(isnow.day) + '-' + str(isnow.hour) + str(isnow.minute) + '.log'
    f = open(fname, 'w', 0)

    try:
        main(f, MAC, user, pwd)
    except KeyboardInterrupt:
        f.write('\n\n----------------------------------------------\n')
        f.write('Start: ' + str(datetime.datetime.now()))

    finally:
        f.close()
