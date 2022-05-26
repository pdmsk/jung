a = []

f = open('aaaa.txt', 'r', encoding='cp1251', errors='ignore')
content = f.read()
while len(content) > 0:
    content = content[content.find('&#'):]
    temp = content[:content.find(';')]
    content = content[content.find(';'):]
    if temp not in a:
      a.append(temp)
      print(temp)
