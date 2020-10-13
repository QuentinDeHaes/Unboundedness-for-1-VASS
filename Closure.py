class Closure:
    def __init__(self, minVal, maxVal, step):
        """
        simulates a closure, with as arithmetic +step from minVal up to maxVal (use value None to simulate infinity)
        :param minVal: the minimal value in the closure
        :param maxVal: the maximal value in the closure (None to make it upward closed)
        :param step: the step to use in the closure
        """
        self.minVal = minVal
        self.maxVal = maxVal
        self.step = step

    def is_in(self, value):
        """
        gives a boolean value to check whether the value is within the closure
        :param value: the value to be checked
        :return: True or False depending of whether it's part of the closure
        O(1) as amount of steps is constant
        """

        if (self.minVal < value or self.minVal is None) and (value < self.maxVal or self.maxVal is None):
            if (self.minVal is None and value%self.step == self.maxVal %self.step) or (value % self.step == self.minVal % self.step) :
                return True
        return False
