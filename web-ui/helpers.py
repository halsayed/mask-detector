from datetime import datetime


def convert_unixepoch_to_time(timestamp):
    if timestamp:
        timestamp = float(timestamp)
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return 'No feed'