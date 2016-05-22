# -*- coding: utf-8 -*-
import mturk
import querier
import os
import itertools
from error import UsageError
import sys
import twilio
from twilio.rest import TwilioRestClient
from flask import jsonify
from error import UsageError
from config import ADMIN_PHONE, TWILIO_SID, TWILIO_AUTH_TOKEN


# source of terms --> http://arxiv.org/pdf/1409.8152v1.pdf
TT_DIR = 'training_terms'
HELP_STR = 'options:\n\t``test`` <-- uses small subset of training terms \n\t\t\tfor testing mturk\n\t```` <-- (no options) loads all training keywords\n\t``help`` or ``--help`` <-- displays this message\n'


def sms_admin(m):
    client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=m,
                           to=ADMIN_PHONE,
                           from_='+19085437718')

def get_file(name):
    with open(name, 'r') as f:
        data = f.readlines()
    return map(lambda x: x.strip(), data)


def update_progress(n_done, n_tasks):
    pprogress = int(100 * (float(n_done) / n_tasks))
    sys.stdout.write('\r working ... [ %s ] %s%%' 
                     % ('#' * (pprogress / 5), pprogress))
    sys.stdout.flush()


if __name__ == '__main__':
    terms_by_file = map(lambda x: get_file('%s/%s' % (TT_DIR, x)),
                        filter(lambda x: x.endswith('.txt'),
                               os.listdir(TT_DIR)))
    terms = list(itertools.chain(*terms_by_file))

    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            n_terms = sys.argv[2] if len(sys.argv) == 3 else 2
            terms = list(set(terms))[:n_terms]
            print('using %s training terms' % len(terms))
        elif sys.argv[1] in {'--help', 'help'}:
            print(HELP_STR)
            sys.exit(0)

    print('running ... this could take a while')

    n_tasks = len(terms)
    n_done = 0
    n_docs = 0
    n_dup_keywords = 0
    for term in terms:
        if mturk.keyword_exists(term):
            n_dup_keywords += 1
            continue

        try:
            social = querier.perform(term, training=True)
        except UsageError:
            # no articles
            continue

        col = mturk.get_articles_collection()
        social['result']['articles'] = filter(lambda x: mturk.article_is_new(x['url']),
                                              social['result']['articles'])
        n_docs += mturk.new_doc(social)
        n_done += 1

        update_progress(n_done, n_tasks)

    print('\t... done')
    summary = 'summary: %s doc(s) ready for training from %s terms (%s skipped)' % (n_docs, n_tasks, n_dup_keywords)
    sms_admin('mturk_loader finished. %s' % summary)
    print('\t ...' % summary)
