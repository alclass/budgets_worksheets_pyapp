#!/usr/bin/env python3
"""
fs/numberfs/test_tableau_letter_index_generator.py
  Unit Tests for tableau_iletter_index_generator.py
"""
import unittest
import lib.numberfs.tableau_letter_index as tli  # .TableauLetterIndexGenerator
import lib.numberfs.tableau_letter_index_generator as tlig  # .TableauLetterIndexGenerator
import lib.numberfs.letterlist_inherited as llst  # .LetterList


class TestCaseTableauLetterIndexGenerator(unittest.TestCase):

  def setUp(self):
    self.geno = tlig.TableauLetterIndexGenerator()

  def test_generate_some(self):
    expected_letter = 'a'.upper()
    returned_letterindices = self.geno.get_genfirst_n_letterindices(3)
    expected_letterindices = ['A', 'B', 'C']
    self.assertEqual(expected_letterindices, returned_letterindices)
    #      start=3, end=7, decrescent=False
    # self.assertEqual(expected_b1idx, returned_b1idx)

  def test_comparing_the_80_first_gen_indices(self):
    """
    Obs: the generator, specially for letterindices, generates sequencially started at 0-based index 0.
    If an arbitrary "high" index is wanted, it may be gotten from the functions tested above.
    """
    # t1 same as t1 in the method-test above
    # but comparing the 800 first b1_indices with their corresponding letterindices
    total_to_gen = 80
    expected_letterindices = []
    tlio = tli.TableauLetterIndex('A')
    returned_letterindices = list(self.geno.get_genfirst_n_letterindices(total_to_gen))
    for i in range(total_to_gen):
      expected_letterindices.append(tlio.letterindex)
      tlio.add_one()
    returned_b1indices = list(self.geno.get_genfirst_n_base1indices(total_to_gen))
    self.assertEqual(total_to_gen, len(returned_b1indices))
    self.assertEqual(total_to_gen, len(returned_letterindices))
    self.assertEqual(list(range(1, total_to_gen+1)), returned_b1indices)
    self.assertEqual(expected_letterindices, returned_letterindices)

  def test_above_800_first_indices(self):
    # t1 same as the method-tests above, but using a numberindex 'well' greater than 800
    total_to_gen = 1000
    returned_letterindices = self.geno.get_genfirst_n_letterindices(total_to_gen)
    tlio = tli.TableauLetterIndex('A')
    expected_letterindices = []
    for i in range(total_to_gen):
      # notice that the first element 'A' was added previously above
      expected_letterindices.append(tlio.letterindex)
      tlio.add_one()
    returned_b1indices = list(self.geno.get_genfirst_n_base1indices(total_to_gen))
    self.assertEqual(total_to_gen, len(returned_b1indices))
    self.assertEqual(total_to_gen, len(returned_letterindices))
    self.assertEqual(list(range(1, total_to_gen+1)), returned_b1indices)
    self.assertEqual(expected_letterindices, returned_letterindices)

  def test_range_generation_crescent_decrescent(self):
    start, end = 3, 7
    should_be_size = end - start + 1
    # notice that, differently from range(start, end), 'end' here is included
    returned_crescent = self.geno.get_genletterindices_within_range_as_0basedidx(start=start, end=end, decrescent=False)
    returned_decrescent = self.geno.get_genletterindices_within_range_as_0basedidx(start=start, end=end, decrescent=True)
    expected_rev_decrescent = list(reversed(returned_decrescent))
    expected_rev_crescent = list(reversed(returned_crescent))
    self.assertEqual(expected_rev_decrescent, returned_crescent)
    self.assertEqual(expected_rev_crescent, returned_decrescent)
    self.assertEqual(should_be_size, len(returned_crescent))
    self.assertEqual(should_be_size, len(returned_decrescent))

  def test_an_even_greater_letterindex(self):
    letterindex_ini = 'XZTGK'
    tlio_ongo = tli.TableauLetterIndex(letterindex=letterindex_ini)
    displacement = 100
    start, end = tlio_ongo.base0index, tlio_ongo.base0index + displacement - 1
    returned_letterindex_list = []
    expected_letterindex_list = []
    for letterindex in self.geno.gen_letterindices_within_range_as_0basedidx(start=start, end=end):
      returned_letterindex_list.append(letterindex)
      expected_letterindex_list.append(tlio_ongo.letterindex)
      tlio_ongo.add_one(inplace=True)
    self.assertEqual(expected_letterindex_list, returned_letterindex_list)
    self.assertEqual(displacement, len(returned_letterindex_list))
    # loop back up
    # remove the one added extra at the end of the above loop
    tlio_ongo.subtract_one(inplace=True)
    b_returned_letterindex_list = []
    b_expected_letterindex_list = []
    # tn goes now descending
    for letterindex in self.geno.gen_letterindices_within_range_as_0basedidx(start=start, end=end, decrescent=True):
      b_returned_letterindex_list.append(letterindex)
      b_expected_letterindex_list.append(tlio_ongo.letterindex)
      tlio_ongo.subtract_one(inplace=True)
    self.assertEqual(expected_letterindex_list, returned_letterindex_list)
    self.assertEqual(displacement, len(returned_letterindex_list))
    # reverse one of the descending list and compare to one of the ascending
    rev_b_returned_letterindex_list = list(reversed(b_returned_letterindex_list))
    self.assertEqual(expected_letterindex_list, rev_b_returned_letterindex_list)
    # check back the very first one
    # recompose/restore the one lost at the end of the above loop
    tlio_ongo.add_one(inplace=True)
    self.assertEqual(letterindex_ini, tlio_ongo.letterindex)

