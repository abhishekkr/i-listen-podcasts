from fasthtml.common import *
import xml.etree.ElementTree as ET


app = FastHTML()
opml = "./google-podcasts-subscriptions.opml.xml"


def parse_opml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    feeds = []
    for item in root.findall('./body/outline/outline'):
        pod = {}
        if item.get('type') == 'rss':
            pod['name'] = item.get('text')
            pod['rss'] = item.get('xmlUrl')
        else:
            print("[!RSS]", child.text.encode('utf8'))
        feeds.append(pod)
    return feeds


def get_feed_nodes(filepath, filetype='opml'):
    if filetype not in ['opml']:
        raise "Unhandled Podcase Subscription Format."
    feeds = parse_opml(opml)
    pod_links = []
    for pod in feeds:
        if 'rss' not in pod.keys():
            continue
        a = A(pod['name'], href='#', url=pod['rss'])
        line = Li(a)
        pod_links.append(line)
    print(pod_links)
    return tuple(pod_links)


@app.get("/")
def home():
    feeds = get_feed_nodes(opml)
    return Titled("Podcast Feeds",
        Main(
            feeds,
        )
    )


if __name__ == '__main__':
    uvicorn.run("google-podcast:app", host='0.0.0.0', port=8000, reload=True)
