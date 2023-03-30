import time
from datetime import datetime
from datetime import timedelta





def time_difference(date,diff):
    # Marca de tiempo dada en cadena
    time_str = date
    date_format_str="%Y-%m-%d %H:%M:%S.%f"
    # crear un objeto de fecha y hora a partir de una fecha de tipo cadena
    given_time = datetime.strptime(time_str, date_format_str)
    #print('fecha entrante: ', given_time)
    n = diff
    # Reste 2 horas del objeto de fecha y hora
    final_time = given_time - timedelta(hours=n)
    #print('fecha final con 3 horas menos: ', final_time)
    res = str(final_time).split(".")
    return(str(res[0]))


def capture_day():
    return time.strftime("%Y-%m-%d")

def capture_houer():
    return time.strftime("%H:%M:%S")

def capture_full():
    return time.strftime("%Y-%m-%d")+"T"+time.strftime("%H:%M:%S")

def capture_full_upd():
    return time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")

def capture_year():
    return time.strftime("%Y")