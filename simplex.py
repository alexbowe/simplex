import itertools

# use tetrehedral numbers to map simplex to 1D array
t = lambda r, n: (3*n**2 + n**3 * (r - 2) - n*(r-5))/6
f = lambda d,h,v: t(d,h) - t(d,h-v)
def make_mapper(height):
  def map_point(h, v):
    dim = len(v)
    if dim == 1: return v[0]
    return f(dim, h, v[0]) + map_point(h - v[0], v[1:])
  return lambda *v: map_point(height, v)

def num_elements(h, d):
  return binomial(d+h-1, h)

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
        b = binomial(n, k)
        if b is not None:
            product *= b
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
    assert(len(a) == m + 1)

    while True:
        if sum(a[0:-1]) != n: return
        if 0 in a[0:-1]: return
        #assert(sum(a[0:-1]) == n)
        yield a[0:-1]
        if a[1] >= a[0] - 1:
            j = 2
            s = a[0] + a[1] - 1
            while a[j] >= a[0] - 1:
                s = s+a[j]
                j += 1
                if j > m - 1: break
            if j > m -1: break
            else:
                x = a[j] + 1
                a[j] = x
                j -= 1
            while j > 0:
                a[j] = x
                s = s - x
                j -= 1
            a[0] = s
        else:
            a[0] -= 1
            a[1] += 1

def partitions_with_0(n, m):
    if m == 0: return
    if n == 0:
       yield [0] * m
       return
    if n == 1:
        if m > 0:
            yield [0] * (m-1) + [1]
        return
    if m == 1:
        yield [n]
        return
    for i in range(m-1, -1, -1):
        for part in partitions(n, m - i):
            yield [0] * (i) + part

def make_table(row, dimensions):
    entry = lambda ks: (tuple(ks), pascal_simplex(ks))
    return itertools.imap(entry, partitions_with_0(row, dimensions))

def ks_to_str(ks):
    return ','.join(map(str, ks))

make_perms = lambda ks: {}.fromkeys(itertools.permutations(ks)).keys()
def unique_perms(t):
    for ks,v in t:
      for k_perm in make_perms(ks):
        yield k_perm, v

# might be possible to use caching (of upper rows) if performance is needed
# TODO: add graphviz output (as soon as I work out the connectivity)
# I think it is connected if a co-ord differs by +1 in one dimension
# TODO: prettyprint
# TODO: OpenGL point cloud sort of thing (rotate 3d pascal to k rows)
if __name__ == "__main__":
    import sys
    args = sys.argv

    #TODO: use the python cl-args lib so its easy to add pretty print and gl
    usage = 'USAGE: python %s %s %s %s' % (args[0], '<row>', '<# dims>', '[-p]')

    all_perms = False

    if len(args) < 3 or len(args) > 4 or (len(args) == 4 and args[-1] != '-p'):
        print >> sys.stderr, usage
        exit()
    else: 
        try:
            row = int(args[1])
            dims = int(args[2])
            all_perms = (len(args) == 4 and args[-1]=='-p')
        except:
            print >> sys.stderr, usage
            exit()

    t = make_table(row, dims)
    if all_perms:
      t = unique_perms(t)

    for (ks, v) in t:
      print ks_to_str(ks), v
