#!/bin/env python

# Submit jobs to the gpatlas queue
#
#
# davide.gerbaudo@gmail.com
# May 2014

import optparse
import os
import re
import subprocess


usage="""
This script expects several list of input root files in 'filelists/*.txt'.
Run with '--help' to get a list of options
"""
def main():
    parser = optparse.OptionParser()
    parser.add_option("-S", "--submit", action='store_true', default=False, help="submit jobs (default dry run)")
    parser.add_option("-v", "--verbose", action="store_true", default=False, help="print more details about what is going on")
    (options, args) = parser.parse_args()
    submit       = options.submit
    verbose      = options.verbose

    template = 'batch/templates/fill_trees.sh'
    batchdir = 'batch/fill_trees'
    outdir = 'out'
    logdir = 'log'

    inputLists = glob.glob('filelists/*.txt')
    for jobId, inputList in zip(extractJobIndices(inputLists), inputLists):
        outscript = batchdir+'/'+"job%s.sh"%jobId
        fillTemplate(template, jobId, outscript)
        cmd = "qsub " \
              "-j oe -V " \
              "-N %(jobname)s " \
              "-o %(outlog)s " \
              " %(scripname)s" \
              % \
              {'jobname':jobId, 'outlog':outlog, 'scripname':script}
    print cmd
    if submit :
        out = getCommandOutput(cmd)
        if verbose : print out['stdout']
    else : print "This was a dry run; use '--submit' to actually submit the jobs"

#___________________________________________________________

def getCommandOutput(command):
    "lifted from supy (https://github.com/elaird/supy/blob/master/utils/io.py)"
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout,stderr = p.communicate()
    return {"stdout":stdout, "stderr":stderr, "returncode":p.returncode}

def commonPrefix(aList) : return os.path.commonprefix(aList)
def commonSuffix(aList) : return os.path.commonprefix([l[::-1] for l in aList])[::-1]

def extractJobIndices(inputFiles=[], verbose=False):
    inputFiles = [f for f in inputFiles if f] # drop empty elements
    prefix = commonPrefix(inputFiles)
    suffix = commonSuffix(inputFiles)
    if verbose:
        print "extractJobIndices: prefix '%s', suffix '%s'"%(prefix, suffix)
    return [f.replace(prefix, '').replace(suffix, '') for f in inputFiles]

def fillTemplate(template, jobId, outscript):
    outFile = open(outScript, 'w')
    base_dir = os.getcwd()
    dest_dir = base_dir+'/out'
    out_file = jobId+'.root'
    scratch_dir = '/scratch/asoffa/'+jobId # local scratch on the cluser node
    if not os.path.exists(dest_dir) : os.makedirs(dest_dir) 
    for line in open(template).readlines() :
        line = line.replace('${job_number}', jobId)
        line = line.replace('${base_dir}', base_dir)
        line = line.replace('${dest_dir}', dest_dir)
        line = line.replace('${scratch_dir}', scratch_dir)
        outFile.write(line)
    outFile.close()


#___________________________________________________________

if __name__=='__main__':
    main()
