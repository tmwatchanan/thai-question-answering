import os, glob, re
from pythainlp.tokenize import word_tokenize

examples_path = 'Examples\\'
question_list_filename = examples_path + 'question_list.txt'
expected_answer_list_filename = examples_path + 'expected_ans.txt'
sources_dir_name = examples_path + 'Sources\\'

numbers = re.compile(r'(\d+)')
def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

document_list = []
for source_filename in sorted(glob.glob(os.path.join(sources_dir_name, '*.txt')), key=numerical_sort):
    with open(source_filename , encoding='utf-8') as f:
        document = []
        for line in f:
            document.append(line.rstrip('\n'))
        document_list.append(document)

question_list = []
with open(question_list_filename, encoding='utf-8') as f:
    for line in f:
        question_list.append([n for n in line.strip().split('::')])
print("Questions = ", question_list)

expected_answer_list = []
with open(expected_answer_list_filename, encoding='utf-8') as f:
    for line in f:
        expected_answer_list.append([n for n in line.strip().split('::')])
print("Expected answers = ", expected_answer_list)

for document in document_list:
    for paragraph in document:
        normalized_paragraph = " ".join(paragraph.split())
        tokenized_paragraph = word_tokenize(text=normalized_paragraph, engine='deepcut')
        print(tokenized_paragraph)

# for pair in question_list:
#     try:
#         number,question = pair[0],pair[1]
#         normalized_question = " ".join(question.split())
#         tokenized_question = word_tokenize(text=normalized_question, engine='deepcut')
#         print(tokenized_question)
#     except IndexError:
#         print("A question doesn't have enough entries.")

# with open('output.txt', 'w', newline='', encoding='utf-8') as file:
#     file.write('|'.join(list_word))
