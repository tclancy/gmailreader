import argparse
import csv
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


def get_bodies_from_label(label):
    logger.info("Opening mail in %s", label)
    all_mail = []
    mail_bodies = []
    try:
        all_mail = g.label(label).mail(prefetch=True)
    except AttributeError:
        logger.error("'%s' does not appear to be a valid label-- please check the spelling and case", label)
    for email in all_mail:
        logger.info("Reading %s", email.subject)
        body = email.body
        if body:
            mail_bodies.append(body)
    return mail_bodies


def write_counts_to_csv(bodies, filename):
    all_email_bodies = TextBlob(" ".join(bodies).decode("utf8"))
    interesting = {word: count for word, count in all_email_bodies.word_counts.items() if word not in stops}
    sorted_counts = sorted(interesting.items(), key=operator.itemgetter(1), reverse=True)
    filename = "%s.csv" % filename
    with open(filename, "wb") as f:
        logger.warn("Writing to %s", filename)
        writer = csv.writer(f)
        writer.writerow(["Word", "Count"])
        for word, count in sorted_counts:
            writer.writerow([word, count])

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

    for label in args.labels:
        mail_bodies += get_bodies_from_label(label)
    write_counts_to_csv(mail_bodies, "-".join(args.labels))
    g.logout()
