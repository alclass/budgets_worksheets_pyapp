#!/usr/bin/env python3
"""
fs/numberfs/test_tableau_letter_index_generator.py
  Unit Tests for tableau_iletter_index_generator.py
"""
import unittest
import fs.numberfs.tableau_letter_index as tli  # .TableauLetterIndexGenerator
import fs.numberfs.tableau_letter_index_generator as tlig  # .TableauLetterIndexGenerator
import fs.numberfs.letterlist_inherited as llst  # .LetterList


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
      expected_letterindices.append(tlio.letterindex)
      tlio.add_one()
    returned_b1indices = list(self.geno.get_genfirst_n_base1indices(total_to_gen))
    self.assertEqual(total_to_gen, len(returned_b1indices))
    self.assertEqual(total_to_gen, len(returned_letterindices))
    self.assertEqual(list(range(1, total_to_gen+1)), returned_b1indices)
    self.assertEqual(expected_letterindices, returned_letterindices)



  def test_range_generation_crescent_decrescent(self):
    expected_gen_list = list('DEFGH')
    return_gen_list = []
    counted = 0
    crescent = []
    decrescent = []
    # notice that, differently from range(start, end), 'end' here is included
    returned_crescent = self.geno.get_genletterindices_within_range_as_0basedidx(start=3, end=7, decrescent=False)
    returned_decrescent = self.geno.get_genletterindices_within_range_as_0basedidx(start=3, end=7, decrescent=True)
    expected_rev_decrescent = list(reversed(returned_decrescent))
    expected_rev_crescent = list(reversed(returned_crescent))
    self.assertEqual(expected_rev_decrescent, returned_crescent)
    self.assertEqual(expected_rev_crescent, returned_decrescent)


  def ztest_comparing_the_80_first_gen_indices(self):
    """
    Obs: the generator, specially for letterindices, generates sequencially started at 0-based index 0.
    If an arbitrary "high" index is wanted, it may be gotten from the functions tested above.
    """
    # t1 same as t1 in the method-test above
    # but comparing the 800 first b1_indices with their corresponding letterindices
    expected_letter = 'a'.upper()
    b1idx_param = 1
    returned_letteridx = self.tlio.set_letterindex_transposing_from_1basedindex(b1idx_param)
    # t1 starting by b1_idx 1 which maps to letteridx 'A'
    self.assertEqual(expected_letter, returned_letteridx)
    letteridx_param = expected_letter
    returned_b1idx = self.tlio.set_1basedidx_transposing_from_letterindex(letteridx_param)
    expected_b1idx = b1idx_param
    # t2 does the t1 comeback comparison
    self.assertEqual(expected_b1idx, returned_b1idx)
    total_to_gen = 80
    letterindices = list(self.tlio.gen_first_n_letterindices(total_to_gen))
    b1indices = list(self.tlio.gen_first_n_base1indices(total_to_gen))
    for i in range(total_to_gen):
      letteridx = letterindices[i]
      b1idx = b1indices[i]
      returned_letteridx = self.tlio.set_letterindex_transposing_from_1basedindex(b1idx)
      returned_b1idx = self.tlio.set_1basedidx_transposing_from_letterindex(letteridx)
      self.assertEqual(b1idx, returned_b1idx)
      self.assertEqual(letteridx, returned_letteridx)

  def ztest_above_800_first_indices(self):
    # t1 same as the method-tests above, but using a numberindex 'well' greater than 800
    b1idx_param = 10000
    returned_letteridx = self.tlio.set_letterindex_transposing_from_1basedindex(b1idx_param)
    expected_letteridx = 'NTP'
    self.assertEqual(expected_letteridx, returned_letteridx)
    letteridx_param = 'PTN'
    returned_b1idx = self.tlio.set_1basedidx_transposing_from_letterindex(letteridx_param)
    expected_b1idx = 11350
    self.assertEqual(expected_b1idx, returned_b1idx)
    self.assertGreater(expected_b1idx, b1idx_param)
    self.assertGreater(letteridx_param, expected_letteridx)

  def ztest_an_even_greater_letterindex(self):
    # t1 same as the previous method-test above,
    # using a still greater letterindex but only indirectly testing the b1_idx
    letteridx_param = 'XZTGK'  # numberidx will be gotten and compared back
    returned_b1idx = self.tlio.set_1basedidx_transposing_from_letterindex(letteridx_param)
    returned_letteridx = self.tlio.set_letterindex_transposing_from_1basedindex(returned_b1idx)
    self.assertEqual(letteridx_param, returned_letteridx)
    gottenback_b1idx = self.tlio.set_1basedidx_transposing_from_letterindex(returned_letteridx)
    self.assertEqual(gottenback_b1idx, returned_b1idx)

  def ztest_range_generation(self):
    expected_gen_list = list('DEFGH')
    return_gen_list = []
    counted = 0
    # notice that, differently from range(start, end), 'end' here is included
    for lindices in self.tlio.gen_letterindices_within_range_as_0basedidx(start=3, end=7, decrescent=False):
      return_gen_list.append(lindices)
      counted += 1
    self.assertEqual(expected_gen_list, return_gen_list)
    self.assertEqual(len(expected_gen_list), counted)
    return_gen_list = []
    counted = 0
    for lindices in self.tlio.gen_letterindices_within_range_as_0basedidx(start=3, end=7, decrescent=True):
      return_gen_list.append(lindices)
      counted += 1
    expected_gen_list = list(reversed(expected_gen_list))  # list('DEFGH') reverse => list('HGFED')
    # t3 same as t1 but now in descending order (where former list will equal the latter as reversed)
    self.assertEqual(expected_gen_list, return_gen_list)


  def ztest_arithmetic(self):
    """
    tli1.set_letterindex_transposing_from_0basedidx(2)
    tli2.set_letterindex_transposing_from_0basedidx(3)
    tli3 = tli1 + tli2
    print('tli1 + tli2 = tli3', tli1, tli2, tli3)
    tli3 = tli2 - tli1
    print('tli2 - tli1 = tli3', tli2, tli1, tli3)
    tli3 = tli1 - tli2
    print('tli1 - tli2 = tli3', tli1, tli2, tli3)

    """
    letter, number = 'B', 2
    tli1 = tli.TableauLetterIndex(letter)
    self.assertEqual(tli1.letterindex, letter)
    self.assertEqual(tli1.base1idx, number)
    soma = number
    letter, number = 'C', 3
    tli2 = tli.TableauLetterIndex(letter)
    self.assertEqual(tli2.letterindex, letter)
    self.assertEqual(tli2.base1idx, number)
    tli3 = tli1 + tli2
    soma += number
    expected_letter = 'E'  # ie, B=2 + C=3 = E=5
    self.assertEqual(tli3.letterindex, expected_letter)
    self.assertEqual(tli3.base1idx, soma)
    letter = 'BFWX'
    tli1 = tli.TableauLetterIndex(letter)
    n1 = tli1.base1idx
    letter = 'KKKK'
    tli2 = tli.TableauLetterIndex(letter)
    n2 = tli2.base1idx
    tli3 = tli1 + tli2
    # the second param is a concatenation, not an index summing
    self.assertNotEqual(list(tli3.letterindex), list(tli1.letterindex) + list(tli2.letterindex))
    n3 = n1 + n2
    direct_n3 = tli3.base1idx
    self.assertEqual(n3, direct_n3)
    ll1 = llst.LetterList(tli1.letterindex)  # 'BFWX'
    ll2 = llst.LetterList(tli2.letterindex)  # 'KKKK'
    ll3 = ll1 + ll2
    # notice that tli is a TableauLetterIndex and ll3 is a LetterList
    # both were "constructed" from different variables summing up
    self.assertTrue(tli3.letterindex, ll3.get_as_str_n_reversed())
    # list sum is in fact a concatenation not an arithmetic
