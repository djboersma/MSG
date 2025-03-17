#!/usr/bin/env python3

import argparse
from airdefense import radar, IFF, FiringUnit, pads
import logging
#logger=logging.getLogger(__name__)

def get_args():

    description="""
    This script is an application as requested for the Code Assignment MSG for TNO.
    It runs a simulation of a Patriot Air Defense system, consisting of a three elements,
    namely a radar, in IFF (identification of friend or foe) and a firing unit.
    Each of these elements have a standard implementation as described in the assignment (included
    in the 'docs' folder). However, the code should be written with the consideration that it should
    be extended in the future. To facilitate this, I tried to make it easy to replace each of the elements
    with a different implementation. Example config files are 
    """

    parser = argparse.ArgumentParser(
         description=description,
         epilog="The default behavior is the one described in the assignment.")

    parser.add_argument('-c','--config',default="default.json",help="Config file for the simulation (in config folder).")
    parser.add_argument('-S','--time_step_seconds',type=float,default=1.0,help="Scanning time step [seconds].")
    parser.add_argument('-v','--verbose',default=False,action='store_true',help="More output.")
    args=parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=log_level)
    simulation = pads.simulation(args.config, args.time_step_seconds)
    simulation.run()
