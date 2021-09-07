import datetime


def is_open(ip, port):
    import socket
    out = [datetime_now_iso(), ip, port]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, int(port)))
    if result == 0:
        out.append(True)
        sock.close()
        return out
    else:
        out.append(False)
        sock.close()
        return out


def get_file(file_name: str):
    with open(file_name, "r", newline="") as f:
        return f.read().splitlines()


def file_exists(file_name: str):
    import os.path
    if os.path.isfile(file_name):
        return True
    from pathlib import Path
    Path(file_name).touch()
    return True


def write_csv(file_name: str, row_content: list):
    import csv
    file_name = file_name + ".csv"
    file_exists(file_name)
    with open(file_name, "a") as f:
        writer = csv.writer(f)
        writer.writerow(row_content)
        f.flush()
    return 0


def datetime_now_iso():
    from datetime import datetime
    return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S.%f")


def done_yet(start: datetime.datetime, duration_minutes: int):
    now = datetime.datetime.now()
    if int((now - start).total_seconds() / 60) >= duration_minutes:
        return True


def scan_list(ip_list, port_list):
    out = []
    for ip in ip_list:
        for port in port_list:
            out.append([ip, port])
    return out


def main(ip_list, port_list, duration_minutes: int):
    import concurrent.futures
    start_time = datetime.datetime.now()
    write_csv("scan-" + str(start_time), ["DateTime", "IP", "Port", "Alive"])
    print("Scan started at " + str(start_time))
    nodes = scan_list(ip_list, port_list)
    while not done_yet(start_time, duration_minutes):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(is_open, ip=node[0], port=node[1]) for node in nodes]

        for f in concurrent.futures.as_completed(results):
            write_csv("scan-" + str(start_time), f.result())
    end_time = datetime.datetime.now()
    print("Scan completed at " + str(end_time))


main(get_file("ip_list"), get_file("port_list"), 2)
