"""
art/inflmeas/bcb_br/classes/__init__.py
  Some parameters for the package 'bcb_br/classes'
    Import them with:
      import art/inflmeas/bls_us/classes as pkg  # then use pkg.<attribute> to access <attribute>

"""
EXCHRATE_DBTABLENAME = 'currencies_exchangerates'
n_decplaces_for_div_intprices = 4  # EXCHRATE_DIVISOR = 10 ** 4  # i.e., 10000 or 10k
days_gap_when_one_of_the_rangedates_misses = 10
BRL, EUR, USD = 'BRL', 'EUR', 'USD'
DEFAULT_CURR_NUM = BRL
DEFAULT_CURR_DEN = USD
REGISTERED_3LETTER_CURRENCIES = [BRL, USD, EUR]
