import os

import resend
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def db(query):
    url_engine = os.environ["URL_ENGINE"]
    engine = create_engine("postgresql://postgres:139540@localhost:5433/lapalank")
    with engine.connect() as con:
        rs = con.execute(text(query))
    return rs


def generar_recordatorio(usuario):
    """Genera un recordatorio de estudio usando la API de llama3.

    Toma en cuenta el estado de la ruta del usuario.
    """
    ruta = usuario[2]
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Genera un diccionario que contenga la llave asunto con el asunto y la llave contenido con el cuerpo de un recordatorio de no mas de 200 caracteres, segun el primer tema no estudiado de la ruta. Solo devuelve el diccionario, no escribas mas nada, hazlo en espanol solo espanol ningun otro lenguaje"
            },
            {
                "role": "user",
                "content": f"{ruta}"
            }
        ],
        model="llama3-8b-8192",
        temperature=0.01,
        max_tokens=1000,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content


def enviar_recordatorio(usuario):
    recordatorio = eval(generar_recordatorio(usuario))
    resend.api_key = os.environ["RESEND_API_KEY"]
    params = {
        "from": "Hackathon <hackathon@automated.scidroid.co>",
        "to": [usuario[1]],
        "subject": recordatorio['asunto'],
        "html": recordatorio['contenido'],
    }

    email = resend.Emails.send(params)


if __name__ == '__main__':
    load_dotenv()
    client = Groq()

    rs = db("SELECT * FROM usuarios WHERE periodicidad='Diario'")
    for usuario in rs:
        enviar_recordatorio(usuario)
