from mtools.mloginfo.sections.base_section import BaseSection

from mtools.util.grouping import Grouping
from mtools.util.print_table import print_table
from mtools.util import OrderedDict

from operator import itemgetter
from collections import namedtuple

try:
    import numpy as np
except ImportError:
    np = None

LogTuple = namedtuple('LogTuple', ['db', 'collection', 'nscanned', 'ntoreturn', 'writeConflicts',
                                   'operation', 'pattern', 'duration', 'sort_pattern'])


def op_or_cmd(le):
    return le.operation if le.operation != 'command' else le.command


class QuerySectionRevised(BaseSection):
    """
    """

    name = "queries2"

    def __init__(self, mloginfo):
        BaseSection.__init__(self, mloginfo)

        # add --queries flag to argparser
        self.mloginfo.argparser_sectiongroup.add_argument('--queries2', action='store_true',
                                                          help='outputs statistics about query patterns')

    @property
    def active(self):
        """ return boolean if this section is active. """
        return self.mloginfo.args['queries2']

    def run(self):
        """ run this section and print out information. """
        grouping = Grouping(group_by=lambda x: (x.collection, x.operation, x.pattern, x.sort_pattern))
        logfile = self.mloginfo.logfile

        if logfile.start and logfile.end:
            progress_start = self.mloginfo._datetime_to_epoch(logfile.start)
            progress_total = self.mloginfo._datetime_to_epoch(logfile.end) - progress_start
        else:
            self.mloginfo.progress_bar_enabled = False

        for i, le in enumerate(logfile):
            # update progress bar every 1000 lines
            if self.mloginfo.progress_bar_enabled and (i % 1000 == 0):
                if le.datetime:
                    progress_curr = self.mloginfo._datetime_to_epoch(le.datetime)
                    self.mloginfo.update_progress(float(progress_curr - progress_start) / progress_total)

            if le.operation in ['query', 'getmore', 'update', 'remove'] or le.command in ['count', 'findandmodify',
                                                                                          'geonear']:
                db, collection = le.namespace.split(".")
                lt = LogTuple(
                    db=db, collection=collection, nscanned=le.nscanned, ntoreturn=le.ntoreturn,
                    writeConflicts=le.writeConflicts, operation=op_or_cmd(le),
                    pattern=le.pattern, duration=le.duration, sort_pattern=le.sort_pattern)
                grouping.add(lt)

        grouping.sort_by_size(group_limit=30)

        # clear progress bar again
        if self.mloginfo.progress_bar_enabled:
            self.mloginfo.update_progress(1.0)

        # no queries in the log file
        if len(grouping) < 1:
            print 'no queries found.'
            return

        titles = ['collection', 'operation', 'pattern', 'sort_pattern', 'count', 'mean (ms)', 'sum (mins)']
        table_rows = []

        for g in grouping:
            # calculate statistics for this group
            try:
                collection, op, pattern, sort_pattern = g
            except:
                collection, op, pattern, sort_pattern = ['others', 'others', 'others', 'others']

            group_events = [le.duration for le in grouping[g] if le.duration != None]

            stats = OrderedDict()
            stats['collection'] = collection
            stats['operation'] = op
            stats['pattern'] = pattern
            stats['sort_pattern'] = sort_pattern
            stats['count'] = len(group_events)
            stats['mean'] = 0

            stats['sum'] = sum(group_events) if group_events else '-'
            stats['mean'] = stats['sum'] / stats['count'] if group_events else '-'
            stats['sum'] = round(stats['sum'] / 1000.0 / 60, 2) if group_events else '-'

            if self.mloginfo.args['verbose']:
                stats['example'] = grouping[g][0]
                titles.append('example')

            table_rows.append(stats)

        # sort order depending on field names
        reverse = True
        if self.mloginfo.args['sort'] in ['namespace', 'pattern']:
            reverse = False

        table_rows = sorted(table_rows, key=itemgetter(self.mloginfo.args['sort']), reverse=reverse)
        print_table(table_rows, titles, uppercase_headers=False)
        print
