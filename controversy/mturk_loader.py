# -*- coding: utf-8 -*-
import mturk
import querier
import os
import itertools
from error import UsageError
import sys


# http://arxiv.org/pdf/1409.8152v1.pdf <== source of terms
TT_DIR = 'training_terms'


def get_file(name):
    with open(name, 'r') as f:
        data = f.readlines()
    return data


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
            terms = list(set(terms))[:5]
        elif sys.argv[1] in {'--help', 'help'}:
            print('''options:\n\t``test`` <== uses small subset of training terms \n\t\t\tfor testing mturk\n\t```` <== (no options) loads all training keywords\n\t``help`` or ``--help`` <== displays this message\n''')
            sys.exit(0)

    n_tasks = len(terms)
    n_done = 0
    n_docs = 0
    for term in terms:
        update_progress(n_done, n_tasks)
        try:
            scored_keyword = querier.perform(term, sentis=True)
        except UsageError:
            # no articles
            continue

        n_done += 1
        n_docs += mturk.new_doc(scored_keyword)

    update_progress(n_done, n_tasks)
    print('\t... done')
    print('\t ... summary: %s doc(s) ready for training' % n_docs)
