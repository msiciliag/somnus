'''other scripts in the somnus package'''

def calculate_sleep_hour(wake_up_time, duration):
    '''calculate the time to sleep based on the time table'''        
    wake_up_time = wake_up_time.split(':')
    wake_up_time = int(wake_up_time[0])*60 + int(wake_up_time[1])
    duration = duration*60
    print(wake_up_time, duration)
    sleep_time = wake_up_time - duration
    if sleep_time < 0:
        sleep_time = 1440 + sleep_time
    sleep_HH = str(int(sleep_time//60)).zfill(2)
    sleep_mm = str(int(sleep_time%60)).zfill(2)
    sleep_hour = sleep_HH + ':' + sleep_mm
    return sleep_hour

if __name__ == '__main__':
    print(calculate_sleep_hour('06:30', 8.5))
    print("Result should be 22:00")