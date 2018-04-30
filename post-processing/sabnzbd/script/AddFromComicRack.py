#!/usr/bin/env python
#
##############################################################################
### SABNZBD POST-PROCESSING SCRIPT                                         ###
#
# Move and rename comics according to Mylar's autoProcessComics.cfg
#
# NOTE: This script requires Python to be installed on your system.
##############################################################################

# module loading
import sys
import autoProcessComics
import logging
import argparse

logger = logging.getLogger('AddFromComicRack')
fh = logging.FileHandler(r'C:\Mylar\post-processing\sabnzbd\script\AddFromComicRack.log')
logger.setLevel(logging.DEBUG)
# logging.basicConfig(filename='C:\\Mylar\\post-processing\\sabnzbd\\script\\AddFromComicRack.log', level=logging.DEBUG)
# logging.basicConfig(format='%(asctime)s %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.info("Logging is configured and running")

comicrn_version = "1.01"

logger.info("There are {} arguments.".format(len(sys.argv)))
for arg in sys.argv:
    logger.info(arg)

import argparse

parser = argparse.ArgumentParser(description='Add a comic series from ComicRack.')

parser.add_argument('--cmd', dest='cmd', help="The Mylar api command", default="getseries")
parser.add_argument('--comicname', dest='comicname', help="The name of the series")
parser.add_argument('--startyear', dest='startyear', help="The year the series started")
parser.add_argument('--comicid', dest='comicid', help="The ComicVine id for the series")
parser.add_argument('--filedir', dest='filedir', help="The directory where the issues are stored")
args = parser.parse_args()
logger.info("ArgumentParser parsed something")
logger.info(args)

autoProcessComics.getseries(args.comicid)
autoProcessComics.addseries(args.comicname, args.startyear, args.comicid, args.filedir)
# sys.exit(autoProcessComics.getseries(args.comicid))

# sys.exit(autoProcessComics.addseries(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
