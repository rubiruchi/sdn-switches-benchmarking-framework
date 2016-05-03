import logging

#logger = logging.getLogger("SwitchPerformanceMonitor")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter2)
logger.addHandler(ch)
logger.debug("Launching Monitoring App")