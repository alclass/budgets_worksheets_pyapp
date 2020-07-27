#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
import fs.economicfs.financefunctions as finfs


def adhoc_test():
  cell_letter = 'A'; cell_number = 5
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  print (cell_ref)
  cell_ref, letter, number = move_cell_to_right(cell_letter, cell_number)
  print (cell_ref)
  retletter = move_column_to_right(letter)
  print (letter, 'move_column_to_right()', retletter)
  letter = retletter
  retletter = move_column_to_right(letter)
  print (letter, 'move_column_to_right()', retletter)

def process():
  generate_xlsx()
  # adhoc_test()

if __name__ == "__main__":
  process()
