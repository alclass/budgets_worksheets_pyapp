def dbfetch_bcb_cotacao_dolar_or_apifallback(self, recurse_pass=0):
  """
  First look up local sqlite-db, if not found, fallback to its corresponding API call
  """
  if recurse_pass > 5:
    print('recurse_pass > 5 |', recurse_pass)
    return None
  indate = dtfs.returns_date_or_none(self.date)
  if indate is None:
    return None
  today = datetime.date.today()
  if indate >= today:
    # log_msg = 'Date ' + str(indate) + ' is today (the rundate). Recursing without adding 1 to limit of 5 ' \
    #         + str(recurse_pass)
    # logger.info(log_msg)
    # print(log_msg)
    # indate = indate - datetime.timedelta(days=1)
    # return dbfetch_bcb_cotacao_dolar_or_apifallback(indate, recurse_pass)
    print('Date in the future. Please, reenter dateadhoctests up to the moment.')
    return None
  if dtfs.is_date_weekend(indate):
    log_msg = 'Date ' + str(indate) + ' is weekend. Recursing (limit to 5) ' + str(recurse_pass + 1)
    logger.info(log_msg)
    print(log_msg)
    indate = indate - datetime.timedelta(days=1)
    return dbfetch_bcb_cotacao_compra_dolar_apifallback(indate, recurse_pass + 1)
    # recurse one day back right away, today's quotes should be available after market
    # (TO-DO: write a dedicated function for this)
  session = exmod.consa.get_sa_session()
  exchanger = session.query(exmod.ExchangeRateDate). \
    filter(exmod.ExchangeRateDate.quotesdate == indate). \
    first()
  if exchanger:
    log_msg = 'Quote was in db. Returning it: %s' % str(exchanger)
    logger.info(log_msg)
    # print(log_msg)
    res_bcb_api1 = apis.namedtuple_bcb_api1(
      cotacao_compra=exchanger.buyquote, cotacao_venda=exchanger.sellquote, cotacao_datahora=exchanger.quotesdatetime,
      param_date=exchanger.quotesdate, error_msg=None, gen_msg='Fetched from db',
      exchanger=exchanger
    )
    session.close()
    if exchanger.buyquote is None and exchanger.sellquote is None:
      indate = indate - datetime.timedelta(days=1)
      return dbfetch_bcb_cotacao_compra_dolar_apifallback(indate, recurse_pass + 1)
    return res_bcb_api1
  res_bcb_api1 = apis.call_api_bcb_cotacao_dolar_on_date(indate)
  log_msg = str(res_bcb_api1)
  logger.info(log_msg)
  print(log_msg)
  if res_bcb_api1 and res_bcb_api1.error_msg is not None:
    session.close()
    return log_error_namedtuple(res_bcb_api1)
  exchanger = exmod.ExchangeRateDate()
  session.add(exchanger)
  exchanger.numerator_curr3 = sett.CURR_BRL
  exchanger.denominator_curr3 = sett.CURR_USD
  buyquote = res_bcb_api1.cotacao_compra
  if buyquote is not None:
    exchanger.buyquote = buyquote
  sellquote = res_bcb_api1.cotacao_venda
  if sellquote is not None:
    exchanger.sellquote = sellquote
  cotacao_dt = res_bcb_api1.cotacao_datahora
  if cotacao_dt is None:
    cotacao_dt = dtfs.convert_date_to_datetime_or_none(indate)
  exchanger.quotesdatetime = cotacao_dt
  session.commit()
  log_msg = 'After session.commit() ' + str(exchanger)
  logger.info(log_msg)
  print(log_msg)
  # now it's time to set exchanger, ie it's been instantiated, in the namedtuple var
  res_bcb_api1 = add_exchanger_to_res_bcb_api_namedtuple(exchanger, res_bcb_api1)
  session.close()
  return res_bcb_api1



def adhoc_test1():
  dates = []
  strdate = '22/9/2015'  # '2020-01-07'
  strdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate, tosep='-', sourceposorder='dmy')
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  strdate = '12/5/2016'  # '2020-01-07'
  strdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate, tosep='-', sourceposorder='dmy')
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)

  ptab = PrettyTable()
  ptab.field_names = ['seq', 'data dmy', 'compra', 'venda', 'data ymd']
  for i, pdate in enumerate(dates):
    seq = i + 1
    res_bcb_api1 = dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    quotesdate = dtfs.convert_datetime_to_date_or_none(res_bcb_api1.cotacao_datahora)
    dmypdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(
      quotesdate, tosep='/', targetposorder='dmy'
    )
    cotacao_compra_with_comma = strfs.replace_point_to_comma(res_bcb_api1.cotacao_compra, decimal_places=4)
    cotacao_venda_with_comma = strfs.replace_point_to_comma(res_bcb_api1.cotacao_venda, decimal_places=4)
    ptab.add_row([seq, dmypdate, cotacao_compra_with_comma, cotacao_venda_with_comma, res_bcb_api1.param_date])
  print(ptab)
  text = ptab.get_html_string()
  filename = 'exchange_rate_on_dates.html'
  filepath = dtfs.get_datafolder_abspath_for_filename_w_tstamp(filename)
  fp = open(filepath, 'w', encoding='utf8')
  fp.write(text)
  fp.close()


def batch_fetch_brl_usd_cotacoes_month_by_month(inidate, findate):
  res_bcb_api1_list = []
  for pdate in dtfs.generate_daterange(inidate, findate):
    print(pdate, '-'*30)
    res_bcb_api1 = dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    do_wait = False
    if type(res_bcb_api1) == apis.namedtuple_bcb_api1:
      res_bcb_api1_list.append(res_bcb_api1)
      if res_bcb_api1.gen_msg is not None and res_bcb_api1.gen_msg.lower().find('bcb api') > -1:
        do_wait = True
    if do_wait:
      wait_in_seconds = get_random_wait_seconds()
      log_msg = '=== wait %d seconds === namedtuple_res_bcb_api1 (%s)' % (wait_in_seconds, str(res_bcb_api1))
      print(log_msg)
      logger.info(log_msg)
      time.sleep(wait_in_seconds)
  apis.pretry_print_api_list(res_bcb_api1_list)


def batch_fetch_brl_usd_cotacoes(year):
  today = datetime.date.today()
  yesterday = today - datetime.timedelta(days=1)
  for nmonth in range(1, 13):
    inidate = datetime.date(year, nmonth, 1)
    if inidate >= yesterday:
      break
    findate = dtfs.get_monthslastday_date_via_calendar(inidate)
    if findate > yesterday:
      break
    log_msg = 'ini=%s fin=%s batch_fetch_brl_usd_cotacoes()'
    logger.info(log_msg)
    batch_fetch_brl_usd_cotacoes_month_by_month(inidate, findate)


def batch_years_fetch_brl_usd_cotacoes(iniyear, finyear):
  for year in range(iniyear, finyear):
    batch_fetch_brl_usd_cotacoes(year)