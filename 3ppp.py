# -*- coding: cp1251 -*-
import re
import sys

iterations = 0	# переменная для подсчета итераций (используется при выводе)

# ------------------------------------------------------------------------------------
# Функция считывания условий из файла
def read_data(filename):
	try: f = open(filename, "r")
	except:
		print "\nERROR: File %s not found.\nNow try to open input.txt..." % filename
		try:
			f = open("input.txt", "r")
		except:
			print "\nERROR: File 'input.txt' not found."
			sys.exit(raw_input("Press enter to exit..."))

	return [ map(int, condition) for condition in						# для каждой "строки(массива)" массива 
																		# каждый элемент превращаем в число.
				[ re.findall(r'\d+', line) for line in f.readlines()]
			]															# для каждой линии из считанного файла
																		# регулярным выражением выделяем массив чисел в 
																		# этой строке, которые разделены пробелом.

# ------------------------------------------------------------------------------------
# Функция проверки условий
def check(tab, row, conditions):
	# Вывод матрицы на итерации с шагом 1000
	global iterations
	iterations +=1
	if  iterations % 1000000 == 0 :
		for i in range(8):
			print tab[i]
		print "   "
	
	#Обязательное правило №1 #top-side conditions
	# Проверка строк на соответствие верхним ограничениям
	
	# Проверка первой строки 
	# Тут могут быть либо нули, либо ограничивающая цифра, иначе выход на перегенерацию строки
	if row == 0:
		for col in range(8):
			if (conditions[2][col] != 0):
				if (tab[0][col] != conditions[2][col]		and
					tab[0][col] != 0						and
					tab[0][col] != 7
					):		# Грустный смайлик. Почему, ведь всё прекрасно работает?
					return 0
	
	# Если в первой строке нули, то во второй должно быть верхнее ограничение, либо ноль
	if row == 1:
		for col in range(8):
			if (conditions[2][col] != 0):
				if (
					(tab[0][col] == 0 or tab[0][col] == 7)	and
					 tab[1][col] != conditions[2][col]		and
					 tab[1][col] != 0						and
					 tab[1][col] != 7
					):
					return 0
					
	# Если в первой и второй строках нули, то в третьей должно быть верхнее ограничение, без вариантов
	if row == 2:
		for col in range(8):
			if (conditions[2][col] != 0):
				if (
					(tab[0][col] == 0 or tab[0][col] == 7)	and
					(tab[1][col] == 0 or tab[1][col] == 7)	and
					 tab[2][col] != conditions[2][col]
					):
					return 0
	
	#Обязательное правило №2 #left-side conditions
	# Проверка строк на соответствие левым ограничениям, вызывается для каждой строки
	if (conditions[0][row] != 0): # если первое условин не нулевое. Какое первое? Левое! Первое оно у нас в файле, зачем привязывать к формату
		if (
			(tab[row][0] != conditions[0][row]		and	# если на первой позиции не стоит граничное
			 tab[row][1] != conditions[0][row]		and	#если на второй тоже не стоит граничное
			 tab[row][2] != conditions[0][row]			#если на 3-й тоже не стоит граничное
			)
			or
			(tab[row][1] == conditions[0][row]		and	# вторая позиция равна условию
			(tab[row][0] != 0 and tab[row][0] != 7)		# при этом на 1-й позиции не 0 и не 7
			)
			or
			(
				tab[row][2] == conditions[0][row]	and
				(
				tab[row][0] != 0 and tab[row][0] != 7 
				or 
				tab[row][1] != 0 and tab[row][1] != 7
				)
			)
			):
			return 0
	
	#Обязательное правило №3 #right-side conditions
	# Проверка строк на соответствие правым ограничениям, вызывается для каждой строки
	if (conditions[1][row] != 0):
		if (
			(tab[row][-1] != conditions[1][row]		and	# если на первой позиции не стоит граничное
			 tab[row][-2] != conditions[1][row]		and	#если тут тоже не стоит граничное
			 tab[row][-3] != conditions[1][row]
			)
			or
			(tab[row][-2] == conditions[1][row]		and
			 tab[row][-1] != 0 and tab[row][-1] != 7
			)
			or
			(
				tab[row][-3] == conditions[1][row]		and
				(
					tab[row][-1] != 0 and tab[row][-1] != 7 
					or 
					tab[row][-2] != 0 and tab[row][-2] != 7
				)
			)
			):
			return 0

	#Необязательное правило #Оптимизация
	# Проверка того, что числа в нижних ограничениях не встречаются раньше 5-й строки
	if row < (len(tab) - 3):	# 8 - 3 = 5
		for i in range(len(tab)):
			if tab[row][i]==conditions[3][i]:
				return 0
				
	
	#Обязательные правила №5-6, переставлены сюда для оптимизации
	# Проверка того, что цифры в столбце не повторились и что количество пробелов не больше 2
	for j in range(0, row) :
			for h in range(0, 8):
					if (tab[row][h] == tab[j][h] and tab[row][h] != 0 and tab[row][h] != 7) :
							return 0
	sum = 0
	for k in range(0, 8) :
			for n in range(0, row + 1):
					if (tab[n][k] == 0 or tab[n][k] == 7) :
							sum += 1
					if (sum > 2):
							return 0
			sum = 0
	
	#Обязательное правило №4 #down-side conditions
	# Проверка строк на соответствие нижним ограничениям (ТОДО: исправить и проверить)
	if (row == 7):
		for col in range(len(tab)):
			if conditions[3][col] != 0 :  #если 3-е условие не равно 0. Не 3-е, нижнее ведь. Давайте не будем путать людей
				if (
					(tab[-1][col] != conditions[3][col]	and	# Исправил индексы так, чтобы они были единой системы счисления
					 tab[-2][col] != conditions[3][col]	and
					 tab[-3][col] != conditions[3][col]
					)
					or
					(tab[-2][col] == conditions[3][col]	and
					 tab[-1][col] !=0 and tab[-1][col] !=7
					)
					or
					(
						tab[-3][col] == conditions[3][col]	and
						(
							tab[-1][col] !=0 and tab[-1][col] !=7 
							or 
							tab[-2][col] !=0 and tab[-2][col] !=7 
						)
					)
					):
					return 0

	return 1

# ------------------------------------------------------------------------------------
# Функция генерирования строки (почти без комментариев, потому что поздно)
def generate(row):
	if (row[0] == -1):
		row[:] = range(len(row))
		return 1
	a = -1
	for j in reversed(range(len(row)-1)):
		if (row[j] < row[j+1]):
			a = j
			break
	if a == -1:
		return 0
	b = -1
	for j in reversed(range(a, len(row))):
		if (row[j] > row[a]):
			b = j
			break

	row[a], row[b] = row[b], row[a]		# Обмен значений для получения новой строки
	row[(a+1):] = reversed(row[(a+1):])
	return 1

# ------------------------------------------------------------------------------------
# Функция рекурсивного подбора строк матрицы
def rekurs(tab, row, conditions):
	while (1):
		if (generate(tab[row]) == 0):	# Если не осталось больше вариантов строк - забиваем минус единицы, выходим
			tab[row] = [-1 for i in range(len(tab))]
			return 0
		if (check(tab, row, conditions) == 1):
			if row < 7:					# Пока не заполним таблицу полностью, спускаемся по уровням, т.е. по строкам
				if (rekurs(tab, row + 1, conditions)):
					return 1
			else:
				return 1

## -------------------- run program -------------------
if __name__ == '__main__':
	conditions = read_data(raw_input("Input file:  "))
	tab = [ [-1 for j in range(len(conditions[0]))] for i in range( len(conditions[0]) ) ]
	print "\nSuccess. \nNow search for solutions..."
	if rekurs(tab, 0, conditions) == 0:
		print "\nThere is no solution:"
		for i in range(len(tab)): print tab[i]
	else:
		print "\nGood news:"
		for i in range(len(tab)): 
			for k in range(len(tab)):
				if (tab[i][k] == 7): tab[i][k] = 0
			print tab[i]
	raw_input("Press enter to exit...")
