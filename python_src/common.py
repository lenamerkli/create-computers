import sys
import threading
from random import randint
import ctypes
from hashlib import sha3_256
from os.path import join
from os import listdir
from datetime import datetime
import pathlib
import importlib.util
import traceback


class CCThread:

    def __init__(self, root: str, thread_id: int = None, file: str = None, drive: str = None):
        if thread_id is None:
            thread_id = randint(1_000_000, 9_999_999)
        self._thread_id = thread_id
        self._thread_name = f"CC,{thread_id},{drive},{file}"
        self._thread = None
        self._file = None
        self._root = root
        for thread in threading.enumerate():
            if len(thread.name.split(',')) == 4:
                if thread.name.split(',')[1] == self._thread_name.split(',')[1]:
                    self.thread = thread
                    self._file = thread.name.split(',')[3]
                    self._drive = thread.name.split(',')[2]
                    break
        if self._thread is None:
            self._file = file
            self._drive = drive
            if None in [self._file, self._drive, self._root]:
                raise ValueError()
            self._thread = threading.Thread(name=self._thread_name, target=self._run, args=(file, drive, root))

    @staticmethod
    def _run(file, drive, root):
        path1 = join(root, 'libs', 'libs')
        path2 = join(root, 'drives', drive, str(pathlib.Path(file).parent.absolute())[1:])
        path3 = join(root, 'drives', drive, file[1:])
        path4 = join(root, 'drives', drive, 'modules')
        try:
            sys.path.extend([path1, path2])
            modname = pathlib.Path(file).name
            spec = importlib.util.spec_from_file_location(modname, path3)
            module = importlib.util.module_from_spec(spec)
            sys.modules[modname] = module
            spec.loader.exec_module(module)
            module.main()
        except Exception as e:
            date = datetime.now().isoformat().replace(':', '-').replace(' ', '_')
            with open(join(root, 'drives', drive, 'logs', f"crash_{date}.txt"),
                      'w') as f:
                exc = '\n'.join(traceback.format_exception(type(e), e, e.__traceback__))
                f.write(f"Error while executing '{file}' at {date}: \n{exc}")
        finally:
            if path1 in sys.path:
                sys.path.remove(path1)
            if path2 in sys.path:
                sys.path.remove(path2)
            if path3 in sys.path:
                sys.path.remove(path3)
            if path4 in sys.path:
                sys.path.remove(path4)

    def get_id(self):
        return self._thread_id

    def interrupt(self):
        if self._thread.isAlive():
            exc = ctypes.py_object(KeyboardInterrupt)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._thread.ident), exc)
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self._thread.ident, None)
                raise SystemError(f"PyThreadState_SetAsyncExc failed on thread '{self._thread_id}'")

    def run(self):
        self._thread.run()


def fast_hash(data):
    h = sha3_256()
    h.update(data)
    return h.hexdigest()[:12]


def kill_all(drive=None):
    for thread in threading.enumerate():
        if len(thread.name.split(',')) == 4:
            if (thread.name.split(',')[2] == drive) or (drive is None):
                if thread.isAlive():
                    exc = ctypes.py_object(KeyboardInterrupt)
                    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
                    if res > 1:
                        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
                        raise SystemError(
                            f"PyThreadState_SetAsyncExc failed on thread '{thread.ident}' during 'killall'")


def run_hook(root, drive, hook):
    root_path = join(root, 'drives', drive, 'hooks', hook)
    files = listdir(root_path)
    for file in files:
        if file.endswith('.py'):
            c = CCThread(root=root, file=join('hooks', hook, file), drive=drive)
            c.run()
