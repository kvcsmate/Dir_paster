import configparser,os,stat
from shutil import copy2, Error,ignore_patterns, copystat
import pathlib
from datetime import datetime
configtype = 'config'
patterns_to_ignore = ['*.config']

def format(txt):
    txt.strip()
    for x in txt:
        if x == '\\':
            x = '/'

def include_patterns(*patterns):
    def _ignore_patterns(path, names):
        keep = set(name for pattern in patterns
                            for name in filter(names, pattern))
        ignore = set(name for name in names
                        if name not in keep and not os.path.isdir(os.path.join(path, name)))
        return ignore
    return _ignore_patterns

def make_old(path):
    path = path.split("/")
    path[-1] = path[-1]+ "/_old" + datetime.now().strftime("%Y%m%d%H%M%S")
    path = '/'.join(path)
    ##if not os.path.isdir(path):
      ##  os.mkdir(path)
    return path


def copytree_with_old(src,dst,oldsrc,symlinks=False,ignore=None,):
    _old = make_old(dst)
    copytree(dst,_old,ignore=ignore_patterns())
    os.chmod(dst, 0o777)
    copytree(src,dst,ignore=ignore_patterns())


def copytree(src, dst, symlinks = False, ignore = None):
  if not os.path.exists(dst):
    os.makedirs(dst)
    copystat(src, dst)
  lst = os.listdir(src)
  if ignore:
    excl = ignore(src, lst)
    lst = [x for x in lst if x not in excl]
  for item in lst:
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if symlinks and os.path.islink(s):
      if os.path.lexists(d):
        os.remove(d)
      os.symlink(os.readlink(s), d)
      try:
        st = os.lstat(s)
        mode = stat.S_IMODE(st.st_mode)
        os.lchmod(d, mode)
      except:
        pass # lchmod not available
    elif os.path.isdir(s):
        if not s.split("\\")[-1].startswith("_old"):
            copytree(s, d, symlinks, ignore)
    else:

        if os.path.isfile(d):
            os.chmod(d, 0o777)
        if not d.endswith(".config"):
            copy2(s, d)

config = configparser.RawConfigParser()
configFilePath = r'CaminoDir.config'
config.read(configFilePath)
copyfrom = pathlib.PureWindowsPath(config.get(configtype, 'copyfrom')).as_posix()
copyfrom = copyfrom.strip()
copyto = config.get(configtype,'copyto')
copyto = copyto.split(',')
##print(copyfrom)

for x in copyto:
    x = pathlib.PureWindowsPath(x).as_posix().strip()
    # copytree_multi(copyfrom, x, ignore=ignore_patterns(patterns_to_ignore)) ##'C:/Users/User/Desktop/copyfrom'
    try:
        print("Másolás "+ copyfrom +"-ból " + x + "-ba...")
        copytree_with_old(copyfrom, x,x, ignore=include_patterns())
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
#input("Press Enter to continue...")