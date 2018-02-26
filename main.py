from pythainlp.tokenize import word_tokenize
list_word = word_tokenize(text='ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด',engine='deepcut')
with open('output.txt', 'w', newline='', encoding='utf-8') as file:
    file.write('|'.join(list_word))
