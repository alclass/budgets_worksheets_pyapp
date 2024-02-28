#!/usr/bin/env python3
"""
models/budgets/pb/price_data_as_dict.py

"""
import copy
import os
from models.budgets.pb.prices_processor import PriceItem
from models.budgets.pb.prices_processor import Prices
from models.budgets.pb.prices_processor import show_qtd_of_prices_per_nm
import models.budgets.pb.tests.check_n_of_nms_in_filenames as chknm  # chknm.get_unique_nms_from_filenames


def gather_data():
  prices = Prices()
  # pricedata_list = []
  # NM 1
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 10668440, None
  pi.fname = '01 centelhador fêmea-fêmea p cc [A002] 10668440.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 72.59, 'Mercado Livre / Comunicação10'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3115630592-centelhador-n-fmea-x-n-fmea-reto-painel-surto-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 69.0, 'Tolentino Radiocomunicação'
  pi.url = 'https://www.tolentinoradiocomunicacao.com.br/index.php?route=product/product&product_id=319'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 123.83, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 2
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12790478, None
  pi.fname = '02 Conjunto de aterramento cellflex1_2 [601] 12790478.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 128.6, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/conjunto-de-aterramento-para-cabo-de-rg-213-rfs-kmp/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2019-08-15'
  pi.sapreq = 4509486915
  pi.netprice, pi.currency = 89.44, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 93.75, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 3
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12788990, None
  pi.fname = '03 Conjunto de aterramento cellflex7_8 [512455] 12788990.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 168.8, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/conjunto-de-aterramento-para-cabo-de-rg-213-rfs-kmp/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 70.2, 'Cross do Brasil'
  pi.url = 'https://crossdasil.commercesuite.com.br/kit-aterramentos/kit-aterramento-78-'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 93.75, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 4
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11874626, None
  pi.fname = '04 conjunto de aterramento coaxial RGC213 [512450] 11874626.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 42.0, 'Cross do Brasil'
  pi.url = 'https://www.crossdobrasil.com.br/kit-aterramentos/kit-aterramento-rgc213-'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 148.60, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/conjunto-de-aterramento-para-cabo-de-rg-213-rfs-kmp/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 61.6, 'MercadoLivre / Cross do Brasil'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2045345929-kit-aterramento-rgc213-3-unidades-_JM#position=14&search_layout=stack&type=item&tracking_id=bc5fa194-752e-4058-b227-7dd495a4ff08'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 74.64, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 5
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12787540, 11884472
  pi.fname = '05 protetor contra surtos antena [CA17] 12787540.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 127.55, 'Mercado Livre / Store Comércio'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-1791043867-protetor-dps-contra-raios-e-surtos-cabo-coaxial-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 85.9, 'Oficina dos Bits'
  pi.url = 'https://www.oficinadosbits.com.br/produto/protetor-dps-clamper-s800-812-x-050-bnc-fm-fm-7482/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 82.2, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 6
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11839470, 11884472
  pi.fname = '06 adaptador p cc mini-UHF macho p UHF fêmea [KLC-20] 11839470.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 19.9, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/conector-conversor-uhf-femea-x-uhf-mini-motorola-klc-20-klc-conectores-p489'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-24'
  pi.openprice, pi.supplier = 24.0, 'Shop Antenas'
  pi.url = 'https://www.shopantenas.com.br/radiocomunicacao/conectores/conector-uhf-femea-para-uhf-macho-mini-motorola-ap0318'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 24.57, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 7
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11671439, None
  pi.fname = '07 adaptador cabo coaxial [KLC1] 11671439.xlsx'
  pi_tmp = copy.copy(pi)
  prices.add_price_via_nm(pi.nmcode, pi)
  pi.date = '2021-10-28'
  pi.openprice, pi.supplier = 27.95, 'Magalu'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-10-28'
  pi.openprice, pi.supplier = 26.68, 'Rádio Componentes'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-10-28'
  pi.openprice, pi.supplier = 25.90, 'ShopAntenas'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 26.07, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 8
  pi = PriceItem()
  pi.nmcode, nm_alt = 11642305, None
  pi.fname = '08 adaptador cabo coaxial [KLC-18] 11642305.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-24'
  pi.openprice, supplier = 27.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-de-conversao-n-femea-x-tnc-macho-klc-18-p1084'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-24'
  pi.openprice, supplier = 36.67, 'Magalu / MultComercial'
  pi.url = 'https://www.magazineluiza.com.br/adaptador-macho-tnc-reto-e-femea-n-klc-18-gav-134-klc-multcomercial/p/cbckj24gje/ga/otga/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 24.64, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 9
  pi = PriceItem()
  pi.nmcode, nm_alt = 11642768, None
  pi.fname = '09 adaptador cabo coaxial [KLC-19] 11642768.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 36.8, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/adaptador-n-macho-x-femea-tnc-klc-klc-19/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 32.6, 'Mercado Livre / STM Telecom'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2778718223-adaptador-converso-reto-n-50-ohms-macho-x-tnc-fmea-klc-19-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 24.57, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 10
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 10394994, None
  pi.fname = '10 adaptador cabo coaxial [KA-1] 10394994.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 20.0, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/adaptador-uhf-femea-x-femea-reto-ka-1-gav-97-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 16.9, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-uhf-femea-x-femea-emenda-para-cabo-rg-58-rg-213-p467'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 16.38, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 11
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11718061, None
  pi.fname = '11 adaptador cabo coaxial [KLC-2] 11718061.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 22.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-bnc-femea-x-n-macho-p585'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 19.01, 'Shop Antena'
  pi.url = 'https://www.shopantenas.com.br/conectores/adaptadores/conversao-entre-series/adaptador-de-conversao-reto-n-50-ohms-macho-x-bnc-50-ohms-femea-klc-2'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 23.11, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 12
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11460039, None
  pi.fname = '12 adaptador cabo coaxial [CA-1] 11460039.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 21.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-n-emenda-reto-2-femea-p532'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 27.21, 'Magalu / MultComercial'
  pi.url = 'https://www.magazineluiza.com.br/adaptador-n-50-ohms-femea-x-femea-reto-ca-1-gav-53-klc-multcomercial/p/kg6b2e02e4/in/otin/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 22.3, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 13
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11467734, None
  pi.fname = '13 adaptador cabo coaxial [KLC-6] 11467734.xlsx'
  # adaptador de conversão reto UHF Macho x N 50 Ohms Fêmea klc-6
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 19.57, 'Magalu / Shop Antena'
  pi.url = 'https://www.magazineluiza.com.br/adaptador-de-conversao-reto-uhf-macho-x-n-50-ohms-femea-klc-6-klc-conectores/p/fckjf7664c/ga/otga/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 22.44, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 14
  pi = PriceItem()
  pi.nmcode, nm_alt = 11460040, None
  pi.fname = '14 adaptador cabo coaxial [CA-7] 11460040.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 28.0, 'Rádio Componentes'
  pi.url = 'https://www.shopantenas.com.br/conectores/adaptadores/conversao-entre-series/adaptador-de-conversao-reto-n-50-ohms-macho-x-uhf-femea-klc-5'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 23.5, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # MN 15
  pi = PriceItem()
  pi.nmcode, nm_alt = 11468023, None
  pi.fname = '16 adaptador cabo coaxial [CA-3] 11468023.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 29.0, 'Rádio Componentes'
  pi.url = 'https://www.shopantenas.com.br/conectores/adaptadores/conversao-entre-series/adaptador-de-conversao-reto-n-50-ohms-macho-x-uhf-femea-klc-5'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 27.19, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 16
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11642770, 11795587
  pi.fname = '16 adaptador cabo coaxial [KLC-5] 11642770.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 34.9, 'Shop Antena'
  pi.url = 'https://www.shopantenas.com.br/conectores/adaptadores/conversao-entre-series/adaptador-de-conversao-reto-n-50-ohms-macho-x-uhf-femea-klc-5'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 27.7, 'Shopee Sckytecc Telecom'
  pi.url = 'https://shopee.com.br/Adaptador-Convers%C3%A3o-Reto-N-50ohms-Macho-X-Uhf-F%C3%AAmea-Klc-5-i.373766666.2923729706'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 26.82, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 17
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12787443, None
  pi.fname = '17 adaptador cabo coaxial [KA-8] 12787443.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 17.8, 'Fazolo Componentes'
  pi.url = 'https://fazolo.com.br/componentes-eletronicos/adaptador-uhf-machouhf-femea-reto-ka-8'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 19.95, 'Shopee / Rádio Componentes'
  pi.url = 'https://shopee.com.br/Adaptador-Uhf-Macho-x-Uhf-F%C3%AAmea-KA-8-i.341183200.9963662804'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 23.57, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 18
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11484889, None
  pi.fname = '18 cabo cellflex 1_2 Andrew ou simi [RFS] 11484889.xlsx'
  pi.meas_unit = 'metro'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 39.9, 'Shop Web'
  pi.url = 'https://shopweb.com.br/produto/cabo-cellflex-1-2-hansen-100-metros/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 58.67, 'Magalu / Bit Electronics'
  pi.url = 'https://www.magazineluiza.com.br/cabo-cellflex-1-2-kmp-metro-rfs/p/adeg446jk5/in/cbad/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 65.86, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 19
  pi = PriceItem()
  pi.nmcode, nm_alt = 12152353, None
  pi.fname = '19 cabo cellflex 7_8 Andrew ou simi [LCF78-50JA-A0] 12152353.xlsx'
  pi.meas_unit = 'metro'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 49.5, 'Drucos'
  pi.url = 'https://www.lojadrucos.com.br/cabo-de-descida-cellflex-7-8-quot-40-metros-copia-drt-626-h'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 44.35, 'Bit Electronics'
  pi.url = 'https://www.bitelectronics.com.br/telecomunicacao/cabos/cabo-cellflex-78-kmp-metro'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 137.29, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 20
  pi = PriceItem()
  pi.nmcode, nm_alt = 11783027, None
  pi.fname = '20 cabo coaxial RGC213 [RGC213-50J] 11783027.xlsx'
  pi.meas_unit = 'metro'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 14.5, 'Aquário'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi.url = 'https://loja.aquario.com.br/cabo-coaxial-por-metro-linear-tipo-rgc-213/p'
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 14.9, 'Cross do Brasil'
  pi.url = 'https://www.crossdobrasil.com.br/cabos/cabo-coaxial-rgc213'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 12.9, 'Keraxstore'
  pi.url = 'https://www.keraxstore.com.br/cabo-coaxial-rgc213-50-ohms'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 13.57, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 21
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12791677, None
  pi.fname = '21 conector fêmea cabo coaxial RG59 [USF 00907D] 12791677.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 9.49, 'Village Home Center BR'
  pi.url = 'https://www.villagehomecenter.com.br/conector-femea-de-rosca-rg59-para-cabo-coaxial-com-4-pecas-tblack/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 5.0, 'Comercial EletronSP'
  pi.url = 'https://www.comercialeletronsp.com.br/conector-f-keystone-para-cabo-coaxial-rg-59-rg-6-antena-femea-femea'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 13.0, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 22
  pi = PriceItem()
  pi.nmcode, nm_alt = 12790140, None
  pi.fname = '22 conector BNC macho RG59 [USM 000900-D] 12790140.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 5.7, 'Solução Cabos'
  pi.url = 'https://www.solucaocabos.com.br/conector-bnc-macho-rg59-compressao-pino-fixo/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 5.09, 'Loja Elétrica'
  pi.url = 'http://www.lojaeletrica.com.br/conector-bnc-macho-rg5962-com-rosca-cbn1110-quest,product,2170100680049,dept,0.aspx'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 13.73, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 23
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787917, None
  pi.fname = '23 conector BNC macho RG58 [608005] 12787917.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 2.4, 'Ecotron'
  pi.url = 'https://www.ecotroncomponentes.com.br/componentes-eletronicos/conector-bnc-macho-50r-crimpar-rg58-twb108a-tower'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 2.8, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-bnc-macho-rg58-u-jl31085a-jiali.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 11.38, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 24
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12787854, None
  pi.fname = '24 conector IEC fêmea reto [602000] 12787854.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 11.0, 'Cross do Brasil'
  pi.url = 'https://www.crossdobrasil.com.br/conectores/conector-iec-femea-reto-0-6x3-7-solda'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 15.05, 'Magalu / Mult E-commerce'
  pi.url = 'https://www.magazineluiza.com.br/conector-iec-169-13-tipo-1-6-5-6-femea-angular-cabo-painel-prensa-cabo-0-3-1-8-60318-gav-85-klc-multcomercial/p/ec2dkd2f2j/te/ppcl/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 54.85, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 25
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12790072, None
  pi.fname = '25 conector mini-UHF macho p cc RG58 [USM 00304] 12790072.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 12.35, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/mc145436ap-mc145lc436p-freq-receiver-p858'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 17.9, 'Shop Antenas'
  pi.url = 'https://www.shopantenas.com.br/conector-mini-uhf-macho-solda-rg58-mini-motorola-ap0562'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 12.19, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 26
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11762152, None
  pi.fname = '26 conector N fêmea angular p cc RG58 [CF-74] 11762152.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 33.34, 'Central Cabos'
  pi.url = 'https://www.centralcabos.com.br/conector-n-femea-rgc-58/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 25.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/conector-n-femea-prensa-cabo-rgc-rg58-cf-19-p840'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 22.75, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 27
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12790046, None
  pi.fname = '27 conector N fêmea p cabo RG6 [USF 00013-C] 12790046.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 33.34, 'Village Home Center BR'
  pi.url = 'https://www.villagehomecenter.com.br/conector-femea-de-compressao-rg6-para-cabo-coaxial-com-4-pecas-tblack/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 25.19, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 28
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12790421, None
  pi.fname = '28 conector N fêmea RGC213 [USF 00012-E] 12790421.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 15.9, 'Cross do Brasil'
  pi.url = 'https://www.crossdobrasil.com.br/conectores/conector-n-femea-reto-rgc213'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 39.8, 'Mercado Livre / Tolentino1'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-1460401056-conector-n-femea-prensa-cabo-para-cabo-rgc213-usf-12e-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 18.12, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 29
  pi = PriceItem()
  pi.nmcode, nm_alt = 11717388, None
  pi.fname = '29 conector N F p Cabo Cellflex 1_2 [KLF-44] 11717388.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 42.59, 'Bit Electronics'
  pi.url = 'https://www.bitelectronics.com.br/telecomunicacao/conectores/conector-n-femea-p-cabo-cellflex-12-k'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 59.40, 'Mercado Livre / STM Telecom'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2853486875-5-conectores-cellflex-n-50-ohms-fmea-12-rigido-klf-44-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 41.45, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 30
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12792861, None
  pi.fname = '30 conector N F p cabo cellflex 7_8 [KLF-51] 12792861.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 76.21, 'Magalu / Bit Electronics'
  pi.url = 'https://www.magazineluiza.com.br/conector-n-femea-p-cabo-cellflex-7-8-k-klc/p/dkhc4gca9k/te/ppcl/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 68.33, 'Bit Electronics'
  pi.url = 'https://www.bitelectronics.com.br/telecomunicacao/conectores/conector-n-femea-p-cabo-cellflex-78-k'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 112.3, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 31
  pi = PriceItem()
  pi.nmcode, nm_alt = 12791698, None
  pi.fname = '31 conector N fêmea reto p cc RG58 [USF 00013] 12791698.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 19.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/conector-n-femea-reto-prensa-rg58-cf-3e-p1082'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 17.9, 'Oficina dos Bits'
  pi.url = 'https://www.oficinadosbits.com.br/produto/conector-n-femea-rgc-58-para-pigtail/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 16.25, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 32
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12790074, None
  pi.fname = '32 conector N macho p RG58 [USM 00011-A] 12790074.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 15.0, 'Loja Integrada / Só Conectores'
  pi.url = 'https://soconectores.lojaintegrada.com.br/conector-n-macho-de-crimp-rgc-58'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 20.0, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-n-50-ohms-macho-reto-cabo-crimpagem-rg-rgc-58-pino-solto-cm-4cr-gav-18-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 18.69, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 33
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12787869, None
  pi.fname = '33 conector N macho p RG6 [CM-63] 12787869.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 16.9, 'Shopee / VP Telecom'
  pi.url = 'https://shopee.com.br/Conector-Tnc-Macho-Reto-Para-Cabo-Rgc6-Tm-28-Klc-i.328080137.4587757884'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 29.05, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 34
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12790123, None
  pi.fname = '34 conector N Macho RGC213 [USM 00010-E] 12790123.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 26.9, 'Aquário'
  pi.url = 'https://loja.aquario.com.br/conector-plug-n-macho-para-cabo-rgc213/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 33.5, 'Net Computadores'
  pi.url = 'https://netcomputadores.com.br/p/nmachorgc213-conector-nmacho-para-cabos/17615'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 22.35, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 35
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 12787728, None
  pi.fname = '35 conector N M p cabo cellflex 1_2 [CM-23] 12787728.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 49.05, 'Shopee / STM Telecom'
  pi.url = 'https://shopee.com.br/Conector-Cellflex-N-50-Ohms-Macho-1-2%27%27-Flex%C3%ADvel-Cm-23-i.1060572709.23696917485'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 55.65, 'Mercado Livre / STM Telecom'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2778721703-conector-cellflex-n-50-ohms-macho-12-flexivel-cm-23-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 42.26, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 36
  pi = PriceItem()
  pi.nmcode, pi.nm_alt = 11474498, None
  pi.fname = '36 conector N M p cabo cellflex 7_8 [NM-LCF78-C02] 11474498.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 185.0, 'Broadcast Shop BR'
  pi.url = 'https://www.broadcastshop.com.br/produtos/conector-cabo-7-8-n-macho-rfs-kmp-nm-lcf78-c02/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 186.0, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/conector-cabo-7-8-n-macho-rfs-kmp-nm-lcf78-c02/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 115.91, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 37
  pi = PriceItem()
  pi.nmcode, nm_alt = 12791749, None
  pi.fname = '37 conector TNC fêmea p RG58 [USF 00108] 12791749.xlsx'
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 15.64, 'Shop Antena'
  pi.url = 'https://www.shopantenas.com.br/radiocomunicacao/conectores/conector-tnc-femea-rg58-crimpagem-ap2221'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 13.54, 'Central Cabos'
  pi.url = 'https://www.centralcabos.com.br/conector-tnc-femea-rgc58-crimp/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 9.75, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 38
  pi = PriceItem()
  pi.nmcode, nm_alt = 12347598, None
  pi.fname = '38 conector TNC fêmea p RGC213 [TF-10] 12347598.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2018-05-07'
  pi.sapreq = 4508324093
  pi.netprice, pi.currency = 12.05, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 16.0, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-tnc-femea-reto-cabo-prensa-cabo-rg-213-rgc-213-tf-10-gav-125-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 31.75, 'Mercado Livre / STM Telecom'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3204278693-conector-tnc-fmea-reverso-reto-prensa-cabo-rgrgc-213-tf-21-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 17.07, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 39
  pi = PriceItem()
  pi.nmcode, nm_alt = 10999118, None
  pi.fname = '39 conector TNC macho p RG58 [TM-1] 10999118.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 15.2, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-tnc-macho-reto-cabo-prensa-cabo-rg-58-rgc-58-tm-1-gav-92-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 15.35, 'Pradosom'
  pi.url = 'https://www.pradosom.com.br/telefonia-e-radio/acessorios/conector-tnc-macho-reto-psoldar-tm-1-rgc58-klc'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 11.78, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 40
  pi = PriceItem()
  pi.nmcode, nm_alt = 11766051, None
  pi.fname = '40 conector TNC macho p RGC213 [TM-10] 11766051.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 27.9, 'Ecotron Componentes'
  pi.url = 'https://www.ecotroncomponentes.com.br/componentes-eletronicos/conectores/conector-tnc-macho-rg-rgc213-tm-10-15816'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 22.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/conector-tnc-macho-prensa-cabo-rgc-rg213-tm-10-p1124'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 17.07, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 41
  pi = PriceItem()
  pi.nmcode, nm_alt = 11584447, None
  pi.fname = '41 terminador tipo N macho p cc [J2017] 11584447.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2019-12-09'
  pi.sapreq = 4509808470
  pi.netprice, pi.currency = 363.0, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 232.53, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 42
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787926, None
  pi.fname = '42 divisor potência faixa 800-900MHz tipo-N fêmea [PS727-02-BB] 12787926.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-27'
  pi.openprice, pi.supplier = 396.13, 'VH Telecom'
  pi.url = 'https://vhtelecom.lojaintegrada.com.br/DIVISOR-SPLITTER-1_2-700-2700MHZ-140DBC-IP65-VHT'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 421.91, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 43
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787945, None
  pi.fname = '43 acoplador direcional F p cc 10dB [DC3827-8_10-B] 12787945.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 80.83, 'Amazon / Daji-Direct'
  pi.url = 'https://www.amazon.com.br/Acoplador-Direcional-800MHz-2500MHz-Manuseamento-Imped%C3%A2ncia/dp/B0C4Z3XZCN'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 534.28, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 44
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787904, None
  pi.fname = '44 acoplador direcional F p cc 6dB [DC3827-05_07-B] 12787904.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 80.83, 'Amazon / Daji-Direct'
  pi.url = 'https://www.amazon.com.br/Acoplador-Direcional-800MHz-2500MHz-Manuseamento-Imped%C3%A2ncia/dp/B0C4Z3XZCN'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 526.09, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 45
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787906, None
  pi.fname = '45 acoplador direcional F p cc 20dB [DC3827-20-B] 12787906.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 80.83, 'Amazon / Daji-Direct'
  pi.url = 'https://www.amazon.com.br/Acoplador-Direcional-800MHz-2500MHz-Manuseamento-Imped%C3%A2ncia/dp/B0C4Z3XZCN'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 528.0, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 46
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787907, None
  pi.fname = '46 acoplador direcional F p cc 30dB [DC3827-30-B] 12787907.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 80.83, 'Amazon / Daji-Direct'
  pi.url = 'https://www.amazon.com.br/Acoplador-Direcional-800MHz-2500MHz-Manuseamento-Imped%C3%A2ncia/dp/B0C4Z3XZCN'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 554.82, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 47
  pi = PriceItem()
  pi.nmcode, nm_alt = 12789790, None
  pi.fname = '47 adaptador p cc tipo mini-UHF fêmea p N macho [USF 00742] 12789790.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 26.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-n-macho-x-uhf-mini-femea-klc-23-p1047'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 24.24, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 48
  pi = PriceItem()
  pi.nmcode, nm_alt = 12790022, None
  pi.fname = '48 adaptador p cc tipo TNC fêmea p N fêmea [USF 00718] 12790022.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 28.0, 'KLP Conectores'
  pi.url = 'https://www.casadosconectores.com.br/product/adaptador-tnc-femea-n-femea/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 17.37, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 49
  pi = PriceItem()
  pi.nmcode, nm_alt = 12490469, None
  pi.fname = '49 cabo coaxial corrugado 1_2pol radiaflex [RCF12-50JFN] 12490469.xlsx'
  pi.meas_unit = 'metro'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 27.0, 'DataComm BR'
  pi.url = 'https://www.datacomm.com.br/cabo-cellflex-rf-1-2-scf12-50j-lance-50m-c-conector-uhf/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 40.3, 'Mercado Livre / BrComm'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2125349698-cabo-coaxial-cellflex-rf-12-lcf12-50j-am-fm-vhf-uhf-hf-etc-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency = 124.74, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 50
  pi = PriceItem()
  pi.nmcode, nm_alt = 12790056, None
  pi.fname = '50 conector UHF macho p cc RGC213 [USM 00200-T] 12790056.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 28.9, 'KLP Conectores'
  pi.url = 'https://www.casadosconectores.com.br/product/conector-uhf-macho-crimpe-rgc-213/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 34.0, 'Shop Antenas'
  pi.url = 'https://www.shopantenas.com.br/conector-uhf-macho-solda-rg213-steelbras-ap0017'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-07-01'
  pi.sapreq = 4511088861
  pi.netprice, pi.currency = 14.71, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-06-15'
  pi.sapreq = 4511041025
  pi.netprice, pi.currency = 19.96, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 51
  pi = PriceItem()
  pi.nmcode, nm_alt = 12791836, None
  pi.fname = '51 conector UHF fêmea p cc RGC 213 [USF 00208] 12791836.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 32.9, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-uhf-femea-reto-cabo-prensa-cabo-rg-213-rgc-213-kf-7-gav-126-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 19.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/conector-uhf-femea-reto-p-cabo-rg-213-crimpagem-kf-20-p716'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 52
  pi = PriceItem()
  pi.nmcode, nm_alt = 12793067, None
  pi.fname = '52 conector UHF macho p cc RGC58 [KM-8] 12793067.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 27.0, 'Shop Antenas'
  pi.url = 'https://www.shopantenas.com.br/conector-uhf-macho-solda-rg58-steelbras-ap0018'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 26.5, 'Fozolo Componentes'
  pi.url = 'https://fazolo.com.br/componentes-eletronicos/conector-uhf-macho-rgrgc58-km-8'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 53
  pi = PriceItem()
  pi.nmcode, nm_alt = 11416820, None
  pi.fname = '53 conector UHF fêmea p cc RGC58 [KF-10] 11416820.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 22.0, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-uhf-femea-reto-prensa-cabo-rg-58-rgc-58-kf-10-gav-135-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 20.0, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/conector-uhf-femea-cabo-rg58-rgc58-klc-kf-10/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2020-10-15'
  pi.sapreq = 4508567165
  pi.netprice, pi.currency = 27.04, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 54
  pi = PriceItem()
  pi.nmcode, nm_alt = 11472752, None
  pi.fname = '54 conector BNC macho p cc RGC213 [LM-10] 11472752.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 32.0, 'Shop Antenas'
  pi.url = 'https://www.shopantenas.com.br/conectores/bnc-50/conector-bnc-macho-prensa-cabo-para-cabo-rg213-lm-10'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 29.5, 'KLP Conectores'
  pi.url = 'https://www.casadosconectores.com.br/product/stanley-1000500-amp-jump-starter-w120-psi-compressor-j5c09/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2018-09-13'
  pi.sapreq = 4508567165
  pi.netprice, pi.currency = 11.98, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 55
  pi = PriceItem()
  pi.nmcode, nm_alt = 11473744, None
  pi.fname = '55 conector F macho p cc RGC11 [AC-6M] 11473744.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 12.0, 'Casa dos Conectores'
  pi.url = 'https://www.casadosconectores.com.br/product/conector-f-macho-rg-11-crimpe/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 40.0, 'Trekking Tecnologia'
  pi.url = 'https://loja.trekkingtecnologia.com/rede-e-telefonia/acessorios/conectores/conectores-f-macho-reto-crimpagem-rgrgc-11-ac-6m'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-06-17'
  pi.sapreq = 4511050362
  pi.netprice, pi.currency = 16.29, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 56
  pi = PriceItem()
  pi.nmcode, nm_alt = 12788215, None
  pi.fname = '56 divisor de potência RF1_2 [PS447-02-B] 12788215.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 303.18, 'Mercado Livre / 48.900.etc'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3206884114-divisor-de-potncia-microstrip-combinador-divisor-de-2-vias-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency =  298.54, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 57
  pi = PriceItem()
  pi.nmcode, nm_alt = 12788204, None
  pi.fname = '57 divisor de potência RF1_3 [PS447-03-B] 12788204.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 275.0, 'Bit Electronics BR'
  pi.url = 'https://www.bitelectronics.com.br/telecomunicacao/divisores-de-alta-potencia/divisor-de-alta-potencia-1-entrada-e-3-saidas'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 950.0, 'Mercado Livre / Cabo Eletro'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3326590279-divisor-de-potncia-3-vias-hubersuhner-698-3800-mhz-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency =  334.95, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 58
  pi.nmcode, nm_alt = 12788214, None
  pi.fname = '58 divisor de potência RF1_4 [PS447-04-B] 12788214.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 267.88, 'Mercado Livre / Fenganshopbr'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3556528457-divisor-de-potncia-rf-divisor-de-4-vias-sinal-de-800-25-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency =  354.97, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 59
  pi = PriceItem()
  pi.nmcode, nm_alt = 12787893, None
  pi.fname = '59 acoplador direcional F p cc 15dB [DC3827-15-B] 12787893.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 80.83, 'Amazon / Daji-Direct'
  pi.url = 'https://www.amazon.com.br/Acoplador-Direcional-800MHz-2500MHz-Manuseamento-Imped%C3%A2ncia/dp/B0C4Z3XZCN'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-11-03'
  pi.openprice, pi.supplier = 72.60, 'Americanas / Soubarato'
  pi.url = 'https://www.americanas.com.br/produto/2378488197'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2021-11-03'
  pi.openprice, pi.supplier = 71.81, 'Soubarato'
  pi.url = 'https://www.soubarato.com.br/produto/2378488197'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 60
  pi = PriceItem()
  pi.nmcode, nm_alt = 11843707, None
  pi.fname = '60 adaptador conversão UHF fêmea p N fêmea [KLC-55] 11843707.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 267.88, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/adaptador-uhf-femea-x-femea-n-klc-klc-55/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 26.25, 'Mercado Livre / STM Telecom'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2853288595-10-adaptadores-n-50-ohms-fmea-x-uhf-fmea-so239-klc-55-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 61
  pi = PriceItem()
  pi.nmcode, nm_alt = 11791219, None
  pi.fname = '61 adaptador conversão reto macho p RCA fêmea [KLC-121] 11791219.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 23.1, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/adaptador-de-conversao-reto-macho-tnc-pf-sma-femea-pm-klc-130-gav-55-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 37.80, 'Magalu / Multi E-commerce'
  pi.url = 'https://www.magazineluiza.com.br/adaptador-macho-tnc-reto-e-femea-n-klc-18-gav-134-klc-multcomercial/p/cbckj24gje/ga/otga/'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 62
  pi = PriceItem()
  pi.nmcode, nm_alt = 12522729, None
  pi.fname = '62 adaptador conversão UHF macho p macho reto [KA-6] 12522729.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 19.9, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-uhf-macho-x-uhf-macho-klc-ka-6-p169'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 32.0, 'Ponto Eletrônico'
  pi.url = 'https://www.pontoeletronicolojavirtual.com.br/produtos/adaptador-uhf-macho-x-macho-reto-klc-ka-6/'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 63
  pi = PriceItem()
  pi.nmcode, nm_alt = 12601670, None
  pi.fname = '63 atenuador p cc N macho N fêmea tipo IEC [5930_N-50-050_19-_N] 12601670.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-25'
  pi.openprice, pi.supplier = 5504.00, 'Mouser Electronics (Europa)'
  pi.url = 'https://br.mouser.com/ProductDetail/HUBER%2BSUHNER/5930_N-50-050-19-_NE'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 5717.27, 'Distrelec (Europa)'
  pi.url = 'https://www.radiocomponentes.com.br/cabo-coaxial-flexivel-rg58-95-de-malha-50-ohms-cabletech-metro-p829'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 64
  pi = PriceItem()
  pi.nmcode, nm_alt = 11819330, None
  pi.fname = '64 cabo coaxial 50_Ohms RGC58 [30507] 11819330.xlsx'
  pi.meas_unit = 'metro'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 4.79, 'Magalu / GSM Cell'
  pi.url = 'https://www.magazineluiza.com.br/cabo-coaxial-rgc58-50-ohms-85-preto-100m-rgc-58-gsmcell/p/af3834ahcb/et/coxi/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 7.82, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/cabo-coaxial-flexivel-rg58-95-de-malha-50-ohms-cabletech-metro-p829'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2023-05-01'
  pi.sapreq = 4600670023
  pi.netprice, pi.currency =  69.48, 'BRL'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 65
  pi = PriceItem()
  pi.nmcode, nm_alt = 12088177, None
  pi.fname = '65 cabo coaxial 75_Ohms RGC6 [B3092A] 12088177.xlsx'
  pi_tmp = copy.copy(pi)
  pi.meas_unit = 'metro'
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 2.92, 'Portal Elétrico'
  pi.url = 'https://www.portaleletrico.com.br/cabo-coaxial-75-ohms-rgc-06-branco-97--malha-aluminizada-rolo-com-100-metros-gp-cabos-784/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 2.6, 'Mercado Livre / GGMaxCondutores'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3413693199-cabo-coaxial-rgc6-malha-95-100-metros-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 66
  pi = PriceItem()
  pi.nmcode, nm_alt = 11762345, None
  pi.fname = '66 conector fêmea reto prensa cabo RGC213 [AC-17F] 11762345.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 28.0, 'KLP Conectores'
  pi.url = 'https://www.casadosconectores.com.br/product/conector-n-femea-rgc-rg-213-prensa-cabo/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 25.0, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/conector-n-femea-reto-prensa-longo-cabo-rg-rgc213-cf-3c-p835'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 67
  pi = PriceItem()
  pi.nmcode, nm_alt = 12756391, None
  pi.fname = '67 conector BNC 75_Ohms macho reto cabo crimpagem pino solto [LM-102] 12756391.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 22.1, 'Mercado Livre / STM Telecom'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-2855649262-10-conectores-bnc-75-ohms-macho-crimpagem-rgrgc-59-lm-89-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 16.5, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-bnc-75-ohms-macho-reto-cabo-crimpagem-rgc-59-lm-64-gav-42-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 3.33, 'Solução Cabos'
  pi.url = 'https://www.solucaocabos.com.br/conector-bnc-para-crimpar-rg59-75-ohms/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 68
  pi = PriceItem()
  pi.nmcode, nm_alt = 12794101, None
  pi.fname = '68 conector BNC 50_Ohms macho reto cabo prensa RGC11 [LM-44] 12794101.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 18.95, 'MultComercial'
  pi.url = 'https://www.multcomercial.com.br/conector-bnc-50-ohms-macho-reto-cabo-crimpagem-rg-11-pino-solto-lm-34-gav-64-klc.html'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 13.8, 'Mercado Livre / Info Connect'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3178995436-conector-bnc-macho-reto-prensa-cabo-0318-50-ohms-50un-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 69
  pi = PriceItem()
  pi.nmcode, nm_alt = 12525468, None
  pi.fname = '69 conector coaxial tipo N p rosquear cabo LMR600 DLC600 [C118] 12525468.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 18.47, 'Elecbee (Internacional)'
  pi.url = 'https://www.elecbee.com/pt-480-n-type-connector-lmr-600-straight-plug-for-cable'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 40.8, 'Casa dos Conectores'
  pi.url = 'https://www.casadosconectores.com.br/product/mopar-oil-filter-mo-409/'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 70
  pi = PriceItem()
  pi.nmcode, nm_alt = 12181812, None
  pi.fname = '70 conector F Macho RG6 [CNF60012AZ] 12181812.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 1.90, 'Magalu / King Antenas'
  pi.url = 'https://www.magazineluiza.com.br/conector-de-compressao-para-cabo-rg-6-ppc/p/ja37bbj13c/te/ppcl/'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 1.43, 'Solução Cabos'
  pi.url = 'https://www.solucaocabos.com.br/conector-f-macho-rosca-rg6/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 1.94, 'Mundo Max'
  pi.url = 'https://www.mundomax.com.br/conector-f-de-compressao-rg6-cfmp0002-storm'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 71
  pi = PriceItem()
  pi.nmcode, nm_alt = 10282454, None
  pi.fname = '71 conector F macho cabo RGC59 [AC-3M] 10282454.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 8.19, 'Mercado Livre / EletroInffoCiaGold'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-904436340-conector-f-rgc59-de-rosca-p-cabo-c-friso-55mm-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 4.49, 'Eletro Peças'
  pi.url = 'https://www.eletropecas.com/conector-f-vedado-compressao-rgc59/p'
  prices.add_price_via_nm(pi.nmcode, pi)
  # NM 72
  pi = PriceItem()
  pi.nmcode, nm_alt = 12875147, None
  pi.fname = '72 adaptador dupla fêmea UHF com base quadrada [KA-10] 12875147.xlsx'
  pi_tmp = copy.copy(pi)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 26.9, 'Rádio Componentes'
  pi.url = 'https://www.radiocomponentes.com.br/adaptador-uhf-f-base-quadrada-4-furos-rosca-p588'
  prices.add_price_via_nm(pi.nmcode, pi)
  pi = copy.copy(pi_tmp)
  pi.date = '2024-02-26'
  pi.openprice, pi.supplier = 39.0, 'Mercado Livre / Rádio Componentes'
  pi.url = 'https://produto.mercadolivre.com.br/MLB-3243580757-5-adaptador-uhf-fmea-base-quadrada-4-furos-painel-ka-10-_JM'
  prices.add_price_via_nm(pi.nmcode, pi)
  return prices


def adhoctest():
  prices = gather_data()
  for tupl in prices.get_unique_nms_n_filenames():
    nm = tupl[0]
    fname = tupl[1]
    name, _ = os.path.splitext(fname)
    pp = name.split(' ')
    seq = pp[0]
    nm_comp = int(pp[-1])
    print(nm, seq, nm_comp, nm == nm_comp)


def process():
  prices = gather_data()
  show_qtd_of_prices_per_nm(prices)
  nms_from_filenames = chknm.get_unique_nms_from_filenames()
  print('nms_from_prices', prices.size, 'nms_from_filenames', len(nms_from_filenames))


if __name__ == '__main__':
  """
  """
  # adhoctest()
  process()
