#!/usr/bin/env python
# -*- coding: utf-8 -*-

from monitor import Monitor

class Eccfailures(Monitor):

    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """
    _sysfs = "/sys/class/mtd/mtd3/ecc_failures"

    def __init__(self):
        super(Eccfailures, self).__init__()

    @property
    def value(self):
        with open(Eccfailures._sysfs, "r") as fd:
            self._value = int(fd.readline())
        return self._value

    def __repr__(self):
        value = self.value
        if value > 9:
            return "{:02d}".format(value)
        else:
            return "{:d}".format(value)


