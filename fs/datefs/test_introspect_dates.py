#!/usr/bin/env python3
"""
fs/datefs/test_introspect_dates.py
  unit-tests to fs/datefs/introspect_dates.py functions.

Notice that not all functions in module introspect_dates.py are tested,
  because, naturally, some functions are 'sort of' private, ie,
  they are called from others that themselves are under unit-test here.

Example:
  function introspect_possible_month_position_in_date() is not tested here,
    because it's tested indirectly via other functions.
  Another detail of introspect_possible_month_position_in_date() is that
    it is used in a 'composite way', ie, to find posorder [ymd, ydm, dmy, mdy],
    two fields among the three (year, month & day) must be found conclusively,
    so the function mentioned above is also used together with other functions.

Conclusive vs unconclusive strdates:
    # in a strdate, year is 'conclusive' if above 31 (ie, it does not confuse with day)
    # in a strdate, day is 'conclusive' if above 12 (ie, it does not confuse with month)
Examples:
  a) unconclusive strdates
    2023.1.3 is unconclusive, because one does not know whether digit 1 is day or month, same to 3;
    13-1-3 is also unconclusive, because, adding to the above, one does not know whether 13 is day or year;
  b) conclusive strdates
    2023-1-13 is conclusive, for 2023 is greater than 31 and 13 greater than 12 (sep='-', posorder='ymd')
    2/22/2022 is conclusive, idem as above, though different in sep & posorder (sep='/', posorder='mdy')
"""
import datetime
import unittest
import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order


class Test(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_convert_strdate_to_date_or_none_w_sep_n_order(self):
    sep = '-'
    posorder = 'ymd'
    # t1
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, posorder)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t2
    y, m, d = 2023, 14, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, posorder)
    self.assertIsNone(returned_date)
    # t3
    strdate = '2023-10-15'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, posorder)
    expected_date = datetime.date(year=2023, month=10, day=15)
    self.assertEqual(returned_date, expected_date)
    # t4
    strdate = 'bla blah'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, posorder)
    self.assertIsNone(returned_date)
    # t5
    y, m, d = 13, 10, 15
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, posorder)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)

  def test_convert_strdate_w_or_wo_sep_to_dtdate_or_none(self):
    # t1
    # On t1, month is unconclusive with day, ie both are less than 13
    # Notice that the target function does not know posorder, ie the positional order of year, month & day
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m:02}-{d:02}'
    returned_date = intr.convert_strdate_w_or_wo_sep_to_date_or_none(strdate)
    self.assertIsNone(returned_date)
    # t2
    # year is unconclusive with month, ie both are less than 12
    y, m, d = 12, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_w_or_wo_sep_to_date_or_none(strdate)
    self.assertIsNone(returned_date)
    # t3
    # both month and day are less than 13, so date is unconclusive
    y, m, d = 13, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_w_or_wo_sep_to_date_or_none(strdate)
    self.assertIsNone(returned_date)
    # t4
    # both month and day are less than 13, so date is unconclusive
    y, m, d = 13, 4, 13
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_w_or_wo_sep_to_date_or_none(strdate)
    self.assertIsNone(returned_date)
    # t5
    # here, differently from above, year, month & day are logically obtained, no matter it's positioning,
    # ie date is 'conclusive'
    y, m, d = 32, 4, 13
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_w_or_wo_sep_to_date_or_none(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)

  def test_convert_date_to_mmddyyyy_str_or_none(self):
    # t1
    # this first hypothesis used zfill = 2
    y, m, d = 2023, 4, 5
    zfill = 2
    pdate = datetime.date(year=y, month=m, day=d)
    returned_date = intr.convert_date_to_mmddyyyy_str_or_none_with_date_opt_sep_zfill(pdate, sep='/', zfill=zfill)
    expected_strdate = f'{m:02}/{d:02}/{y}'
    self.assertEqual(returned_date, expected_strdate)
    # t2
    # this second hypothesis used zfill = 0 (next one is the same, but let it be defaulted)
    zfill = 0
    returned_date = intr.convert_date_to_mmddyyyy_str_or_none_with_date_opt_sep_zfill(pdate, sep='/', zfill=zfill)
    expected_strdate = f'{m}/{d}/{y}'
    self.assertEqual(returned_date, expected_strdate)
    # t3
    # same as above, but letting zfill goes in as default, ie, it's not passed into
    returned_date = intr.convert_date_to_mmddyyyy_str_or_none_with_date_opt_sep_zfill(pdate, sep='/')
    self.assertEqual(returned_date, expected_strdate)
    # t4
    # same as above, but changing the value of sep
    sep = '.'
    returned_date = intr.convert_date_to_mmddyyyy_str_or_none_with_date_opt_sep_zfill(pdate, sep)
    expected_strdate = f'{m}{sep}{d}{sep}{y}'
    self.assertEqual(returned_date, expected_strdate)
    # t5
    # something weird to get back None
    y, m, d = 'bla', 'foo', 'bar'
    pdate = y + m + d
    returned_date = intr.convert_date_to_mmddyyyy_str_or_none_with_date_opt_sep_zfill(pdate)
    self.assertIsNone(returned_date)
    # t6
    # testing function's variation that instead of returning None returns 'today'
    sep = '/'
    returned_date = intr.convert_date_to_mmddyyyy_str_or_today_with_date_opt_sep_zfill('rubish', sep)
    expected_strdate = f'{self.today.month}{sep}{self.today.day}{sep}{self.today.year}'
    self.assertEqual(returned_date, expected_strdate)

  def test_convert_to_date_or_none_w_strdate_opt_sep_posorder(self):
    # t1
    # this first hypothesis keeps day above 12 so that date is conclusive
    # ie, day and month are not unconclusive between themselves,
    # for sep and posorder are not passed into, needing to be introspected somewhere inside the code
    y, m, d = 2023, 4, 15
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t2
    # this second hypothesis keeps day below 13, making date unconclusive, and then
    # expecting None
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate)
    self.assertIsNone(returned_date)
    # t3
    # this third hypothesis is like the one above but passes in sep and posorder
    # expecting None
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m}-{d}'
    sep, posorder = '-', 'ymd'
    returned_date = intr.introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate, sep, posorder)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t4
    # this fourth hypothesis uses a function variation that returns today instead of None
    rubbish_to_pass_in = 'bla bla'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_today(rubbish_to_pass_in)
    expected_date = self.today
    self.assertEqual(returned_date, expected_date)

  def test_find_sep_n_posorder_from_a_strdatelist(self):
    """
    Curiosity:
    In this code, assertRaises uses the signature: (exception, callable, *args, **kwargs)
    In the following page:
      https://www.pythonclear.com/unittest/python-unittest-assertraises/
    the author shows a second manner of use with "with", e.g.:

      # the function to be unit-tested
      def raise_if_negative(value):
          if value < 0:
              raise ValueError('Value cannot be negative')
      # the unit-test
      import unittest
      class TestRaiseIfNegative(unittest.TestCase):
          def test_raise_if_negative(self):
              with self.assertRaises(ValueError):
                  raise_if_negative(-1)
    """
    # t1
    # this first hypothesis shows input data having only the last item ['2023-04-14']
    # as conclusive, for posorder, which also shows that the target function
    # is able to find it having at least this one conclusive year-month-day combination
    # year is 'conclusive' if above 31 (ie, it does not confuse with day)
    # day is 'conclusive' if above 12 (ie, it does not confuse with month)
    # if year and day are 'conclusive', date altogether is 'conclusive'
    sd1, sd2, sd3 = ('2023-05-04', '2023-03-04', '2023-04-14')
    strdatelist = [sd1, sd2, sd3]
    expected_sep = '-'
    expected_posorder = 'ymd'
    sep, posorder = intr.find_sep_n_posorder_from_a_strdatelist(strdatelist)
    self.assertEqual((sep, posorder), (expected_sep, expected_posorder))
    # t2
    # this second hypothesis shows all input dates as unconclusive between month and day
    # so it expects a ValueError exception raised
    sd1, sd2, sd3 = ('2023-05-04', '2023-03-04', '2023-2-4')
    strdatelist = [sd1, sd2, sd3]
    self.assertRaises(ValueError, intr.find_sep_n_posorder_from_a_strdatelist, strdatelist)
    # t3
    # this third hypothesis is somewhat an odd case, because the introspection
    # picks up the very first possible sep and posorder
    # and (purposely) does not check every element in the list thereafter
    # @see below: this is resolved with extract_datelist_from_strdatelist_sep_n_posorder_consistent()
    sd1, sd2, sd3 = ('2023.14.05', '2023/03-04', 'bla foo bar')  # only the first one is good
    strdatelist = [sd1, sd2, sd3]
    expected_sep = '.'
    expected_posorder = 'ydm'
    sep, posorder = intr.find_sep_n_posorder_from_a_strdatelist(strdatelist)
    self.assertEqual((sep, posorder), (expected_sep, expected_posorder))
    # t4
    # this fouth hypothesis expands on the one above with removing non-conforming strdates
    # to sep and posorder found
    returned_strlist = intr.remove_strdates_not_conforming_to_sep_n_posorder(strdatelist, sep, posorder)
    expected_strlist = [sd1]  # only the first one is good
    self.assertEqual(returned_strlist, expected_strlist)
    # t5
    # this fifth hypothesis compounds the former two, ie it gets a datelist that
    # is consistent within sep and posorder
    # notice that strdatelist above has inconsistent items in terms of sep and posorder
    returned_datelist = intr.extract_datelist_from_strdatelist_sep_n_posorder_consistent(strdatelist)
    y, d, m = tuple(sd1.split('.'))  # pay attention to posorder, ie ydm from '2023.14.05'
    y, m, d = int(y), int(m), int(d)
    sd1_as_date = datetime.date(year=y, month=m, day=d)
    expected_datelist = [sd1_as_date]
    self.assertEqual(returned_datelist, expected_datelist)
