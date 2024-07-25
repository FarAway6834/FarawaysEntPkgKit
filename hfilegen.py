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
  assert ext == '.myhc', TypeError(f'Only MyHCore file supports, [file : {f}]')
  fn = f'{fnt}.h'
  fhn = fn.replace('.', '_').upper()
  fhn = f'_{fhn}'
  src = txtloader(f)
  txtdumper(f'''\
#ifndef {fhn}
# define {fhn}

{src}

#endif''')
