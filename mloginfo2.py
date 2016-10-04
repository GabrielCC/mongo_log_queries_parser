#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
from mtools.mloginfo.mloginfo import MLogInfoTool
from query_section_revised import QuerySectionRevised


class MLogInfoTool2(MLogInfoTool):
    def __init__(self):
        super(MLogInfoTool2, self).__init__()
        self.sections.append(QuerySectionRevised(self))


def main():
    tool = MLogInfoTool2()
    tool.run()
    return 0  # we need to return an integer


if __name__ == '__main__':
    sys.exit(main())
