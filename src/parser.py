import os
import re
import json
import argparse
from collections import Counter
from operator import itemgetter

method_regexp = r"\] \"(POST|GET|PUT|DELETE|HEAD|OPTIONS)"
ip_regexp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
time_regexp = r"(\d)*$"
url_regexp = url = r"(/\D*) HTTP"


def get_args():
    parser = argparse.ArgumentParser(description="Process access.log")
    parser.add_argument("-f", dest="file", action="store", help="Path to log file")
    parser.add_argument('-d', dest="directory", help='Path to directory with log files')
    return parser.parse_args()


def get_ip(filename):
    with open(filename) as file:
        log = file.read()
        ips = Counter(re.findall(ip_regexp, log)).most_common(3)
        return dict(ips)


def get_requests_methods(filename):
    with open(filename) as file:
        log = file.read()
        request_methods = Counter(re.findall(method_regexp, log))
        return dict(request_methods)


def get_count_request(filename):
    count_request = 0
    with open(filename) as file:
        for _ in file:
            count_request += 1
    return count_request


def get_longest_requests(filename):
    requests = []
    with open(filename) as file:
        counter = 0
        for log in file:
            counter += 1
            if re.search(ip_regexp, log) and re.search(method_regexp, log):
                if re.search(url_regexp, log) and re.search(time_regexp, log):
                    requests.append([
                        re.search(ip_regexp, log).group(0),
                        re.search(method_regexp, log).group(1),
                        re.search(url_regexp, log).group(1),
                        re.search(time_regexp, log).group(0)
                    ])
    return sorted(requests, key=itemgetter(3), reverse=True)[:3]


def main():
    args = get_args()
    if args.file:
        result = {
            "TOTAL_REQUESTS": get_count_request(args.file),
            "TOP_IP_ADDRESS": get_ip(args.file),
            "REQUESTS_METHODS": get_requests_methods(args.file),
            "TOP_LONGEST_REQUESTS": get_longest_requests(args.file)
        }
        with open("result_file.json", "w") as result_file:
            json_dumps = json.dumps(result, indent=4)
            print(json_dumps)
            result_file.write(json_dumps)
    if args.directory:
        if os.path.exists(args.directory):
            if os.path.isdir(args.directory):
                dir_files = os.listdir(args.directory)
                for file in dir_files:
                    if file.endswith('.log'):
                        result = {
                            "TOTAL_REQUESTS": get_count_request(os.path.join(args.directory, file)),
                            "TOP_IP_ADDRESS": get_ip(os.path.join(args.directory, file)),
                            "REQUESTS_METHODS": get_requests_methods(os.path.join(args.directory, file)),
                            "TOP_LONGEST_REQUESTS": get_longest_requests(os.path.join(args.directory, file))
                        }
                        with open("result_dir.json", "a") as result_file:
                            json_dumps = json.dumps(result, indent=4)
                            print(json_dumps)
                            result_file.write(json_dumps)
                            result_file.write(", \n")
            else:
                raise Exception(f"Is not a directory: {args.directory}")
        else:
            raise Exception(f"No such directory exists: {args.directory}")


if __name__ == '__main__':
    main()
