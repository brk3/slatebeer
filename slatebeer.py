import ratebeer

import sys
import urllib2

from bs4 import BeautifulSoup
from time import gmtime, strftime

html = urllib2.urlopen("http://www.indymanbeercon.co.uk/beer/").read()

soup = BeautifulSoup(html, 'html.parser')

rb = ratebeer.RateBeer()

table = soup.find('table', {'class':'beer-table'})
rows = table.find_all('tr')

out = """
<!DOCTYPE html>
<html>
<body>
<script src="sorttable.js"></script>
<table class="sortable">
<thead>
<th>Brewery</th>
<th>Beer</th>
<th>Ratebeer</th>
</thead>
"""

for row in rows:
  cols = row.find_all('td')
  if cols:
    try:
      brewery = cols[0].a.contents[0]
      beer = cols[1].contents[0]
      style = cols[2].a.contents[0]

      beer_lookup = rb.search('{0} {1}'.format(brewery, ' '.join(beer.split()[:-1])))
      if len(beer_lookup.get('beers')) > 0:
          details = beer_lookup.get('beers')[0]
          print('{0} - {1} - {2}'.format(brewery, beer, details.overall_rating))
          out = out + '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(
              brewery, beer, details.overall_rating)
    except Exception as e:
      print(e)

out = out + """
</table>
</body>
</html>
"""

msg = "\nLast Updated: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print(msg)
out = out + msg + '\n'

with open('/tmp/slatebeer/slatebeer.html', 'w') as f:
  f.write(out)
