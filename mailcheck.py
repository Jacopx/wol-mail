# Importing all Dependencies
import poplib
from email import parser
import time
from wakeonlan import wol
from prettytable import PrettyTable

# Variables
MAC = 'AA:BB:CC:DD:EE:FF'
user = 'jacopo.nasi'
pwd = '123456abcde'

def close(f, l):

    f.write('{0}'.format(l))
    f.write('\nStop: ' + time.strftime("%d-%m-%y @ %H:%M.%S"))
    f.close()

def login(f, l, user, pwd):
    # Gmail POP3 Server
    try:
        pop_link = poplib.POP3_SSL('pop.gmail.com')
        pop_link.set_debuglevel(2)
    except:
        l.add_row(["ERR", "POP3", time.strftime("%H:%M.%S"), "---"])
        time.sleep(3)
        main(l, MAC, user, pwd)

    try:
        pop_link.user(user)
    except:
        l.add_row(["ERR", "USER", time.strftime("%H:%M.%S"), "---"])
        raise SystemExit(close(f, l))

    try:
        pop_link.pass_(pwd)
    except:
        l.add_row(["ERR", "PWD", time.strftime("%H:%M.%S"), "---"])
        raise SystemExit(close(f, l))

    return pop_link

def main(l, MAC, user, pwd):

    t=10
    # Infinite cycle
    while 1:
        # Call login function
        pop_link = login(f, l, user, pwd)

        # Get messages from server:
        msg = [pop_link.retr(i) for i in range(1, len(pop_link.list()[1]) + 1)]
        # Concat message pieces:
        msg = ["\n".join(mssg[1]) for mssg in msg]
        msg = [parser.Parser().parsestr(mssg) for mssg in msg]

        # Printing log and cheching MSG syntax
        for msg in msg:
            if msg['subject']=='WOL': # Correct Message receiver
                l.add_row(["WOL", "YES", time.strftime("%H:%M.%S"), msg['from']])
                # Sending MP to MAC, Broadcast IP and Port 9
                wol.send_magic_packet(MAC, ip_address='255.255.255.255', port=9)
            else: # Wrong message receiver
                l.add_row(["WOL", "NO", time.strftime("%H:%M.%S"), msg['from']])

        # Close the active connection
        pop_link.quit()
        # Waiting t time before recheck
        time.sleep(t)

# Managing signal KeyboardInterrupt
if __name__ == '__main__':

    # Opening table
    l = PrettyTable(["Type", "Correct", "Time", "From"])

    # Opening file with date of the day
    fname='WOL_' + time.strftime("%y%m%d-%H%M") + '.log'
    f = open(fname, 'w', 0)
    # Writing starting time and divisor
    f.write('Start: ' + time.strftime("%d-%m-%y @ %H:%M.%S") + '\n')

    # Main call and KeyboardInterrupt handler
    try:
        main(l, MAC, user, pwd)
    except KeyboardInterrupt:
        close(f, l)
