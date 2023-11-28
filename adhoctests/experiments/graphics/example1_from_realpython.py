#!/usr/bin/env python3
"""

https://realpython.com/pandas-plot-python/
download_url = (
    "https://raw.githubusercontent.com/fivethirtyeight/"
    "data/master/college-majors/recent-grads.csv"
)
"""
import pandas as pd
import matplotlib.pyplot as plt
import commands.graphics.bcb.make_graphics_datafolder_n_dld_if_needed as grph


def plot1():
  """
  type(df)
  pandas.core.frame.DataFrame
  """

  df = pd.read_csv(grph.get_example1_filepath())
  pd.set_option("display.max.columns", None)
  df.head()
  df.plot(x="Rank", y=["P25th", "Median", "P75th"])
  plt.show()


def adhoctest():
  plot1()


def process():
  """
  """
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
