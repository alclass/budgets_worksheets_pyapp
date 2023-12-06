#!/usr/bin/env python3
"""
fs/datefs/read_write_datelist_files.py
"""
import os
import fs.datefs.introspect_dates as fromto
import fs.os.sufix_incrementor as sfx_incr
import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order
import settings as sett
DEFAULT_TXT_INPUT_DATES_FILENAME = 'datesfile.txt'
DEFAULT_TXT_OUTPUT_DATES_FILENAME = 'datesfile_processed_to_norm_yyyy-mm-dd.txt'


def fetch_wordlist_from_textfile_w_filepath(p_filepath=None):
  """
  gets a list of words from the text inside filepath
  """
  if p_filepath is None or not os.path.isfile(p_filepath):
    filepath = form_datesfilepath_w_folderpath_n_filename()
  else:
    filepath = p_filepath
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


def fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath(filepath=None):
  """
  strdates with sep come in 12 combinations
  strdates without a sep can only be an 8-digit stringnumber
  """
  strdatelist = fetch_wordlist_from_textfile_w_filepath(filepath)
  datelist = intr.introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist)
  datelist = sorted(filter(lambda e: e is not None, datelist))
  return sorted(datelist)


def fetch_dates_from_strdates_intext_from_filepath_w_sep_n_posorder(filepath=None, sep='/', posorder='dmy'):
  """
  This function extracts dates from files but dates must conform to sep & posorder
  @see other functions in this module that extracts dates under other ways

  strdates with sep & posorder come in 12 different combinations
  strdates without a sep can only be an 8-digit stringnumber

  # notice that dates may be in some different formats (eg "2021-01-21" or "21/1/2021")
  # among these strdates, those that return as "datetime.date" go into datelist
  """
  strdatelist = fetch_wordlist_from_textfile_w_filepath(filepath)
  datelist = intr.extract_datelist_from_strdatelist_w_sep_n_posorder(strdatelist, sep, posorder)
  datelist = sorted(filter(lambda e: e is not None, datelist))
  return sorted(datelist)


def form_new_datesfilepath_w_folderpath_n_filename(p_filename=None, p_folderpath=None, followsuffix=True):
  filepath = form_datesfilepath_w_folderpath_n_filename(p_filename, p_folderpath)
  if os.path.exists(filepath):
    if not followsuffix:
      error_msg = f"""Output file {p_filename} already exists in folder:
      => [{p_folderpath}]
      Please, remove it or, programatically, set parameter followsuffix."""
      raise OSError(error_msg)
    else:
      filepath = sfx_incr.get_filepath_if_available_or_increment_numbersufix(filepath)
  return filepath


def form_datesfilepath_w_folderpath_n_filename(p_filename=None, p_folderpath=None):
  """
  Forms filepath with folderpath & filename
  """
  folderpath = p_folderpath or sett.get_datafolder_abspath()
  filename = p_filename or DEFAULT_TXT_INPUT_DATES_FILENAME
  if not os.path.exists(folderpath):
    os.makedirs(folderpath)
  filepath = os.path.join(folderpath, filename)
  return filepath


def form_default_datesfilepath():
  return form_datesfilepath_w_folderpath_n_filename(None, None)


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
    self.words = None
    self.strdatelist = None    # may be the whole or a subset of self.words
    self.n_dates_gencounted = 0
    self.sep = '-'  # default, it may be replaced at runtime
    self.posorder = 'ymd'  # default, it may be replaced at runtime
    self.bool_keep_sep_n_posorder_fix = True
    self.bool_generator_ongoing = False  # either datelist is taken all at once or 'generated'
    self.bool_generator_has_run = False
    self.datelist = None
    self.sep = None  # it's either - (dash), / (forward slash) or . (dot)
    self.orderpos = None  # it's either ymd, ydm, dmy or mdy
    self.read_datefile_get_words_n_first_sep_n_posorder()
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
      self.input_filepath = form_default_datesfilepath()
    if not os.path.isfile(self.input_filepath):
      error_msg = f"""Input dates file {self.input_filename} does not exist.
      In folderpath = {self.input_folderpath}
      Please, make the file available in the above folder and rerun."""
      raise OSError(error_msg)

  def treat_output_filepath(self):
    if self.output_filepath is None:
      self.output_filepath = form_new_datesfilepath_w_folderpath_n_filename(
        None, None, followsuffix=True
      )
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

  def read_datefile_get_words_n_first_sep_n_posorder(self):
    self.words = fetch_wordlist_from_textfile_w_filepath(self.input_filepath)
    self.strdatelist = []  # copy.copy(self.words)  # to be processed ahead
    self.sep, self.orderpos = intr.find_sep_n_posorder_from_a_strdatelist(self.strdatelist)

  def extract_dates(self):
    """
    folderpath, filename = os.path.split(self.input_filepath)
    if sep is None:
      folderpath, filename = os.path.split(self.input_filepath)
      error_msg = f""The three (3) possible strdate separators were not found.
      Separators are: {intr.STRDATE_SEPARATORS}
      input file is {filename} in:
        => {folderpath}
      ""
      raise ValueError(error_msg)
    if orderpos is None:
      error_msg = f""The four (3) possible date field positionings were not found.
      There are: {intr.ORDERPOS_TOKENS_AVAILABLE}
      input file is {filename} in:
        => {folderpath}
      ""
      raise ValueError(error_msg)
    """
    if self.bool_keep_sep_n_posorder_fix:
      self.datelist = intr.extract_datelist_from_strdatelist_w_sep_n_posorder(
        self.words, self.sep, self.posorder
      )
    else:
      self.datelist = intr.extract_datelist_from_strdatelist_considering_any_sep_n_posorder(self.words)

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
      if self.bool_keep_sep_n_posorder_fix:
        pdate = fromto.convert_strdate_to_date_or_none_w_sep_n_fieldorder(word, self.sep, self.orderpos)
      else:
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
    if self.words is None:
      self.read_datefile_get_words_n_first_sep_n_posorder()
    if self.datelist is None:
      self.get_dates_converting_all_at_once()
    for i, pdate in enumerate(self.datelist):
      scrmsg = f"{i+1} orig={self.words[i]} | strdate={self.strdatelist[i]} | date={pdate}"
      print(scrmsg)


def adhoc_test():
  dates_rw = DateFileReaderWriter()
  dates_rw.bool_keep_sep_n_posorder_fix = False
  for i, pdate in enumerate(dates_rw.gen_dates_converting_one_by_one()):
    print(i+1, pdate)
  print('n dates', dates_rw.n_dates)
  dates_rw.show_input_outside_side_by_side()
  dates_rw.save_output_datelist_to_file()
  output_filepath = dates_rw.output_filepath
  print(output_filepath)
  dates_rw2 = DateFileReaderWriter()
  dates_rw2.bool_keep_sep_n_posorder_fix = True
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
