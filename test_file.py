from config import *

array1 = np.array([1, 2, 3, 4])    # Numpy array (1D)
array2 = np.array([[4,5],[6,7]])  # Numpy matrix
array3 = np.zeros((3,4))           # 2D numpy array
array_list = [array1, array2, array3]
array4 = np.array([[4,5],[6,7]])
array_list.append(array4)

# print(array4-10)
for k, array in enumerate(array_list):
    print(array -10)
    print("/n")

# a = ['hello', 9, 3.14, 9]
# for i, item in enumerate(a):
#     if i+1 == a.__len__():  # print a separator if this isn't the first element
#         print(',')
#     print(item, end='')

