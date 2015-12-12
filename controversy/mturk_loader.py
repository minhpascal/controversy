# -*- coding: utf-8 -*-
import mturk
import querier
import os
import itertools
from error import UsageError
import sys


# source of terms --> http://arxiv.org/pdf/1409.8152v1.pdf
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

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        n_terms = sys.argv[2] if len(sys.argv) == 3 else 2
        terms = list(set(terms))[:n_terms]
        print('using %s training terms' % len(terms))
    elif sys.argv[1] in {'--help', 'help'}:
        print('''options:\n\t``test`` <-- uses small subset of training terms \n\t\t\tfor testing mturk\n\t```` <-- (no options) loads all training keywords\n\t``help`` or ``--help`` <-- displays this message\n''')
        sys.exit(0)

    n_tasks = len(terms)
    n_done = 0
    n_docs = 0
    for term in terms:
        update_progress(n_done, n_tasks)
        try:
            social = querier.perform(term, training=True)
        except UsageError:
            # no articles
            continue

        n_done += 1
        n_docs += mturk.new_doc(social)

    update_progress(n_done, n_tasks)
    print('\t... done')
    print('\t ... summary: %s doc(s) ready for training from %s terms' % (n_docs, n_tasks))
