import unittest
from LinearEquation import LinearEquation
from LinearExpression import LinearExpression

class TestLinearEquation(unittest.TestCase):
    def test_create_equation(self):
        s = '-2x+3y+z+2=x+y+10'
        eq = LinearEquation.from_string(s)
        self.assertEqual(str(eq), s)

    def test_get_vars(self):
        eq = LinearEquation.from_string('x+2y-z=a+b+x')
        self.assertEqual(eq.vars(), set(['a','b','x','y','z']))

    def test_solve_for(self):
        self.assertEqual(str(LinearEquation.from_string('x+y-6=0').solve_for('y')), 'y=-x+6')
        self.assertEqual(str(LinearEquation.from_string('x+2y-z=a+b+x').solve_for('z')), 'z=-a-b+2y')

    def test_zero_form(self):
        eq = LinearEquation.from_string('x+2y-z=a+b+x').zero_form()
        self.assertEqual(str(eq), '-a-b+2y-z=0')
        eq = LinearEquation.from_string('x+y-6=0').zero_form()
        self.assertEqual(str(eq), 'x+y-6=0')

    def test_is_consistent(self):
        self.assertTrue(LinearEquation.from_string('1=1').is_consistent())
        self.assertFalse(LinearEquation.from_string('1=0').is_consistent())

    def test_equation_equals(self):
        self.assertEqual(LinearEquation.from_string('x+y=3'), LinearEquation.from_string('x+y=3'))
        self.assertEqual(LinearEquation.from_string('y=3-x'), LinearEquation.from_string('y=3-x'))
        self.assertNotEqual(LinearEquation.from_string('x+y=3'), LinearEquation.from_string('x+z=3'))
        self.assertNotEqual(LinearEquation.from_string('x+y=3'), LinearEquation.from_string('x+y=4'))
        self.assertNotEqual(LinearEquation.from_string('x+y=3'), LinearEquation.from_string('x+2y=3'))
        
    def test_substitute(self):
        self.assertEqual(LinearEquation.from_string('x+y=3').substitute('x', LinearExpression.from_string('y-2')), 
                        LinearEquation.from_string('2y-2=3'))

if __name__ == '__main__':
    unittest.main()
