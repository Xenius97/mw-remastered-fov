import ctypes as c
from ctypes import wintypes as w
import struct,time,sys,hashlib,subprocess,traceback,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Runtime FOV adjustment for the verified MWR 1.3 single-player executable. Requires Windows and 64-bit Python 3.9+.')
parser.add_argument('--fov',type=float,default=90.0,help='FOV between 65 and 110 (default: 90)')
parser.add_argument('--game-dir',type=Path,help='Game folder, if the game is not already running and is not beside this tool or one folder above it')
parser.add_argument('--test',action='store_true',help='Stop after 60 seconds')
args=parser.parse_args()
if not 65<=args.fov<=110: parser.error('--fov must be between 65 and 110')
if sys.platform!='win32' or struct.calcsize('P')!=8 or sys.version_info<(3,9):
 parser.error('Windows and 64-bit Python 3.9 or newer are required')
TARGET=args.fov
LOG=HERE/'FOV-runtime.log'
k=c.WinDLL('kernel32',use_last_error=True)
class PROCESS(c.Structure):
 _fields_=[('size',w.DWORD),('usage',w.DWORD),('pid',w.DWORD),('heap',c.c_size_t),('module',w.DWORD),('threads',w.DWORD),('parent',w.DWORD),('priority',w.LONG),('flags',w.DWORD),('name',w.WCHAR*260)]
class MODULE(c.Structure):
 _fields_=[('size',w.DWORD),('id',w.DWORD),('pid',w.DWORD),('globalUsage',w.DWORD),('processUsage',w.DWORD),('base',c.c_void_p),('length',w.DWORD),('handle',w.HMODULE),('name',w.WCHAR*256),('path',w.WCHAR*260)]
k.CreateToolhelp32Snapshot.argtypes=[w.DWORD,w.DWORD];k.CreateToolhelp32Snapshot.restype=w.HANDLE
k.Process32FirstW.argtypes=k.Process32NextW.argtypes=[w.HANDLE,c.POINTER(PROCESS)]
k.Module32FirstW.argtypes=[w.HANDLE,c.POINTER(MODULE)]
k.CloseHandle.argtypes=[w.HANDLE]
k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)]
k.GetExitCodeProcess.restype=w.BOOL
k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
k.ReadProcessMemory.argtypes=[w.HANDLE,c.c_void_p,c.c_void_p,c.c_size_t,c.POINTER(c.c_size_t)];k.ReadProcessMemory.restype=w.BOOL
k.WriteProcessMemory.argtypes=k.ReadProcessMemory.argtypes;k.WriteProcessMemory.restype=w.BOOL

def log(s):
 print(s,flush=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(time.strftime('%H:%M:%S ')+s+'\n')
def process():
 snap=k.CreateToolhelp32Snapshot(2,0)
 try:
  p=PROCESS();p.size=c.sizeof(p);ok=k.Process32FirstW(snap,c.byref(p))
  while ok:
   if p.name.lower()=='h1_sp64_ship.exe':return p.pid
   ok=k.Process32NextW(snap,c.byref(p))
 finally:k.CloseHandle(snap)
 return None
def read(h,a,n):
 buf=c.create_string_buffer(n);got=c.c_size_t()
 if not k.ReadProcessMemory(h,a,buf,n,c.byref(got)) or got.value!=n:raise OSError(c.get_last_error(),'ReadProcessMemory '+hex(a))
 return buf.raw

def main():
 LOG.write_text('',encoding='utf-8')
 log(f'MWR 1.3 - FOV {TARGET:g}. CTRL+C: stop. EXE is not changed.')
 if not c.windll.shell32.IsUserAnAdmin():raise RuntimeError('Run this launcher as administrator: the game requires it.')
 pid=process()
 if not pid:
  candidates=[args.game_dir.resolve()] if args.game_dir else [HERE,HERE.parent]
  exe=next((folder/'h1_sp64_ship.exe' for folder in candidates if (folder/'h1_sp64_ship.exe').is_file()),None)
  if exe is None:raise RuntimeError('Start the campaign first, place this tool beside the game EXE (or in a subfolder), or use --game-dir "D:\\Games\\MWR".')
  log('Starting game: '+str(exe));subprocess.Popen([str(exe)],cwd=str(exe.parent))
  for _ in range(120):
   time.sleep(.5);pid=process()
   if pid:break
 if not pid:raise RuntimeError('Game process not found.')
 snap=k.CreateToolhelp32Snapshot(0x18,pid)
 try:
  m=MODULE();m.size=c.sizeof(m)
  if not k.Module32FirstW(snap,c.byref(m)):raise OSError(c.get_last_error(),'Cannot inspect game module')
  base=m.base;path=Path(m.path)
 finally:k.CloseHandle(snap)
 if args.game_dir and path.parent.resolve()!=args.game_dir.resolve():raise RuntimeError('The running game is not in --game-dir: '+str(path))
 log('Game: '+str(path))
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest not in {'f89c09864b88ef09bcceeebc1cdd7dcd19adeaf073ff464b1cc186e667f77cb5','d150b4414edcde81c9eed844ac232326d46cf4cd0ebb155506a80b3687b48702'}:raise RuntimeError('Unsupported executable; no memory writes performed.')
 h=k.OpenProcess(0x438,False,pid)
 if not h:raise OSError(c.get_last_error(),'OpenProcess')
 try:
  code=read(h,base+0x139d93,24)
  if code[:8]!=bytes.fromhex('f30f103df9da5900') or code[19:24]!=bytes.fromhex('b9c7b27285'):raise RuntimeError('Runtime code does not match verified version.')
  log('Attached PID '+str(pid)+' base '+hex(base))
  end=time.monotonic()+60 if args.test else float('inf')
  last=None;writes=0;initialized=False
  while time.monotonic()<end:
   status=w.DWORD()
   if not k.GetExitCodeProcess(h,c.byref(status)) or status.value!=259:
    log('Game closed.');break
   ptr=struct.unpack('<Q',read(h,base+0x2261718,8))[0]
   if not ptr:
    time.sleep(.1);continue
   raw=read(h,ptr,96);dvhash=struct.unpack_from('<I',raw)[0]
   if dvhash!=0x8572b2c7 or raw[8] not in (1,11):raise RuntimeError('FOV pointer validation failed; no further writes.')
   current,latched,reset=[struct.unpack_from('<f',raw,o)[0] for o in (16,32,48)]
   state=(current,latched,reset)
   if state!=last:log('cg_fov current/latched/default: '+str(state));last=state
   if not initialized:
    for label,rva in [('other FOV',0x2261720),('FOV scale',0x2261730)]:
     q=struct.unpack('<Q',read(h,base+rva,8))[0]
     if q:log(label+': '+str(struct.unpack('<f',read(h,q+16,4))[0]))
    initialized=True
   for off,val in zip((16,32,48),state):
    if not 1<=val<=180:raise RuntimeError('Unexpected FOV value; stopping.')
    if abs(val-TARGET)>.001:
     data=c.create_string_buffer(struct.pack('<f',TARGET));got=c.c_size_t()
     if not k.WriteProcessMemory(h,ptr+off,data,4,c.byref(got)) or got.value!=4:raise OSError(c.get_last_error(),'WriteProcessMemory')
     if struct.unpack('<f',read(h,ptr+off,4))[0]!=TARGET:raise RuntimeError('FOV write verification failed')
     writes+=1
   time.sleep(.05)
  log('Test complete. Verified FOV writes: '+str(writes))
 finally:k.CloseHandle(h)
if __name__=='__main__':
 if not c.windll.shell32.IsUserAnAdmin():
  result=c.windll.shell32.ShellExecuteW(None,'runas',sys.executable,subprocess.list2cmdline([str(Path(__file__).resolve()),*sys.argv[1:]]),str(Path(__file__).parent),1)
  if result<=32: input('Administrator permission was not granted. Press ENTER...')
  sys.exit(0)
 try:main()
 except KeyboardInterrupt:log('Stopped.')
 except Exception:log(traceback.format_exc());input('Press ENTER to close...')
