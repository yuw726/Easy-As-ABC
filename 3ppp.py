# -*- coding: cp1251 -*-
import re
import sys

iterations = 0	# ���������� ��� �������� �������� (������������ ��� ������)

# ------------------------------------------------------------------------------------
# ������� ���������� ������� �� �����
def read_data(filename):
	try: f = open(filename, "r")
	except:
		print "\nERROR: File %s not found.\nNow try to open input.txt..." % filename
		try:
			f = open("input.txt", "r")
		except:
			print "\nERROR: File 'input.txt' not found."
			sys.exit(raw_input("Press enter to exit..."))

	return [ map(int, condition) for condition in						# ��� ������ "������(�������)" ������� 
																		# ������ ������� ���������� � �����.
				[ re.findall(r'\d+', line) for line in f.readlines()]
			]															# ��� ������ ����� �� ���������� �����
																		# ���������� ���������� �������� ������ ����� � 
																		# ���� ������, ������� ��������� ��������.

# ------------------------------------------------------------------------------------
# ������� �������� �������
def check(tab, row, conditions):
	# ����� ������� �� �������� � ����� 1000
	global iterations
	iterations +=1
	if  iterations % 1000000 == 0 :
		for i in range(8):
			print tab[i]
		print "   "
	
	#������������ ������� �1 #top-side conditions
	# �������� ����� �� ������������ ������� ������������
	
	# �������� ������ ������ 
	# ��� ����� ���� ���� ����, ���� �������������� �����, ����� ����� �� ������������� ������
	if row == 0:
		for col in range(8):
			if (conditions[2][col] != 0):
				if (tab[0][col] != conditions[2][col]		and
					tab[0][col] != 0						and
					tab[0][col] != 7
					):		# �������� �������. ������, ���� �� ��������� ��������?
					return 0
	
	# ���� � ������ ������ ����, �� �� ������ ������ ���� ������� �����������, ���� ����
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
					
	# ���� � ������ � ������ ������� ����, �� � ������� ������ ���� ������� �����������, ��� ���������
	if row == 2:
		for col in range(8):
			if (conditions[2][col] != 0):
				if (
					(tab[0][col] == 0 or tab[0][col] == 7)	and
					(tab[1][col] == 0 or tab[1][col] == 7)	and
					 tab[2][col] != conditions[2][col]
					):
					return 0
	
	#������������ ������� �2 #left-side conditions
	# �������� ����� �� ������������ ����� ������������, ���������� ��� ������ ������
	if (conditions[0][row] != 0): # ���� ������ ������� �� �������. ����� ������? �����! ������ ��� � ��� � �����, ����� ����������� � �������
		if (
			(tab[row][0] != conditions[0][row]		and	# ���� �� ������ ������� �� ����� ���������
			 tab[row][1] != conditions[0][row]		and	#���� �� ������ ���� �� ����� ���������
			 tab[row][2] != conditions[0][row]			#���� �� 3-� ���� �� ����� ���������
			)
			or
			(tab[row][1] == conditions[0][row]		and	# ������ ������� ����� �������
			(tab[row][0] != 0 and tab[row][0] != 7)		# ��� ���� �� 1-� ������� �� 0 � �� 7
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
	
	#������������ ������� �3 #right-side conditions
	# �������� ����� �� ������������ ������ ������������, ���������� ��� ������ ������
	if (conditions[1][row] != 0):
		if (
			(tab[row][-1] != conditions[1][row]		and	# ���� �� ������ ������� �� ����� ���������
			 tab[row][-2] != conditions[1][row]		and	#���� ��� ���� �� ����� ���������
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

	#�������������� ������� #�����������
	# �������� ����, ��� ����� � ������ ������������ �� ����������� ������ 5-� ������
	if row < (len(tab) - 3):	# 8 - 3 = 5
		for i in range(len(tab)):
			if tab[row][i]==conditions[3][i]:
				return 0
				
	
	#������������ ������� �5-6, ������������ ���� ��� �����������
	# �������� ����, ��� ����� � ������� �� ����������� � ��� ���������� �������� �� ������ 2
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
	
	#������������ ������� �4 #down-side conditions
	# �������� ����� �� ������������ ������ ������������ (����: ��������� � ���������)
	if (row == 7):
		for col in range(len(tab)):
			if conditions[3][col] != 0 :  #���� 3-� ������� �� ����� 0. �� 3-�, ������ ����. ������� �� ����� ������ �����
				if (
					(tab[-1][col] != conditions[3][col]	and	# �������� ������� ���, ����� ��� ���� ������ ������� ���������
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
# ������� ������������� ������ (����� ��� ������������, ������ ��� ������)
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

	row[a], row[b] = row[b], row[a]		# ����� �������� ��� ��������� ����� ������
	row[(a+1):] = reversed(row[(a+1):])
	return 1

# ------------------------------------------------------------------------------------
# ������� ������������ ������� ����� �������
def rekurs(tab, row, conditions):
	while (1):
		if (generate(tab[row]) == 0):	# ���� �� �������� ������ ��������� ����� - �������� ����� �������, �������
			tab[row] = [-1 for i in range(len(tab))]
			return 0
		if (check(tab, row, conditions) == 1):
			if row < 7:					# ���� �� �������� ������� ���������, ���������� �� �������, �.�. �� �������
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
