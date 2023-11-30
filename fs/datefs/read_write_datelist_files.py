#!/usr/bin/env python3
"""
fs/datefs/read_write_datelist_files.py
"""
import copy
import os
import fs.datefs.introspect_dates as intr
import fs.datefs.from_to_convert_date_formats as fromto
import fs.os.sufix_incrementor as sfx_incr
# import fs.datefs.datefunctions as dtfs
import settings as sett
DEFAULT_TXT_INPUT_DATES_FILENAME = 'datesfile.txt'
DEFAULT_TXT_OUTPUT_DATES_FILENAME = 'datesfile_processed_to_norm_yyyy-mm-dd.txt'


def fetch_wordlist_from_textfile_w_filepath(filepath=None):
  """
  gets a list of words from the text inside filepath
  """
  if filepath is None or not os.path.isfile(filepath):
    return []
  text = open(filepath).read()
  lines = text.split('\n')
  strdatelist = []
  for line in lines:
    words = line.split(' ')
    words = list(map(lambda e: e.strip('\t\r\n'), words))
    # notice that words itself is an iterable/list, so the list-comprehension below
    # will help pick up the elment(s) to be appended to strdatelist
    _ = [strdatelist.append(word) for word in words]
  return strdatelist


def fetch_dates_from_textfile_w_filepath(filepath=None):
  # notice that dates may be in some different formats (eg "2021-01-21" or "21/1/2021")
  # but they must all be converted to type datetime.date
  strdatelist = fetch_wordlist_from_textfile_w_filepath(filepath)
  datelist = intr.introspect_n_convert_strdatelist_to_dates(strdatelist)
  datelist = sorted(filter(lambda e: e is not None, datelist))
  return sorted(datelist)


def form_datesfilepath_from_datafolder_w_filename(p_filename=None):
  filename = p_filename or DEFAULT_TXT_INPUT_DATES_FILENAME
  folderpath = sett.get_datafolder_abspath()
  filepath = os.path.join(folderpath, filename)
  return filepath


def form_default_output_datesfilepath(p_folderpath=None, p_filename=None, followsuffix=True):
  filename = p_filename or DEFAULT_TXT_OUTPUT_DATES_FILENAME
  folderpath = p_folderpath
  if folderpath is None:
    folderpath = sett.get_datafolder_abspath()
  if not os.path.exists(folderpath):
    os.makedirs(folderpath)
  filepath = os.path.join(folderpath, filename)
  if os.path.exists(filepath):
    if not followsuffix:
      error_msg = f"""Output file {filename} already exists in folder:
      => [{folderpath}]
      Please, remove it """
      raise OSError(error_msg)
    else:
      filepath = sfx_incr.get_filepath_if_available_or_increment_numbersufix(filepath)
  return filepath


def get_datesfilepath_from_datafolder_w_filename(p_filename=None):
  filepath = form_datesfilepath_from_datafolder_w_filename(p_filename)
  if not os.path.isfile(filepath):
    error_msg = 'File does not exist [%s].' % str(filepath)
    raise OSError(error_msg)
  return filepath


def get_default_datesfilepath():
  return get_datesfilepath_from_datafolder_w_filename()


def save_without_existence_check_text_to_file(text, output_filepath):
  fd = open(output_filepath, 'w', encoding='utf-8')
  fd.write(text)
  fd.close()
  return output_filepath


def save_without_existence_check_genarator_to_file(genfunc, output_filepath):
  fd = open(output_filepath, 'w', encoding='utf-8')
  n_lines = 0
  for word in genfunc():
    line = f"{str(word)}\n"
    n_lines += 1
    fd.write(line)
  fd.close()
  return n_lines


class DateFileReaderWriter:

  def __init__(self, input_filepath=None, output_filepath=None):
    self.input_filepath, self.output_filepath = input_filepath, output_filepath
    self.treat_filepaths()
    self.orginal_strdatelist = None
    self.strdatelist = None
    self.n_dates_gencounted = 0
    self.bool_generator_ongoing = False  # either datelist is taken all at once or 'generated'
    self.bool_generator_has_run = False
    self.datelist = None
    self.sep = None  # it's either - (dash), / (forward slash) or . (dot)
    self.orderpos = None  # it's either ymd, ydm, dmy or mdy
    self.read_datefile_n_set_sep_n_orderpos()
    self.introspect_seq_n_orderpos_from_datelist()

  def treat_filepaths(self):
    self.treat_input_filepath()
    self.treat_output_filepath()

  @property
  def input_filename(self):
    return os.path.split(self.input_filepath)[-1]

  @property
  def input_folderpath(self):
    return os.path.split(self.input_filepath)[0]

  @property
  def output_filename(self):
    if self.output_filepath:
      return os.path.split(self.output_filepath)[-1]
    return None

  @property
  def output_folderpath(self):
    if self.output_filepath:
      return os.path.split(self.output_filepath)[0]
    return None

  def treat_input_filepath(self):
    if self.input_filepath is None:
      self.input_filepath = get_default_datesfilepath()
    if not os.path.isfile(self.input_filepath):
      error_msg = f"""Input dates file {self.input_filename} does not exist.
      In folderpath = {self.input_folderpath}
      Please, make the file available in the above folder and rerun."""
      raise OSError(error_msg)

  def treat_output_filepath(self):
    if self.output_filepath is None:
      self.output_filepath = form_default_output_datesfilepath()
    if os.path.exists(self.output_filepath):
      self.output_filepath = sfx_incr.get_filepath_if_available_or_increment_numbersufix(self.output_filepath)

  @property
  def n_dates(self):
    if self.datelist and iter(self.datelist):
      return len(self.datelist)
    if self.bool_generator_has_run:
      return self.n_dates_gencounted
    return 0

  def introspect_seq_n_orderpos_from_datelist(self):
    self.sep, self.orderpos = intr.find_sep_n_posorder_from_a_strdatelist(self.strdatelist)

  def read_datefile_n_set_sep_n_orderpos(self):
    self.orginal_strdatelist = fetch_wordlist_from_textfile_w_filepath(self.input_filepath)
    self.strdatelist = copy.copy(self.orginal_strdatelist)
    sep, orderpos = intr.find_sep_n_posorder_from_a_strdatelist(self.strdatelist)
    folderpath, filename = os.path.split(self.input_filepath)
    if sep is None:
      folderpath, filename = os.path.split(self.input_filepath)
      error_msg = f"""The three (3) possible strdate separators were not found.
      Separators are: {intr.STRDATE_SEPARATORS}
      input file is {filename} in:
        => {folderpath}
      """
      raise ValueError(error_msg)
    if orderpos is None:
      error_msg = f"""The four (3) possible date field positionings were not found.
      There are: {intr.ORDERPOS_TOKENS_AVAILABLE}
      input file is {filename} in:
        => {folderpath}
      """
      raise ValueError(error_msg)

  def join_datelist_as_text_or_none(self):
    if self.datelist and len(self.datelist) > 0:
      strdatelist = list(map(lambda e: str(e), self.datelist))
      text = '\n'.join(strdatelist)
      return text
    return None

  def save_output_datelist_to_file(self):
    scrmsg = f"""Saving file {self.output_filename}" in
    => {self.output_folderpath}"""
    print(scrmsg)
    text = self.join_datelist_as_text_or_none()
    if text:
      _ = save_without_existence_check_text_to_file(text, self.output_filepath)
      n_lines = self.n_dates
    else:
      # second option, go through the generator
      genfunc = self.gen_dates_converting_one_by_one
      n_lines = save_without_existence_check_genarator_to_file(genfunc, self.output_filepath)
    print(f'Saved n_dates {self.n_dates} | n_lines {n_lines} lines')
    return True

  def get_dates_converting_all_at_once(self, sort_them=True):
    self.bool_generator_ongoing = False
    words_to_del = []
    self.datelist = []
    for word in self.strdatelist:
      pdate = fromto.convert_strdate_to_date_or_none_w_sep_n_fieldorder(word, self.sep, self.orderpos)
      if pdate is None:
        words_to_del.append(word)
        continue
      self.datelist.append(pdate)
    for word in words_to_del:
      self.strdatelist.remove(word)
    if sort_them:
      sorted(self.datelist)
    return self.datelist

  def gen_dates_converting_one_by_one(self):
    self.bool_generator_ongoing = True
    words_to_del = []
    for word in self.strdatelist:
      pdate = fromto.convert_strdate_to_date_or_none_w_sep_n_fieldorder(word, self.sep, self.orderpos)
      if pdate is None:
        words_to_del.append(word)
        continue
      self.n_dates_gencounted += 1
      yield pdate
    self.bool_generator_ongoing = False
    self.bool_generator_has_run = True
    for word in words_to_del:
      self.strdatelist.remove(word)
    return

  def show_input_outside_side_by_side(self):
    if self.orginal_strdatelist is None:
      self.read_datefile_n_set_sep_n_orderpos()
    if self.datelist is None:
      self.get_dates_converting_all_at_once()
    for i, pdate in enumerate(self.datelist):
      scrmsg = f"{i+1} orig={self.orginal_strdatelist[i]} | strdate={self.strdatelist[i]} | date={pdate}"
      print(scrmsg)


def adhoc_test():
  dates_rw = DateFileReaderWriter()
  for i, pdate in enumerate(dates_rw.gen_dates_converting_one_by_one()):
    print(i+1, pdate)
  print('n dates', dates_rw.n_dates)
  dates_rw.show_input_outside_side_by_side()
  dates_rw.save_output_datelist_to_file()
  outfp = dates_rw.output_filepath
  dates_rw2 = DateFileReaderWriter(input_filepath=outfp)
  print('='*40)
  dates_rw2.show_input_outside_side_by_side()



def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
