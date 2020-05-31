#!/usr/bin/env python
# -*- coding: utf-8 -*-

from monitor import Monitor

class Badblocks(Monitor):

    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """
    _sysfs = "/sys/class/mtd/mtd3/bad_blocks"

    def __init__(self):
        super(Badblocks, self).__init__()
        self._value = 0

    def __get__(self, obj, objtype):
        value = 0
        with open(Badblocks._sysfs, "r") as fd:
            value = int(fd.readline())
        return value

    @property
    def value(self):
        with open(Badblocks._sysfs, "r") as fd:
            self._value = int(fd.readline())
        return self._value


    def __repr__(self):
        value = self.value
        if value > 9:
            return "{:02d}".format(value)
        else:
            return "{:d}".format(value)


