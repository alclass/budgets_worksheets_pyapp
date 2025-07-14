import datetime
import unittest
import art.budgetings.histprice.histprices_workbook_mod as hp  #.TripleHistPrice


class TestCase(unittest.TestCase):

  def test_triplehist(self):
    """
    """
    tuplelist = []
    # t1 an input set, expecting conversion from which the class
    y, m, d = 2013, 7, 30
    strdotd = f'{d}.{m}.{y}'
    dotd, commasep_n, sap_order = strdotd, '2.466,44', 4505421893
    expect_float = float(commasep_n.replace('.', '').replace(',', '.'))
    expect_date = datetime.date(year=y, month=m, day=d)
    thp = hp.TripleHistPrice(dotd, commasep_n, sap_order)
    self.assertEqual(thp.date, expect_date)
    self.assertAlmostEquals(thp.price, expect_float)
    self.assertEqual(thp.sap_order, sap_order)
    # t2 same as t1 with another input set and with zfill=2 (ie, leftzero for dd & mm)
    y, m, d = 2020, 2, 28
    strdotd = f'{d}.{m:02}.{y:02}'
    dotd, commasep_n, sap_order = strdotd, '8.865,67', 4510003704
    expect_float = float(commasep_n.replace('.', '').replace(',', '.'))
    expect_date = datetime.date(year=y, month=m, day=d)
    thp = hp.TripleHistPrice(dotd, commasep_n, sap_order)
    self.assertEqual(thp.date, expect_date)
    self.assertAlmostEquals(thp.price, expect_float)
    self.assertEqual(thp.sap_order, sap_order)
    # t3 same as t2 with another input set
    y, m, d = 2020, 3, 31
    strdotd = f'{d}.{m:02}.{y:02}'
    dotd, commasep_n, sap_order = strdotd, '5.601,70', 4510087906
    expect_float = float(commasep_n.replace('.', '').replace(',', '.'))
    expect_date = datetime.date(year=y, month=m, day=d)
    thp = hp.TripleHistPrice(dotd, commasep_n, sap_order)
    self.assertEqual(thp.date, expect_date)
    self.assertAlmostEquals(thp.price, expect_float)
    self.assertEqual(thp.sap_order, sap_order)
