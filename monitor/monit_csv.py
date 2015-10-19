import socket
import sys

TIMEOUT=5

def tcp_ping(host, port,timeout=TIMEOUT):
    addr = (str(host), int(port))
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.settimeout(timeout)
    try:
        sc.connect(addr)
    except (ConnectionRefusedError, OSError) as msg:
        print('Connection to {}:{} failed: {}'.format(addr[0], addr[1], msg))
        return False
        
    sc.shutdown(socket.SHUT_RDWR)
    sc.close()
    return True

def alarm():
    pass

def write_csv(csvfile, rows):
    import csv

    with open(csvfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if '__main__' == __name__:

    import csv

    UP = 1
    DOWN = 0

    alarmed = Fasle

    CONF = 'monit.csv'
    new_cfg = []

    with open(CONF, 'r', newline='') as f:
        reader = csv.reader(f)
        for i in reader:
            #print(i)
            host = i[0]
            port = int(i[1])
            timeout = int(i[2])
            status = int(i[3])

            if DOWN == status:
                alarmed = True

            if tcp_ping(host, port, timeout):
                status = UP
            else:
                status = DOWN

            if DOWN == status and not alarmed:
                alarm()

            i[3] = status
            new_cfg.append(i)

    write_csv(CONF, new_cfg)
