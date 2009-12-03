# Copyright David Abrahams 2009. Distributed under the Boost
# Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import hashlib, cPickle 

# A map from sha1 hash to stored object
unsha = {}

hashtype = type(hashlib.sha1(''))

def sha1(x):
    if isinstance(x,hashtype):
        return x
    result = hashlib.sha1(
        x if isinstance(x, str) else cPickle.dumps(x))
    if not unsha.has_key(result):
        #print 'storing',x,'as',result.hexdigest()
        unsha[result] = x
    return result

class stored(object):
    def __getattribute__(self, name):
        x = object.__getattribute__(self, name)
        return unsha[x] if isinstance(x, hashtype) else x

    def __setattr__(self, name, x):
        object.__setattr__(
            self, name, 
            x if isinstance(x,hashtype) else sha1(x))

    def __hash__(self):
        return hash(hashlib.sha1(cPickle.dumps(self)).digest())

class tree(stored):
    def __init__(self, children):
        self.children = dict([ (sha1(obj),sha1(metadata)) for obj,metadata in children ])

class blob(stored):
    def __init__(self, content):
        self.content = sha1(content)

class commit(stored):
    def __init__(self, tree, parents):
        self.tree = tree
        self.parents = set( [ sha1(x) for x in parents ] )

class repo(object):
    def __init__(self):
        self.refs = []
        self.commits = set() # All commits in the repository
        self.index_tree = None
        self.HEAD = None
        self.index_parents = set()

def contents(x):
    if isinstance(x, file): 
        return x.read()
    return x

class git(object):
    @staticmethod
    def hash_object(s):
        '''
        >>> greeting = 'Hello, World!'
        >>> git.hash_object(greeting)
        >>> 0a0a9f2a6772942557ab5355d76af442f8f65e01
        '''
        return hashlib.sha1(s.read() if isinstance(s,file) else s).hexdigest()

    @staticmethod
    def init():
        git.repo = repo()

    @staticmethod
    def add(path):

def gftbu():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    gftbu()
