# -*- coding: cp1251 -*-
import serial, time
import propites
import re
ser = serial.Serial()
ser.port = "COM3"
#ser.port = "/dev/ttyS2"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
#ser.timeout = 0             #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 3     #timeout for write

# Переменные из динамического файла


def out_(sleep = 0): # Функция вывода с устройства
    out = b''
    while ser.inWaiting() > 0:
        r = ser.read(1)
        if not(r == b'\r' or r ==b'\n'):
            out += r
        elif r == b'\n':
            out += b'\n'
    time.sleep(sleep)
    return out.decode("utf-8")

def start_test(sleep = 10):
    log_in_out = ''
    while True:
        log_in_out += out_(sleep)
        if re.search(r"Username:", log_in_out) is not None:
            # ser.write(b"\r\n")
            break
        else:
            ser.write(b"\r\n")

def reset_():
    log_in_out = ''
    ser.write(b"admin\r\n")
    log_in_out += out_()
    ser.write(b"12345\r\n")
    log_in_out += out_()
    ser.write(b"erase startup-config\r\n")
    log_in_out += out_()
    ser.write(b"y\r\n")
    ser.write(b"exi\r\n")
    return log_in_out


try: # Проверка на включение
    if ser.isOpen():
        ser.close()
    ser.open()

except Exception as e:
    print("error open serial port:" + str(e))
    exit()

if ser.isOpen():
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput() #flush output buffer, aborting current output 

        log_in_out = ''
        #write data
        # start_test(7)
        #log_in_out += reset_()
        # log_in_out += out_()

        while True:
            ser.write(b"admin\r\n")
            time.sleep(1)
            r = out_()
            if re.search("No such user or bad password", r) is None:
                break
            log_in_out += r

        ser.write(b"12345\r\n")
        log_in_out += out_()
        print(log_in_out)
        exit()
        ser.write(b'show system\r\n')
        log_in_out += out_()
        ser.write(b'show version\r\n')
        log_in_out += out_()
        ser.write(b"conf\r\n")
        log_in_out += out_()
        ser.write(b"vlan 25\r\n")
        log_in_out += out_()
        ser.write(b"interface vlan 25\r\n")
        log_in_out += out_()
        ser.write(b"ip address " + propites.ip + b"\r\n") # Меняется только IP
        log_in_out += out_()
        ser.write(b"exi\r\n")
        log_in_out += out_()
        ser.write(b"ip route-static 0.0.0.0 0.0.0.0 10.223.147.1\r\n")
        log_in_out += out_()
        ser.write(b"interface xgigaethernet 1/1/1\r\n")
        log_in_out += out_()
        ser.write(b"port link-type trunk\r\n")
        log_in_out += out_()
        ser.write(b"port trunk allow-pass vlan 25\r\n")
        log_in_out += out_()
        ser.write(b"exi\r\n")
        log_in_out += out_()
        ser.write(b"interface xgigaethernet 1/1/2\r\n")
        log_in_out += out_()
        ser.write(b"port link-type trunk\r\n")
        log_in_out += out_()
        ser.write(b"port trunk allow-pass vlan 25\r\n")
        log_in_out += out_()
        ser.write(b"exi\r\n")
        log_in_out += out_()
        ser.write(b"interface xgigaethernet 1/2/1\r\n")
        log_in_out += out_()
        ser.write(b"port link-type trunk\r\n")
        log_in_out += out_()
        ser.write(b"port trunk allow-pass vlan 25\r\n")
        log_in_out += out_()
        ser.write(b"exi\r\n")
        log_in_out += out_()
        ser.write(b"interface xgigaethernet 1/2/2\r\n")
        log_in_out += out_()
        ser.write(b"port link-type trunk\r\n")
        ser.write(b"port trunk allow-pass vlan 25\r\n")
        ser.write(b"exi\r\n")
        time.sleep(1.5)
        ser.write(b"write file\r\n")
        time.sleep(2.5)
        ser.write(b"y\r\n")
        log_in_out += out_()

        ser.write(b"show system\r\n")
        time.sleep(0.5)
        log_in_out += out_()


        # let's wait one second before reading output (let's give device time to answer)

        

        time.sleep(2.5)  #give the serial port sometime to receive the data

        numOfLines = 0

        # while True:
        #
        #     response = ser.readline()
        #
        #     print("read data: " + response.decode("utf-8"))
        #
        #     numOfLines = numOfLines + 1
        #
        #     if (numOfLines >= 250):
        #
        #         break

        ser.close()
        with open("log.txt", "w") as file:
            file.write(log_in_out)
        mac_ = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', log_in_out)[0]
        serial_numb = re.search(r'(:  )(\w+\b)', log_in_out)[2]
        with open("info.txt", "w") as file:
            file.write(mac_ + '\n' + serial_numb)
    except Exception as e1:

        print ("error communicating...: " + str(e1))

else:

    print ("cannot open serial port ")
