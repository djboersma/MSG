"""
This module implements the simulation of a patriot air defense system,
using three configurable elements for the radar, IFF and firing unit.
"""

import json
from pathlib import Path
from airdefense import radar, IFF, FiringUnit
import time
from datetime import datetime, timedelta
import logging
logger=logging.getLogger(__name__)

class simulation:
    """
    Simulation of patriot air defense system. The configuration of the
    radar, IFF and firing unit is taken from a json file.
    """
    config_dir = Path(__file__).parent.parent / "config"
    default_step = 1.0
    default_config = "default.json"
    def __init__(self,cnf_filename:str=default_config, time_step_seconds=default_step):
        config_path = simulation.config_dir / cnf_filename
        self._time_step_seconds = time_step_seconds
        logger.debug(f"going to read config file {str(config_path)}")
        with config_path.open() as fp:
            config = json.load(config_path.open())
        logger.debug(f"Successfully read config file {str(config_path)}")
        name=config["radar"]["name"]
        options=config["radar"].get("options",dict())
        self._radar = radar.get_element(name=name,options=options)
        name=config["IFF"]["name"]
        options=config["IFF"].get("options",dict())
        self._IFF = IFF.get_element(name=name,options=options)
        name=config["FiringUnit"]["name"]
        options=config["FiringUnit"].get("options",dict())
        self._FiringUnit = FiringUnit.get_element(name=name,options=options)
        logger.info("Air Defense System ready")
    def run(self):
        sim_start=datetime.now()
        logger.info(f"starting simulation at {sim_start}")
        for lineno,line in enumerate(self._radar.lines()):
            verdict = self._IFF.evaluate(line)
            if verdict == IFF.IFFVerdict.FRIEND:
                logger.info("FRIEND")
            elif verdict == IFF.IFFVerdict.FOE:
                logger.info("FOE")
                hit = self._FiringUnit.fire()
                if hit:
                    logger.info("HIT")
                else:
                    logger.info("MISS")
            next_time=sim_start+timedelta(seconds=(lineno+1)*self._time_step_seconds)
            sleep_seconds=(next_time-datetime.now()).total_seconds()
            time.sleep(sleep_seconds)
