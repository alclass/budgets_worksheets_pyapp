#!/usr/bin/env python3
import os, pathlib
import xlsxwriter
import fs.economicfs.financefunctions as finfs
'''
MonetCorrNT = coll.namedtuple('MonetCorrNamedTuple',
                'ini_montant, fin_montant, '
                'ini_rate, fin_rate, '
                'corr_fraction, '
                'ini_date, fin_date, '
                'ret_ini_date, ret_fin_date'
              )

'''

dataitems = []
item = ('2018-7-11', 123)
dataitems.append(item)
item = ('2019-3-11', 1234)
dataitems.append(item)
item = ('2019-11-12', 1234)
dataitems.append(item)

def write_header(worksheet):
  worksheet.write('B3', 'Correção Monetária dos Preços Históricos')
  worksheet.write('B5', 'Data')
  worksheet.write('C5', 'Preço')
  worksheet.write('D5', 'Valor do Dólar')
  worksheet.write('E5', 'Data do Câmbio')
  worksheet.write('F5', 'Índice de Correção')
  worksheet.write('G5', 'Valor Corrigido')

import string

def move_column_to_right(cell_letter):
  cell_letter = cell_letter.upper()
  i = string.ascii_uppercase.index(cell_letter)
  next_i = i + 1 % len(string.ascii_uppercase)
  next_letter = string.ascii_uppercase[next_i]
  return next_letter

def move_cell_to_right(cell_letter, nrow):
  next_letter = move_column_to_right(cell_letter)
  cell_ref = next_letter + str(nrow)
  return cell_ref, next_letter, nrow

def write_row(cell_letter, cell_number, worksheet, monet_corr_nt):
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.ini_date)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.ret_ini_date)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.ini_montant)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.ini_rate)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.fin_rate)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.corr_fraction)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.ret_fin_date)
  cell_ref, cell_letter, cell_number = move_cell_to_right(cell_letter, cell_number)
  worksheet.write(cell_ref, monet_corr_nt.fin_montant)
  return cell_letter, cell_number

# 'hello.xlsx'
xlsx_filename = 'correção_monetária.xlsx'
def generate_xlsx():
  workbook = xlsxwriter.Workbook(xlsx_filename)
  worksheet = workbook.add_worksheet()
  write_header(worksheet)
  cell_number = 5
  for date_n_montant in dataitems:
    ini_date, ini_montant = date_n_montant
    monet_corr_nt = finfs.monetarily_correct_by_exchange_rate(ini_montant=ini_montant, ini_date=ini_date)
    cell_number += 1
    _, _ = write_row('A', cell_number, worksheet, monet_corr_nt)
  workbook.close()

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
