"""
This module provides access to the implementations of the Firing Unit of the air defense system.
"""

import numpy as np
import unittest
import logging
logger=logging.getLogger(__name__)

class PkFiringUnit:
    """
    This implementation is for coding assessment test only.
    """
    short_name="PK"
    def __init__(self,Pk:float=0.8):
        self._pk = Pk
    def fire(self):
        """
        This method performs the firing operation by issuing a log message.
        The success is determined randomly, with an average success rate 
        of Pk (configured via the corresponding constructor parameter).

        Returns:
            True in case of a hit, False in case of a miss.
        """
        logger.info("FIRE!")
        p=np.random.uniform()
        success = p<self._pk
        return success

class FailingFiringUnit:
    """
    This implementation is for coding assessment test only.
    """
    short_name="FAIL"
    def __init__(self):
        pass
    def fire(self):
        """
        This method performs the firing operation by issuing a log message.

        Returns:
            False. This unit is guaranteed to fail.
        """
        logger.info("FIRE!")
        return False

def get_names():
    ' ' 'Returns list of short names of Firing Unit implementations.' ' '
    return [impl.short_name for impl in [PkFiringUnit,FailingFiringUnit]]

def get_element(name:str=PkFiringUnit.short_name,options:dict={}):
    """
    Factory function to create an Firing Unit element.

    Parameters:
        name(str): should be the short name of a Firing Unit element implementation.
        options(dict): keyword arguments to be forwarded to the Firing Unit element constructor

    Returns:
        Firing Unit element of the specified kind
    """
    implementations = [PkFiringUnit,FailingFiringUnit]
    for impl in implementations:
        if name==impl.short_name:
            return impl(**options)
    raise RuntimeError(f"Unknown IFF implementation '{name}'")

#######################################################################

class TestPkFiringUnit(unittest.TestCase):
    def test_normal(self):
        ntest=100000
        Pk=0.8
        nsuccess=0
        fu = PkFiringUnit(Pk=Pk)
        for itest in range(ntest):
            if fu.fire():
                nsuccess += 1
        nmin=(Pk-0.1)*ntest
        self.assertTrue(nsuccess>nmin)
    def test_perfect(self):
        ntest=100000
        nsuccess=0
        fu = PkFiringUnit(Pk=1.0)
        for itest in range(ntest):
            if fu.fire():
                nsuccess += 1
        self.assertEqual(nsuccess,ntest)
    def test_fail(self):
        ntest=100000
        nsuccess=0
        fu = PkFiringUnit(Pk=0.0)
        for itest in range(ntest):
            if fu.fire():
                nsuccess += 1
        self.assertEqual(nsuccess,0)

class TestFailingFiringUnit(unittest.TestCase):
    def test_normal(self):
        ntest=100000
        nsuccess=0
        fu = FailingFiringUnit()
        for itest in range(ntest):
            if fu.fire():
                nsuccess += 1
        self.assertEqual(nsuccess,0)
