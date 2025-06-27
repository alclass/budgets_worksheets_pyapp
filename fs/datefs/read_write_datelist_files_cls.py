#!/usr/bin/env python3
"""
fs/datefs/read_write_datelist_files_cls.py
"""
import datetime
import os
import fs.datefs.read_write_datelist_files_fs as rwfs
# from urllib3.contrib.pyopenssl import orig_util_SSLContext
import fs.os.sufix_incrementor as sfx_incr
import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv  # .convert_str_or_attrsobj_to_date_or_none
import settings as sett


class DateFileReaderWriter:

  ALL_DATE_POSORDER_COMBS = [
    # year is never in the middle (like for example dym)
    'ymd', 'ydm', 'dmy', 'mdy'
  ]
  ALL_DATE_SEPARATORS = [
    '-', '/', '.',
  ]

  def __init__(self, input_filepath=None, output_filepath=None):
    self.input_filepath, self.output_filepath = input_filepath, output_filepath
    self.treat_filepaths()
    self.words = None
    self.strdatelist = None    # may be the whole or a subset of self.words
    self.n_dates_gencounted = 0
    self.sep = '-'  # default, it may be replaced at runtime
    self._posorder = 'ymd'  # default, it may be replaced at runtime
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
  def posorder(self):
    if self._posorder is None:
      self._posorder = rwfs.DEFAULT_DATE_POSORDER
    return os.path.split(self.input_filepath)[0]

  @posorder.setter
  def posorder(self, p_posorder):
    if p_posorder is None or p_posorder not in self.ALL_DATE_POSORDER_COMBS:
      self._posorder = DEFAULT_DATE_POSORDER
    else:
      self._posorder = p_posorder

  @property
  def sep(self):
    if self._sep is None:
      self._sep = rwfs.DEFAULT_DATE_SEPARATOR
    return self._sep

  @sep.setter
  def sep(self, p_sep):
    if p_sep is None or p_sep not in self.ALL_DATE_SEPARATORS:
      self._sep = rwfs.DEFAULT_DATE_SEPARATOR
    else:
      self._sep = p_sep

  @property
  def input_filename(self):
    try:
      _, filename = os.path.split(self.input_filepath)
      return filename
    except (IndexError, ValueError):
      pass
    return None

  @property
  def input_folderpath(self):
    try:
      folderpath, _ = os.path.split(self.input_filepath)
      return folderpath
    except (IndexError, ValueError):
      pass
    return None

  @property
  def output_filename(self):
    try:
      _, filename = os.path.split(self.output_filepath)
      return filename
    except (IndexError, ValueError):
      pass
    return None

  @property
  def output_folderpath(self):
    try:
      folderpath, _ = os.path.split(self.output_filepath)
      return folderpath
    except (IndexError, ValueError):
      pass
    return None

  def treat_input_filepath(self):
    if self.input_filepath is None:
      self.input_filepath = rwfs.form_default_inputdatesfilepath()
    if not os.path.isfile(self.input_filepath):
      error_msg = f"""Input dates file {self.input_filename} does not exist.
      In folderpath = {self.input_folderpath}
      Please, make the file available in the above folder and rerun."""
      raise OSError(error_msg)

  def treat_output_filepath(self):
    if self.output_filepath is None:
      self.output_filepath = rwfs.form_new_datesfilepath_w_folderpath_n_filename(
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
    self.words = rwfs.fetch_wordlist_from_textfile_w_filepath(self.input_filepath)
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
        self.words, self.sep, self._posorder
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
      _ = rwfs.save_without_existence_check_text_to_file(text, self.output_filepath)
      n_lines = self.n_dates
    else:
      # second option, go through the generator
      genfunc = self.gen_dates_converting_strdates_w_or_wo_sep_n_posorder
      n_lines = rwfs.save_without_existence_check_genarator_to_file(genfunc, self.output_filepath)
    print(f'Saved n_dates {self.n_dates} | n_lines {n_lines} lines')
    return True

  def fetch_dates_converting_from_strlist_w_sep_n_posorder(self, sort_them=True):
    self.bool_generator_ongoing = False
    words_to_del = []
    self.datelist = []
    for word in self.strdatelist:
      # pdate = intr.convert_strdate_to_date_or_none_wo_sep_n_fieldorder(word, self.sep, self.orderpos)
      pdate = intr.introspect_n_convert_strdate_to_date_or_today(word, self.sep, self.orderpos)
      if pdate is None:
        words_to_del.append(word)
        continue
      self.datelist.append(pdate)
    for word in words_to_del:
      self.strdatelist.remove(word)
    if sort_them:
      sorted(self.datelist)
    return self.datelist

  def gen_dates_converting_strdates_w_or_wo_sep_n_posorder(self):
    self.bool_generator_ongoing = True
    words_to_del = []
    for word in self.strdatelist:
      if self.bool_keep_sep_n_posorder_fix:
        pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(word, self.sep, self.orderpos)
      else:
        pdate = intr.convert_strdate_to_date_or_none_wo_sep_n_fieldorder(word)
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
      self.fetch_dates_converting_from_strlist_w_sep_n_posorder()
    for i, pdate in enumerate(self.datelist):
      scrmsg = f"{i+1} orig={self.words[i]} | strdate={self.strdatelist[i]} | date={pdate}"
      print(scrmsg)

  def read_input(self):
    pass

  def __str__(self):
    outstr = f"""Class ReaderWriter:
    input_filepath = {self.input_filepath}
    output_filepath = {self.output_filepath}
    n_dates_gencounted = {self.n_dates_gencounted}
    sep = {self.sep}
    posorder = {self.posorder}
    bool_keep_sep_n_posorder_fix = {self.bool_keep_sep_n_posorder_fix}
    bool_generator_ongoing = {self.bool_generator_ongoing}
    bool_generator_has_run = {self.bool_generator_has_run}
    datelist = {self.datelist}
    """
    return outstr


def adhoc_test1():
  dates_rw = DateFileReaderWriter()
  dates_rw.bool_keep_sep_n_posorder_fix = False
  for i, pdate in enumerate(dates_rw.gen_dates_converting_strdates_w_or_wo_sep_n_posorder()):
    print(i+1, pdate)
  print('n dates', dates_rw.n_dates)
  dates_rw.show_input_outside_side_by_side()
  # dates_rw.save_output_datelist_to_file()
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
  adhoc_test1()
