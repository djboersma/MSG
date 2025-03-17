"""
This module provides access to implementations of the radar element for our air
defense systems.  Currently two radar implementations are provided, one of them
implements the CSV based radar as specified in the assignment, the other is
purely to test that the system can run with a different radar element
implementation.

A radar element class implementation should have a lines method that behaves
like a generator of arrays of radar data. The radar data array should an fixed
length integer array. The class should also have properties "ncols" and
"nrows", which represent the (nonzero) length of the array and the
(nonnegative) number of lines, respectively.  A value of zero for "ncols"
signifies an infinite number of lines, i.e. the radar never stops.
"""

import numpy as np
import functools
import unittest
from pathlib import Path
import logging

logger=logging.getLogger(__name__)

class CsvFileRadar:
    """
    This class implements the radar element for the code assignment exercise.
    It reads data from a CSV file. We allow some formatting flexibility.
    """
    short_name = "CSV"
    data_dir = Path(__file__).parent.parent / "data"
    default_csv = "radar_data.csv"
    def __init__(self,filename:str=default_csv,delim:str=";",base:int=2):
        """
        Initializes a CsvFileRadar object.

        Parameters:
            filename(str): file name of the CSV file to use (in the data directory). The default CSV file contains the data from the code assignment.
            delim(str): delimiter to assume for parsing the CSV file.
            base(int): e.g. 2 for binary, 16 for hex.
        """
        csv_filepath = CsvFileRadar.data_dir / filename
        logger.debug(f"going to read CSV file {str(csv_filepath)}")
        self._read_csv_file(csv_filepath,delim,base)
    @property
    def nrows(self):
        ' ' 'Number of rows / radarlines available from the CSV file.' ' '
        return self._nrows
    @property
    def ncols(self):
        ' ' 'Number of data values per radar line.' ' '
        return self._ncols
    def lines(self):
        ' ' 'Generator method that will yield the radar lines one at a time.' ' '
        for lineno,line in enumerate(self._radar_data):
            logger.info(f"radar sweep No. {lineno}")
            yield line
    # implementation details
    def _read_csv_file(self,filepath,delim,base):
        try:
            conv=functools.partial(int,base=base)
            self._radar_data=np.loadtxt(filepath,dtype=int,converters=conv,delimiter=delim)
            logger.debug(f"got radar data with shape {self._radar_data.shape}")
            self._nrows, self._ncols = self._radar_data.shape
            self._csv_file_path = filepath
        except Exception as e:
            logger.error(f"Problem reading radar CSV data from {filepath}: {e}")
            raise

class RandomTestRadar:
    """
    This class is intended to be used only for tests.
    It implements the same interface as CsvFileRadar.
    """
    short_name="RND"
    def __init__(self,nrows:int=0,ncols:int=11,low:int=10,high:int=100):
        """
        Initializes a RandomTestRadar object.

        Parameters:
            nrows(int): number of rows to be generated (0=infinity)
            ncols(int): number of values to be generated per radar line
            low(int): minimum value (inclusive) to be generated
            high(int): maximum value (exclusive) to be generated
        """
        self._nrows = nrows
        self._ncols = ncols
        self._low = low
        self._high = high
    @property
    def nrows(self):
        ' ' 'Number of rows / radarlines to be generated (0=infinity).' ' '
        return self._nrows
    @property
    def ncols(self):
        ' ' 'Number of values to be generated per radar line.' ' '
        return self._ncols
    def lines(self):
        ' ' 'Generator method that will yield the radar lines one at a time.' ' '
        lineno=0
        while self._nrows==0 or lineno<self._nrows:
            yield np.random.randint(high=self._high,low=self._low,size=self._ncols)
            lineno += 1

def get_names():
    ' ' 'Returns list of short names of radar system implementations.' ' '
    return [impl.short_name for impl in [CsvFileRadar,RandomTestRadar]]

def get_element(name:str=CsvFileRadar.short_name,options:dict={}):
    """
    Factory function to create a radar element.

    Parameters:
        name(str): should be the short name of a radar element implementation.
        options(dict): keyword arguments to be forwarded to the radar element constructor

    Returns:
        Radar element of the specified class
    """
    implementations = [CsvFileRadar,RandomTestRadar]
    for impl in implementations:
        if name==impl.short_name:
            return impl(**options)
    raise RuntimeError(f"Unknown radar element implementation '{name}'")


#######################################################################

class TestCsvFileRadar(unittest.TestCase):
    """
    Some basic, non exhaustive unit tests for the CSV file radar class.
    """
    def test_nonexistent(self):
        with self.assertRaises(FileNotFoundError, msg="this is supposed to crash"):
            logger.error("The following error message about a nonexistent csv file is intentional.")
            impossible = CsvFileRadar(filename="nonexistent.csv")
    def test_default(self):
        csv_radar = CsvFileRadar()
        self.assertEqual(csv_radar.ncols,11)
        self.assertEqual(csv_radar.nrows,20)
        lastbits=[1,0,1,1,0,1,1,1,0,0,0,0,1,0,1,0,0,1,1,0]
        for lineno,line in enumerate(csv_radar.lines()):
            self.assertEqual(len(line),11,msg="wrong line length")
            self.assertTrue(lineno<20,msg="CSV radar element should yield exactly 20 lines of data")
            self.assertEqual(line[10]%2 , lastbits.pop(0))
        self.assertEqual(lineno+1,20, msg="Wrong number of lines yielded from default CSV radar element.")
    def test_custom(self):
        for ncols,nrows in [(4,5),(360,1000)]:
            nmod=ncols-1
            test_data = a=np.array(np.arange(nrows*ncols)%nmod).reshape(nrows,ncols)
            test_delim = "|"
            test_filename =  f"unittest_radar_data_{ncols}_{nrows}.csv"
            test_path = CsvFileRadar.data_dir / test_filename
            self.assertFalse(test_path.exists(), msg=f"Test file '{test_path}' already/still exists, please move it out of the way.")
            np.savetxt(str(test_path),test_data,fmt="%x",delimiter=test_delim)
            self.assertTrue(test_path.exists(), msg="Failed to create test data '{test_path}'.")
            csv_radar = CsvFileRadar(filename=test_filename,delim=test_delim,base=16)
            self.assertEqual(csv_radar.ncols,ncols)
            self.assertEqual(csv_radar.nrows,nrows)
            for lineno,line in enumerate(csv_radar.lines()):
                self.assertEqual(len(line),ncols,msg="wrong line length")
                self.assertTrue(np.all(line>=0),msg=f"In this unit test, all values in the CSV radar file should be >= 0")
                self.assertTrue(np.all(line<nmod),msg=f"In this unit test, all values in the CSV radar file should be < {nmod}")
                self.assertEqual(line[ncols-1],lineno%nmod,msg=f"In this unit test, the last value of every line should equal line number modulo {nmod}")
            self.assertEqual(lineno+1,nrows, msg="Wrong number of lines yielded from customized test CSV radar element.")
            Path(test_path).unlink()

class TestRandomTestRadar(unittest.TestCase):
    """
    Some basic, non exhaustive unit tests for the random radar test class.
    """
    def test_default(self):
        rnd_radar = RandomTestRadar()
        self.assertEqual(rnd_radar.ncols,11)
        self.assertEqual(rnd_radar.nrows,0)
        all_values=set(range(10,100))
        npatience=10000
        for lineno,line in enumerate(rnd_radar.lines()):
            self.assertEqual(len(line),11,msg="wrong line length")
            self.assertTrue(all(line>=10))
            self.assertTrue(all(line<100))
            all_values = all_values - set(line[:])
            if len(all_values) == 0:
                break
            npatience -= 1
            self.assertTrue(npatience>0,msg="Maybe the random values are not generated entirely uniformly.")
    def test_custom(self):
        for ncols,nrows in [(4,5),(360,1000)]:
            for low,high in [(0,128),(0,1024)]:
                rnd_radar = RandomTestRadar(nrows=nrows, ncols=ncols, high=high, low=low)
                self.assertEqual(rnd_radar.ncols,ncols)
                self.assertEqual(rnd_radar.nrows,nrows)
                for lineno,line in enumerate(rnd_radar.lines()):
                    self.assertEqual(len(line),ncols,msg="wrong line length")
                    self.assertTrue(all(line>=low))
                    self.assertTrue(all(line<high))
                    self.assertTrue(lineno<nrows,msg=f"In this test we expected exactly {nrows} lines of data.")
                self.assertEqual(lineno+1,nrows, msg="Wrong number of lines yielded from 'random test' radar element.")
