import argparse
import re
from collections import Counter

parser = argparse.ArgumentParser(description="Process access.log")
parser.add_argument("-f", dest="file", action="store", help="Path to log file")
args = parser.parse_args()

method_regexp = r"\] \"(POST|GET|PUT|DELETE|HEAD|OPTIONS)"
ip_regexp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"


def log_reader(file_name):
    total = 0
    with open(file_name) as file:
        log = file.read()
        ips = re.findall(ip_regexp, log)
        methods = re.findall(method_regexp, log)
        return {
            "total_requests": total,
            "ips": ips,
            "methods": methods
        }


def counter(log_data):
    top_ips = Counter(log_data["ips"]).most_common(3)
    count_of_methods = Counter(log_data["methods"])
    print(f"top_ip: {top_ips} \ncount_of_methods: {count_of_methods}")


file_data = log_reader(args.file)
counter(file_data)
