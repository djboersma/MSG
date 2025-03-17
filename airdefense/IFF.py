"""
This module provides access to implementations of the 'Identification Friend or
Foe' (IFF) algorithm for our air defense systems. Currently one IFF algorithm
are provided.  namely the one that is specified in the MSG code assignment.
That algorithm is purely fictional and should be replaced as soon as possible,
using the same interface, with something that has a basis in reality.
"""

import numpy as np
import unittest
from enum import Enum
import logging
logger=logging.getLogger(__name__)

class IFFVerdict(Enum):
    """
    This class defines the possible outcomes of an IFF algorithm.
    In the current implementation, the verdict is either "friend" or "foe",
    but as more fancy algorithms get implemented, it is likely that there will
    be a need for other verdicts, such as "unknown", "none" or "multiple".
    """
    FRIEND = 0
    FOE = 1

class EvenOddIffMethod:
    """
    This class implements the IFF method specified in the Coding Assignment
    MSG: when the number of odd values in a radar line is strictly greater than
    the number of even values, then the verdict is 'FOE', otherwise 'FRIEND'.
    """
    short_name="EvenOdd"
    def __init__(self):
        pass
    def evaluate(self,line):
        """
        Counts the number of odd and even values in an array of integer values.

        Parameter:
            line(numpy array): a non-empty 1-dimensional numpy array with an integer dtype.

        Returns:
            An IFFVerdict value ('FRIEND' or 'FOE').
        """
        if len(line.shape)!=1:
            raise ValueError("input line is not 1d")
        if line.shape[0]==0:
            raise ValueError("input line is empty")
        n_even = np.sum(line%2==0)
        n_odd = np.sum(line%2==1)
        logger.debug(f"n_even={n_even} n_odd={n_odd}")
        if n_odd>n_even:
            return IFFVerdict.FOE
        else:
            return IFFVerdict.FRIEND

class FortyTwoIffMethod:
    """
    This class implements an alternative to the IFF method specified in the
    Coding Assignment MSG: if the line contains the value 42, then a verdict is
    FRIEND, otherwise FOE.
    """
    short_name="FortyTwo"
    def __init__(self):
        pass
    def evaluate(self,line):
        """
        Checks if the input array contains the value 42.

        Parameter:
            line(numpy array): a non-empty 1-dimensional numpy array with an integer dtype.

        Returns:
            An IFFVerdict value ('FRIEND' or 'FOE').
        """
        if len(line.shape)!=1:
            raise ValueError("input line is not 1d")
        if line.shape[0]==0:
            raise ValueError("input line is empty")
        if 42 in line:
            return IFFVerdict.FRIEND
        else:
            return IFFVerdict.FOE

def get_names():
    ' ' 'Returns list of short names of IFF implementations.' ' '
    return [impl.short_name for impl in [EvenOddIffMethod,FortyTwoIffMethod]]

def get_element(name:str=EvenOddIffMethod.short_name,options:dict={}):
    """
    Factory function to create an IFF element.

    Parameters:
        name(str): should be the short name of a IFF element implementation.
        options(dict): keyword arguments to be forwarded to the IFF element constructor

    Returns:
        IFF element of the specified kind
    """
    implementations = [EvenOddIffMethod,FortyTwoIffMethod]
    for impl in implementations:
        if name==impl.short_name:
            return impl(**options)
    raise RuntimeError(f"Unknown IFF implementation '{name}'")

#######################################################################

class TestEvenOddIffMethod(unittest.TestCase):
    """
    Some basic, non exhaustive unit tests for the even/odd IFF method.
    """
    def test_normal_input(self):
        iff = EvenOddIffMethod()
        self.assertEqual(iff.evaluate(np.ones(11)),IFFVerdict.FOE)
        self.assertEqual(iff.evaluate(np.zeros(11)),IFFVerdict.FRIEND)
        self.assertEqual(iff.evaluate(np.arange(1,12)),IFFVerdict.FOE)
        self.assertEqual(iff.evaluate(np.arange(0,11)),IFFVerdict.FRIEND)
        self.assertEqual(iff.evaluate(np.arange(0,10)),IFFVerdict.FRIEND)
    def test_bad_input(self):
        with self.assertRaises(ValueError, msg="this is supposed to crash: empty input"):
            iff = EvenOddIffMethod()
            #logger.error("The following error message about a nonexistent csv file is intentional.")
            iff.evaluate(np.ones(0,dtype=int))
        with self.assertRaises(ValueError, msg="this is supposed to crash: non-1D input"):
            iff = EvenOddIffMethod()
            #logger.error("The following error message about a nonexistent csv file is intentional.")
            iff.evaluate(np.ones((11,20),dtype=int))

class TestFortyTwoIffMethod(unittest.TestCase):
    """
    Some basic, non exhaustive unit tests for the '42' IFF method.
    """
    def test_normal_input(self):
        iff = FortyTwoIffMethod()
        self.assertEqual(iff.evaluate(np.ones(11)),IFFVerdict.FOE)
        self.assertEqual(iff.evaluate(np.zeros(11)),IFFVerdict.FOE)
        self.assertEqual(iff.evaluate(42*np.ones(11)),IFFVerdict.FRIEND)
        self.assertEqual(iff.evaluate(np.arange(1,12)),IFFVerdict.FOE)
        self.assertEqual(iff.evaluate(np.arange(0,111)),IFFVerdict.FRIEND)
        self.assertEqual(iff.evaluate(np.arange(40,50)),IFFVerdict.FRIEND)
    def test_bad_input(self):
        with self.assertRaises(ValueError, msg="this is supposed to crash: empty input"):
            iff = FortyTwoIffMethod()
            #logger.error("The following error message about a nonexistent csv file is intentional.")
            iff.evaluate(np.ones(0,dtype=int))
        with self.assertRaises(ValueError, msg="this is supposed to crash: non-1D input"):
            iff = FortyTwoIffMethod()
            #logger.error("The following error message about a nonexistent csv file is intentional.")
            iff.evaluate(np.ones((11,20),dtype=int))
