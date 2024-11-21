#系統模擬與分析的作業
import numpy as np

#m = [3,3]
matrix = np.array([[0.25,0.2,0.12,0.43],[0.25,0.2,0.12,0.43],[0,0.25,0.20,0.55],[0,0,0.25,0.75]])
print("初始機率")
print(matrix)
for loop in range(4):
    matrix = matrix.dot(matrix)
print("矩陣相乘後機率")
print(matrix.dot(matrix))


#def matrix_multiplication(m):
#    mm = []
#    for loop1 in range(m[0]):
#        for loop2 in range(m[1]):
#           mm[loop1][loop2] 
#    return 
