#RandomQuizGenerator.py skapar slumpmässigt quiz med frågor från boken ATBS
#Allt är i slumpmässig ordning tillsammans med svaren i form av keys

import random
#Den här funktionen importerar "random" modulen vilket gör att 
# #den kan använda sig av slumpmässiga funktioner
#som att slumpa fram frågor och svar.

#Quiz datan, själva keys är staterna och values är huvudstäderna i dictionary form.
capitals = {
    'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
    'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
    'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
    'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
    'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines',
    'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge',
    'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston',
    'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson',
    'Missouri': 'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln',
    'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton',
    'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
    'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
    'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
    'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville',
    'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier',
    'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston',
    'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

#Skapar 35 quiz filer, 35 elever i klassen varje elev ska ha ett unikt quiz
for quiz_num in range(35):
    #skapar quiz med svarsfiler
    quiz_file = open(f'capitalsquiz{quiz_num + 1}.txt', 'w', encoding='utf-8')
    answer_file = open(f'capitalsquiz_answers{quiz_num + 1}.txt', 'w', encoding='utf-8')

    #skapar rubrik för quiz
    quiz_file.write('name:\n\nDate:\n\nPeriod:\n\n')
    quiz_file.write((' ' * 20) + f'State Capitals Quiz (form {quiz_num + 1}) \n\n')

    states = list(capitals.keys())
    random.shuffle(states)
    #shufflar ordningen på staterna så att varje quiz blir unikt

    # Loopar igenom alla 50 stater och skapar frågor

    for num in range(50):
        correct_answer = capitals[states[num]]
        wrong_answers = list(capitals.values())
        del wrong_answers[wrong_answers.index(correct_answer)]
        wrong_answers = random.sample(wrong_answers, 3)
        answer_options = wrong_answers + [correct_answer]
        random.shuffle(answer_options)
        # skapar frågorna med 3 felaktiga svar och 1 korrekt svar

        quiz_file.write(f'{num + 1}. What is the capital of {states[num]}?\n')
        for i in range(4):
            quiz_file.write(f"  {'ABCD'[i]}. {answer_options[i]}\n")
        quiz_file.write('\n')


        answer_file.write(f"{num + 1}. {'ABCD'[answer_options.index(correct_answer)]}")
    quiz_file.close()
    answer_file.close()
