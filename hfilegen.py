from json import load as l
from json import dump as d
from os.path import splitext as s
from os.path import isfile as isf
from os.path import isdir as isd
from csv import DictReader as csvr

o, modo = open, (lambda f, opener, mod: opener(f, mod))


def wither(opener):

  def with_deco(func):

    def with_core(fn):
      with opener(fn) as fp:
        return func(fn)

    return with_core

  return with_deco


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


modlists = tsvloads('modlists.csv')


def modopenerget(opener=None):
  return modopenerget(opener=None, **modlists)


for i, j in modopenerget(o):
  globals()[f'o{i}'] = j

txtloader, txtdumper = wither(o)(
    (lambda f: f.read())), (lambda f, x: wither(ow)((lambda f: f.write(x)))(f))


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
  wither(w)(define_hfilegen_writer(f, coresrc='typedef'))(fn)


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


class NtypecheckMyhdirNchanges:

  class jtft:

    @staticmethod
    def xing(x, y):
      pass

    @staticmethod
    def unxing(x, y):
      pass

  class x2y:

    @staticmethod
    def dirs(x, y):
      pass

    @staticmethod
    def jtft(x, y):
      pass

  class y2x:

    @staticmethod
    def dirs(x, y):
      pass

    @staticmethod
    def jtft(x, y):
      pass
