from FileTransManCores import *

class MyExter(ExtManagerInterface):
  def __init__(self, filename, mode):
    self.__fn = filename

  @wither((lambda f : EntryFileOpener(f, mode = 'r:gz')))
  def __ext_all_opener(self, fp):
    return fp.extractall(path = self.__where)

  def ext_all(self, where):
    self.__where = where
    return self.__ext_all_opener(self.__fn)