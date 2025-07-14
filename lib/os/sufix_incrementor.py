"""
fs/os/sufix_incrementor.py
  contains class SufixIncrementor which finds a filepath, starting from on a first name, that is available,
    i.e., a file that does not exist in directory

How Does It Do It?
==================

If a name is taken, class SufixIncrementor contains functionality
  to increment a numbered sufix in filename until it is available,
  i.e., until a non-existing path is formed.

Example:
  if filename 'bls_cpi.json' is on folder, an incremented one (as 'bls_cpi-001.json')
  will be checked if available. If so, that one is returned, if not, with another increment,
  'bls_cpi-002.json' will be checked. If so, that one is returned,
  if not, another increment will be tried and so on until it reaches max_tries and then raises an exception.

The example mentioned above in a nutshell:
  step 1 => 'bls_cpi.json' exists on folder
  step 2 => 'bls_cpi-001.json' also exists on folder
  step 3 => 'bls_cpi-002.json' does not exist, so it's returned as an available name

  However, there are only n max_tries ('hardwired' instead of 'configured' at this version)
    available tries.  If all tries are attempted and no names available, an OSError will be raised.
    TODO: a pre-executed routine might stop program run before
      the exception above mentioned so to tell the user about the name unavailability
      and ask him or her to perform a directory cleaning up.
"""
import re
from collections.abc import Iterable
import os
import settings as sett
DEFAULT_FILENAME = 'datesfile.txt'
# in the regex belows file-extension is ruled by \.[A-Za-z0-9]{1-10}$ i.e., letters and numbers max 10-char
repatt_sufix_ending_name_in_fn = r"^.+?[-](?P<nsufix>\d+)\.[A-Za-z0-9]{1,10}$"
recmpl_sufix_ending_name_in_fn = re.compile(repatt_sufix_ending_name_in_fn)


def get_default_datafilepath():
  fopath = sett.get_datafolder_abspath()
  return os.path.join(fopath, DEFAULT_FILENAME)


def extract_folderpath_from_filepath_or_none(filepath):
  try:
    return os.path.split(filepath)[0]
  except (AttributeError, TypeError):
    pass
  return None


def print_filenames_from_filepaths(filepaths, folderpath=None):
  if not isinstance(filepaths, Iterable):
    return
  if folderpath:
    print('Folderpath', folderpath)
  for fp in filepaths:
    try:
      filename = os.path.split(fp)[-1]
      print('\t', filename)
    except TypeError:
      continue


class SufixIncrementor:
  """
  This class implements a sufix integer incrementor so that a filename that already exists
    in a directory is transformed to an "available", i.e., a filename not existing in directory
  """

  MAX_TRIES = 999
  DEFAULT_ZFILL = 3

  def __init__(self, p_filepath: os.path = None, zfill: int = None):
    """
    Derivable immutable attributes: foldername & dot_ext
    Derivable mutable attributes: name from filename, not its extension
    """
    self._dot_ext = None  # should be init'd first and go immutable
    self._folderpath = None
    self.first_entered_filename = None
    self.filename = None
    self.treat_filepath_to_set_immutable_folderpath_n_dotext(p_filepath)
    self.ntries = 0
    self.nsufix = 0
    self.zfill = zfill or self.DEFAULT_ZFILL
    self.bool_finder_has_run = False
    self.treat_attrs()

  def treat_filepath_to_set_immutable_folderpath_n_dotext(self, p_filepath):
    if p_filepath is None:
      p_filepath = get_default_datafilepath()
    folderpath, self.first_entered_filename = os.path.split(p_filepath)
    if folderpath is None or not os.path.isdir(folderpath):
      error_msg = f'Error: folderpath [{folderpath}] does not exist in class SufixIncrementor.'
      raise OSError(error_msg)
    self.filename = self.first_entered_filename
    self._folderpath = folderpath
    self._dot_ext = os.path.splitext(self.filename)[1]

  def treat_attrs(self):
    pass

  @property
  def folderpath(self) -> os.path:
    return self._folderpath

  @property
  def first_entered_filepath(self) -> os.path:
    return os.path.join(self.folderpath, self.first_entered_filename)

  @property
  def filepath(self) -> os.path:
    """
    folderpath is immutable in the context of this class
    filename is mutable

    if self._folderpath is None or self.filename is None:
      return None
    """
    return os.path.join(self._folderpath, self.filename)

  @property
  def name(self):
    if self.filename is None:
      return None
    name, _ = os.path.splitext(self.filename)
    return name

  @property
  def dot_ext(self):
    """
    if self._dot_ext is not None:
      return self._dot_ext
    _, self._dot_ext = os.path.splitext(self.filename)
    """
    return self._dot_ext

  def change_name_case1_or_case3_when_file_has_no_numbered_sufix(self):
    self.nsufix = 1
    str_sufix = str(self.nsufix).zfill(self.zfill)
    newname = f"{self.name}-{str_sufix}"
    self.filename = f"{newname}{self.dot_ext}"

  def change_name_case2_when_file_has_a_numbered_sufix(self, namepieces, i_sufix):
    i_sufix += 1
    self.nsufix = i_sufix
    name_up_to_sufix = '-'.join(namepieces[:-1])
    str_sufix = str(i_sufix).zfill(self.zfill)
    newname = f"{name_up_to_sufix}-{str_sufix}"
    self.filename = f"{newname}{self.dot_ext}"

  def raise_oserror_maxtries_is_reached(self):
    self.ntries += 1
    if self.ntries > self.MAX_TRIES:
      error_msg = f'Error: Too many tries ({self.ntries}) in attempting to find an availablie numbered sufix filename.'
      error_msg += f'\t Last filename({self.filename}) tried.'
      error_msg += f'\t Base folder is ({self.folderpath}). Please, move/emove/delete excess files and retry.'
      raise OSError(error_msg)

  def increment_one_to_names_sufix_n_return(self):
    self.raise_oserror_maxtries_is_reached()
    if self.name.find('-') < 0:
      return self.change_name_case1_or_case3_when_file_has_no_numbered_sufix()
    namepieces = self.name.split('-')
    try:
      i_sufix = int(namepieces[-1])
      return self.change_name_case2_when_file_has_a_numbered_sufix(namepieces, i_sufix)
    except ValueError:
      # as sufix not being a number, it leads to case 3
      pass
    return self.change_name_case1_or_case3_when_file_has_no_numbered_sufix()

  def get_the_last_index_from_objsparams(self):
    if not self.bool_finder_has_run:
      self.process()
    pass

  def get_next_available_filepath_from_objsparams(self):
    """
    Returns the next available filepath starting from the filename and directory given this class
    This method is the PUBLIC-to-the-client one in this class
    """
    if not self.bool_finder_has_run:
      self.process()
    return self.filepath

  def get_next_available_filename_from_objsparams(self):
    if not self.bool_finder_has_run:
      self.process()
    return self.filename

  def find_next_available_filepath_from_objsparams(self, rerun=False):
    """
    Finds (and does not return - @see method get_next_available_filepath_from_objsparams() for that)
    the next available filepath starting from the filename and directory given this class
    This method is the PUBLIC-to-the-client one in this class
    """
    if self.bool_finder_has_run and not rerun:
      return
    while os.path.isfile(self.filepath):
      # to avoid an infinite loop, max_tries will guard from it and raise an exception if max_tries is reached
      self.increment_one_to_names_sufix_n_return()
    self.bool_finder_has_run = True

  def process(self):
    self.find_next_available_filepath_from_objsparams()
    print(self)

  def __str__(self):
    outstr = f"""{self.__class__.__name__}:
    first_entered_filepath = {self.first_entered_filepath}
    filepath = {self.filepath}
    filename = {self.filename}
    nsufix = {self.nsufix}
    ntries = {self.ntries}
    zfill = {self.zfill}
    max tries = {self.MAX_TRIES}
    """
    return outstr


def adhoctest2():
  names = []
  fn = 'test-1.txt'
  names.append(fn)
  fn = 'test-080.dat'
  names.append(fn)
  fn = 'test-a1c.dasdsfasd'
  names.append(fn)
  fn = 'test-1010.db777'
  names.append(fn)
  for fn in names:
    match = recmpl_sufix_ending_name_in_fn.match(fn)
    nsufix = None if match is None else match.group('nsufix')
    scrmsg = f"fn={fn} -> nsufix={nsufix}"
    print(scrmsg)


def adhoctest():
  si = SufixIncrementor()
  si.process()
  fipath = si.get_next_available_filepath_from_objsparams()
  print('fipath', fipath)
  finame = si.get_next_available_filename_from_objsparams()
  print('fipath', finame)


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  # adhoctest()
  adhoctest2()
