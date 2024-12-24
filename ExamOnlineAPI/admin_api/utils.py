import pdfplumber
import re

def extract_data_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        # print("Extracted Text:", text)

    return parse_text_to_questions(text)

import re

def parse_text_to_questions(text):
    questions = []
    question_pattern = re.compile(r"Question (\d+)\n(.*?)Options(.*?)The correct answer is (\w+)\.", re.DOTALL)
    
    matches = question_pattern.findall(text)

    for match in matches:
        question_number, question_text, options_text, correct_option = match
        options = {}

        # Extract options
        option_pattern = re.compile(r"([A-D])\) ([^A-D]+)")
        options_matches = option_pattern.findall(options_text)
        
        for option in options_matches:
            label, option_text = option
            options[label] = option_text.strip()

        question = {
            'text': question_text.strip(),
            'options': options,
            'correct_option': correct_option,
        }
        questions.append(question)
    
    return questions
