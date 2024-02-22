#!/usr/bin/env python3
"""
"""
import re


text = """
1-Fêmea cabo coaxial.xlsx
2-Conjunto de aterramento.xlsx
3-Conjunto de aterramento.xlsx
4-Conjunto de aterramento.xlsx
5- Protetor surtos antena.xlsx
6-Adaptador cabo coaxial.xlsx
7-Adaptador cabo coaxial.xlsx
8-Adaptador cabo coaxial.xlsx
9-Adaptador cabo coaxial.xlsx
10-Adaptador cabo coaxial.xlsx
11-Adaptador cabo coaxial.xlsx
12-Adaptador cabo coaxial.xlsx
13-Adaptador cabo coaxial.xlsx
14-Adaptador cabo coaxial.xlsx
15-Adaptador cabo coaxial.xlsx
16-Adaptador cabo coaxial.xlsx
17-Adaptador cabo coaxial.xlsx
18-Adaptador cabo coaxial.xlsx
19-CABO CELLFLEX 1-2.xlsx
20-CABO CELLFLEX 7-8.xlsx
21-Cabo coaxial RGC213.xlsx
22-Conector BNC Fêmea.xlsx
23-Conector BNC Macho.xlsx
24-Conector BNC Macho.xlsx
25-Conector IEC Fêmea Reto.xlsx
26-Conector Mini-UHF M.xlsx
27-Conector N Fêmea Angular.xlsx
28-Conector N Fêmea Cabo RG6.xlsx
29-Conector N Fêmea RGC 213.xlsx
30-Conector N F Cabo Cellflex 1-2.xlsx
31-Conector N F Cabo Cellflex 7-8.xlsx
32-Conector N Fêmea Reto.xlsx
33-Conector N Macho RG58.xlsx
34-Conector N Macho RG6.xlsx
35-Conector N Macho RGC213.xlsx
36-Conector N M Cabo Cellflex 1-2.xlsx
37-Conector N M Cabo Cellflex 7-8.xlsx
38- Conector TNC Fêmea RG58.xlsx
39- Conector TNC Fêmea RGC213.xlsx
40-Conector TNC Macho RG58.xlsx
41-Conector TNC Macho RGC213.xlsx
42-Terminador Tipo N Macho.xlsx
43-Divisor_Combinador N-Fêmea.xlsx
44-Acoplador direcional F cabo coaxial 10 dB.xlsx
45-Acoplador direcional F cabo coaxial 6 dB.xlsx
46-Acoplador direcional F cabo coaxial 20 dB.xlsx
47-Acoplador direcional F cabo coaxial 30 dB.xlsx
48-Adaptador KLC-23.xlsx
49-Adaptador KLC-27.xlsx
50-Cabo coaxial corrugado.xlsx
51-Cabo coaxial 50 OHMS.xlsx
52-Conector UHF Macho RGC 213.xlsx
53-Conector UHF Fêmea RGC 213.pdf
53-Conector UHF Fêmea RGC 213.xlsx
54-Conector UHF Macho RG-58.xlsx
55-Conector UHF Fêmea RG-58.xlsx
56-Conector BNC Macho RG-213.xlsx
57-Conector F Macho RG-11.xlsx
59-Divisor de potência de RF 1-3.xlsx
60-Divisor de potência de RF 1-4.xlsx
61-Acoplador Direcional F.xlsx
"""

restr = r'(\d+)-(.+)'
recomp = re.compile(restr)


def mount_dict_pycode():
  lines = text.split('\n')
  lines = filter(lambda it: it != '', lines)
  lines = list(map(lambda it: it.rstrip('.xlsx'), lines))
  scrmsg = 'lt1_item_dict = {\n'
  for it in lines:
    match_obj = recomp.match(it)
    if match_obj:
      n = match_obj.group(1)
      name = match_obj.group(2)
      scrmsg += f"\t'{n}': '{name}',\n"
  scrmsg += '}\n'
  print(scrmsg)


def adhoctest():
  pass


def process():
  mount_dict_pycode()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
