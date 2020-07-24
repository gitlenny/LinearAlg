from decimal import Decimal, getcontext
from constants import ALMOST_ZERO, DECIMAL_PRECISION
import copy

getcontext().prec = DECIMAL_PRECISION


def formatDecimal(d):
    return format(d, '+.6f').rstrip('0').rstrip('.')


def renderTerm(v, coe):
    abscoe = abs(coe)
    if abscoe < ALMOST_ZERO:
        return ''
    
    if v == '1':
        return formatDecimal(coe)

    if abscoe == 1:
        return ('+' if coe > 0 else '-') + v
    else:
        return formatDecimal(coe) + v


class LinearExpression:
    def __init__(self, terms):
        self.terms = terms


    @classmethod
    def from_string(cls, s):
        return cls(terms = cls.parse(s))

    @staticmethod
    def parse(s):
        terms = {}
        if s == None:
            return terms
        s = s.replace(' ', '')
        s = s.replace('-', '+-')
        if s[0] == '+': #special case for when first term is negative
            s = s[1:]
        for term in s.split('+'):
            if term[-1].isalpha():
                var = term[-1]
                coe = term[:-1]
            else:
                var = '1'
                coe = term
            
            if coe == '':
                coe = '1'
            elif coe == '-':
                coe = '-1'

            if coe != '0':
                if var in terms:
                    terms[var] += Decimal(coe)
                else:
                    terms[var] = Decimal(coe)
        return terms


    def __str__(self):
        result = ''
        for var in self.sorted_keys():
            result += renderTerm(var, self.terms[var])
        if result == '':
            result = '0'
        if result[0] == '+':
            result = result[1:]            
        return result
    

    def __repr__(self):
        return "LinearExpression('{0}')".format(self.__str__())


    def __eq__(self, exp2):
        if self.sorted_keys() != exp2.sorted_keys():
            return False
        for v, coe in self.terms.items():
            if abs(coe-exp2.terms[v]) > ALMOST_ZERO:
                return False
        return True

    def vars(self):
        return set([var for var in self.terms.keys() if var != '1'])

    def sorted_keys(self):
        keys = sorted(self.terms.keys())
        if keys and keys[0] == '1':
            del keys[0]
            keys.append('1')
        return keys
    
    def clone(self):
        return LinearExpression(terms=copy.deepcopy(self.terms))

    def __add__(self, e2):
        result = self.clone()
        for var,coe in e2.terms.items():
            if var in result.terms:
                result.terms[var] += coe
            else:
                result.terms[var] = coe
        result.remove_zero_terms()
        return result

    def __sub__(self, e2):
        return self + (e2 * -1)

    def __mul__(self, scalar):
        result = self.clone()
        for var in result.terms.keys():
            result.terms[var] *= scalar
        return result

    def __truediv__(self, scalar):
        result = self.clone()
        for var in result.terms.keys():
            result.terms[var] /= scalar
        return result

    def remove_zero_terms(self):
        self.terms = {var:coe for (var,coe) in self.terms.items() if abs(coe) > ALMOST_ZERO}


    def substitute(self, var, expression):
        eq = self.clone()
        if not var in self.terms:
            return eq
        coe = eq.terms.pop(var, 0)
        if abs(coe) < ALMOST_ZERO:
            return eq

        for v, c in expression.terms.items():
            if v in eq.terms:
                eq.terms[v] += c * coe
            else:
                eq.terms[v] = c * coe
        
        eq.remove_zero_terms()
        
        if not eq.terms:
            return LinearExpression.from_string('0')

        return eq
