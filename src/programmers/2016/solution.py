class SimpleCalendar(object):
    DAY_OF_WEEK = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, start_day_offset=0):
        if 0 <= start_day_offset <= len(self.DAY_OF_WEEK):
            self.start_day_offset = start_day_offset
        else:
            raise ValueError('Invalid offset: {}'.format(start_day_offset))

    def calc_day(self, month, day):
        current_day_offset = self.start_day_offset + day - 1

        if month > 1:
            current_day_offset += sum(self.DAYS_IN_MONTH[:month - 1])

        return self.DAY_OF_WEEK[current_day_offset % len(self.DAY_OF_WEEK)]


def solution(a, b):
    return SimpleCalendar(5).calc_day(a, b)
