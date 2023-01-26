def in_range(i, l, h):
    return i >= l and i <= h

class Activity:
    marks_names = [
        'Абсолютная оценка количества проделанной работы',
        'Относительная оценка количества проделанной работы',
        'Абсолютная оценка настроения',
        'Относительная оценка настроения'
    ]

    limits_low = [0, -100, 0, -100]
    limits_high = [100, 100, 100, 100]

    def __init__(self) -> None:
        self.marks = []
    
    def next_title(self):
        if len(self.marks) > 3:
            return None
        return Activity.marks_names[len(self.marks)]

    def write_mark(self, value):
        self.check_limits(value)
        self.marks.append(value)
    
    def check_limits(self, value):
        index = len(self.marks)
        val = int(value)
        if not in_range(val, Activity.limits_low[index], Activity.limits_high[index]):
            raise ValueError(f'Введите значение между {Activity.limits_low[index]} и {Activity.limits_high[index]}')
    
    def get_marks(self):
        return self.marks[0], self.marks[1], self.marks[2], self.marks[3]
