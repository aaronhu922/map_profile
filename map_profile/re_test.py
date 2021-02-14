import re

domain_list = ['Literary Text: Key Ideas and Details', 'Informational Text: Language, Craft,',
                           'Literary Text: Language, Craft, and', 'Vocabulary: Acquisition and Use',
                           'Informational Text: Key Ideas and', 'Vocabulary Use and Functions',
                           'Language and Writing', 'Foundational Skills', 'Literature and Informational Text',
                           'Writing: Write, Revise Texts for', 'Language: Understand, Edit for'
                           ]
data = 'available&99 RD&Quadrant&99 TH&Q&95 TH&Q'
regex1 = '&(\d+ (TH|RD|ST|ND))&'
value = re.findall(regex1, data)
print(value)
value1 = re.search(regex1, data)
print(value1)
print(value1.group().strip('&'))
print(value1.string)
print(value1.span())
str = ""
print(str == "")
print(len(str))
if not str:
    print(str + "is null")
if str == "":
    print(str + "is \"\"")

list1 = '1'.strip(',')
print(list1[0])
list1 = '1,2,'.strip(',').split(',')
print(list1)
# results = list(map(int, list1))
# print(domain_list(list[0]))
# print(results)
for index in list1:
    print(domain_list[int(index)])
# print(domain_list(results[0]))