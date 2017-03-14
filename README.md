# Wake-on-Lan after Mail

Python script for waking up devices with a mail with some defined condition.
This version is now working with a log file only. The idea is to run it on a RaspberryPy in background with setsid command.
I have set up a timer that increase/decrease the interval of checks looking at the hours of the day.

### Prerequisites

To run this script you need to have Python installed.

```
brew install python
```
You'll also need this package:
```
pip install wakeonlan prettytable
```

### Preparing script

There are 3 main variables necessary for the correct working of the software, MAC (of the devices to be waked), username and password of the mail account.
```
MAC = 'AA:BB:CC:DD:EE:FF' ---> MAC = 'your MAC address'
user = 'example' ---> user = 'your mail address'
...
```

## Running the tests

To run the system use:
```
python mailcheck.py
```
For the MagicPacket check you can use Wireshark.

# How it works?

The software is studied to be runned in background like this:

```
setsid python mailcheck.py
```
the script will check every 2s the presence of a new mail, then it will compare the received mail with the fields that you want, in this case with the SUBJECT of the mail that it must to be equal to 'WOL' if it will be then scrit will send the MagicPacket to the specified MAC.
This software is build for managing the Keyboard Interrupt signal for the correct shutdown of the script.

The script can manage multiple situations:
* Internet Fail - In case of this it will restart the procedure after a waiting time like 30s
* Wrong user - This will cause the close of the script with a proper record in the log
* Wrong pwd - This will cause the close of the script with a proper record in the log

## Dependencies

* [poplib] - For POPSSL framework
* [datetime] - Date time Library
* [time] - Time library
* [email] - To Parse the the mail
* [wakeonlan] - For sending MagicPacket
* [PrettyTable] - For the .log file
(https://pypi.python.org/pypi/wakeonlan/0.2.2)


## Built With

* [Python](http://pythoncentral.io) - The programming language

## Authors

* **Jacopo Nasi** - *Initial work* - [Jacopx](https://github.com/Jacopx)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Use at your own risk
* I'm not responsible of your use of this code
