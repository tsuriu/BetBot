from collections import Counter
from datetime import datetime
from .db import database


def str2float(num):
    return float(num.replace(".", "").replace(",", "."))


def unique(list1,k):
    keys = [item[k] for item in list1]
    return list(Counter(keys).keys())


def time_formater(datetime_str):
    l = list(datetime_str)
    l.insert(13, ":")
    l.insert(16, ":")
    
    return ''.join(l)


def datetime_formater(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
    return datetime.timestamp(datetime_obj)


def getDuration(then, now = datetime.now(), interval = "default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)   
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]


def save_data(data, b_key, b_name):
    db_path = "./data/"

    for k in unique(data, "date"):
        db_name = ((k.split(" "))[0]).replace("/","_")

        DB = database("".join([db_path,db_name+"_"+b_name,".json"]))

        dt_keep = DB.check_by_key(data, "date", k)

        if len(DB.get()) != 0:
            dt_keep = DB.remove_duplicates(dt_keep, b_key)

        DB.add(dt_keep)