import math


class Closure:
    def __init__(self, minVal, maxVal, step):
        """
        simulates a closure, with as arithmetic +step from minVal up to maxVal (use value None to simulate infinity)
        :param minVal: the minimal value in the closure
        :param maxVal: the maximal value in the closure (None to make it upward closed)
        :param step: the step to use in the closure
        """
        if maxVal is not None and minVal is not None and maxVal < minVal:
            temp = maxVal
            maxVal = minVal
            minVal = temp
        self.minVal = minVal
        self.maxVal = maxVal
        self.step = step

    def len(self):
        """
                give the "amount of items" this would contain if it were represented as a list
                 not the builtin function because it does not allow infinity
                :return: (int) length/ float inf if inf
                """
        if self.minVal is None or self.maxVal is None:
            return math.inf

        return int((self.maxVal - self.minVal) / self.step + 1)

    def __getitem__(self, item):
        """
        UNUSED
        return the item on index item if the closure was represented as a list
        :param item: the index we need to return
        :return: the value on location item
        """
        if self.minVal is None:
            raise Exception("no minimal value")

        if item >= self.len():
            raise Exception("value out of bounds")
        return self.minVal + self.step * item

    def find_index(self, value):
        """
        find the index where the value resides
        :param value: the value for which we are looking for the index
        :return:
        """
        if value not in self:
            raise Exception("value not part of closure, so no index found")
        if self.minVal is None:
            raise Exception("lower unbounded closure has no indices")
        return (value - self.minVal) // self.step

    def get_index_list(self, start, end):
        """
        get a list values from index start to index end (not necessarily polynomial)
        used only when ensured only a polynomial amount of items (top) remain in closure
        :param start:
        :param end:
        :return:
        """
        lis = []
        for i in range(start, end):
            lis.append(self[i])

        return lis

    def __repr__(self):
        string = "Closure: minimumvalue:{} , maximumvalue:{}, stepsize:{}".format(self.minVal, self.maxVal, self.step)
        return string
