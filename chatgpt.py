import gradio as gr
import openai

openai.api_key = open("key.txt", "r").read().strip("\n")

message_history = [{"role": "user",
                    "content": f"Dein Name ist \"Ki1i-Bot\" und du bist ein Chatbot. Sag OK wenn du das verstanden hast."},
                   {"role": "assistant", "content": f"OK"}]


def predict(input):
    # den neuen Eingabesatz tokenisieren und an die Nachrichtenhistorie anhängen
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 10x billiger als Davinci, und besser. 0,002 $ pro 1k Token
        messages=None
    )
    # Just the reply:
    reply_content = completion.choices[0].message.content  # .replace('```python', '<pre>').replace('```', '</pre>')

    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # erhalte Paare von  msg["content"] der Nachrichtenhistorie, überspringe des pre-prompt:              hier.
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                range(2, len(message_history) - 1, 2)]  # convert to tuples of list
    return response


# erstellt eine neue Blocks-App und ordnet sie der Variablen demo zu.
with gr.Blocks() as demo:
    # erstellt eine neue Chatbot-Instanz und weist sie der Variablen chatbot zu.
    chatbot = gr.Chatbot()

    # erstellt eine neue Komponente Row, die einen Container für andere Komponenten darstellt.
    with gr.Row():
        '''erstellt eine neue Textbox-Komponente, die zur Erfassung von Benutzereingaben verwendet wird. Der 
        Parameter show_label wird auf False gesetzt, um die Beschriftung auszublenden, und der Parameter placeholder 
        wird auf "Enter text and press enter" gesetzt, um einen Platzhaltertext in der Textbox anzuzeigen. Die 
        Methode style wird verwendet, um die Eigenschaften der Textbox zu ändern. Der Parameter container wird auf 
        False gesetzt, um die Textbox ohne Rahmen anzuzeigen.'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''Aktion der Textbox an die Vorhersagefunktion übergeben,  die als Argumente die Eingabe aus der Textbox, 
    die Chatbot-Instanz und die Zustandsinstanz als Argumente nimmt. Diese Funktion verarbeitet die Eingabe und 
    erzeugt eine Antwort des Chatbots, die im Ausgabebereich angezeigt wird.'''
    txt.submit(predict, txt, chatbot)  # submit(function, input, output)
    # txt.submit(lambda :"", None, txt)  #Setzt die Absendeaktion auf eine Lambda-Funktion, die einen leeren String
    # zurückgibt

    '''setzt die Submit-Aktion der Textbox auf eine JavaScript-Funktion, die einen leeren String zurückgibt. Diese 
    Zeile entspricht der auskommentierten Zeile oben, verwendet aber eine andere Implementierung.  Der Parameter _js 
    wird verwendet, um eine JavaScript-Funktion an die Submit-Methode zu übergeben. Die JavaScript-Funktion wird in 
    der Methode submit ausgeführt, wenn der Benutzer die Eingabetaste drückt. Die JavaScript-Funktion muss einen 
    leeren String zurückgeben, um die Eingabe aus der Textbox zu löschen.'''
    txt.submit(None, None, txt,
               _js="() => {''}")  # Keine Funktion, keine Eingabe in diese Funktion, die Submit-Aktion für das
    # Textfeld ist eine js-Funktion, die einen leeren String zurückgibt, also wird sie sofort gelöscht.

demo.launch(share=True)
