#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
The sysmonitor module implements SysMonitor class which controlls all system critical parameters such as:

- media (ecc_failures, corrected_bits, bad_blocks)
- ram (total, free space)
- cpu usage
- cpu temperature
- etc

The configuration for each of monitor is read out the sysmonitor.conf file. In this configuration in general section
the individual montinors can be disabled:
.. code::
    [general]
    disable=correctedbits,badblocks

SystemMonitor should run as a signleton and in it's own thread. It also implements Publish-Subscribe mechanism for the
end client. The configuration must also define the threshold values(min, max) and refresh rate in seconds for each of
the individual monitor. Within the period defined in refresh rate it must read out the new value and compare it
with the threshold values, if the new value exceeds the threshold, the client must be informed and a new value must
be published.
.. code::
    [eccfailures]
    min=0
    max=2
    refresh=14400

It might be useful to keep some number of samples for each of the monitor to make a statistics.

TODO:
     - Implement ram, cpu usage and temperature monitors
     - Configuration load and parsing
     - Singleton, thread and syncronization
     - Publish and Subscribe
     - Pereodic monitor retrieve mechanism
     - Connect to AWS/back office to gather statics

**Attention!  At the moment only ecc_failures, corrected_bits and bad_blocks are used to print out on the screen during boot**
'''
from os import (
    listdir,
    path,
    environ
)

import sys
import importlib


# pylint: disable=C0325


class SysMonitor(object):
    """
    SysMonitor class provides API to access to all available monitors. To start with it, import this module
    .. code::
        from sysmonitor.agent import SysMonitor

    In this version it's possible to retrieve the value of the monitor by using period with
    SysMonitor object:
    .. code::
        system_monitor = SysMonitor()
        print("get single ecc_failures value")
        print("{}".format(system_monitor.eccfailures))

    to list all available monitors
    .. code::
        print("available monitors:")
        print(system_monitor.listall())

    to retrieve and print all monitors values
    .. code::
        print("get all monitors values")
        print(system_monitor)

    """

    namespace = dict()
    monitor_home = path.join(environ["OCPP_HOME"], "sysmonitor", "monitors")
    klasses = dict()

    def __new__(cls):

        modulenames = [module.strip(".py") for module in listdir(cls.monitor_home)
                       if path.isfile(path.join(cls.monitor_home, module))
                       and module != "__init__.py"
                       and ".pyc" not in module
                       and "monitor" not in module]

        sys.path.insert(0, cls.monitor_home)
        for modulename in modulenames:
            module = importlib.import_module(modulename)
            cls.klasses.update({name: klass for name, klass in module.__dict__.iteritems()
                                if modulename.capitalize() in name})
        for name, klass in cls.klasses.iteritems():
            cls.namespace.setdefault(name.lower(), klass())
        cls._inst = super(SysMonitor, cls).__new__(cls, **cls.namespace)
        return cls._inst

    def __init__(self):
        self.__dict__ = SysMonitor.namespace

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        output = ""
        for name, obj in self.__dict__.iteritems():
            output += "{} : {} \n".format(name, obj)
        return output

    def listall(self):
        ''' listall
        '''
        monitors = []
        for monitor in self.__dict__.iterkeys():
            monitors.append(monitor)
        return monitors
