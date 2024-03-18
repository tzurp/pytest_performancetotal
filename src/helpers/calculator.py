import math


class Calculator:
    def get_average_and_standard_deviation(self, duration_list):
        mean = self.get_average_time_span(duration_list)
        sos = 0
        sem = 0

        # calculate sem
        if len(duration_list) > 1:
            for d in duration_list:
                sos += math.pow(d - mean, 2)
            std = math.sqrt(sos / (len(duration_list) - 1))
            sem = std / math.sqrt(len(duration_list))
        return [round(mean), round(sem)]

    def get_average_time_span(self, duration_list):
        result = sum(duration_list) / len(duration_list)
        return round(result)
