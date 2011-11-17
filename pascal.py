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

# m parts k_1, k_2, ... k_m, where the sum is n
# has to be at least 2
def partitions(n, m):
    a = [n - m + 1] + [1] * (m-1) + [-1]

    while True:
        yield a[0:-1]
        if a[1] >= a[0] - 1:
            j = 2
            s = a[0] + a[1] - 1
            while a[j] >= a[0] - 1:
                s = s+a[j]
                j += 1
            if j > m-1: return
            else:
                x = a[j] + 1
                a[j] = x
                j -= 1
            while j > 0:
                a[j] = x
                s = s - x
                j = j - 1
            a[0] = s
        else:
            a[0] -= 1
            a[1] += 1

def prefix(padding, it):
    pre = [0] * (padding)
    prefixit = lambda tup: pre + tup
    return itertools.imap(prefixit, it)

def partitions_with_0(n, m):
    yield [0] * (m-1) + [n]
    if n < m: return
    for i in range(2,m+1):
        for part in partitions(n, i):
            yield [0] * (m-i) + part

def make_table(row, dimensions):
    entry = lambda ks: (ks, pascal_simplex(ks))
    return itertools.imap(entry, partitions_with_0(row, dimensions))

def ks_to_str(ks):
    return ','.join(map(str, ks))

if __name__ == "__main__":
    import sys
    args = sys.argv

    usage = 'USAGE: python %s %s %s' % (args[0], '<row>', '<# dims>')


    if len(args) != 3:
        print >> sys.stderr, usage
        exit()
    else:
        try:
            row = int(args[1])
            dims = int(args[2])
        except:
            print >> sys.stderr, usage
            exit()
            
    t = make_table(row, dims)
    for (ks, v) in t:
        print ks_to_str(ks), v
