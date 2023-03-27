import time


def capture_day():
    return time.strftime("%Y-%m-%d")

def capture_houer():
    return time.strftime("%H:%M:%S")

def capture_full():
    return time.strftime("%Y-%m-%d")+"T"+time.strftime("%H:%M:%S")

def capture_year():
    return time.strftime("%Y")