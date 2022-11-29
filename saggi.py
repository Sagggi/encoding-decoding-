import sys
import string
import numpy as np
import streamlit as st

dict = {}
user_inp = st.text_input('enter string')
bhen = st.button("when finished click here")
stri_num = ""

my_chrs = "abcdefghijklmnopqrstuvwxyz?,_"
my_chrs.index('_')

ins = []
for i in user_inp:
    ins.append(my_chrs.index(i))
ins = np.array(ins)
# print ins
# print(len(ins))


# matrix generation

mat = np.random.randint(5, size=(len(ins), len(ins)))
for i in range(len(ins)):
    if mat[i][i] == 0:
        mat[i][i] = np.random.randint(1, 5)

# encoding


outs = np.dot(mat, ins)
outs2 = list(outs)
# print(outs2)


outs4 = []
for i in outs:
    if i > 29:
        i = i % 29
        outs4.append(i)
    else:
        outs4.append(i)
print('encoded data: ', outs4)


# reverse mapping
enc = []
for i in outs4:
    enc.append(my_chrs[i])
print("encoded word", enc)
print("".join(enc))


# determinant


def submatrix(M, c):
    B = [[1] * len(M) for i in range(len(M))]

    for l in range(len(M)):
        for k in range(len(M)):
            B[l][k] = M[l][k]

    B.pop(0)

    for i in range(len(B)):
        B[i].pop(c)
    return B


def det(M):
    X = 0
    if len(M) != len(M[0]):
        print('singular matrix')

    if len(M) <= 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    else:
        for i in range(len(M)):
            X = X + ((-1) ** (i)) * M[0][i] * det(submatrix(M, i))
    return X


# def det(M):
#     return np.linalg.det(M)
    # inverse


n = len(ins)
inverser = np.zeros((n, n))
a = np.zeros((n, 2*n))
for i in range(n):
    for j in range(n):
        a[i][j] = mat[i][j]


for i in range(n):
    for j in range(n):
        if i == j:
            a[i][j+n] = 1


for i in range(n):
    if a[i][i] == 0:
        sys.exit('divided by zero detection')

    for j in range(n):
        if i != j:
            ratio = a[j][i]/a[i][i]

            for k in range(2*n):
                a[j][k] = a[j][k] - ratio*a[i][k]


for i in range(n):
    divisor = a[i][i]
    for j in range(2*n):
        a[i][j] = a[i][j]/divisor


print('\ninverted matrix is')
for i in range(n):
    for j in range(n, 2*n):
        inverser[i][j-n] = a[i][j]
print('inverse matrix', inverser)
print(mat)
print(det(mat))

# inverse matix
mati = (inverser)*round(det(mat))


def modInverse(a, m):
    a = a % m
    for x in range(1, m):
        if ((a * x) % m == 1):
            return x
    return 1


print('round det', modInverse(det(mat), 29))

invert = mati
invert = invert*modInverse(det(mat), 29)
print(invert)

# decoding
final = np.dot(invert, outs4) % 29


decrypt = []
for i in final:
    decrypt.append(round(i))
print(decrypt)


dec = []
for i in decrypt:
    dec.append(my_chrs[i % 29])


print("".join(dec))
ste = "".join(enc)
ste_out = "".join(dec)
if bhen == True:
    st.write("encoded data:")
    st.write(ste)
    st.write("encoded Key")
    st.write(mat)
    st.write('decoded ')
    st.write(ste_out)
