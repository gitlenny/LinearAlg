from LinearExpression import LinearExpression

import unittest
from LinearExpression import LinearExpression

class TestLinearExpression(unittest.TestCase):
    def test_create_expression(self):
        s = '-2x+3y+z+2'
        exp = LinearExpression.from_string(s)
        self.assertEqual(str(exp), s)

    def test_get_vars(self):
        e = LinearExpression.from_string('x+2y-z')
        self.assertEqual(e.vars(), set(['x','y','z']))

    def test_remove_zero_terms(self):
        e = LinearExpression.from_string('x+0y+0z+0')
        e.remove_zero_terms()
        self.assertEqual(str(e), 'x')

    def test_add(self):
        e1 = LinearExpression.from_string('x+2y-z')
        e2 = LinearExpression.from_string('x+2')
        self.assertEqual(str(e1+e2), '2x+2y-z+2')

    def test_sub(self):
        e1 = LinearExpression.from_string('x+2y-z')
        e2 = LinearExpression.from_string('x+2')
        self.assertEqual(str(e1-e2), '2y-z-2')

    def test_mul(self):
        e1 = LinearExpression.from_string('x+2y-z-3')
        self.assertEqual(str(e1*2), '2x+4y-2z-6')

    def test_div(self):
        e1 = LinearExpression.from_string('x+2y-z-3')
        self.assertEqual(str(e1/2), '0.5x+y-0.5z-1.5')

    def test_equals(self):
        self.assertEqual(LinearExpression.from_string('x+y+3'), LinearExpression.from_string('x+y+3'))
        self.assertEqual(LinearExpression.from_string('x+y'), LinearExpression.from_string('y+x'))
        self.assertEqual(LinearExpression.from_string('x+y+3'), LinearExpression.from_string('x+3+y'))
        self.assertEqual(LinearExpression.from_string('x+y+3+3x'), LinearExpression.from_string('4x+1+y+2'))
        self.assertNotEqual(LinearExpression.from_string('x+y'), LinearExpression.from_string('2x+y'))
        self.assertNotEqual(LinearExpression.from_string('x+y'), LinearExpression.from_string('x+y+4'))
        self.assertNotEqual(LinearExpression.from_string('x+y'), LinearExpression.from_string('x+y+z'))

    def test_substitute(self):
        self.assertEqual(LinearExpression.from_string('x+2y+3z').substitute('x', LinearExpression.from_string('2y+4')),
                        LinearExpression.from_string('4y+3z+4'))
        self.assertEqual(LinearExpression.from_string('x+2y+3z').substitute('g', LinearExpression.from_string('2y+4')),
                        LinearExpression.from_string('x+2y+3z'))

if __name__ == '__main__':
    unittest.main()
