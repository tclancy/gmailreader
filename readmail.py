import argparse
import gmail
import logging
import sys

# TODO: set to WARN by default once done with development
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("Gmail Reader")

try:
    from credentials import username, password
except ImportError:
    logger.error(
        "You need to create a file named 'credentials.py' in this folder with two variables: username and password")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("labels", nargs="*")
    parser.add_argument("-v", dest="verbose", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logger.level = logging.DEBUG
    g = gmail.login(username, password)
    for lbl in args.labels:
        logger.info("Opening mail in %s", lbl)
        try:
            print g.label(lbl).mail()
        except AttributeError:
            logger.error("'%s' does not appear to be a valid label", lbl)
