__author__ = 'S Hinse'
s = 'accelerate'
t = 'adventure'
print s[0:3] + t[3:]

print('Hello {}, you reached {} of {}points'.format('Thomas', 87, 100))
d = 12
print('Hello {fname:s}, you reached\
{yp:d} of {tp:7} points'.
      format(fname='Thomas', yp=87, tp=100))


def halloWelt(name):
    print "Hallo Welt, " + name


halloWelt("sven")


def median(a, b, c):
    median = ( a + b + c ) / 3
    return median


print median(1.0, 2, 31)