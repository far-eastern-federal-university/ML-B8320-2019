# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 13:47:24 2019

@author: Dmitry
"""

import pandas as pd
import numpy as np
import glob
import sys 
import csv
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
    headers_for_file = 'Фамилия,Имя,Вопрос'
    f = open('students_questions.csv', 'w', encoding="utf-8")
    f.write(headers_for_file + '\n')
    f.close()
    existing_questions = pd.read_csv('students_questions.csv')

print('---------------------')
print('Существующий список вопросов')
print('---------------------')
print(existing_questions)

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
        
if len(existing_questions) > 0:
    for lst in list_of_questions_by_groups:
        for qst in lst:
            if qst in list(existing_questions['Вопрос']):
                lst.remove(qst)

print('---------------------')
print('Список вопросов по группам')
print('---------------------')

idx = 0
print()
print(obligatory_question)
for lst in list_of_questions_by_groups:
    print()
    print(group_models[idx])
    print(np.array(lst).reshape(-1,1))
    idx += 1

surname = input('Введите свою фамилию: ')

if surname in surnames:
    idx = surnames.index(surname)
    name = names[idx]
    idx = int(groups[idx])
    chooser = np.random.randint(len(list_of_questions_by_groups[idx]))
    student_question = surname + ',' + name + ',' + list_of_questions_by_groups[idx][chooser]
else:
    print('Такой фамилии нет в списке')
    sys.exit()



if not surname in list(existing_questions['Фамилия']):
    print()    
    print(student_question)
    with open('students_questions.csv', 'a', encoding="utf-8") as f:
            f.write(student_question)
            f.write('\n')
else:
    print('Вам и одного вопроса хватит')
    