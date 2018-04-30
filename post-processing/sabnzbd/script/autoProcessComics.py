import sys
import os.path
import urllib
import logging
if sys.version_info[0] < 3:
    import ConfigParser
    config = ConfigParser.ConfigParser()
    from urllib2 import urlopen
else:
    import configparser
    config = configparser.ConfigParser()
    from urllib.request import urlopen
try:
    import requests
    use_requests = True
except ImportError:
    print ("Requests module not found on system. I'll revert so this will work, but you probably should install ")
    print ("requests to bypass this in the future (ie. pip install requests)")
    use_requests = False

apc_version = "2.01"

logger = logging.getLogger('autoProcessComics')
fh = logging.FileHandler(r'C:\Mylar\post-processing\sabnzbd\script\autoProcessComics.log')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


def processEpisode(dirName, nzbName=None):
    print ("Your ComicRN.py script is outdated. I'll force this through, but Failed Download Handling and possible enhancements/fixes will not work and could cause errors.")
    return processIssue(dirName, nzbName)

'''
def addseries(**kwargs):
    logging.info('addseries')
    logging.info('kwargs: {}'.format(kwargs))
    params = {'cmd': 'addseries',
              'comicname': kwargs['comicname'],
              'comicid': kwargs['seriesid'],
              'filedir': kwargs['filedir'],
              'startyear': kwargs['startyear']}
    logging.info('Received: {}'.format(params))
    sendRequestToApi(params)
'''


def getseries(seriesid):
    logger.info("seriesid() with seriesid of {}".format(seriesid))
    params = {'cmd': 'getComic',
              'id': seriesid}
    logger.info('Looking for a comic with the id of {}'.format(seriesid))
    result = sendRequestToApi(params)
    if result.text.find("4050-" + seriesid) >= 0 or result.text.find("4000-" + seriesid) >= 0:
        return result
    else:
        return None


def addseries(comicname, startyear, seriesid, filedir):
    params = {'cmd': 'addseries',
              'comicname': comicname,
              'startyear': startyear,
              'comicid': seriesid,
              'filedir': filedir}
    logger.info('Received: {}'.format(params))
    if getseries(seriesid) is None:
        result = sendRequestToApi(params)


def processIssue(dirName, nzbName=None, failed=False, comicrn_version=None):
    apikey, url = getconfig()

    params = {'cmd': 'forceProcess',
              # 'apikey': apikey,
              'nzb_folder': dirName}

    if nzbName is not None:
        params['nzb_name'] = nzbName
    params['failed'] = failed

    params['apc_version'] = apc_version
    params['comicrn_version'] = comicrn_version
    result = sendRequestToApi(url, params)
    if "Post Process SUCCESSFUL" in result.text:
        return 0
    else:
        return 1


def sendRequestToApi(params):
    apikey, url = getconfig()
    params['apikey'] = apikey

    if use_requests is True:
        try:
            # logger.debug("Opening URL for post-process of %s @ %s/forceProcess:" % (params['nsb_name'], url))
            pp = requests.post(url, params=params, verify=False)
        except Exception as e:
            logger.debug("Unable to open URL: %s" % e)
            sys.exit(1)
        else:
            logger.info('statuscode: %s' % pp.status_code)
            logger.info(pp.text)
    else:
        url += "?" + urllib.urlencode(params)
        logger.debug("Opening URL: ", url)
        try:
            # urlObj = urllib2.urlopen(url)
            urlObj = urlopen(url)
        except IOError as e:
            logger.error("Unable to open URL: ", str(e))
            sys.exit(1)
        else:
            result = urlObj.readlines()
            for line in result:
                logger.info(line)

    return pp

def getconfig():
    # config = ConfigParser.ConfigParser()
    configFilename = os.path.join(os.path.dirname(sys.argv[0]), "autoProcessComics.cfg")
    logger.debug("Loading config from {}".format(configFilename))
    if not os.path.isfile(configFilename):
        logger.error("ERROR: You need an autoProcessComics.cfg file - did you rename and edit the .sample?")
        sys.exit(-1)
    try:
        fp = open(configFilename, "r")
        config.readfp(fp)
        fp.close()
    except IOError as e:
        logger.exception("Could not read configuration file: {}".format(str(e)))
        sys.exit(1)
    host = config.get("Mylar", "host")
    port = config.get("Mylar", "port")
    apikey = config.get("Mylar", "apikey")
    if apikey is None:
        logger.error("No ApiKey has been set within Mylar to allow this script to run. This is NEW. Generate an API within "
              "Mylar, and make sure to enter the apikey value into the autoProcessComics.cfg file before re-running.")
        sys.exit(1)
    try:
        ssl = int(config.get("Mylar", "ssl"))
    except (ConfigParser.NoOptionError, ValueError):
        ssl = 0
    try:
        web_root = config.get("Mylar", "web_root")
    except ConfigParser.NoOptionError:
        web_root = ""
    if ssl:
        protocol = "https://"
    else:
        protocol = "http://"
    url = protocol + host + ":" + port + web_root + '/api'
    return apikey, url
