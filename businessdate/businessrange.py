# -*- coding: utf-8 -*-

#  businessdate
#  ------------
#  A fast, efficient Python library for generating business dates inherited
#  from float for fast date operations. Typical banking business methods
#  are provided like business holidays adjustment, day count fractions.
#  Beside dates generic business periods offer to create time periods like
#  '10Y', '3 Months' or '2b'. Periods can easily added to business dates.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Copyright: 2016, 2017 Deutsche Postbank AG
#  Website: https://github.com/pbrisk/businessdate
#  License: APACHE Version 2 License (see LICENSE file)


from .businessperiod import BusinessPeriod
from .businessdate import BusinessDate


class BusinessRange(list):
    def __init__(self, start, stop=None, step=None, rolling=None):
        """ range like class to build list of `BusinessDate`

        :param BusinessDate start: date to begin schedule,
         if stop not given, start will be used as stop and
         default in rolling to BusinessDate()
        :param BusinessDate stop: date to stop before,
         if not given, start will be used for stop instead
        :param BusinessPeriod step: period to step schedule,
         if not given 1 year is default
        :param BusinessDate rolling: date to roll on
         (forward and backward) between start and stop,
         if not given default will be start

        **Ansatz** First, `rolling` and `step`
        defines a infinite grid of dates.
        Second, this grid is sliced by `start` (included ,
        if meeting the grid) and `end` (excluded).

        """

        # set default args and build range grid
        start, stop, step, rolling = self._default_args(start, stop, step, rolling)
        schedule = self._build_grid(start, stop, step, rolling)

        # push to super and sort
        super(BusinessRange, self).__init__(set(schedule))
        self.sort()

    @staticmethod
    def _default_args(start, stop, step, rolling):
        if stop is None:
            stop = start
            start = BusinessDate()
        if step is None:
            step = BusinessPeriod(years=1)
        if rolling is None:
            rolling = start
        # make proper businessdate objects
        start = BusinessDate(start)
        rolling = BusinessDate(rolling)
        stop = BusinessDate(stop)
        step = BusinessPeriod(step)
        return BusinessDate(start), BusinessDate(stop), BusinessPeriod(step), BusinessDate(rolling)

    @staticmethod
    def _build_grid(start, stop, step, rolling):
        # setup grid and turn step into positive direction
        grid = list()
        step = step if rolling <= rolling + step else -1 * step

        # roll backward before start
        i = 0
        current = rolling + step * i
        while start <= current:
            i -= 1
            current = rolling + step * i

        # fill grid from start until end
        current = rolling + step * i
        while current < stop:
            current = rolling + step * i
            if start <= current < stop:
                grid.append(current)
            i += 1

        return grid

    def adjust(self, convention='', holidays=None):
        """ returns adjusted `BusinessRange` following given convention

        For details of adjusting `BusinessDate` see 'BusinessDate.adjust()`.

        For possible conventions invoke `BusinessDate().adjust()`

        For more details on the conventions see module `businessdate.conventions`)
        """

        adj_list = [d.adjust(convention, holidays) for d in self]
        del self[:]
        super(BusinessRange, self).extend(adj_list)
        return self
