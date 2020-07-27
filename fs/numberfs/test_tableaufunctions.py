#!/usr/bin/env python3
'''
Unit Tests for tableaufunctions.py
'''
import unittest
import fs.numberfs.tableaufunctions as tblfs

class TestCaseNumFunctions(unittest.TestCase):

  def test_convert_columnletters_to_number_nonrecursely_n_back(self):
    # 1 forward
    cell_letters = 'a'
    expected_number = 0
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 1 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 2 forward
    cell_letters = 'Ac'
    expected_number = 28
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 2 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 3 forward
    cell_letters = 'CbD'
    expected_number = 3*26**2 + 2*26**1 + 3
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 3 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 4 forward
    cell_letters = 'zead'
    expected_number = 26*26**3 + 5*26**2 + 1*26**1 + 3
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 4 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 5 forward
    cell_letters = 'zz'
    expected_number = 26*26 + 25
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 5 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

  def test_convert_columnletters_to_number_recursely_n_back(self):
    # 1 forward
    cell_letters = 'a'
    expected_number = 0
    returned_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 1 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 2 forward
    cell_letters = 'Ac'
    expected_number = 28
    returned_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 2 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 3 forward
    cell_letters = 'CbD'
    expected_number = 3*26**2 + 2*26**1 + 3
    returned_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 3 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 4 forward
    cell_letters = 'zead'
    expected_number = 26*26**3 + 5*26**2 + 1*26**1 + 3
    returned_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 4 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 5 forward
    cell_letters = 'zz'
    expected_number = 26*26 + 25
    returned_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 5 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

  def test_move_thru_tableau(self):
    cellref = 'a5'; ncolumns = 2; nrows = 3
    expected_cellref = 'c8'.upper()
    returned_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
    self.assertEqual(expected_cellref, returned_cellref)
    cellref = returned_cellref; ncolumns = -2; nrows = -3
    expected_cellref = 'a5'.upper()
    returned_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
    self.assertEqual(expected_cellref, returned_cellref)

    cellref = 'a5'; ncolumns = -1; nrows = 3
    self.assertRaises(IndexError, tblfs.move_cell_along_tableau, cellref, ncolumns, nrows)
    cellref = 'a5'; ncolumns = 3; nrows = -8
    self.assertRaises(IndexError, tblfs.move_cell_along_tableau, cellref, ncolumns, nrows)

    cellref = 'a5'; ncolumns = 0; nrows = 0
    expected_cellref = cellref.upper()
    returned_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
    self.assertEqual(expected_cellref, returned_cellref)

  def test_crossed_convert_columnletters_to_number_recur_n_nonrecur(self):
    # 1 forward
    cell_letters = 'zead'
    rec_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
    nonrec_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(rec_number, nonrec_number)
    # 1 backward
    rec_letters = tblfs.convert_number_to_columnletters_recursively(nonrec_number)
    nonrec_letters = tblfs.convert_number_to_columnletters_nonrecursively(rec_number)
    self.assertEqual(rec_letters, nonrec_letters)
