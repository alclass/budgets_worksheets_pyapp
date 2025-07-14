#!/usr/bin/env python3
"""
fs/datefs/test_introspect_dates.py
  unit-tests to fs/datefs/introspect_dates.py functions.

Notice that NOT all functions in module introspect_dates.py are explicitly tested.
  The idea is that, at the end, functions not present here will be tested through functions in here.

Example:
  function introspect_possible_month_position_in_date() is not tested here,
    because it's tested indirectly via other functions
    (those that 'introspect' dates without receiving posorder as paramater).

  Another detail of introspect_possible_month_position_in_date() is that
    it is used in a 'composite way', ie, to find posorder [ymd, ydm, dmy, mdy].
  In that, it is necessary that two fields (among the three: year, month & day) be found conclusively
    so that it's able to gen_first_n_letterindices a datetime.date.
  This above function, though it's not present here as of the time of this writing, it may in the future.

Conclusive vs unconclusive strdates:
    # in a strdate, year is 'conclusive' if above 31 (ie, it does not confuse iself with day)
    # in a strdate, day is 'conclusive' if above 12 (ie, day does not confuse itself with month)
Examples:
    a) unconclusive strdates
  2023.1.3 is unconclusive, because one does not know whether digit 1 is day or month, same to 3;
  13-1-3 is also unconclusive, because, adding to the above, one does not know whether 13 is day or year;
    b) conclusive strdates
  2023-1-13 is conclusive, for 2023 is greater than 31 and 13 greater than 12 (sep='-', posorder='ymd'
  2/22/2022 is also conclusive, idem as above, though different in sep & posorder (sep='/', posorder='mdy'

As of 2023-12-09, there are 9 tests here with about 40 subtests
  (a test is a method prefixed with 'test_')
  (a subtest is generally a variation hypothesis inside a test)
"""
import datetime
import unittest
import lib.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order
import lib.datefs.introspect_dates_datamass as dmass  # .get_tuple_12strdatelist_n_corresp_date_datamass


class Test(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_convert_strdate_to_date_or_none_w_sep_n_order(self):
    sep = '-'
    posorder = 'ymd'
    # t1
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t2
    y, m, d = 2023, 14, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    self.assertIsNone(returned_date)
    # t3
    strdate = '2023-10-15'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    expected_date = datetime.date(year=2023, month=10, day=15)
    self.assertEqual(returned_date, expected_date)
    # t4
    strdate = 'bla blah'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    self.assertIsNone(returned_date)
    # t5
    y, m, d = 13, 10, 15
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)

  def test_convert_strdate_w_or_wo_sep_to_dtdate_or_none(self):
    # t1
    # On t1, month is unconclusive with day, ie both are less than 13
    # Notice that the target function does not know posorder, ie the positional order of year, month & day
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m:02}-{d:02}'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    self.assertIsNone(returned_date)
    # t2
    # year is unconclusive with month, ie both are less than 12
    y, m, d = 12, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    self.assertIsNone(returned_date)
    # t3
    # both month and day are less than 13, so date is unconclusive
    y, m, d = 13, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    self.assertIsNone(returned_date)
    # t4
    # both month and day are less than 13, so date is unconclusive
    y, m, d = 13, 4, 13
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    self.assertIsNone(returned_date)
    # t5
    # this hypothesis tests an exception and both day and month are less than 13
    # ie, when both (day & month) are equal
    y, m, d = 32, 4, 4
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t6
    # here, differently from above, year, month & day are logically obtainable, no matter it's positioning,
    # ie date is 'conclusive'
    y, m, d = 32, 4, 13
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)

  def test_convert_date_to_mmddyyyy_str_or_none(self):
    # t1
    # this hypothesis used zfill = 2
    y, m, d = 2023, 4, 5
    zfill = 2
    pdate = datetime.date(year=y, month=m, day=d)
    returned_date = intr.convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep='/', zfill=zfill)
    expected_strdate = f'{m:02}/{d:02}/{y}'
    self.assertEqual(returned_date, expected_strdate)
    # t2
    # this hypothesis used zfill = 0 (next one is the same, but let it be defaulted)
    zfill = 0
    returned_date = intr.convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep='/', zfill=zfill)
    expected_strdate = f'{m}/{d}/{y}'
    self.assertEqual(returned_date, expected_strdate)
    # t3
    # same as above, but letting zfill goes in as default
    returned_date = intr.convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep='/')
    self.assertEqual(returned_date, expected_strdate)
    # t4
    # same as above, but changing the value of sep
    sep = '.'
    returned_date = intr.convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep)
    expected_strdate = f'{m}{sep}{d}{sep}{y}'
    self.assertEqual(returned_date, expected_strdate)
    # t5
    # something weird to send in and get back None
    y, m, d = 'bla', 'foo', 'bar'
    pdate = y + m + d
    returned_date = intr.convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate)
    self.assertIsNone(returned_date)
    # t6
    # testing an above function's variation that instead of returning None returns 'today'
    sep = '/'
    returned_date = intr.convert_date_to_strmmddyyyy_or_itsreprtoday_opt_sep_zfill('rubish', sep)
    expected_strdate = f'{self.today.month}{sep}{self.today.day}{sep}{self.today.year}'
    self.assertEqual(returned_date, expected_strdate)

  def test_convert_to_date_or_none_w_strdate_opt_sep_posorder(self):
    # t1
    # this hypothesis keeps day above 12 so that date is conclusive
    # ie, day and month are not unconclusive between themselves,
    # for sep and posorder are not passed into, needing to be introspected somewhere inside the code
    y, m, d = 2023, 4, 15
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t2
    # this hypothesis keeps day below 13, making date unconclusive, and then
    # expecting None
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m}-{d}'
    returned_date = intr.introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate)
    self.assertIsNone(returned_date)
    # t3
    # this third hypothesis is like the one above but passes in sep and posorder
    # expecting not None but a valid date
    y, m, d = 2023, 4, 5
    strdate = f'{y}-{m}-{d}'
    sep, posorder = '-', 'ymd'
    returned_date = intr.introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate, sep, posorder)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(returned_date, expected_date)
    # t4
    # though sending in 'rubish', this hypothesis uses a function variation
    # that returns today instead of None
    rubbish_to_pass_in = 'bla bla'
    returned_date = intr.introspect_n_convert_strdate_to_date_or_today(rubbish_to_pass_in)
    expected_date = self.today
    self.assertEqual(returned_date, expected_date)

  def test_transform_transpose_strdate_to_date_under_posfield_variations(self):
    # t1 transform/transpose an arbitrary strdate giving its sep & posorder
    strdate = '2020-7-15'
    fromsep, tosep = '-', '/'
    from_posorder, to_posorder = 'ymd', 'mdy'
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate, fromsep, from_posorder, tosep, to_posorder, zfill=2
    )
    expected_strdate = '07/15/2020'
    self.assertEqual(expected_strdate, returned_strdate)
    # 2 same as t1 with a different input set
    strdate = '7/8/2020'
    fromsep, tosep = '/', '-'
    from_posorder, to_posorder = 'mdy', 'ymd'
    expected_strdate = '2020-07-08'
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate, fromsep, from_posorder, tosep, to_posorder, zfill=2
    )
    self.assertEqual(expected_strdate, returned_strdate)
    # 3 same as 2 but with leftzero in d & m in input str
    strdate = '07/08/2020'
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate, fromsep, from_posorder, tosep, to_posorder, zfill=2
    )
    self.assertEqual(expected_strdate, returned_strdate)
    # 4 same as 2 & 3 but with no leftzero in d & m in output str, ie without zfill=2
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate, fromsep, from_posorder, tosep, to_posorder
    )
    expected_strdate = '2020-7-8'
    self.assertEqual(expected_strdate, returned_strdate)

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

    # recapitulating:
    # year is 'conclusive' if above 31 (ie, it does not confuse with day)
    # day is 'conclusive' if above 12 (ie, it does not confuse with month,
    # excepting when day and month are equal)
    # if year and day are 'conclusive', date altogether is 'conclusive'
    # date validation itself is done at construction time (datetime.date())
    """
    # t1
    # this hypothesis shows input data having only the last item ['2023-04-14']
    # as conclusive, for posorder, which also shows that the target function
    # is able to find it having at least this one conclusive year-month-day combination
    sd1, sd2, sd3 = ('2023-05-04', '2023-03-04', '2023-04-14')
    strdatelist = [sd1, sd2, sd3]
    expected_sep = '-'
    expected_posorder = 'ymd'
    sep, posorder = intr.find_sep_n_posorder_from_a_strdatelist(strdatelist)
    self.assertEqual((sep, posorder), (expected_sep, expected_posorder))
    # t2
    # this hypothesis shows all input dates as unconclusive between month and day,
    # so it expects a ValueError exception raised
    sd1, sd2, sd3 = ('2023-05-04', '2023-03-04', '2023-2-4')
    strdatelist = [sd1, sd2, sd3]
    self.assertRaises(ValueError, intr.find_sep_n_posorder_from_a_strdatelist, strdatelist)
    # t3
    # this hypothesis concerns an internal rule on the introspection devised here-in
    # which picks up the very first possible sep and posorder found when looping through the list;
    # this particular function does not check the whole consistency; other functions do it;
    # e.g. @see below: function extract_datelist_from_strdatelist_sep_n_posorder_consistent()
    sd1, sd2, sd3 = ('2023.14.05', '2023/03-04', 'bla foo bar')  # only the first one is good
    strdatelist = [sd1, sd2, sd3]
    expected_sep = '.'
    expected_posorder = 'ydm'
    sep, posorder = intr.find_sep_n_posorder_from_a_strdatelist(strdatelist)
    self.assertEqual((sep, posorder), (expected_sep, expected_posorder))
    # t4
    # this hypothesis expands on the one above with removing non-conforming strdates
    # to sep and posorder found
    returned_strlist = intr.remove_strdates_not_conforming_to_sep_n_posorder(strdatelist, sep, posorder)
    expected_strlist = [sd1]  # only the first one is good
    self.assertEqual(returned_strlist, expected_strlist)
    # t5
    # this hypothesis compounds the former two, ie it gets a datelist that
    # is consistent within sep and posorder
    # notice that strdatelist above has only one onsistent item in terms of sep and posorder
    returned_datelist = intr.extract_datelist_from_strdatelist_sep_n_posorder_consistent(strdatelist)
    y, d, m = tuple(sd1.split('.'))  # pay attention to posorder, ie ydm from '2023.14.05'
    y, m, d = int(y), int(m), int(d)
    sd1_as_date = datetime.date(year=y, month=m, day=d)
    expected_datelist = [sd1_as_date]
    self.assertEqual(returned_datelist, expected_datelist)

  def test_strdate_form_with_datamass(self):
    """
    @see module fs/datefs/introspect_dates_datamass.py
      that produces the 12 combination strdates (with zfill=0)
    Example = [
      '2023-5-15', '2023/5/15', '2023.5.15',  # ymd with -, / & '.'
      '2023-15-5', '2023/15/5', '2023.15.5',  # ydm with -, / & '.'
      '15-5-2023', '15/5/2023', '15.5.2023',  # dmy with -, / & '.'
      '5-15-2023', '5/15/2023', '5.15.2023'   # mdy with -, / & '.'
    ]
    With zfill=2, days and months are 2-digit shown, examples:
      instead of '2023-5-15', it's formed as '2023-05-15'
      instead of '5/15/2023', it's formed as '05/15/2023
    """
    # t1
    # this first hypothesis uses zfill = 0
    zfill = 0
    strdatelist, expected_date = dmass.get_testtuple_12strdatelist_n_corresp_date_datamass(zfill)
    for strdate in strdatelist:
      returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
      self.assertEqual(expected_date, returned_date)
    # t2
    # this hypothesis uses zfill = 2
    zfill = 2
    strdatelist, expected_date = dmass.get_testtuple_12strdatelist_n_corresp_date_datamass(zfill)
    for strdate in strdatelist:
      returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
      self.assertEqual(expected_date, returned_date)
    # t3
    # this hypothesis uses zfill = -500 (which will be normalized to 2)
    zfill = -500
    strdatelist, expected_date = dmass.get_testtuple_12strdatelist_n_corresp_date_datamass(zfill)
    for strdate in strdatelist:
      returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
      self.assertEqual(expected_date, returned_date)
    returned_zfill = intr.normalize_zfill_to_0_1_or_2(zfill)
    expected_zfill = 2
    # t4
    # this hypothesis tests zfill separately, ie if zfill = -500, it's normalized to 2
    self.assertEqual(expected_zfill, returned_zfill)

  def test_extract_datelist_from_strdatelist_considering_any_sep_n_posorder(self):
    # t1
    # this hypothesis tests a strdatelist against its one-by-one convertion datelist
    # both strdatelist & datelist are prepared in module 'dmass'
    strdatelist, datelist = dmass.get_testtuple_strdatelist_n_datelist_for_extraction_wo_sep_n_posorder()
    for i, strdate in enumerate(strdatelist):
      expected_date = datelist[i]
      returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
      self.assertEqual(expected_date, returned_date)
    # t2
    # this hypothesis tests ValueError exception due to different sizes
    # between datelist & strdatelist
    self.assertRaises(ValueError, intr.check_n_raise_if_strdatelist_has_any_nonconformant_sep_n_posorder, strdatelist)
    # t3
    # this hypothesis has 'negative' strdates,
    # ie all strdates are unconclusive (expected_dates must all be None's)
    strdatelist = dmass.get_unconclusive_strdatelist_f_extr_wo_sep_n_posorder()
    datelist = [None]*len(strdatelist)
    for i, strdate in enumerate(strdatelist):
      expected_date = datelist[i]
      returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
      self.assertEqual(expected_date, returned_date)
    # t4
    # this hypothesis has day-month-coincidence strdates
    # e.g. 2023-1-1 is consistent for it is indifferent in relation to day & month
    # the rule is day and month should have day about 12 but when both are equal, resulting date is consistent;
    strdatelist, datelist = dmass.get_testtuple_coinc_day_month_sdlist_n_dlist_f_extr_wo_sep_n_posorder()
    for i, strdate in enumerate(strdatelist):
      expected_date = datelist[i]
      returned_date = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
      self.assertEqual(expected_date, returned_date)

  def test_trans_strdate_from_one_format_to_another_w_sep_n_posorder(self):
    # t1
    # this hypothesis (subtest) aims to transform
    # from: '5/12/2023' with ['/', 'dmy']
    # to:  '12.05.2023' with ['.', 'mdy']
    from_strdate, fromsep, from_posorder = '5/12/2023', '/', 'dmy'
    expected_strdate, tosep, to_posorder = '12.05.2023', '.', 'mdy'
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate=from_strdate, fromsep=fromsep, tosep=tosep,
      sourceposorder=from_posorder, targetposorder=to_posorder, zfill=2,
    )
    self.assertEqual(expected_strdate, returned_strdate)
    # t2
    # idem as t1 with another datum sample
    from_strdate, fromsep, from_posorder = '5/6/2023', '/', 'dmy'
    expected_strdate, tosep, to_posorder = '6-5-2023', '-', 'mdy'  # zfill is default
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate=from_strdate, fromsep=fromsep, tosep=tosep,
      sourceposorder=from_posorder, targetposorder=to_posorder,
    )
    self.assertEqual(expected_strdate, returned_strdate)
    # t3
    # this subtest uses a dynamical date (self.today)
    y, m, d = self.today.year, self.today.month, self.today.day
    from_strdate, fromsep, from_posorder = f'{d}/{m}/{y}', '/', 'dmy'
    expected_strdate, tosep, to_posorder = f'{m}-{d}-{y}', '-', 'mdy'  # zfill is default
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate=from_strdate, fromsep=fromsep, tosep=tosep,
      sourceposorder=from_posorder, targetposorder=to_posorder,
    )
    self.assertEqual(expected_strdate, returned_strdate)
    # t4
    # a "non-date" (Feb 30 does not exist!) will be sent in expecting back None
    from_strdate, fromsep, from_posorder = '2023-30-2', '-', 'ydm'
    tosep, to_posorder = '-', 'mdy'  # zfill is default
    returned_strdate = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      strdate=from_strdate, fromsep=fromsep, tosep=tosep,
      sourceposorder=from_posorder, targetposorder=to_posorder,
    )
    self.assertIsNone(returned_strdate)
