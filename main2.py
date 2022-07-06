import sys, requests, bs4, re
import webbrowser
from PIL import Image
from io import BytesIO

def main() -> int:
    link = "https://www.google.dz/search?q="
    search = "balckbird"
    page = requests.get(link + search)
    soup = bs4.BeautifulSoup(page.content,features="lxml")
    import re
    links = []
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        print (re.split(":(?=http)",link["href"].replace("/url?q=","")))

    return 0
if __name__ == "__main__":
    sys.exit(main())