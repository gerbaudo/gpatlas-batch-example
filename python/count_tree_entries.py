#!/bin/env python

import optparse

import ROOT as r
r.gROOT.SetBatch(True)                     # no windows popping up
r.PyConfig.IgnoreCommandLineOptions = True # don't let root steal our cmd-line options

def main():
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--input", help="list of root files")
    parser.add_option("-o", "--output", help="output root file")
    (options, args) = parser.parse_args()
    input = options.input
    output = options.output

    treeName = 'truth'
    chain = r.TChain(treeName)
    for l in open(input).readlines():
        l = l.strip()
        if l:
            chain.Add(l)
    print "Number of entries: %d"%chain.GetEntries()

if __name__=='__main__':
    main()
