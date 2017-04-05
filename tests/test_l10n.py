# coding=utf-8
from datetime import date, datetime, time, timedelta

from babel import Locale
from babel.dates import UTC, get_timezone

from allspeak import L10n


def test_init_l10n():
    l10n = L10n()
    assert l10n.default_locale == Locale('en')
    assert l10n.default_timezone == UTC
    assert repr(l10n) == 'L10n(default_locale=en, default_timezone=UTC)'


def test_init_l10n_defaults():
    l10n = L10n(default_locale='es', default_timezone='America/Lima')
    assert l10n.default_locale == Locale('es')
    assert l10n.default_timezone == get_timezone('America/Lima')


def test_to_user_timezone():
    l10n = L10n(default_timezone='America/Lima')
    now = datetime.utcnow().replace(hour=12)
    assert l10n.to_user_timezone(now).hour == now.hour - 5


def test_to_some_timezone():
    l10n = L10n()
    now = datetime.utcnow().replace(hour=12)
    result = l10n.to_user_timezone(now, tzinfo='America/Lima')
    assert result.hour == now.hour - 5


def test_to_some_timezone_obj():
    l10n = L10n()
    now = datetime.utcnow().replace(hour=12)
    tzinfo = get_timezone('America/Lima')
    result = l10n.to_user_timezone(now, tzinfo=tzinfo)
    assert result.hour == now.hour - 5


def test_to_utc():
    l10n = L10n()
    now = datetime.utcnow()
    # America/Lima = UTC-5
    dtz = l10n.to_user_timezone(now, tzinfo='America/Lima')
    assert l10n.to_utc(dtz) == now


def test_to_utc_use_default_tzinfo():
    # America/Lima = UTC-5
    l10n = L10n(default_timezone='America/Lima')
    now = datetime.utcnow()
    dt = now - timedelta(hours=5)
    assert dt.tzinfo is None
    assert l10n.to_utc(dt) == now


def test_format_date():
    l10n = L10n(default_timezone=UTC)
    d = date(2007, 4, 1)

    dformat = "EEE, MMM d, ''yy"
    expected = u"Sun, Apr 1, '07"
    assert l10n.format_date(d, dformat, locale='en') == expected

    # datetimes are converted to dates
    dt = datetime(2007, 4, 1, 15, 30)
    assert l10n.format_date(dt, dformat, locale='en') == expected

    assert l10n.format_date(None, dformat, locale='en')


def test_format_date_by_name():
    l10n = L10n()
    d = date(2007, 4, 1)

    assert l10n.format_date(d, 'short', locale='en') == u'4/1/07'
    assert l10n.format_date(d, 'medium', locale='en') == u'Apr 1, 2007'
    assert l10n.format_date(d, 'long', locale='en') == u'April 1, 2007'
    assert l10n.format_date(d, 'full', locale='en') == u'Sunday, April 1, 2007'

    assert l10n.format_date(d, '...', locale='en') == u'...'
    assert l10n.format_date(d, locale='en') == u'Apr 1, 2007'


def test_set_date_formats():
    date_formats = {'date': 'short'}
    l10n = L10n(date_formats=date_formats)

    d = date(2007, 4, 1)
    assert l10n.format_date(d, locale='en') == u'4/1/07'

    l10n.set_date_formats({
        'date': 'full',
        'date.short': "'trolololo'"
    })
    assert l10n.format_date(d, locale='en') == u'Sunday, April 1, 2007'
    assert l10n.format_date(d, 'short', locale='en') == u'trolololo'
    l10n.set_date_formats({})  # cleanup


def test_format_datetime():
    l10n = L10n()
    dt = datetime(2007, 4, 1, 15, 30)

    dformat = "yyyyy.MMMM.dd GGG hh:mm a"
    expected = u'02007.April.01 AD 03:30 PM'
    assert l10n.format_datetime(dt, dformat, locale='en') == expected


def test_format_now():
    l10n = L10n()
    now = datetime.utcnow()
    dformat = "yyyy"
    expected = str(now.year)
    assert l10n.format_datetime('now', dformat) == expected


def test_format_datetime_tzinfo():
    l10n = L10n()
    dt = datetime(2007, 4, 1, 15, 30, tzinfo=UTC)
    eastern = get_timezone('US/Eastern')

    dformat = 'H:mm Z'
    expected = u'11:30 -0400'
    assert l10n.format_datetime(dt, dformat, tzinfo=eastern, locale='en_US') == expected


def test_format_time():
    l10n = L10n()
    t = time(15, 30)

    tformat = "hh 'o''clock' a"
    expected = u"03 o'clock PM"
    assert l10n.format_time(t, tformat, locale='en') == expected

    tformat = 'H:mm a'
    expected = u'15:30 nachm.'
    assert l10n.format_time(t, tformat, locale='de') == expected


def test_format_timedelta():
    l10n = L10n()
    delta = timedelta(days=6)

    expected = u'1 week'
    assert l10n.format_timedelta(delta, locale='en_US') == expected

    expected = u'1 month'
    assert l10n.format_timedelta(delta, granularity='month', locale='en_US') == expected

    assert l10n.format_timedelta(None, locale='en_US') == ''


def test_format_timedelta_direction_forward():
    l10n = L10n()
    delta = datetime.utcnow() + timedelta(days=6)

    expected = u'dentro de 1 semana'
    assert l10n.format_timedelta(delta, locale='es_PE', add_direction=True) == expected

    expected = u'dentro de 1 mes'
    assert l10n.format_timedelta(
        delta,
        granularity='month',
        locale='es_PE',
        add_direction=True
    ).lower() == expected

    assert l10n.format_timedelta(None, locale='es_PE') == ''


def test_format_timedelta_direction_backward():
    l10n = L10n()
    delta = datetime.utcnow() - timedelta(days=6)

    expected = u'hace 1 semana'
    assert l10n.format_timedelta(delta, locale='es_PE', add_direction=True) == expected

    expected = u'hace 1 mes'
    assert l10n.format_timedelta(
        delta,
        granularity='month',
        locale='es_PE',
        add_direction=True
    ).lower() == expected


def test_format_number():
    l10n = L10n()

    assert l10n.format_number(1099, locale='en_US') == u'1,099'
    assert l10n.format_number(1099, locale='de_DE') == u'1.099'
    assert l10n.format_number(None, locale='en_US') == ''


def test_format_decimal():
    l10n = L10n()

    assert l10n.format_decimal(1.2345, locale='en_US') == u'1.234'
    assert l10n.format_decimal(1.2345, locale='sv_SE') == u'1,234'
    assert l10n.format_decimal(12345, locale='de_DE') == u'12.345'
    assert l10n.format_decimal(-1.2345, format='#,##0.##;-#', locale='en') == u'-1.23'
    assert l10n.format_decimal(None, locale='en_US') == ''


def test_format_currency():
    l10n = L10n()

    assert (l10n.format_currency(1099.98, 'USD', locale='en_US') ==
            u'$1,099.98')
    assert (l10n.format_currency(1099.98, 'CAD', locale='en_US') ==
            u'CA$1,099.98')
    assert (l10n.format_currency(1099.98, 'EUR', locale='de_DE') ==
            u'1.099,98\xa0\u20ac')
    assert (l10n.format_currency(1099.98, 'EUR', locale='en_US') ==
            u'\u20ac1,099.98')
    assert (l10n.format_currency(1099.98, 'EUR', u'\xa4\xa4 #,##0.00', locale='en_US') ==
            u'EUR 1,099.98')
    assert l10n.format_currency(None, 'USD', locale='en_US') == ''


def test_format_percent():
    l10n = L10n()

    assert l10n.format_percent(0.34, locale='en_US') == u'34%'
    assert l10n.format_percent(25.1234, locale='en_US') == u'2,512%'
    assert l10n.format_percent(25.1234, locale='sv_SE') == u'2\xa0512\xa0%'
    assert l10n.format_percent(25.1234, u'#,##0\u2030', locale='en_US') == u'25,123\u2030'
    assert l10n.format_percent(None, locale='en_US') == ''


def test_format_scientific():
    l10n = L10n()

    assert l10n.format_scientific(0.1, '#E0', locale='en_US') == '1E-1'
    assert l10n.format_scientific(-12345.6, '00.###E0', locale='en_US') == '-12.346E3'
    assert l10n.format_scientific(123.45, '#.##E0 m/s', locale='en_US') == '1.23E2 m/s'
    assert l10n.format_scientific(None, '#E0', locale='en_US') == ''


def test_format():
    l10n = L10n()

    d = date(2007, 4, 1)
    dformat = "EEE, MMM d, ''yy"
    expected = u"Sun, Apr 1, '07"
    assert l10n.format(d, dformat, locale='en') == expected

    dt = datetime(2007, 4, 1, 15, 30)
    dformat = "yyyyy.MMMM.dd GGG hh:mm a"
    expected = u'02007.April.01 AD 03:30 PM'
    assert l10n.format(dt, dformat, locale='en') == expected

    dt = datetime(2007, 4, 1, 15, 30, tzinfo=UTC)
    eastern = get_timezone('US/Eastern')
    dformat = 'H:mm Z'
    expected = u'11:30 -0400'
    assert l10n.format(dt, dformat, tzinfo=eastern, locale='en_US') == expected

    t = time(15, 30)
    tformat = "hh 'o''clock' a"
    expected = u"03 o'clock PM"
    assert l10n.format(t, tformat, locale='en') == expected

    delta = timedelta(days=6)
    assert l10n.format(delta, locale='en_US') == u'1 week'

    assert l10n.format(delta, granularity='month', locale='en_US') == u'1 month'

    assert l10n.format(1099, locale='en_US') == u'1,099'

    assert l10n.format(1.2345, locale='en_US') == u'1.234'

    assert l10n.format('test', locale='en') == 'test'
    assert l10n.format(None, locale='en_US') == ''
