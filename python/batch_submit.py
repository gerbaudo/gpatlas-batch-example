#!/bin/env python

# Submit jobs to the gpatlas queue
#
#
# davide.gerbaudo@gmail.com
# May 2014

import glob
import optparse
import os
import re
import subprocess


usage="""
This script expects several list of input root files in 'filelists/*.txt'.
You can generate the filelists for example with the following commands

find  /gdata/atlas/ucintprod/SusyNt/tmp_gerbaudo/mc12_8TeV.147771.Sherpa_CT10_Zmumu.merge.NTUP_TRUTH.e1434_p1032 -name "*root*" > filelist_all_mumu.txt
mkdir filelists
cd filelists
split -a 4 -d -l 100   ../filelist_all_mumu.txt mumu_
ls mumu_* | xargs -I %  mv % %.txt
cd ..
rm filelist_all_mumu.txt

Run with '--help' to get a list of options
"""
def main():
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-S", "--submit", action='store_true', default=False, help="submit jobs (default dry run)")
    parser.add_option("-v", "--verbose", action="store_true", default=False, help="print more details about what is going on")
    (options, args) = parser.parse_args()
    submit       = options.submit
    verbose      = options.verbose

    template = 'batch/templates/fill_trees.sh'
    batchdir = 'batch/fill_trees'
    outdir = 'out'
    logdir = 'log'
    if not os.path.exists(outdir) : os.makedirs(outdir)
    if not os.path.exists(logdir) : os.makedirs(logdir)

    inputLists = glob.glob('filelists/*.txt')
    for jobId, inputList in zip(extractJobIndices(inputLists), inputLists):
        outscript = batchdir+'/'+"job_%s.sh"%jobId
        outlog = logdir+'/'+"job_%s.log"%jobId
        fillTemplate(template, jobId, inputList, outscript)
        cmd = "qsub " \
              "-j oe -V " \
              "-N %(jobname)s " \
              "-o %(outlog)s " \
              " %(scripname)s" \
              % \
              {'jobname':jobId, 'outlog':outlog, 'scripname':outscript}
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

def fillTemplate(template, jobId, filelist, outscript):
    outFile = open(outscript, 'w')
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
        line = line.replace('${input_filelist}', filelist)
        line = line.replace('${out_file}', out_file)
        outFile.write(line)
    outFile.close()


#___________________________________________________________

if __name__=='__main__':
    main()
