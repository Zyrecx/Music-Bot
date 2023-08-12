import datetime

def convert_from_ms(milliseconds):
    seconds = milliseconds / 1000
    time = datetime.timedelta(seconds=seconds)
    minutes, seconds = divmod(time.seconds + time.days * 86400, 60)
    return f"{minutes:02d}:{seconds:02d}"
def convert_to_ms(time_str):
    if "-" in time_str:
        return 1000
    if ":" in time_str:
        m, s = time_str.split(":")
        return (int(m) * 60000 + int(s) * 1000) + 18000
    else:
        return (int(time_str) * 1000) + 18000