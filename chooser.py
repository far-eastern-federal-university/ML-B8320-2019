# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 13:47:24 2019

@author: Dmitry
"""

import pandas as pd
import numpy as np
import glob
import sys 
import re

data = []

# Считываем вопросы из файла
with open('questions.txt', 'r') as questions:
    for line in questions:
        data.append(line)

print('---------------------')
print('Общий список вопросов')
print('---------------------')
print(data)

# Считываем фамилии из файла
  
students = pd.read_csv('students.csv', header=0)
surnames = list(students['Фамилия'])
groups = list(students['Группа'])
names = list(students['Имя'])

print('---------------------')
print('Список  студентов')
print('---------------------')

print(students)

# Считываем текущий список распределённых вопросов

if 'students_questions.csv' in glob.glob('*.csv'):
    existing_questions = pd.read_csv('students_questions.csv', header=0, encoding="utf-8")
    print('---------------------')
    print('Существующий список вопросов')
    print('---------------------')
    print(existing_questions)
else:
    headers_for_file = 'Фамилия,Имя,Вопрос,Дополнительный вопрос'
    f = open('students_questions.csv', 'w', encoding="utf-8")
    f.write(headers_for_file + '\n')
    f.close()
    existing_questions = pd.read_csv('students_questions.csv')
    print('---------------------')
    print('Ещё никто не получил вопросы')
    print('---------------------')


# Раскидываем вопросы по группам

obligatory_question = data[0]
group1 = []
group2 = []
group3 = []
group4 = []

list_of_questions_by_groups = [group1, group2, group3, group4]
group_models = []

pointer = -1
for i in data:
    if re.match('1', i):
        continue
    elif re.match('[2-9]', i):
        group_models.append(i)
        pointer += 1
    elif re.match('\*', i):
        list_of_questions_by_groups[pointer].append(i)
    else:
        print('strange string')

# Приводим данные в порядок
    
for lst in list_of_questions_by_groups:
    for j in range(len(lst)):
        lst[j] = lst[j].replace('* ', '')
        lst[j] = lst[j].replace('\n', '')

surname = input('Введите свою фамилию: ')

if surname in surnames:
    idx = surnames.index(surname)
    name = names[idx]
    group_num = groups[idx]
else:
    print('Такой фамилии нет в списке')
    sys.exit()

list_of_questions = []
counter = 0
for g in list_of_questions_by_groups:
    if counter != group_num:
        for q in g:
            list_of_questions.append(q)
    counter += 1

print('---------------------')
print('Все вопросы')
print('---------------------')

print(list_of_questions)

full_list_of_questions = list_of_questions + list(existing_questions['Дополнительный вопрос'])

p = []

for qst in list_of_questions:
    p.append(full_list_of_questions.count(qst))
    
p = np.array(p)
s = np.sum(p)

p = p**2
p = 1/p
    
p = p/s
p = p/np.sum(p)
    
print('---------------------')
print('Веса')
print('---------------------')

print(p)

print(np.random.choice(list_of_questions, p=p))
        
if len(existing_questions) > 0:
    for lst in list_of_questions_by_groups:
        for qst in lst:
            if qst in list(existing_questions['Вопрос']):
                lst.remove(qst)

print('---------------------')
print('Список вопросов по группам (оставшиеся)')
print('---------------------')

idx = 0
print()
print(obligatory_question)
for lst in list_of_questions_by_groups:
    print()
    print(group_models[idx])
    print(np.array(lst).reshape(-1,1))
    idx += 1

print()

if not surname in list(existing_questions['Фамилия']):
    chooser = np.random.randint(len(list_of_questions_by_groups[group_num]))
    student_question = surname + ',' + name + ',' + list_of_questions_by_groups[group_num][chooser]
    subquestion = np.random.choice(list_of_questions, p=p)
    student_question += (',' + subquestion)    
    print(student_question.split(','))
    with open('students_questions.csv', 'a', encoding="utf-8") as f:
            f.write(student_question)
            f.write('\n')
else:
    print('Вам уже выдали вопросы, см. "students_questions.csv"')
    