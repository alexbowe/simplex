import itertools

def pascal_2D_row(n):
    """Returns a generator where the ith element of the """
    # Which side of pascal's triangle is the kth position on?
    v = 1
    yield v
    for i in range(0, n):
        v = ((n - i) * v) / (i+1)
        yield v

def get_ith(gen, n):
    for i in xrange(0, n+1):
        x = gen.next()
        if i == n: return x

def binomial(n, k):
    return get_ith(pascal_2D_row(n), k)

def multinomial(ks):
    product = 1 
    n = 0
    for k in ks:
	n += k
	product *= binomial(n, k)
    return product

def lower_coeffs(ks):
    ks = list(ks)
    for i in xrange(len(ks)):
	if ks[i] == 0:
            continue
        ks[i] -= 1
        yield ks
        ks[i] += 1

# 2D cross sections of 3D:
# pascal_simplex([k1, k2, k3]) where sum(k1,k2,k3) = i
# for ith cross section
# hence, generate each integer partition of 123
# and call it for that... (try to use the symmetry if it is too much)
# leave it running on bruce or something
def pascal_simplex(ks):
    if sum(ks) == 0: return 1
    total = 0
    for k in lower_coeffs(ks):
        total += multinomial(k)
    return total
