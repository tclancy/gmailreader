import argparse
import gmail
import logging
from nltk.corpus import stopwords
import operator
import sys
from textblob import TextBlob

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
    mail_bodies = []
    try:
        stops = set(stopwords.words("english"))
    except LookupError:
        import nltk
        nltk.download("stopwords")
        logger.warn("Need to download NLTK data for stopwords. This should only happen the first time you run me.")
        stops = set(stopwords.words("english"))

    for lbl in args.labels:
        logger.info("Opening mail in %s", lbl)
        all_mail = []
        try:
            all_mail = g.label(lbl).mail(prefetch=True)
        except AttributeError:
            logger.error("'%s' does not appear to be a valid label", lbl)
        for email in all_mail:
            logger.info("Reading %s", email.subject)
            body = email.body
            if body:
                mail_bodies.append(body)
    all_email_bodies = TextBlob(" ".join(mail_bodies))
    interesting = {word: count for word, count in all_email_bodies.word_counts.items() if word not in stops}
    sorted_counts = sorted(interesting.items(), key=operator.itemgetter(1), reverse=True)
    print sorted_counts
    g.logout()
