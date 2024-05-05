from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()
def llamar(text):
    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "dadas estas skills y el rol deseado dame una ruta de aprendizaje con el siguiente formato en una lista de python[{'tema':'tema1', 'estudiado': False},{'tema':'tema2', 'estudiado': False}]ordenalas en orden de aprendizaje recomendadomarca como true las habilidades que ya tenga, recuerda generar todas las respuestas en español, ademas recueda solo generar la lista"
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": f"{text}",
            }
        ],

        # The language model which will generate the completion.
        model="llama3-8b-8192",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1000,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    return chat_completion.choices[0].message.content
