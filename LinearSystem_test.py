import unittest
from LinearSystem import LinearSystem, NoSolutionError
from LinearEquation import LinearEquation

class TestLinearSystem(unittest.TestCase):

    def test_solve_linear_system_simple(self):
        solution = LinearSystem.from_strings(
            'x=10',
        ).solve()
        self.assertEqual(solution, LinearSystem.from_strings(
            'x=10',
        ))


    def test_solve_linear_system_2_terms(self):
        solution = LinearSystem.from_strings(
            'x-y-2=0',
            'x+y-6=0'
        ).solve()
        self.assertEqual(solution, LinearSystem.from_strings(
            'x=4',
            'y=2'
        ))

    def test_solve_linear_system_3_terms(self):
        solution = LinearSystem.from_strings(
            'x-y+z-2=0',
            'x+y+z-6=0',
            '-x+y+z-4=0'
        ).solve()
        self.assertEqual(solution, LinearSystem.from_strings(
            'x=1',
            'y=2',
            'z=3',
        ))

    def test_solve_linear_system_decimal_terms(self):
        solution = LinearSystem.from_strings(
            '5.262x+2.739y-9.878z+3.441=0',
            '5.111x+6.358y+7.638z+2.152=0',
            '2.016x-9.924y-1.367z+9.278=0',
            '2.167x-13.543y-18.883z+10.567=0',
        ).solve()
        self.assertEqual(solution, LinearSystem.from_strings(
            'z=-0.082664',
            'y=0.707151',
            'x=-1.177202',
        ))

    def test_solve_linear_system_parallel_lines(self):
        self.assertRaises(NoSolutionError, lambda: LinearSystem.from_strings(
            'x+y=0',
            'x+y=1',
        ).solve())

if __name__ == '__main__':
    unittest.main()

