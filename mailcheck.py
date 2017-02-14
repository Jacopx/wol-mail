# Importing all Dependencies
import poplib
from email import parser
import time
from wakeonlan import wol

def login(f, user, pwd):
    # Gmail POP3 Server
    pop_link = poplib.POP3_SSL('pop.gmail.com')

    # Try login
    try:
        pop_link.user(user)
    except poplib.socket.error, poplib.error_proto:
        f.write('LOGIN ERROR @ ' + time.strftime("%d-%m-%y %H:%M.%S") + '\n')
    # Try password
    try:
        pop_link.pass_(pwd)
    except poplib.socket.error, poplib.error_proto:
        f.write('LOGIN ERROR @ ' + time.strftime("%d-%m-%y %H:%M.%S") + '\n')

    return pop_link

def main(f, MAC, user, pwd):
    # Writing starting time and divisor
    f.write('Start: ' + time.strftime("%d-%m-%y @ %H:%M.%S") + '\n')
    f.write('----------------------------------------------\n')

    t=10
    # Infinite cycle
    while 1:
        # Call login function
        pop_link=login(f, user, pwd)
        # Get messages from server:
        msg = [pop_link.retr(i) for i in range(1, len(pop_link.list()[1]) + 1)]
        # Concat message pieces:
        msg = ["\n".join(mssg[1]) for mssg in msg]
        msg = [parser.Parser().parsestr(mssg) for mssg in msg]

        # Printing log and cheching MSG syntax
        for msg in msg:
            if msg['subject']=='WOL': # Correct Message receiver
                f.write('WOL --> YES @ {0} from {1}\n'.format(time.strftime("%H:%M.%S"), msg['from']))
                # Sending MP to MAC, Broadcast IP and Port 9
                wol.send_magic_packet(MAC, ip_address='255.255.255.255', port=9)
            else: # Wrong message receiver
                f.write('WOL --> NO @ {0} from {1}\n'.format(time.strftime("%H:%M.%S"), msg['from']))

        # Close the active connection
        pop_link.quit()
        # Waiting t time before recheck
        time.sleep(t)

# Managing signal KeyboardInterrupt
if __name__ == '__main__':

    # Variables
    MAC = 'AA:BB:CC:DD:EE:FF'
    user = 'jacopo.nasi'
    pwd = '123456prova'

    # Opening file with date of the day
    fname='WOL_' + time.strftime("%y%m%d-%H%M") + '.log'
    f = open(fname, 'w', 0)

    # Main call and KeyboardInterrupt handler
    try:
        main(f, MAC, user, pwd)
    except KeyboardInterrupt:
        f.write('----------------------------------------------\n')
        f.write('Stop: ' + time.strftime("%d-%m-%y @ %H:%M.%S"))
    finally:
        f.close()
