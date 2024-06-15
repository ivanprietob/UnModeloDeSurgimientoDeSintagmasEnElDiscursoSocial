
import math
import random


ZERO_ONE = [0, 1]


#
#  Reduces a series of nested lists to a single list. I use to compute
#  distances between multidimensional lists and to compute sums over
#  several indices.
#
def flatten(lst):
    res = []
    for ele in lst:
        if type(ele) == list:
            res += flatten(ele)
        else:
            res += [ele]
    return res


#
# Distance between two vectors
#
def dst(a, b):
    if a is None or b is None:
        return 100000.0
    else:
        return math.sqrt(sum([(x-y)**2 for (x, y) in zip(a, b)]))


#
# normalizes alpha, beta, tau
#
def alphanorm(alpha):
    return [[alpha[j][i]/max(0.01, sum(alpha[j])) for i in ZERO_ONE] for j in ZERO_ONE]


def betanorm(beta):
    return [[[beta[h][k][j]/max(0.01, sum(beta[h][k])) for j in ZERO_ONE] for k in ZERO_ONE] for h in ZERO_ONE]


def taunorm(tau):
    return [[[[tau[i][j][k][h]/max(0.01, sum(flatten(tau[i]))) for h in ZERO_ONE] for k in ZERO_ONE] for j in ZERO_ONE ] for i in ZERO_ONE]


#
#  Applies the ER algorithm to a series of observations Pi along a
#  stretch of time to obtain the probability that an event that caused
#  the syntagm to emerge ocurred at any given time instant
#
#  Input:
#  T:     number of time steps during which we observe the event
#  Pi: array of size 2 x T; element Pi[i][t] is the relative
#         probability of not observing the syntagm (i=0) or observing
#         it (i=1). The way it is measures is as follows. Suppose that
#         at time t the syntagm is composed nw times, while the
#         individual words that compose it are observed n1,...nm
#         times. Then
#
#         NP0 = Sum(n1,...nm)
#         NP1 = nw
#
#         Pi[0][t] = NP0/(NP0+NP1)
#         Pi[1][t] = NP1/(NP0+NP1)
#
#         It must be Pi[0][t]+ Pi[1][t] = 1 for all t
#  Tol:   Error for the stopping criterion
#  Nmax:  Max number of iteration
#
#  Output:
#
#  Ab array Psi of T elements. Element Psi[t] is the probability that
#  the event that caused the syntagm to emerge ocurred at time t
#
#
#
#  Notice that, for the sake of convenience, in alpha and beta the
#  indices are backwards with respect to tau. That is, the generic
#  element of tau is
#
#  tau[i][j][k][h]
#
#  while the corresponding elements of alpha and beta are
#
#  alpha[j][i]  beta[h][k][j]
#
#  This is simply for convenience of making the sums
def ER(T, Pi, Tol, Nmax):
    Psi = []
    #
    # Nu[i][t]: Prob(s(t)=i)
    #
    Nu = [[0 for _ in range(T+1)] for _ in range(2)]
    Nu[0][-1] = 0.95
    Nu[1][-1] = 0.05
    for t in range(T):
        prev = None
        iter = 0
        alpha = [[random.uniform(0, 1) for i in ZERO_ONE] for j in ZERO_ONE]
        alpha = alphanorm(alpha)

        beta = [[[random.uniform(0, 1) for j in ZERO_ONE] for k in ZERO_ONE] for h in ZERO_ONE]
        beta = betanorm(beta)

        gamma = [random.uniform(0, 1) for h in ZERO_ONE]
        gamma = [ gamma[h]/max(0.01, sum(gamma)) for h in ZERO_ONE]

        tau = [[[[ random.uniform(0, 1) for h in ZERO_ONE] for k in ZERO_ONE] for j in ZERO_ONE ] for i in ZERO_ONE]
        tau = taunorm(tau)

        elst = flatten(alpha) + flatten(beta) + flatten(gamma) + flatten(tau)
        while iter < Nmax and dst(elst, prev)/max(0.01, dst(elst, len(elst)*[0.0])) > Tol:
            iter += 1
            prev = elst[:]

            tau = [[[[alpha[j][i]*beta[h][k][j]*Nu[k][t-1]*gamma[h] for i in ZERO_ONE] for j in ZERO_ONE] for k in ZERO_ONE ] for h in ZERO_ONE]
            tau = taunorm(tau)

            alpha = [[Pi[i][t]*sum(flatten(tau[i][j])) for i in ZERO_ONE] for j in ZERO_ONE]
            alpha = alphanorm(alpha)

            for j in ZERO_ONE:
                for k in ZERO_ONE:
                    for h in ZERO_ONE:
                        beta[h][k][j] = Pi[0][t]*tau[0][j][k][h]+Pi[1][t]*tau[1][j][h][k]
            beta = betanorm(beta)

            for h in ZERO_ONE:
                s = 0
                for i in ZERO_ONE:
                    for j in ZERO_ONE:
                        for k in ZERO_ONE:
                            s += Pi[i][t]*tau[i][j][k][h]
                gamma[h] = s
            gamma = [gamma[h]/max(0.01, sum(gamma)) for h in ZERO_ONE]
            elst = flatten(alpha) + flatten(beta) + flatten(gamma) + flatten(tau)
        s = [0, 0]
        for h in ZERO_ONE:
            for k in ZERO_ONE:
                s[0] += beta[h][k][0]*Nu[k][t-1]*gamma[h]
                s[1] += beta[h][k][1]*Nu[k][t-1]*gamma[h]
        Nu[0][t] = s[0]
        Nu[1][t] = s[1]
        Psi += [gamma[1]]
    return [Psi[0]] + [max(Psi[i]-Psi[i-1], 0) for i in range(1, len(Psi))]


Pi0 = [min(1, 0.1*random.uniform(0, 1)) for _ in range(40)] + [min(1, 1-0.1*random.uniform(0, 1)) for _ in range(40)]
Pi1 = [1-x for x in Pi0]

Pi = [ [x/(x+y) for (x, y) in zip(Pi1, Pi0)], [y/(x+y) for (x, y) in zip(Pi1, Pi0)]]


# print Pi

res = ER(len(Pi0), Pi, 0.01, 20)

for r in res:
    print("%5.3f" % r)
