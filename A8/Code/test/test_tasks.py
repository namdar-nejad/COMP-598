import unittest
from unittest import TestCase
# from unittest import assertion
from pathlib import Path
import os, sys, json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.compile_word_counts import load_stop_words, count, write_dict, FINAL_DICT
from src.compute_pony_lang import process, load_pony_count, PONY_WORDS_DICT


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
    
        
    def test_task1(self):

        # load true_word_counts
        with open(self.true_word_counts, "r") as json_file:
            true_counts_dict = json.load(json_file)

        # load stopwords 
        load_stop_words()

        # process file and count words
        count(self.mock_dialog)

        # check if the two dicts contaning the word counts are the same
        self.assertDictEqual(true_counts_dict, FINAL_DICT)

    def test_task2(self):

        # load true_tf_idfs
        with open(self.true_tf_idfs, "r") as json_file:
            true_idfs_dict = json.load(json_file)

        num_words = 4

        # load true_word_counts
        load_pony_count(self.true_word_counts)
        
        # process the word counds and create a dict contaning the idfs
        rtn_dict = process(num_words)

        # check if the two dicts contaning the idfs are the same
        self.assertDictEqual(true_idfs_dict, rtn_dict)
        
    
if __name__ == '__main__':
    unittest.main()