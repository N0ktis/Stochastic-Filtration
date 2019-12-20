from random import uniform
import math
import numpy



def function(X):
    F = []
    for i in range(len(X)):
        F.append(math.sin(X[i]) + 0.5)
    return F


def x_fuction(x_min, x_max, K):
    X = []
    for i in range(K+1):
        X.append(x_min + i * (x_max - x_min) / K)
    return X


def noise(F):
    n_F = []
    for i in range(len(F)):
        n_F.append(F[i] + uniform(-0.25, 0.25))
    return n_F


def filtered(n_F, alpha):
    filt_F = [0] * len(n_F)
    M = len(alpha) // 2
    for i in range(len(n_F)):
        for j in range(i - M, i + M + 1):
            if (i - M < 0 or j > len(n_F) - 1):   continue
            filt_F[i] += alpha[j + M - i] * n_F[j] ** 2
        filt_F[i] = math.sqrt(filt_F[i])
    return filt_F


def alpha(r):
    alpha = [0] * r
    if (r == 3):
        alpha[1] = uniform(0, 1)
        alpha[0] = alpha[2] = (1 - alpha[1]) / 2
    elif (r == 5):
        alpha[2] = uniform(0, 1)
        alpha[1] = alpha[3] = uniform(0, 1 - sum(alpha)) / 2
        alpha[0] = alpha[4] = (1 - sum(alpha)) / 2
    return alpha


def delta(filt_F, n_F):
    return sum(abs(numpy.array(filt_F) - numpy.array(n_F))) / len(filt_F)


def omega(filt_F):
    omega = 0
    for i in range(1, len(filt_F)):
        omega += abs(filt_F[i] - filt_F[i - 1])
    return omega


def random_search(l, r, n_F):


    P = 0.95
    e = 0.01
    alpha_ = alpha(r)
    filt_F = filtered(n_F, alpha_)
    J_min = l * omega(filt_F) + (1 - l) * delta(filt_F, n_F)
    ans = [l, J_min, alpha_, delta(filt_F, n_F), omega(filt_F)]
    N = int(math.log(1 - P) / math.log(1 - e / math.pi)) + 1
    for i in range(N):
        filt_F = filtered(n_F, alpha_)
        J = l * omega(filt_F) + (1 - l) * delta(filt_F, n_F)
        if (J < ans[1]):
            ans[1] = J
            ans[2] = alpha_
            ans[3] = delta(filt_F, n_F)
            ans[4] = omega(filt_F)

    return ans


def lamda(r, n_F):
    ans_matrix = []
    min_dist = math.inf
    min_i = -1
    print(" +-----+--------+--", "--------" * r, "+--------+--------+", sep="")
    print(" |  h  |  dist  | ", "alpha".center(8 * r - 1), "|  omega |  delta |")
    print(" +-----+--------+--", "--------" * r, "+--------+--------+", sep="")
    for i in range(11):
        ans_matrix.append(random_search(i / 10, r, n_F))
        dist = abs(ans_matrix[i][3]) + abs(ans_matrix[i][4])
        if (dist < min_dist):
            min_dist = dist
            min_i = i
        print("", ans_matrix[i][0], '%.4f' % dist, "[", sep=' | ', end='')
        for j in range(r):
            print('%.4f' % ans_matrix[i][2][j], end="")
            if j != r - 1:
                print(", ", end="")
        print("]", '%.4f' % ans_matrix[i][4], '%.4f' % ans_matrix[i][3], "", sep=" | ")
    print(" +-----+--------+--", "--------" * r, "+---------+--------+", sep="")
    return ans_matrix[min_i]


def print_result(ans, r):
    print(" +-----+--------+--" + "--------" * r + "+--------+--------+")
    print(" |  h* |    J   | " + "alpha".center(8 * r + 1) + "|  omega |  delta |")
    print(" +-----+--------+--" + "--------" * r + "+--------+--------+")
    print("", ans[0], '%.4f' % ans[1], "[", sep=' | ', end='')
    for j in range(r):
        print('%.4f' % ans[2][j], end="")
        if j != r - 1:
            print(", ", end="")
    print("]", '%.4f' % ans[4], '%.4f' % ans[3], "", sep=" | ")
    print(" +-----+--------+--" + "--------" * r + "+--------+--------+")
    return


fx = open('x.txt', 'w')
f = open('f.txt', 'w')
fn = open('fn.txt', 'w')
ff = open('ff.txt', 'w')

for i in x_fuction(0, math.pi, 100):
    fx.write(str(i) + '\n')
F = function(x_fuction(0, math.pi, 100))
for i in F:
    f.write(str(i) + '\n')
n_F = noise(F)
for i in n_F:
    fn.write(str(i) + '\n')
print("\nРазмер скользящего окна:", 3)
result_3 = lamda(3, n_F)
print()
filt_F=filtered(n_F,result_3[2])
for i in filt_F:
    ff.write(str(i) + '\n')
print_result(result_3, 3)
print()
print()
print("\nРазмер скользящего окна:", 5)
result_5 = lamda(5, n_F)
print()
print_result(result_5, 5)
fx.close()
f.close()
fn.close()
ff.close()
