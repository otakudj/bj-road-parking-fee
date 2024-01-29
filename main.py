from datetime import datetime, timedelta


def price():
    while True:
        level_num = input(f'Price Level (e.g. 1-3):')
        if level_num in ['1', '2', '3']:
            level_num = int(level_num)
            break
        else:
            print('Error Level, Please reenter !')

    while True:
        car_type = input(f'Car Type (e.g. S for small, L for large):')
        if car_type == 'S':
            param = 1
            break
        elif car_type == 'L':
            param = 2
            break
        else:
            print('Error Level, Please reenter !')

    # calculate different level fee
    # http://m.bj.bendibao.com/zffw/324554.html
    first_fee = (3.5 - level_num) * param
    then_fee = first_fee * 1.5
    night_fee = param

    return first_fee, then_fee, night_fee


class TimeParser:
    def __init__(self):
        self.less_than_24h = None
        self.start_time = None
        self.end_time = None
        self.time_format = '%H:%M:%S'
        self.datetime_format = '%Y-%m-%d %H:%M:%S'

    def parse_time(self, mode):
        time_str = input(f'{mode} Time (e.g. xx:xx:xx):')
        try:
            struct_time = datetime.strptime(time_str, self.time_format)
        except ValueError:
            print('Error format of time, Please reenter !')
            return self.parse_time(mode)
        else:
            return struct_time

    def parse_datetime(self, mode):
        time_str = input(f'{mode} Time (e.g. xxxx-xx-xx xx:xx:xx):')
        try:
            struct_time = datetime.strptime(time_str, self.datetime_format)
        except ValueError:
            print('Error format of time, Please reenter !')
            return self.parse_datetime(mode)
        else:
            return struct_time

    def parse_datetime_and_time(self, mode):
        time_str = input(f'{mode} Time (e.g. xx:xx:xx or xxxx-xx-xx xx:xx:xx):')
        try:
            struct_time = datetime.strptime(time_str, self.time_format)
        except ValueError:
            try:
                struct_time = datetime.strptime(time_str, self.datetime_format)
            except ValueError:
                print('Error format of time, Please reenter !')
                return self.parse_datetime_and_time(mode)
            else:
                self.less_than_24h = False
                return struct_time
        else:
            self.less_than_24h = True
            return struct_time

    def parse(self):
        # parse start time
        self.start_time = self.parse_datetime_and_time('Start')

        # according to start time format, parse end time
        if self.less_than_24h is True:
            self.end_time = self.parse_time('End')
            # see end time as tomorrow
            if self.end_time < self.start_time:
                self.end_time += timedelta(days=1)
        if self.less_than_24h is False:
            self.end_time = self.parse_datetime('End')
            if self.end_time < self.start_time:
                print('End time is earlier than start time, Please reenter !')
                self.end_time = self.parse_datetime('End')


if __name__ == '__main__':
    # parse 3 type fee
    first, then, night = price()

    # parse start and end time
    time_parser = TimeParser()
    time_parser.parse()
    start_time = time_parser.start_time
    end_time = time_parser.end_time

    now = start_time
    fee_times = 0
    res = 0

    # key time for interval change
    day_end = timedelta(hours=19)
    night_end = timedelta(hours=7)

    fee_interval = None

    while now < end_time:
        # accumulate the fee
        if fee_interval == timedelta(minutes=15):
            # first level fee
            if fee_times < 4:
                res += first
            # then level fee
            else:
                res += then
        elif fee_interval == timedelta(hours=2):
            res += night
        fee_times += 1

        # determine the fee bounds
        now_time = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        if night_end < now_time <= day_end:
            if fee_interval != timedelta(minutes=15):
                fee_interval = timedelta(minutes=15)
                fee_times = 0
        else:
            if fee_interval != timedelta(hours=2):
                fee_interval = timedelta(hours=2)
                fee_times = 0
        now += fee_interval

    print(f'Your Fee: {res} ￥')
