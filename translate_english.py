import io
import time
import openai

import deepl
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont("Abhaya", "/Users/bartoszkobylinski/Programming/Python/anki/AbhayaLibre-Regular.ttf"))

AUTH_KEY = "aaa"
translator = deepl.Translator(AUTH_KEY)


def check_translation_with_chatgpt(phrase, api_key):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a professional translator from English to Polish, specializing in B1 level translations. You receive phrases to validate, such as:
dislike (verb) - niechęć, czasownik
Your task is to determine if the translation provided aligns with the most commonly used translation at the B1 level.
If the translation is correct, your response should be formatted as follows:
{"answer": "ok"}
If the translation is incorrect, provide the most frequently used translation at the B1 level in the following format:
{"word":"correct translation"}
Please ensure your response strictly follows the given JSON format. Always provide your answer using this structure. In cases where multiple translations are acceptable, your priority is to choose the most popular one."""
             },
            {"role": "user", "content": phrase}
        ]
    )
    print(response.choices[0].message)


abbreviation_mapping = {
    "(adj)": "(adjective)",
    "(n)": "(noun)",
    "(adv)": "(adverb)",
    "(v)": "(verb)",
    "(n & v)": "(noun and verb)",
    "(av & v)": "(adverb and verb)",
    "(adj, adv & n)": "(adjective, adverb and noun)",
    "(prep,  conj)": "(preposition and conjunction)",
    "(adv, det & pron)": "(adverb, determiner and pronoun)",
    "(adverb and verb)": "(adverb and verb)",
    "(phr v)": "(phrasal verb)",
    "(noun and verb)": "(noun and verb)",
}

grammar_mapping = {
    '(noun)': 'rzeczownik',
    '(verb)': 'czasownik',
    '(adjective)': 'przymiotnik',
    '(prep)': 'przyimek',
    '(conj)': 'spójnik',
    '(adv)': 'przysłówek',
    '(det)': 'określnik',
    '(pron)': 'zaimek'
}


def process_page_text(text):
    for abbr, full in abbreviation_mapping.items():
        text = text.replace(abbr, full)
    return text


with open("/Users/bartoszkobylinski/Downloads/b1_words.pdf", "rb") as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    print(f"total pages:{len(pdf_reader.pages)}")

    full_text = ""
    pdf_writer = PyPDF2.PdfWriter()

    for i in range(18, 20):
        page = pdf_reader.pages[i]
        page_text = page.extract_text()
        processed_text = process_page_text(page_text)
        full_text += processed_text + "\n"

    lines = full_text.split("\n")
    y_offset = 800
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Abhaya", 12)

    for line in lines:
        words = line.split()
        final_line = ""

        if words and not words[0].startswith('©') and not words[0] == "B1" and not words[0] == '•':
            print(f"oryginal: {line}")
            to_translate = ""
            for i, word in enumerate(words):

                if word.startswith("(") and to_translate:
                    translated_grammar = grammar_mapping.get(word, word)
                    translated_text = translator.translate_text((to_translate.strip()), target_lang="PL")
                    checked_translation = check_translation_with_chatgpt(translated_text)

                    final_line += f"{to_translate.strip()} {word} - {translator.translate_text(to_translate.strip(), target_lang='PL')}, {translated_grammar}"
                    print(f"tlumaczenie: {final_line}")
                    break
                else:
                    to_translate += f"{word} "
            time.sleep(4)
        if y_offset < 50:
            can.showPage()
            y_offset = 800

        can.drawString(10, y_offset, final_line)
        y_offset -= 15

    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    for page in new_pdf.pages:
        pdf_writer.add_page(page)

    with open("translated_words.pdf", "wb") as out_file:
        pdf_writer.write(out_file)
