from shutil import run as r


def s(x, islogs=True):
  ret = r(x, shell=True)
  if islogs: print(ret)
  return ret


def pipscore(x,
             py='Python',
             pyv='3',
             pipv='3',
             ispy=False,
             ispipv=False,
             ispyv=False):
  pipvs, pyvs = (pipv if ispipv else ''), (pyv if ispyv else '')
  y = f'{py}{pyvs} -m ' if ispy else ''
  return y + f'pip{pipvs} {x}'


def pipscmdcore():

  def CMDinstall(x):
    return f'install {x}'

  yield CMDinstall

  def CMDdelete(x):
    return 'un' + CMDinstall(x)

  yield CMDdelete

  def CMDupgrade(x):
    return CMDinstall(f'--upgrade {x}')

  yield CMDupgrade

  def CMDUpdatePip(x, v='3', isv=False):
    vs = v if isv else ''
    return CMDupgrade(f'pip{vs}')

  yield CMDUpdatePip


def decorelambdagen(f):

  def core(f2):
    return lambda x: f(f2(x))

  return core


def mypipscore():
  yield from (i for i in map(decorelambdagen(pipscore), pipscmdcore()))


def mypipcores():
  yield from (i for i in map(decorelambdagen(s), mypipscore()))


_my_arr = mypipcores()
myinstall = next(_my_arr)
mydelete = next(_my_arr)
myupgrade = next(_my_arr)
mypipupdate = next(_my_arr)

def mixfunc(arrs, pipupdates):
  def gen(*n, is_first_pip_update = False):
    v = map((lambda x : arrs[x]), n)
    if is_first_pip_update:
      def core(x):
        pipupdates()
        for i in v: i(x)
    else:
      def core(x):
        for i in v: i(x)
    return core
  return gen

mymixfunc = fixfunc([myinstall, mydelete, myupgrade], mypipupdate)