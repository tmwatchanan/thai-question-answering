# -*- coding: utf-8 -*-

import os
import glob
import re
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag
from pythainlp.corpus import stopwords
import heapq
from gensim.models import Word2Vec

stopwords = stopwords.words('thai')

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

document_data = []

count_doc = 1
for document in document_list:
    # paragraph_struct = {
    #     'original': '',
    #     'tokenized': '',
    #     'tagged': ''
    # }
    for paragraph in document:
        normalized_paragraph = " ".join(paragraph.split())
        normalized_paragraph = normalized_paragraph.replace('"', '')
        tokenized_paragraph = word_tokenize(text=normalized_paragraph, engine='deepcut')
        tokenized_paragraph = [x for x in tokenized_paragraph if x != ' ']
        # try:
        #     tagged_paragraph = pos_tag(tokenized_paragraph, engine='artagger')
        # except:
        #     pass
        # document_data.append(tagged_paragraph)
        # filtered_words = [word for word in tokenized_paragraph if word not in stopwords]
        # document_data.append(filtered_words)
        document_data.append(tokenized_paragraph)
        print(tokenized_paragraph)
    count_doc = count_doc + 1
    # if count_doc > 28:
    #     break
print(document_data)

# Word2Vec =============================================================================================================
model = Word2Vec(document_data, size=100, window=3, min_count=0)
# Word2Vec =============================================================================================================

# print("")
# print(document_data)

numeric_question_keywords = ['กี่', 'เท่าไหร่', 'เท่าใด', 'เท่าไร']
location_question_keywords = ['ที่ใด', 'แห่งใด', 'ที่ไหน', 'บริเวณใด', 'จังหวัดใด']
person_question_keywords = ['ตือใคร', 'ใครเป็น', 'ใคร', 'ผู้ใด', 'ชนชาติใด', 'ชื่ออะไร']

KEE_question_index_list = [1, 3, 4, 5, 6, 8]
this_question = question_list[4]
question_num = this_question[0]
question_text = this_question[1]

print(question_text)

question_type = ''
question_keyword = ''

for keyword in numeric_question_keywords:
    if question_text.__contains__(keyword):
        question_type = 'numeric'
        question_keyword = keyword
        break
if not question_type:
    for keyword in location_question_keywords:
        if question_text.__contains__(keyword):
            question_type = 'location'
            question_keyword = keyword
            break
if not question_type:
    for keyword in person_question_keywords:
        if question_text.__contains__(keyword):
            question_type = 'person'
            question_keyword = keyword
            break

tokenized_question_text = word_tokenize(text=question_text, engine='deepcut')
# question_text = question_text.replace(question_keyword, '')
print(tokenized_question_text)
print(question_type, question_keyword)

if question_keyword == 'กี่':
    unit_keyword = tokenized_question_text[tokenized_question_text.index(question_keyword) + 1]
    print(question_keyword, unit_keyword)

print(tokenized_question_text)

found_paragraph_list = []
for paragraph in document_data:
    # print(paragraph)
    for question_word in tokenized_question_text:
        matching = [s for s in paragraph if question_word in s]
        if matching:
            found_paragraph_list.append(paragraph)
            # print(matching)

unique_found_paragraph = [list(x) for x in set(tuple(x) for x in found_paragraph_list)]
print("unique_found_paragraph", unique_found_paragraph)
print("found_paragraph_list", found_paragraph_list)
print("-----------------")
for p in unique_found_paragraph:
    para_text = ''.join(p)
    print(para_text)
print("-----------------")

peak_occurence = [0] * len(unique_found_paragraph)
distributed_occurence = [0] * len(unique_found_paragraph)
for idx, para in enumerate(unique_found_paragraph):
    for word in tokenized_question_text:
        peak_occurence[idx] += para.count(word)
        if (para.count(word) > 0):
            distributed_occurence[idx] = distributed_occurence[idx] + 1
        print(para.count(word), word, para)
print("peak_occurence", peak_occurence)
concept = unique_found_paragraph[peak_occurence.index(max(peak_occurence))]
concept2 = unique_found_paragraph[distributed_occurence.index(max(distributed_occurence))]
max_distributed = heapq.nlargest(5, distributed_occurence)
for idx in max_distributed:
    print("concept2", unique_found_paragraph[idx])
print("concept", concept)

print(tokenized_question_text)

aa=model.similar_by_word('เป็น')
print(aa)
aa=model['เป็น']
print(aa)
print(model.similarity('รถ', 'รถ'))
exit(1)

if question_keyword == 'กี่':
    main_index = tokenized_question_text.index(question_keyword)
    scoped_tokenized_question_text = tokenized_question_text[:main_index]
    print("scoped_tokenized_question_text", scoped_tokenized_question_text)
    c_index = concept.index(scoped_tokenized_question_text[-1])
    keyword_index = concept.index(unit_keyword)
    scoped_concept = concept[c_index+1:keyword_index+1]
    print("scoped_concept", scoped_concept)

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
