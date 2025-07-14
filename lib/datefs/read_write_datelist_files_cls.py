#!/usr/bin/env python3
"""
fs/datefs/read_write_datelist_files_cls.py
  Contains class DateFileReaderWriter which is a client for functions module:
    fs/datefs/read_write_datelist_files_fs.py

"""
import os
import lib.datefs.read_write_datelist_files_fs as rwfs
import lib.os.sufix_incrementor as sfx_incr
import lib.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order


class DateFileReaderWriter:
  """
  This class organizes reading and writing of dates text files. The dates in these files are placed one at a line
    and are considered to be the first 'word' in the line

  In a practical sense for this system, one of its use-case is to read a set of dates
    which will be used for finding exchange rates for their dates

  As this class is a client for functions module:
    fs/datefs/read_write_datelist_files_fs.py
      it can read dates in various formats varying sep (separator as '-'., '/' amd '.')
        and posorder as 'ymd', 'ydm', 'dmy' and 'mdy'  (y=year, m=month, d=day)

  As a class, some strategies were planed for it, the main ones are:

    Strategy 1  - after reading line for line of the input text file and converting each strdate to 'date',
      the strdates (the text lines) are deleted (or not stored) and the dates are stored in the object

    Strategy 2 - (for cases where the data file is big enough, the user has to decide this 'big enough' frontier)
      the reading, converting and returning is done by an interation-scheme,
      ie 'yielding' each line that produces a date output as needed and nothing is store in the object

    Strategy number 2 is the one appropriate and preferrable for very large date data sets,
      but the client user has to control it choosing the appropriate methods. These are:

        => gen_n_dont_store_pydates_converting_textfile_w_sep_n_posorder()
        => gen_n_dont_store_pydates_converting_textfile_w_or_wo_sep_n_posorder()

    Their counterparts for Strategy 1 are:

        => get_n_store_pydates_converting_textfile_w_sep_n_posorder()
        => et_n_store_pydates_converting_textfile_w_or_wo_sep_n_posorder()


  """

  DEFAULT_DATE_POSORDER = 'ymd'
  ALL_DATE_POSORDER_COMBS = [
    # year is never in the middle (like for example dym, but: does any country use "year in the middle"?)
    'ymd', 'ydm', 'dmy', 'mdy'
  ]
  DEFAULT_DATE_SEPARATOR = '-'
  ALL_DATE_SEPARATORS = [
    '-', '/', '.',
  ]

  def __init__(self, input_filepath=None, output_filepath=None):
    self.bool_sep_n_posorder_introspection_happened = False
    self.input_filepath, self.output_filepath = input_filepath, output_filepath
    self.treat_filepaths()
    self.strdates = []
    self.datelist = None  # the converted Python date dates from strdates
    self.n_strdates_in_file = 0
    self.n_dates_gencounted = 0
    self._sep = None  # the default, when needed, is returned dynamically under condition
    self._posorder = None  # default, when needed, is returned dynamically under condition
    # this is to the situation when reading will try to find sep & posorder for each strdate
    # 'True' means sep & posorder are always the same throughout the whole dates file reading
    self.bool_keep_sep_n_posorder_fix = True
    self.bool_generator_has_completed_run = False
    self.introspectread_datefile_firstlines_to_set_sep_n_posorder()  # it's going to find out sep & posorder

  def treat_filepaths(self):
    self.treat_input_filepath()
    self.treat_output_filepath()

  @property
  def posorder(self):
    if self._posorder is None and self.bool_sep_n_posorder_introspection_happened:
      return rwfs.DEFAULT_DATE_POSORDER
    return self._posorder

  @posorder.setter
  def posorder(self, p_posorder):
    if p_posorder is None or p_posorder not in self.ALL_DATE_POSORDER_COMBS:
      self._posorder = rwfs.DEFAULT_DATE_POSORDER
    else:
      self._posorder = p_posorder

  @property
  def sep(self):
    if self._sep is None and self.bool_sep_n_posorder_introspection_happened:
      return rwfs.DEFAULT_DATE_SEPARATOR
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
      filepath = {self.input_filepath}
      Please, make the file available in the above folder and rerun."""
      raise OSError(error_msg)

  def treat_output_filepath(self):
    """
    output_filepath, in the context of this class, should not exist, so it aims a new file
    """
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
    if self.bool_generator_has_completed_run:
      return self.n_dates_gencounted
    return 0

  def introspectread_datefile_firstlines_to_set_sep_n_posorder(self, rerun=False):
    """
    This method only reads the date text file enough to introspect (find out)
      which separator and which posorder there are in its string dates
    """
    self.bool_sep_n_posorder_introspection_happened = False
    sep, posorder = self.sep, self.posorder
    if posorder and sep and not rerun:
      return
    for i, strdate in enumerate(rwfs.fetch_iter_wordlist_from_textfile_w_filepath(self.input_filepath)):
      if sep is None:
        sep = intr.introspect_sep_char_in_strdate(strdate)
        self.sep = sep
      if posorder is None and sep:
        posorder = intr.introspect_year_month_day_field_order_in_date(strdate, sep)
        self.posorder = posorder
      if posorder and sep:
        break
    self.bool_sep_n_posorder_introspection_happened = True

  def gen_n_dont_store_pydates_converting_textfile_w_sep_n_posorder(self):
    """
    This method generates (yields) Python dates one by one and do not store them
    A strdate conversion will be tried with sep and posorder
      and not attempt to get it without them as the method above does

    Notice:
      1 - a call to this method also empties 'datelist'
        (which might not have stored anything is the user is following the iteration-approach
      2 - sorting is not possible, as output is one by one with storing them up
    """
    self.datelist = []
    self.n_dates_gencounted = 0
    for strdate in rwfs.fetch_iter_wordlist_from_textfile_w_filepath(self.input_filepath):
      pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, self.sep, self.posorder)
      if pdate is None:
        continue
      self.n_dates_gencounted += 1
      yield pdate
    return

  def gen_n_dont_store_pydates_converting_textfile_w_or_wo_sep_n_posorder(self):
    """
    This method generates (yields) Python dates one by one and do not store them
    A strdate conversion will be tried with sep and posorder and, if None,
      fall back to an attempt to get it without them
    """
    self.datelist = []
    self.n_dates_gencounted = 0
    for strdate in rwfs.fetch_iter_wordlist_from_textfile_w_filepath(self.input_filepath):
      pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, self.sep, self.posorder)
      if pdate is None:
        pdate = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
        if pdate is None:
          continue
      self.n_dates_gencounted += 1
      yield pdate
    return

  def get_n_store_pydates_converting_textfile_w_sep_n_posorder(self, sort_them=True, rerun=False):
    """
    This method converts and returns Python dates storing them in the object
      Obs:
        this is the first approach mentioned above for this class,
        the second 'generates' (yields) it one by one and do not store the result list in the object

    Each strdate conversion will be tried with sep and posorder
      and a second attempt without them is not issued as it happens in the method below
    """
    if self.datelist is not None and not rerun:
      return self.datelist
    self.datelist = []
    self.strdates = rwfs.fetch_wordlist_from_textfile_w_filepath(self.input_filepath)
    for strdate in self.strdates:
      pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, self.sep, self.posorder)
      if pdate is None:
        continue
      self.datelist.append(pdate)
    # empty strdates (it will also save its allocated memory)
    self.strdates = []
    if sort_them:
      self.datelist.sort()
    return self.datelist

  def get_n_store_pydates_converting_textfile_w_or_wo_sep_n_posorder(self, sort_them=True, rerun=False):
    """
    This method converts and returns Python dates storing them in the object
      Obs:
        this is the first approach mentioned above for this class,
        the second 'generates' (yields) it one by one and do not store the result list in the object

    A strdate conversion will be tried with sep and posorder and, if None,
      fall back to an attempt to get it without them
    """
    if self.datelist is not None and not rerun:
      return self.datelist
    self.datelist = []
    self.strdates = rwfs.fetch_wordlist_from_textfile_w_filepath(self.input_filepath)
    for strdate in self.strdates:
      pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, self.sep, self.posorder)
      if pdate is None:
        pdate = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
        if pdate is None:
          continue
      self.datelist.append(pdate)
    # empty strdates (it will also save its allocated memory)
    self.strdates = []
    if sort_them:
      self.datelist.sort()
    return self.datelist

  def get_joint_datelist_one_per_line_as_text_or_empty(self):
    if self.datelist is None:
      _ = self.get_n_store_pydates_converting_textfile_w_sep_n_posorder()
    if self.datelist and len(self.datelist) > 0:
      strdatelist = list(map(lambda e: str(e), self.datelist))
      text = '\n'.join(strdatelist)
      return text
    return ''

  def save_output_datelist_to_file(self):
    scrmsg = f"""Saving file {self.output_filename}" in
    => {self.output_folderpath}"""
    print(scrmsg)
    text = self.get_joint_datelist_one_per_line_as_text_or_empty()
    if text:
      _ = rwfs.save_without_existence_check_text_to_file(text, self.output_filepath)
      n_lines = self.n_dates
    else:
      # second option, go through the generator
      genfunc = self.gen_n_dont_store_pydates_converting_textfile_w_or_wo_sep_n_posorder
      n_lines = rwfs.save_without_existence_check_genarator_to_file(genfunc, self.output_filepath)
    print(f'Saved n_dates {self.n_dates} | n_lines {n_lines} lines')
    return True

  def __str__(self):
    outstr = f"""Class ReaderWriter:
    input_filepath = {self.input_filepath}
    output_filepath = {self.output_filepath}
    n_dates_gencounted = {self.n_dates_gencounted}
    sep = {self.sep}
    posorder = {self.posorder}
    bool_keep_sep_n_posorder_fix = {self.bool_keep_sep_n_posorder_fix}
    bool_generator_has_run = {self.bool_generator_has_completed_run}
    datelist = {self.datelist}
    """
    return outstr


def adhoc_test3():
  dates_rw = DateFileReaderWriter()
  dates_rw.bool_keep_sep_n_posorder_fix = False
  for i, pdate in enumerate(dates_rw.gen_n_dont_store_pydates_converting_textfile_w_or_wo_sep_n_posorder()):
    print(i+1, pdate)
  print('n dates', dates_rw.n_dates)
  # dates_rw.save_output_datelist_to_file()
  output_filepath = dates_rw.output_filepath
  print(output_filepath)
  dates_rw2 = DateFileReaderWriter()
  dates_rw2.bool_keep_sep_n_posorder_fix = True
  print('='*40)


def adhoc_test2():
  dates_rw = DateFileReaderWriter()
  for i, pdate in enumerate(dates_rw.gen_n_dont_store_pydates_converting_textfile_w_or_wo_sep_n_posorder()):
    seq = i + 1
    scrmsg = f"{seq} pdate = {pdate}"
    print(scrmsg)
  c = dates_rw.n_dates_gencounted
  scrmsg = f"n_dates_gencounted = {c}"
  print(scrmsg)
  c = len(dates_rw.datelist)
  scrmsg = f"len datelist = {c}"
  print(scrmsg)
  for i, pdate in enumerate(dates_rw.gen_n_dont_store_pydates_converting_textfile_w_sep_n_posorder()):
    seq = i + 1
    scrmsg = f"{seq} pdate = {pdate}"
    print(scrmsg)
  c = dates_rw.n_dates_gencounted
  scrmsg = f"n_dates_gencounted = {c}"
  print(scrmsg)
  c = len(dates_rw.datelist)
  scrmsg = f"len datelist = {c}"
  print(scrmsg)
  dates = dates_rw.get_n_store_pydates_converting_textfile_w_sep_n_posorder(rerun=True)
  scrmsg = f"with get = {dates}"
  print(scrmsg)
  c = len(dates_rw.datelist)
  scrmsg = f"len datelist = {c}"
  print(scrmsg)
  dates = dates_rw.get_n_store_pydates_converting_textfile_w_or_wo_sep_n_posorder(rerun=True)
  scrmsg = f"with get = {dates}"
  print(scrmsg)
  c = len(dates_rw.datelist)
  scrmsg = f"len datelist = {c}"
  print(scrmsg)


def adhoc_test1():
  dates_rw = DateFileReaderWriter()
  dates_rw.get_n_store_pydates_converting_textfile_w_sep_n_posorder()
  print(dates_rw.strdates)
  print('get_n_store_pydates_converting_textfile_w_sep_n_posorder()')
  print(dates_rw.datelist)
  txt = dates_rw.get_joint_datelist_one_per_line_as_text_or_empty()
  scrmsg = "Output text for file-content:\n"
  scrmsg += "=============================\n"
  scrmsg += txt
  print(scrmsg)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test2()
