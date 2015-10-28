import json
import urllib2
from bs4 import BeautifulSoup
from flask import Flask, request
app = Flask(__name__)

html = ''
with open('app.html', 'r') as f:
    html += f.read()

def parse_tags(html):
    soup = BeautifulSoup(html, 'html5lib')
    tag_names = [tag.name for tag in soup.find_all(True)]
    return dict((n, len(soup.find_all(n))) for n in tag_names)

@app.route("/")
def index():
    url = request.args.get('url', None)
    if url is None:
        return '<form method="get"><input type="text" name="url" /><input type="submit" /></form>'
    else:
        # NOTE: This does a blocking synchronous request, at scale this should be put on a queue.
        page = urllib2.urlopen(url).read()
        escaped_page = page.replace("<", "<%LT%>")
        output = html.replace('<%HTML%>', json.dumps(escaped_page))
        output = output.replace('<%TAGS%>', json.dumps(parse_tags(page)))
        return output

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8124, debug=True)
