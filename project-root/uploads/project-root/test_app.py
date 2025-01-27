import unittest
from app import allowed_file, list_tables  # Importa las funciones a probar

class TestApp(unittest.TestCase):
    # Prueba para allowed_file
    def test_allowed_file(self):
        self.assertTrue(allowed_file('data.csv'))
        self.assertTrue(allowed_file('report.xlsx'))
        self.assertFalse(allowed_file('image.jpg'))
        self.assertFalse(allowed_file('document'))

    # Prueba para list_tables
    def test_list_tables(self):
        tables = list_tables()
        self.assertIn('alumnos3', tables)
        self.assertIn('grades', tables)


if __name__ == '__main__':
    unittest.main()
