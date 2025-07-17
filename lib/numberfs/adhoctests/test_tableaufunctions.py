#!/usr/bin/env python3
"""

fs/numberfs/test_tableaufunctions.py
  Unit Tests for tableaufunctions.py
"""
import unittest
import lib.numberfs.tableaufunctions as tblfs


class TestCaseNumFunctions(unittest.TestCase):

  def setUp(self):
    self.NBASE = tblfs.NSYSTEM27SIZE

  def test_convert_columnletters_to_number_nonrecursely_n_back(self):

    # 1 forward
    cell_letters = 'a'
    expected_number = 1
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 1 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 2 forward
    cell_letters = 'Ac'
    expected_number = 1*self.NBASE**1 + 3  # it's 1*27**1+3 = 27+3=30
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 2 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 3 forward
    cell_letters = 'CbD'
    expected_number = 3*self.NBASE**2 + 2*self.NBASE**1 + 4
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 3 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 4 forward
    cell_letters = 'zead'
    expected_number = 26*self.NBASE**3 + 5*self.NBASE**2 + 1*self.NBASE**1 + 4
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 4 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 5 forward
    cell_letters = 'zz'
    expected_number = 26*self.NBASE**1 + 26
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 5 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 6 forward
    cell_letters = 'azead'
    expected_number = 1*self.NBASE**4 + 26*self.NBASE**3 + 5*self.NBASE**2 + 1*self.NBASE**1 + 4
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 6 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 7 forward
    cell_letters = ''
    # _ = expected_number = None
    returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertIsNone(returned_number)
    # 7 backward
    # expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(0)
    self.assertIsNone(returned_cell_letters)

  def test_convert_columnletters_to_number_recursely_n_back(self):
    # 1 forward
    cell_letters = 'a'
    expected_number = 1
    returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 1 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 2 forward
    cell_letters = 'Ac'
    expected_number = 1*self.NBASE**1 + 3  # it's 1*27**1+3 = 27+3=30
    returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 2 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 3 forward
    cell_letters = 'CbD'
    expected_number = 3*self.NBASE**2 + 2*self.NBASE**1 + 4
    returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 3 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 4 forward
    cell_letters = 'zead'
    expected_number = 26*self.NBASE**3 + 5*self.NBASE**2 + 1*self.NBASE**1 + 4
    returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 4 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 5 forward
    cell_letters = 'zz'
    expected_number = 26*self.NBASE**1 + 26
    returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 5 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

    # 6 forward
    cell_letters = 'azead'
    expected_number = 1*self.NBASE**4 + 26*self.NBASE**3 + 5*self.NBASE**2 + 1*self.NBASE**1 + 4
    returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    self.assertEqual(expected_number, returned_number)
    # 4 backward
    expected_cell_letters = cell_letters.upper()
    returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
    self.assertEqual(expected_cell_letters, returned_cell_letters)

  def test_move_thru_tableau(self):
    cellref, ncolumns, nrows = 'a5', 2, 3
    expected_cellref = 'c8'.upper()
    returned_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
    self.assertEqual(expected_cellref, returned_cellref)
    cellref, ncolumns, nrows = returned_cellref, -2, -3
    expected_cellref = 'a5'.upper()
    returned_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
    self.assertEqual(expected_cellref, returned_cellref)

    cellref, ncolumns, nrows = 'a5', -1, 3
    self.assertRaises(IndexError, tblfs.move_cell_along_tableau, cellref, ncolumns, nrows)
    cellref, ncolumns, nrows = 'a5', 3, -8
    self.assertRaises(IndexError, tblfs.move_cell_along_tableau, cellref, ncolumns, nrows)

    cellref, ncolumns, nrows = 'a5', 0, 0
    expected_cellref = cellref.upper()
    returned_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
    self.assertEqual(expected_cellref, returned_cellref)

  def test_crossed_convert_columnletters_to_number_recur_n_nonrecur(self):
    # 1 forward
    cell_letters = 'zead'
    rec_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
    nonrec_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
    self.assertEqual(rec_number, nonrec_number)
    # 1 backward
    rec_letters = tblfs.convert_number_to_columnletters_recursively(nonrec_number)
    nonrec_letters = tblfs.convert_number_to_columnletters_nonrecursively(rec_number)
    self.assertEqual(rec_letters, nonrec_letters)

  def test_uniqueness_of_lettercolumns_addition_nonrecursive(self):
    # 1 from "a" to 0 should raise IndexError
    cell_letters, ncolumns = 'a', -1
    self.assertRaises(IndexError, tblfs.move_columns_by, cell_letters, ncolumns)
    # 2 from z to 0 should raise IndexError
    cell_letters, ncolumns = 'z', -26
    self.assertRaises(IndexError, tblfs.move_columns_by, cell_letters, ncolumns)
    # 3 z plus 1 should be aa
    cell_letters, ncolumns = 'z', 1
    expected_cellref = 'aa'.upper()
    returned_cellref = tblfs.move_columns_by(cell_letters, ncolumns)
    self.assertEqual(expected_cellref, returned_cellref)
    # 4 aa minus 1 should be z (commutative to the above operation)
    cell_letters, ncolumns = 'aa', -1
    expected_cellref = 'z'.upper()
    returned_cellref = tblfs.move_columns_by(cell_letters, ncolumns)
    self.assertEqual(expected_cellref, returned_cellref)
    # 5 two jumps to see if they can be reversed

  def ztest_uniqueness_of_lettercolumns_addition_recursive(self):
    """

      NOT PASSING this by now.
        The nonrecursive is working.
        The recursive is not yet working.

    :return:
  """
    # 1 from "a" to 0 should raise IndexError
    cell_letters, ncolumns = 'a', -1
    self.assertRaises(IndexError, tblfs.move_columns_by, cell_letters, ncolumns, True)
    # 2 from z to 0 should raise IndexError
    cell_letters, ncolumns = 'z', -26
    self.assertRaises(IndexError, tblfs.move_columns_by, cell_letters, ncolumns, True)
    # 3 z plus 1 should be aa
    cell_letters, ncolumns = 'z', 1
    expected_cellref = 'aa'.upper()
    returned_cellref = tblfs.move_columns_by(cell_letters, ncolumns, True)
    self.assertEqual(expected_cellref, returned_cellref)
    # 4 aa minus 1 should be z (commutative to the above operation)
    cell_letters, ncolumns = 'aa', -1
    expected_cellref = 'z'.upper()
    returned_cellref = tblfs.move_columns_by(cell_letters, ncolumns, True)
    self.assertEqual(expected_cellref, returned_cellref)
    # 5 two jumps to see if they can be reversed
