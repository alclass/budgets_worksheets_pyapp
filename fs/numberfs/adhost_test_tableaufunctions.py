#!/usr/bin/env python3
'''
  Adhoc Tests to tableaufunctions.py
  See also the unit tests in folder under its conventioned filename.
'''
import fs.numberfs.tableaufunctions as tblfs


def adhoc_test0():
  cell_letters = 'a'
  nonrec_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  nonrec_number)
  returned_letters = tblfs.convert_number_to_columnletters_nonrecursively(nonrec_number)
  print(nonrec_number, '(recurse) =>',  returned_letters, 'expected', nonrec_number)

def adhoc_test1():
  cell_letters = 'zead'
  rec_number = tblfs.convert_columnletters_to_number_recursively(cell_letters)
  print(cell_letters, '(recurse) =>',  rec_number)
  nonrec_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  nonrec_number)
  expected_number = 26*26**3 + 5*26**2 + 1*26**1+ 3
  returned_letters = tblfs.convert_number_to_columnletters_recursively(nonrec_number)
  print(nonrec_number, '(recurse) =>',  returned_letters, 'expected', expected_number)
  returned_letters = tblfs.convert_number_to_columnletters_nonrecursively(nonrec_number)
  print(nonrec_number, '(nonrecurse) =>',  returned_letters, 'expected', expected_number)

def adhoc_test2():
  cellref = 'A3'; ncolumns = 4
  next_cellref = tblfs.move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  cellref = next_cellref; ncolumns = -4
  next_cellref = tblfs.move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  ncolumns = 7; nrows = 3
  next_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
  print ('cellref', cellref, 'move ncolumns', ncolumns, 'move nrows', nrows, 'results in', next_cellref)
  cellref = next_cellref
  ncolumns = -7; nrows = -3
  next_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
  print ('cellref', cellref, 'move ncolumns', ncolumns, 'move nrows', nrows, 'results in', next_cellref)
  # cellref = next_cellref; ncolumns = 34
  # next_cellref = move_cell_along_columns(cellref, ncolumns)
  cellref = 'A3'; ncolumns = 26+4
  next_cellref = tblfs.move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  cellref = 'A3'; ncolumns = 26*26+26+4
  next_cellref = tblfs.move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  cell_letters = 'D'
  n = tblfs.convert_columnletters_to_number_recursively(cell_letters)
  cell_letters = 'AA'
  n = tblfs.convert_columnletters_to_number_recursively(cell_letters)
  print (cell_letters, '=>', n)
  cell_letters = tblfs.convert_number_to_columnletters_recursively(n)
  print (n, '=>', cell_letters)
  cell_letters = 'CB'
  n = tblfs.convert_columnletters_to_number_recursively(cell_letters)
  print (cell_letters, '=>', n)
  cell_letters = tblfs.convert_number_to_columnletters_recursively(n)
  print (n, '=>', cell_letters)
  '''
  cellref = next_cellref; ncolumns = -(26*26+26+4)
  next_cellref = move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  '''

def adhoc_test3():
  column_as_number = 0 # 'A'
  letters = tblfs.convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (1*26)+0 # 'AA'
  letters = tblfs.convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (1*26)+1 # 'AB'
  letters = tblfs.convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (2*26*26)+((3-1)*26)+(4-1) # 'BCD'
  letters = tblfs.convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (2*26*26)+(0*26)+3 # 'BAD'
  letters = tblfs.convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  cell_letters = 'AC'
  n = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse =>', n)
  cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(n)
  print(n, '(nonrecurse) =>',  cell_letters)
  n = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse =>', n)
  cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(n)
  print(n, '(nonrecurse) =>',  cell_letters)
  cell_letters = 'DBC'
  n = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse =>', n)
  cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(n)
  print(n, '(nonrecurse) =>',  cell_letters)

def adhoc_test4():
  '''
  cell_letters = 'zeaD'
  returned_number = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  returned_number)
  expected_number = 26 * 26 ** 3 + 5 * 26 ** 2 + 1 * 26 ** 1 + 3
  returned_letters = convert_number_to_columnletters_nonrecursively(returned_number)
  print(returned_number, '(nonrecurse) =>',  returned_letters)

  :return:
  '''
  # 4 forward
  cell_letters = 'zz'
  returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  returned_number)
  expected_number = 26*26 + 25
  returned_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
  print(returned_number, '(nonrecurse) =>',  returned_letters)

def adhoc_test5():
  # 2 forward
  cell_letters = 'zead'
  returned_number = tblfs.convert_columnletters_to_number_recursively_entrance(cell_letters)
  print(cell_letters, ' to number =>', returned_number)
  returned_cell_letters = tblfs.convert_number_to_columnletters_recursively(returned_number)
  print(returned_number, ' back to letters =>', returned_cell_letters)

  cell_letters = 'zead'
  returned_number = tblfs.convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, ' nonrec to number =>', returned_number)
  returned_cell_letters = tblfs.convert_number_to_columnletters_nonrecursively(returned_number)
  print(returned_number, ' nonrec back to letters =>', returned_cell_letters)

  cellref = 'b5'; ncolumns = -1; nrows = 3
  next_cellref = tblfs.move_cell_along_tableau(cellref, ncolumns, nrows)
  print(cellref, ' next_cellref =>', next_cellref)

def adhoc_test6():

  # 1 foward
  cell_letters = 'z';
  ncolumns = 26 * 26 ** 3 + 26
  mid_letters = tblfs.move_columns_by(cell_letters, ncolumns)
  ncolumns = 26 * 26 ** 5 + 26 * 26 ** 2 + 26 * 26 ** 1
  next_cell_letters = tblfs.move_columns_by(mid_letters, ncolumns)
  print('1 forward', cell_letters, '| mid =', mid_letters, '| next_cellref =>', next_cell_letters)
  # 1 backward
  cell_letters = 'UODRTA';
  ncolumns = 26 * 26 ** 5 + 26 * 26 ** 2 + 26 * 26 ** 1
  ncolumns = (-1) * ncolumns
  mid_letters = tblfs.move_columns_by(cell_letters, ncolumns)
  ncolumns = 26 * 26 ** 3 + 26
  ncolumns = (-1) * ncolumns
  next_cell_letters = tblfs.move_columns_by(mid_letters, ncolumns)
  print('1 backward', cell_letters,'| mid =', mid_letters, '| next_cellref =>', next_cell_letters)

def process():
  functionname_interpol = 'adhoc_test%d()'
  for i in range(7):
    functionname = functionname_interpol %i
    print('-'*40)
    print( 'Executing ', functionname)
    print('-'*40)
    eval(functionname)


if __name__ == "__main__":
  process()

