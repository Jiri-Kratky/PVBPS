Aplikace:
HRA flappy bird, která musí používat openaiAPI
Použití AI pro vytvoření škodlivého kódu, který bude spuštěn u uživatele

Záměr malwaru: Keylogger

Omezení malware: jazyk systému: (pokud bude jazyk cs_CZ, tak spustí malware)
import locale
system_language, system_encoding = locale.getdefaultlocale()
print(f"Jazyk systému: {system_language}")

Dan:
Udělat DB – 
Data: textId | string(1024) 
Options: Interval (int), force_start(boolean)
Udělat API expres.js – Jen na POST dat a GET pro získání Options

Samuel:
Uložit kód, který vrátí GPT do programu „keylogger.py“. Pokud bude obsahovat nějaké balíčky (u keyloggeru to je myslím balíček „keyboard“, tak ho první nainstaluje pomocí subprocesů (když tak koukni na gpt, ono poradí) a následně spustí samotný program.
Hlavní úkol je rozparsovat odpověď od gpt na kód, který má uložit a balíčky, které má nainstalovat.
Toto vše by mělo být v jedné funkci „execute_malware“, abychom to mohli lehce připojit k naší hře.
Dále potřebujeme funkci „load_data“, která načte data ze souboru „temp.txt“ (soubor, kde se ukládají vstupy z klávesnice) a načtená data smaže ze souboru. Bude vracet string (načtená data)

Jirka:
Funkce pro odesílání dat prostřednictvím API do DB, příjem „nastavení“ z DB a přidání omezení systému na CZ.
