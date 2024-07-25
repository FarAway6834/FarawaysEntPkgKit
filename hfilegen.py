from json import load as l
from json import dump as d
from os.path import splitext as s
from os.path import join as j
from os.path import isfile as isf
from os.path import isdir as isd
from os.path import dirname as getdir
from os.path import abspath as getabs
from os import listdir as ls
from os import mkdir
from os import chdir as cd
from os import getcwd as pwd
from subprocess import run as r
from csv import DictReader as csvr
from sys import path as module_load_roots


def shs(x, logging=True):
  v = r(x, shell=True)
  if logging: print(v)


o, modo, mkcd, cdo = open, (lambda f, opener, mod: opener(f, mod)), (
    lambda x: (mkdir(x), cd(x))), (lambda: cd('..'))


def wither(opener):

  def with_deco(func):

    def with_core(fn):
      with opener(fn) as fp:
        return func(fn)

    return with_core

  return with_deco


class UnknownReteralError(Exception):
  pass


@wither(o)
def mytomlload(fp):  #*.mytoml
  ret = {}
  now = None
  iskbool = lambda x: x[0] == '[' and x[-1] == ']'
  isvbool = lambda x: x[0] == '\t'
  isvendbool = lambda x: x == ''
  for n, i in enumerate(fp.readlines()):
    if iskbool(i):
      now = i.strip()
      ret[now] = []
    elif isvbool(i):
      assert now != None, f'no key, but at {n} line is : {i}'
      ret[now].append(i[1:])
    elif isvendbool(i):
      assert now != None, f'no key, but at {n} line is : {i}'
      ret[now] = '\n'.join(ret[now])
      now = None
    else:
      raise UnknownReteralError(f'Unknown Reteral at {n} first, {i}')
  return ret


def mytomldumpcore(**data):

  @wither
  def mytomldumprealcore(fp):
    for i, j in data.items():
      fp.writelines(f'''\
[{}]
{}
'''.format(i, j))

  return mytomldumprealcore


def mytomldump(f, data):
  mytomldumpcore(**data)(f)


@wither(o)
def tsvloadscore(fp):
  yield from csvr(fp, delimiter='\t')


def tsvloads(f):
  ret = tsvloadscore(f)
  ret = (ret, next(ret))
  ret[0].close()
  return ret[1]


def modogen(mods):

  def openerget(opener):
    return lambda f: modo(f, opener, mods)


def modopenergetcore(opener=None, **types):
  return ({
      i: modogen(j)
      for i, j in types
  } if opener == None else {
      i: modogen(j)(opener)
      for i, j in types
  })


modlists, getJ = tsvloads('modlists.csv'), (lambda f: l(o(f)))


def modopenerget(opener=None):
  return modopenerget(opener=None, **modlists)


for i, j in modopenerget(o):
  globals()[f'o{i}'] = j

txtloader, txtdumper, setJ = wither(o)(
    (lambda f: f.read())), (lambda f, x: wither(ow)((lambda f: f.write(x)))
                            (f)), (lambda f, x: d(x, ow(f)))


def hfilegen_basic(f):
  fnt, ext = s(f)
  assert ext == '.myhc', TypeError(
      f'Only MyHCore file supports in hfilegen_basic, [file : {f}]')
  fn = f'{fnt}.h'
  fhn = fn.replace('.', '_').upper()
  fhn = f'_{fhn}'
  src = txtloader(f)
  txtdumper(f'''\
#ifndef {fhn}
# define {fhn}

{src}

#endif''')


readliner = wither(o)((lambda f: f.readlines()))


def formstrer(x, realform='#{} {}', coresrc='define'):
  return realform.format(coresrc, x)


def define_hfilegen_core(f, realform='#{} {}', coresrc='define'):
  yield from (formstrer(x, realform=realform, coresrc=coresrc)
              for i in readliner(f))


def define_hfilegen_writer(f, realform='#{} {}', coresrc='define'):

  def define_hfilegen_writer_core(fp):
    for i in define_hfilegen_core(f, realform=realform, coresrc=coresrc):
      fp.writelines(i)

  return define_hfilegen_writer_core


def define_hfilegen(f):
  fnt, ext = s(f)
  assert ext == '.domh', TypeError(
      f'Only Defs of MyH file supports in define_hfilegen, [file : {f}]')
  fn = f'domh{fnt}.myhc'
  wither(w)(define_hfilegen_writer(f))(fn)

def directdef_compile(x):
  y = x.split()
  y.append(y.pop())
  y.append(y[-1].upper())
  y.insert(0, y[-1])
  return ' '.join(y[:-2]) + f'\n{} {}'.format(*y[-2:])

@wither(o)
def lvdomh_compile(fp):
  for i in fp.readlines():
    yield directdef_compile(i)

def define_lowerver_hfilegen(f):
  fnt, ext = s(f)
  assert ext == '.lvdomh', TypeError(
      f'Only Defs of MyH file supports in define_hfilegen, [file : {f}]')
  fn = f'lv{fnt}.domh'
  txtdumper(fn, lvdomh_compile(f))

def includes_hfilegen(f):
  fnt, ext = s(f)
  assert ext == '.iomh', TypeError(
      f'Only Includes of MyH file supports in includes_hfilegen, [file : {f}]')
  fn = f'includer{fnt}.myhc'
  wither(w)(define_hfilegen_writer(f, coresrc='include'))(fn)


def std_includes_hfilegen(f):
  fnt, ext = s(f)
  assert ext == '.siomh', TypeError(
      f'Only std ionh file supports in std_includes_hfilegen, [file : {f}]')
  fn = f'std{fnt}.iomh'
  wither(w)(define_hfilegen_writer(f, formstrer='{}<{}>', coresrc=''))(fn)


def unstd_includes_hfilegen(f):
  fnt, ext = s(f)
  assert ext == '.xiomh', TypeError(
      f'Only unstd ionh file supports in unstd_includs_hfilegen, [file : {f}]')
  fn = f'unstd{fnt}.iomh'
  wither(w)(define_hfilegen_writer(f, formstrer='{}"{}"', coresrc=''))(fn)


def typeheaders_gen(f):
  fnt, ext = s(f)
  assert ext == '.thmh', TypeError(
      f'Only TypeHeader MyH file supports in typeheaders_gen, [file : {f}]')
  fn = f'types{fnt}.myhc'
  wither(w)(define_hfilegen_writer(f, realform = "{} {};", coresrc='typedef'))(fn)

def linextering(f):
  txtdumper(f'f2lned{f}.f2ln')(f)(txtloader(f).replace('\\', '\\\\').replace(
      'F2LN\n', 'F2LN\\n'))

def unlinextering(f):
  fnt, ext = s(f)
  assert ext == '.f2ln', TypeError(
      f"can't unlinextering, not linexter fike. [file : {f}]")
  fn = f'types{fnt}.myhc'
  txtdumper(f'{fn}')(f)(txtloader(f).replace('F2LN\\n',
                                             'F2LN\n').replace('\\\\', '\\'))


class NtypecheckMyhdirNchangesButTxtOnly:
  temp = j(getdir(getabs(__file__)), '.temp.{}')

  class libs:

    @staticmethod
    def movMydir(f):
      ret = pwd()
      if (cd(NtypecheckMyhdirNchangesButTxtOnly), ):
        ret = [f(), ret]
        cd(ret.pop())
      return ret.pop()

    @staticmethod
    def dirtrees(D):
      yield from (NtypecheckMyhdirNchangesButTxtOnly.libs.dirtrees(i)
                  if isd(i) else i for i in ls(D))

    @staticmethod
    def good_conditional_tree(i):
      return txtloader(i) if isinstance(
          i, str) else NtypecheckMyhdirNchangesButTxtOnly.libs.dirdict(i)

    @staticmethod
    def dirdict(D):
      return {
          i: NtypecheckMyhdirNchangesButTxtOnly.libs.good_conditional_tree
          for i in NtypecheckMyhdirNchangesButTxtOnly.libs.dirtrees(D)
      }

    @staticmethod
    def jsondirdump(**v):
      for i, j in v.items():
        if isinstance(j, dict):
          if mkcd(i):
            NtypecheckMyhdirNchangesButTxtOnly.libs.jsondirdump(**j)
            cdo()
        else:
          txtdumper(i, j)

  class jtft:

    @staticmethod
    def xing(x, y):
      setJ(y, NtypecheckMyhdirNchangesButTxtOnly.libs.dirdict(x))

    @staticmethod
    def unxing(x, y):
      ret = pwd()
      if mkcd(y):
        NtypecheckMyhdirNchangesButTxtOnly.libs.jsondirdump(**getJ(x))
        cd(ret)

  class x2y:

    @staticmethod
    def dirs(x, y):
      temp = NtypecheckMyhdirNchangesButTxtOnly.temp.format('jftf')
      NtypecheckMyhdirNchangesButTxtOnly.x2y.jtft(x, temp)
      NtypecheckMyhdirNchangesButTxtOnly.jtft.unxing(temp, y)

    @staticmethod
    def jtft(x, y):
      mytomldump(x, getJ(y))

  class y2x:

    @staticmethod
    def dirs(x, y):
      temp = NtypecheckMyhdirNchangesButTxtOnly.temp.format('jftf')
      NtypecheckMyhdirNchangesButTxtOnly.jtft.xing(y, temp)
      NtypecheckMyhdirNchangesButTxtOnly.y2x.jtft(x, temp)

    @staticmethod
    def jtft(x, y):
      setJ(y, mytomlload(x))


@NtypecheckMyhdirNchangesButTxtOnly.libs.movMydir
def myhd_compile(x, justcheck=False):
  I = len(module_load_roots)
  module_load_roots.append(pwd())
  if (cd(x), ):
    assert 'hfilegener.py' in ls(), f'NotMYHDir [{x}], no hfilegner.py'
    if not justcheck: shs('python hfilegener.py')
    cd(module_load_roots.pop(I))
