#!/usr/bin/env python3
"""
models/budgets/pb/worksheet_batcher.py

import copy
"""
import art.budgetings.budgets.pb.prices_processor as ppr  # ppr.PriceItem, Prices etc
import art.budgetings.budgets.pb.tests.check_n_of_nms_in_filenames as chknm  # chknm.get_unique_nms_from_filenames
import art.budgetings.budgets.pb.price_data_as_dict as pdd  # pdd.gather_data


def list_prices():
  """
  for nm_n_its_priceitemlist in prices.self.nn_n_priceitemlist_dict:
    for pi in nm_n_its_priceitemlist:
      prices_per_nm_o.print_allprices_per_nm()
  """
  prices = pdd.gather_data()
  prices.print_allprices_per_nm()


def show_filenames_check():
  prices = pdd.gather_data()
  ppr.show_qtd_of_prices_per_nm(prices)
  nms_from_filenames = chknm.get_unique_nms_from_filenames()
  print('nms_from_prices', prices.size, 'nms_from_filenames', len(nms_from_filenames))


def show_prices_as_df_or_prettyprint():
  prices = pdd.gather_data()
  # prices.show_prices_as_pandas_df()
  prices.show_prices_as_prettyprint()


def process():
  # list_prices()
  show_prices_as_df_or_prettyprint()


if __name__ == '__main__':
  """
  """
  # adhoctest1()
  process()
