import copy
import gzip
import os
from pathlib import Path
from pysat.solvers import Glucose3


class CNF(object):
    def __init__(self, from_file=None, from_fp=None, from_string=None,
                 from_clauses=[], from_aiger=None, comment_lead=['c']):

        self.nv = 0
        self.clauses = []
        self.comments = []

        if from_file:
            self.from_file(from_file, comment_lead, compressed_with='use_ext')
        elif from_fp:
            self.from_fp(from_fp, comment_lead)
        # elif from_string:
        #     self.from_string(from_string, comment_lead)
        elif from_clauses:
            self.from_clauses(from_clauses)
        elif from_aiger:
            self.from_aiger(from_aiger)

    def from_file(self, fname, comment_lead=['c'], compressed_with='use_ext'):

        with FileObject(fname, mode='r', compression=compressed_with) as fobj:
            self.from_fp(fobj.fp, comment_lead)

    def from_fp(self, file_pointer, comment_lead=['c']):

        self.nv = 0
        self.clauses = []
        self.comments = []
        comment_lead = tuple('p') + tuple(comment_lead)

        for line in file_pointer:
            line = line.strip()
            if line:
                if line[0] not in comment_lead:
                    cl = [int(l) for l in line.split()[:-1]]
                    self.nv = max([abs(l) for l in cl] + [self.nv])

                    self.clauses.append(cl)
                elif not line.startswith('p cnf '):
                    self.comments.append(line)

    def from_clauses(self, clauses):
        self.clauses = copy.deepcopy(clauses)

        for cl in self.clauses:
            self.nv = max([abs(l) for l in cl] + [self.nv])

    def from_aiger(self, aig, vpool=None):
        pass

    def copy(self):
        cnf = CNF()
        cnf.nv = self.nv
        cnf.clauses = copy.deepcopy(self.clauses)
        cnf.comments = copy.deepcopy(self.comments)

        return cnf

    def to_file(self, fname, comments=None, compress_with='use_ext'):

        with FileObject(fname, mode='w', compression=compress_with) as fobj:
            self.to_fp(fobj.fp, comments)

    def to_fp(self, file_pointer, comments=None):

        # saving formula's internal comments
        for c in self.comments:
            print(c, file=file_pointer)

        # saving externally specified comments
        if comments:
            for c in comments:
                print(c, file=file_pointer)

        print('p cnf', self.nv, len(self.clauses), file=file_pointer)

        for cl in self.clauses:
            print(' '.join(str(l) for l in cl), '0', file=file_pointer)

    def append(self, clause):
        self.nv = max([abs(l) for l in clause] + [self.nv])
        self.clauses.append(list(clause))

    def extend(self, clauses):
        for cl in clauses:
            self.append(cl)

    def __iter__(self):
        for cl in self.clauses:
            yield cl

    def negate(self, topv=None):
        negated = CNF()

        negated.nv = topv
        if not negated.nv:
            negated.nv = self.nv

        negated.clauses = []
        negated.auxvars = []

        for cl in self.clauses:
            auxv = -cl[0]
            if len(cl) > 1:
                negated.nv += 1
                auxv = negated.nv

                # direct implication
                for l in cl:
                    negated.clauses.append([-l, -auxv])

                # opposite implication
                negated.clauses.append(cl + [auxv])

            # keeping all Tseitin variables
            negated.auxvars.append(auxv)

        negated.clauses.append(negated.auxvars)
        return negated



class FileObject(object):

    def __init__(self, name, mode='r', compression=None):
        self.fp = None  # file pointer to give access to
        self.ctype = None  # compression type

        # in some cases an additional file pointer is needed
        self.fp_extra = None

        self.open(name, mode=mode, compression=compression)

    def open(self, name, mode='r', compression=None):

        if compression == 'use_ext':
            self.get_compression_type(name)
        else:
            self.ctype = compression

        if not self.ctype:
            self.fp = open(name, mode)
        elif self.ctype == 'gzip':
            self.fp = gzip.open(name, mode + 't')


    def close(self):
        if self.fp:
            self.fp.close()
            self.fp = None

        if self.fp_extra:
            self.fp_extra.close()
            self.fp_extra = None

        self.ctype = None

    def get_compression_type(self, file_name):
        ext = os.path.splitext(file_name)[1]

        if ext == '.gz':
            self.ctype = 'gzip'
        elif ext == '.bz2':
            self.ctype = 'bzip2'
        elif ext in ('.xz', '.lzma'):
            self.ctype = 'lzma'
        else:
            self.ctype = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
#


if __name__ == '__main__':
    filename = Path('./edusat/edusat/test/unsat/unsat.cnf')
    my_CNF = CNF(from_file=filename)
    print(my_CNF)
    g = Glucose3(my_CNF)
    print(g.solve())
    print(g.get_model())
