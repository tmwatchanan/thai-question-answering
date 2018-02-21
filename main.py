import deepcut
list_word = deepcut.tokenize('ตัดคำได้ดีมาก')
with open('output.txt', 'w', newline='', encoding='utf-8') as file:
    file.write('|'.join(list_word))
