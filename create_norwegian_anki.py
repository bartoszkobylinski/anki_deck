import genanki
import random
import docx


def generate_anki_package(questions_and_answers):
    id_note = random.randint(1000000, 9999999)

    my_model = genanki.Model(
        id_note,
        name='first_model',
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                'name': "karta_1",
                'qfmt': "{{Question}}",
                "afmt": "<hr id='answer'>{{Answer}}",
            },

        ])

    id2 = random.randint(1000, 9999)
    my_deck = genanki.Deck(id2, 'Norweskie czasowniki')

    for q_and_a in questions_and_answers:
        my_note = genanki.Note(model=my_model, fields=[q_and_a.get("Question", ""), q_and_a.get("Answer", "")])
        my_deck.add_note(my_note)

    package = genanki.Package(my_deck).write_to_file("output.apkg")
    return package


def create_data_with_question_and_answer(filename):
    doc = docx.Document(filename)

    data = []
    current_question = ''
    current_answer = ''
    for table in doc.tables:
        for row in table.rows:
            question_cell = row.cells[0]
            answer_cell = row.cells[1]
            if question_cell.text.strip():
                current_question = question_cell.text.strip().split('\n')
                print(f"to jest quest: {current_question}")
            if answer_cell.text.strip():
                current_answer = answer_cell.text.strip().split('\n')
                print(f"to jest answe: {current_answer}")

    for question, answer in zip(current_question, current_answer):
        data.append({"Question": question, "Answer": answer})

    return data



if __name__ == "__main__":

    data = create_data_with_question_and_answer('07.03.2023.docx')
    print(data)
    generate_anki_package(data)