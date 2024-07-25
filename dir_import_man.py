from os.path import dirname as getdir
from os.path import abspath as getabs
from sys import path as module_root_paths

deapth = 0

def tempload(__file__data):
  '''
  listup module-import-root list
  
  when it runed, the directory is being temploaded root.
  and deapth is getting increased.
  so it need to free tempdump.
  it's works like a stack (temp-loaded dirs.)

  warning : don't use sys.path when useing tempload.
  '''
  global deapth
  module_root_paths.append(getdir(getabs(__file__data)))
  deapth += 1

def tempdump():
  global deapth
  module_root_paths.pop()
  deapth -= 1