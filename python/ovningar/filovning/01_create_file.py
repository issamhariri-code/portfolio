# randomQuizGenerator.py - Creates quizzes with questions and answers in
# random order, along with the answer key.

import random
from pathlib import Path

# 50 U.S. states and their capitals:
capitals = {
    'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock',
    'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover',
    'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
    'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines',
    'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge',
    'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan': 'Lansing',
    'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
    'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord',
    'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany',
    'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Columbus',
    'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg',
    'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre',
    'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier',
    'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston',
    'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'
}

# Utdata-mapp
OUT_DIR = Path(__file__).resolve().parent / "quizzes"
OUT_DIR.mkdir(exist_ok=True)

# Skapa 35 quiz + facit
for quiz_num in range(35):
    quiz_path = OUT_DIR / f"capitalsquiz{quiz_num + 1}.txt"
    ans_path = OUT_DIR / f"capitalsquiz_answers{quiz_num + 1}.txt"

    with quiz_path.open('w', encoding='utf-8') as quiz_file, ans_path.open('w', encoding='utf-8') as answer_file:
        # Header
        quiz_file.write('Name:\n\nDate:\n\nPeriod:\n\n')
        quiz_file.write((' ' * 20) + f'State Capitals Quiz (Form {quiz_num + 1})\n\n')

        # Blanda ordningen på staterna
        states = list(capitals.keys())
        random.shuffle(states)

        # Loop över alla 50 stater och skapa en fråga för varje
        for q_num, state in enumerate(states, start=1):
            correct = capitals[state]  # rätt svar (huvudstad)
            # Ta fram tre felaktiga alternativ (kapitaler för andra stater)
            wrong = list(capitals.values())
            wrong.remove(correct)
            wrong_opts = random.sample(wrong, 3)

            # Blanda alternativen
            options = wrong_opts + [correct]
            random.shuffle(options)

            # Skriv ut frågan till quiz-fil
            quiz_file.write(f"{q_num}. What is the capital of {state}?\n")
            for i, opt in enumerate(options):
                label = "ABCD"[i]
                quiz_file.write(f"    {label}. {opt}\n")
            quiz_file.write('\n')

            # Spara facit (A-D)
            correct_letter = "ABCD"[options.index(correct)]
            answer_file.write(f"{q_num}. {correct_letter}\n")
print