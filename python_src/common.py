import sys
import threading
from random import randint
import ctypes
from hashlib import sha3_256
from os.path import join
from datetime import datetime
import pathlib
from importlib.machinery import SourceFileLoader


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
        path1 = join(root, 'drives', drive, 'libs')
        path2 = join(root, 'drives', drive, pathlib.Path(file).parent)
        try:
            sys.path.extend([path1, path2])
            module = SourceFileLoader(pathlib.Path(file).name, path2).load_module()
            module.main()
        except Exception as e:
            date = datetime.now().isoformat().replace(':', '-').replace(' ', '_')
            with open(join(root, 'drives', drive, 'logs', f"crash_{date}.txt"),
                      'w') as f:
                f.write(f"Error while executing '{file}' at {date}: \n{str(e)}")
        finally:
            if path1 in sys.path:
                sys.path.remove(path1)
            if path1 in sys.path:
                sys.path.remove(path2)

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
        if (thread.name.split(',')[2] == drive) or (drive is None):
            if thread.isAlive():
                exc = ctypes.py_object(KeyboardInterrupt)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
                if res > 1:
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
                    raise SystemError(f"PyThreadState_SetAsyncExc failed on thread '{thread.ident}' during 'killall'")
