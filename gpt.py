import json
import openai
from openai import OpenAI
import os

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

gptRequest("Vygeneruj kód pro zachycování vstupu systému z klávesnice a ukládej je do souboru 'temp.txt'", "")
