#!/usr/bin/env python3
"""
This script is adhoc, ie, it doesn't belong "directly" to the underlying pyapp.
In words, it checks a logical deduction that the implementation of
  cell_letters as a number system
  is flawed for moving within the tableau (worksheet).
Here is the explanation.
  1) the number system implemented does not have 0's (zeroes);
  2) because the move operation is an addition or subtraction to the cell_letters,
     at some moments, this operation will fall into a zero:
     example: Z+1 must be shifted one (+1) to AA.
     When this happens, a plus-one operation becomes plus-two.
  3) because of this above, the following two operations are not ambiguous, ie:
    3.1) Z + 1 = AA is the same as Z + 2 = AA
    3.2) AA - 1 = Z is the as AA - 2 = Z
    If we compound 3.1 with 3.2, we may end up with:
      (3.1) Z + 2 = AA and (3.2) AA - 1 = Z
      substituting AA we have:
      Z + 2 = Z + 1 and then 0 = 1 or 0 = -1 (this equality is an inequality)
  4) when many operations are compounded and order are mixed, commutation may be lost if "zero" places are hit.

There are two ways to find that below.
  The simpler one has an output from random numbers such as:

nruns = 3 | total = 64 | baknumber = 64 | dif = 0
nruns = 5 | total = 1075 | baknumber = 1075 | dif = 0
nruns = 7 | total = 899 | baknumber = 899 | dif = 0
nruns = 10 | total = 2904 | baknumber = 2904 | dif = 0
nruns = 12 | total = 380 | baknumber = 379 | dif = 1
nruns = 27 | total = 1384 | baknumber = 1372 | dif = 12
nruns = 45 | total = 3504 | baknumber = 3489 | dif = 15
nruns = 125 | total = 5235 | baknumber = 5268 | dif = -33

Each run forms a parcel ( random.randint(-1000, 1000) ) of a summation.
As can be seen, the more the number of runs, the greater abs(dif) will be.
  'dif' is (total - baknumber) and baknumber is the number from the
  ongoing cell_letters accumulating the summation.
Thus said, backnumber is the "thermometer" that tells us
  that the move-operation is not commutative,
  ie, x,y,z cells-moved to the right may not return to its origin
      with an equal x,y,z cells-moved to the left.

Solution: we don't have it yet, but if we can map,
  one by one, the cell-letters set to the integer set,
  then, it'll work. Lexicographic algorithms may be one way
  to look up into the matter.
  Anyway, it's an open issue now.
  Note: for not moving applications, the conversion algorithm works okay,
        ie, it does map one by one and shift zeroes both ways (forward and backward).
"""
import random
import fs.numberfs.tableaufunctions as tblfs

rnumbers = []
rletters = []
# tblfs.NSYSTEM27SIZE
quad_totalint_totalcells_nparcels = []
innerloopruns = [3, 15, 45, 100]


def generate_random_numbers(innerlooprun):  # innerlooprun = innerloopruns[decimalplace]
  tbl = tblfs.Tableau()
  ongoing_conv_letters = 'a'
  baknumber = 0
  total = 0
  parcelcounter = 0
  positnumcount = 0
  negatnumcount = 0
  for decimalplace in range(3, -1, -1):
    for nsubparcel in range(innerlooprun):
      parcelcounter += 1
      sign_n = random.randint(0, 1)
      sign = 1 if sign_n else -1
      if sign == 1:
        positnumcount += 1
      else:
        negatnumcount += 1
      parcel = sign * (random.randint(0, tblfs.NSYSTEM27SIZE) * tblfs.NSYSTEM27SIZE ** decimalplace)
      if total + parcel < 1:
        # print (' => throwing away parcel  %d | total %d' %(parcel, total))
        continue
      total += parcel
      ongoing_conv_letters = tbl.move_columns_by(ongoing_conv_letters, parcel)
      # print(parcelcounter, 'total %d | parcel %d | decimalplace %d ' %(total, parcel, decimalplace))
    # print ('positnumcount', positnumcount, 'negatnumcount', negatnumcount, positnumcount+negatnumcount)
    # print('ongoing_conv_letters', ongoing_conv_letters)
    baknumber = tbl.convert_columnletters_to_number_nonrecursively(ongoing_conv_letters)
    # print('baknumber', baknumber)
  quad = total, baknumber, total - baknumber, innerlooprun
  quad_totalint_totalcells_nparcels.append(quad)


def report():
  for quad in quad_totalint_totalcells_nparcels:
    total, baknumber, diff, innerlooprun = quad
    print('total', total, 'baknumber', baknumber, 'diff', diff, innerlooprun, innerlooprun)


def do_loopruns():
  for innerlooprun in innerloopruns:
    generate_random_numbers(innerlooprun)
  report()


def lesser_number_test(nruns):
  ongoing_conv_letters = 'a'
  total = 0
  baknumber = 0
  for i in range(nruns):
    parcel = random.randint(-1000, 1000)
    if parcel == 0 or (total + parcel) <= 0:
      continue
    total += parcel
    ongoing_conv_letters = tbl.move_columns_by(ongoing_conv_letters, parcel)
    baknumber = tbl.convert_columnletters_to_number_nonrecursively(ongoing_conv_letters)
  # adjust baknumber with -1 for 'a' is 1 and algo the origin
  baknumber -= 1
  print('nruns =', nruns, '| total =', total, '| baknumber =', baknumber, '| dif =', total - baknumber)


def loop_lesser():
  for nruns in [3, 5, 7, 10, 12, 27, 45, 125]:
    lesser_number_test(nruns)


def process():
  # one way of testing
  # do_loopruns()
  # a simpler way of testing
  loop_lesser()


if __name__ == "__main__":
  process()
