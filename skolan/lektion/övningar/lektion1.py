file_obj = open('baratext.txt', 'w', encoding='utf-8')
file_obj.write("Hello, World\n Gurkan är bäst!")
file_obj.close()

file_obj = open('baratext.txt', encoding='utf-8')

content = file_obj.readline()
file_obj.close()
print(content)