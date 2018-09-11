import os
import re
import time
import json
import logging
import calendar
import datetime
import functools

import feedparser
from pytz import utc
from dateutil.parser import parse
import os
import re
import time
import json
import logging
import calendar
import datetime
import functools

import feedparser
from pytz import utc
from dateutil.parser import parse

try:
    from urllib2 import urlopen
    from urllib2 import HTTPError
except ImportError:
    from urllib.request import urlopen
    from urllib.error import HTTPError


# In[3]:

FEED_URL = 'http://gdacs.org/rss.aspx?profile=ARCHIVE&from={}'
DISPLACED_RE = re.compile('.*(\d+) displaced')
DEPTH_RE = re.compile('.*Depth:(\d+\.\d+)km')


def dtconv(struct_time):
    dt = datetime.datetime(*struct_time[:7], tzinfo=utc)
    return calendar.timegm(dt.utctimetuple())


def dt_to_date(s):
    dt = parse(s)
    dt = dt.replace(hour=0, minute=0, second=0)
    return calendar.timegm(dt.utctimetuple())


def tsconv(s):
    dt = parse(s)
    return calendar.timegm(dt.utctimetuple())


def get_map(entry):
    try:
        return [l['href'] for l in entry.links if l['rel'] == 'enclosure'][0]
    except IndexError:
        return None


def url_to_filename(url):
    return url.split('/')[-1]


def fetch_asset(url, outdir):
    print "fetching asset from %s" %url
    logging.debug('Fetchings asset from %s', url)
    filename = url_to_filename(url)
    outpath = os.path.join(outdir, filename)
    try:
        with open(outpath, 'w') as f:
            f.write(urlopen(url).read())
    except HTTPError:
        return ''
    return filename


def get_assets(data, outdir):
    for k, url in data.items():
        if url:
            data[k] = fetch_asset(url, outdir)


def gdacs_data(fn):
    @functools.wraps(fn)
    def wrapper(entry, outdir):
        logging.debug('Formatting entry %s', entry.gdacs_eventid)
        data = {
            'id': entry.gdacs_eventid,
            'type': entry.gdacs_eventtype,
            'name': entry.gdacs_eventname,
            'location': entry.gdacs_country or None,
            'alert_level': entry.gdacs_alertlevel.lower(),
            'updated': dtconv(entry.updated_parsed),
            'summary': entry.summary,
            'maps': {
                'thumb': get_map(entry),
                'details': entry.gdacs_mapimage or None,
            }
        }
        get_assets(data['maps'], outdir)
        data['info'] = fn(entry)
        return data
    return wrapper


@gdacs_data
def format_earthquake(entry):
    try:
        depth = float(DEPTH_RE.match(entry.summary).group(1))
    except (AttributeError, ValueError, TypeError):
        depth = None
    return {
        'severity': entry.gdacs_severity['value'],
        'affected_population': entry.gdacs_population['value'],
        'time': tsconv(entry.gdacs_fromdate),
    }


@gdacs_data
def format_flood(entry):
    return {
        'severity': entry.gdacs_severity['value'],
        'affected_population': entry.gdacs_population['value'],
        'duration': {
            'from': dt_to_date(entry.gdacs_fromdate),
            'to': dt_to_date(entry.gdacs_todate),
        },
    }


@gdacs_data
def format_tcyclone(entry):
    try:
        displaced = int(DISPLACED_RE.match(entry.summary).group(1))
    except (AttributeError, ValueError, TypeError):
        displaced = 0
    return {
        'severity': '{} {}'.format(entry.gdacs_severity['value'],
                                   entry.gdacs_severity['unit']),
        'affected_population': displaced,
        'deaths': entry.gdacs_population['value'],
        'duration': {
            'from': dt_to_date(entry.gdacs_fromdate),
            'to': dt_to_date(entry.gdacs_todate),
        },
    }


FORMATTERS = {
    'EQ': format_earthquake,
    'FL': format_flood,
    'TC': format_tcyclone,
}


def get_feed_url():
    dt = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    return FEED_URL.format(dt.strftime('%Y-%m-%d'))


def get_feed():
    logging.debug('Obtaining feed')
    url = get_feed_url()
    data = feedparser.parse(url)
    return data.entries


def formatted_entries(entries, outdir):
    logging.debug('Formatting entries')
    return [FORMATTERS[e.gdacs_eventtype](e, outdir) for e in entries]


def write_json(outfile, entries):
    with open(outfile, 'w') as f:
        json.dump(entries, f, indent=2)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Convert GDACS data to JSON')
    parser.add_argument('--output', '-o', metavar='PATH', default='gdacs.json',
                        help='Output JSON file path')
    parser.add_argument('--verbose', '-V', action='store_true', help='output '
                        'debug messages')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    entries = get_feed()
    outdir = os.path.dirname(args.output)
    write_json(args.output, formatted_entries(entries, outdir))


if __name__ == '__main__':
    main()

who = 'http://www.who.int/feeds/entity/hac/en/rss.xml'
gdacs_eq_24h = 'http://www.gdacs.org/xml/rss_eq_24h.xml'
gdacs_eq_gt55_48h = 'http://www.gdacs.org/xml/rss_eq_48h_med.xml'
gdacs_all_24h = 'http://www.gdacs.org/xml/rss_24h.xml'
gdacs_all_7d = 'http://www.gdacs.org/xml/rss_7d.xml'
gdacs_ts_7d = 'http://www.gdacs.org/xml/rss_tc_7d.xml'
gdacs_ts_3m = 'http://www.gdacs.org/xml/rss_tc_3m.xml'
gdacs_fl_7d = 'http://www.gdacs.org/xml/rss_fl_7d.xml'
gdacs_fl_3m = 'http://www.gdacs.org/xml/rss_fl_3m.xml'
reliefweb = 'https://reliefweb.int/disasters/rss.xml'
reliefweb_map = 'https://reliefweb.int/maps/rss.xml'
dost_pagasa = 'https://www1.pagasa.dost.gov.ph/index.php/738-pagasa-rss-feeds'

outdir = r'C:\Users\Michael\Desktop\gdacs'
fetch_asset(gdacs_all_24h,outdir)

fn = url_to_filename(gdacs_eq_24h)
print fn

gdacs_data(fn)




