import unittest
from pathlib import Path
import os, sys, string

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.clean import load_data, process, set_files

class CleanTest(unittest.TestCase):

    def create_env(self, num):
        set_files("./test/fixtures/test_"+str(num)+".json", "outpath")

        load_data()
        processes_data = process()

        return processes_data


    def test_title(self):
        processes_data = self.create_env(1)

        self.assertTrue(not processes_data)

    def test_createdAt(self):
        processes_data = self.create_env(2)

        self.assertTrue(not processes_data)

    def test_invalid_json(self):
        processes_data = self.create_env(3)

        self.assertTrue(not processes_data)

    def test_invalid_author(self):
        processes_data = self.create_env(4)
        
        self.assertTrue(not processes_data)

    def test_invalid_count (self):
        processes_data = self.create_env(5)
        
        self.assertTrue(not processes_data)

    def test_tags (self):
        processes_data = self.create_env(6)
        
        self.assertTrue(len(processes_data[0]['tags']) == 4)

        for i in processes_data[0]['tags']:
            self.assertFalse(' ' in i)

        self.assertTrue(processes_data)


if __name__ == '__main__':
        unittest.main()

