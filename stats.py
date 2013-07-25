"""A simple little script to plot the changes in the number of lines
   in a git repository over time
"""
import locale
import argparse
from subprocess import Popen, PIPE

from matplotlib import pyplot

def obtain_git_shortlog():
  command_string = "git log --shortstat --reverse --pretty=oneline"
  command = command_string.split()
  process = Popen (command, stdout=PIPE, stderr=PIPE)
  output, errorout = process.communicate()
  if process.returncode != 0:
    raise StandardError("Running git to obtain short log failed")
  encoding = locale.getdefaultlocale()[1]
  return output.decode(encoding)

def analyse_statistics():
  git_output = obtain_git_shortlog()

  file_lines = []
  for line in git_output.split("\n"):
    # The output alternates between commit messages with their identifier
    # first and a stastitics line for that commit. So the output looks
    # like:
    # d1f826cf06f4667d1ecafffa8afbddf6c80a73c2 Initial commit of the ...
    #  3 files changed, 35 insertions(+), 0 deletions(-)
    # 1b6534d2f55fdf132ab2cbf5b0999390b699cce2 Added the git ignore ...
    #  1 files changed, 1 insertions(+), 0 deletions(-)
    # In particular the file lines begin with a space. So that is how we
    # detect them. It might be that if someone uses a full-blown text
    # editor to edit their commit message then we can potentially get this
    # wrong. If that comes up then we will just have to be more
    # sophisticated about detecting commit statistics lines. 
    if line.startswith(" "):
      file_lines.append(line)
    

  number_of_lines = 0
  after_each_commit = []
  for line in file_lines:
    words = line.split()
    insertions = int(words[3])
    number_of_lines += insertions
    if len(words) > 5:
        deletions = int(words[5])
        number_of_lines -= deletions

    after_each_commit.append(number_of_lines)


  X = range(0,len(after_each_commit) + 1)
  Y = [0] + after_each_commit
   
  pyplot.plot( X, Y, '-' )
  pyplot.title( 'Plotting lines after commit' )
  pyplot.xlabel( 'commits' )
  pyplot.ylabel( 'lines of code' )
  # pyplot.savefig( 'Simple.png' )
  pyplot.show()
 

def run():
  """ The main method.  """ 
  analyse_statistics()
  

if __name__ == "__main__":
  run()
