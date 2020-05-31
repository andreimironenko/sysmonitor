#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc


class Monitor(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._value = None
        self._owner = None
        self._instance = None
        self._name = self.__class__.__name__.lower()

   
    @property
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError()


    def __get__(self, instance, owner):
        if not self._instance:
            self._instance = instance
        if not self._owner:
            self._owner = owner

        if instance is None:
            return self
        else:
            self._instance.__dict__[self._name] = self.value
        return self._instance.__dict__[self._name]


    def __set__(self, instance, value):
        raise NotImplementedError("You can only retrieve the value from monitor")

    def __str__(self):
        return self.__repr__()

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError()

