# Must be run via mesos slave VM/deployed to mesos. quick and dirty is better!
#
# Get IP addresses for MongoDB instances
# Get ports to ping
# Ping every second
# Output datetime,port_list,response
import datetime


def is_open(ip, port):
    import socket
    print("Scanning " + ip + ":" + str(port) + " ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(1)
        return True
    except:
        return False


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


def append_csv(file_name: str, row_content: list):
    import csv
    file_name = file_name + ".csv"
    file_exists(file_name)
    with open(file_name, "a") as f:
        writer = csv.writer(f)
        writer.writerow(row_content)


def iso_datetime_now():
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
    print("Scan started")
    start_time = datetime.datetime.now()
    nodes = scan_list(ip_list, port_list)
    while not done_yet(start_time, duration_minutes):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for node in nodes:
                print(node)
                results = [(executor.submit(is_open, ip=node[0], port=node[1]))]
                # results = [iso_datetime_now(), node[0], node[1], (executor.submit(is_open, ip=node[0], port=node[1]))]

            for f in concurrent.futures.as_completed(results):
                append_csv("out", [f.result()])
    print("Done")


main(get_file("ip_list"), get_file("port_list"), 5)
