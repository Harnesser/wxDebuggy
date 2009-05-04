#! /usr/bin/env python

def gen1():
    """ A generator"""
    i=0
    while i < 300:
        yield i
        i += 30
        
def gen2():
    """ A generator on a generator"""
    for num in gen1():
        yield num+1
        
def gen1_list():
    """ A generator returning a list"""
    a = [1,2,3,4,5]
    while a[0] < 30:
        yield a
        for i in xrange(len(a)):
            a[i] += 5


def gen2_list():
    for mylist in gen1_list():
        mylist.append(34)
        yield mylist
                    
if __name__ == '__main__':
    for num in gen2():
        print num
        
    for mylist in gen2_list():
        print mylist
