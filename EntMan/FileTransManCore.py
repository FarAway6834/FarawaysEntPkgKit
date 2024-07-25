from tarfile import open as EntryFileOpener
from os.path import splitext as s
from abc import ABCMeta as abtractcls
from abc import abstractmethod as abstract
from json import load as l
from json import dump as d

o = open
w, getJ = (lambda f : o(f, 'w')), (lambda f : l(o(f)))
setJ = lambda f, x : d(x, o(f))

def wither(opener):
  def with_deco(func):
    def with_core(self, fn):
      with opener(fn) as fp:
        return func(fp)
    return with_core
  return with_deco

extdir = {
  'ent' : 'temp',
  'eo' : 'object'
}

zipedtype = 'tgz'

class ExtManagerInterface(metaclass = abtractcls):
  @abstract
  def __init__(self, filename, mode):
    pass
  
  @abstract
  def __enter__(self):
    pass
  
  @abstract
  def __exit__(self, a, b, c):
    pass

  @abstract
  def ext_all(self, where):
    pass

  @abstract
  def ext_thing(self, where, thing):
    pass

  @abstract
  def managements(self, objoption):
    pass

  class __ManagementClassLikeComponents(metaclass = abtractcls):
    @abstract
    def __init__(self, uppercls, option):
      pass

    @abstract
    def __enter__(self):
      pass

    @abstract
    def __exit__(self, a, b, c):
      pass

    @abstract
    def __onefile(self, option):
      pass

    @abstract
    def __morefile(self, where, thing):
      pass

    @abstract
    def __writes(self, option):
      pass

    @abstract
    def __reads(self, option):
      pass

    @abstract
    def __deletes(self, option):
      pass

    @abstract
    def __etcthings(self, option):
      pass