A = [2,4,7,4,2,9,5,3,1,0,4,3]
for i in range(12):
	for j in range(12):
		if A[i] < A[j]:
			A[i], A[j] = A[j], A[i]
		print(A)
print(A)