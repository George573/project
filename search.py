import time, sys, requests, bs4, re

class search:
    def __init__(self, queries_file, position = "", start_over = False, links_file = "search.txt", position_file = "position.txt") -> None:
        self.set1ngs = settings.settings(queries_file, position, start_over, links_file, position_file)
        
    def extract_links(self, soup):
        with open(self.set1ngs.links_file, 'a') as f:
            links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
            for i in range(0, len(links) - 2): #last two links are accounts.google.com, support.google.com
                    #writing links to a file
                    f.write((re.split(":(?=http)",links[i]["href"].replace("/url?q=","")))[0])
                    f.write("\n")
    
    def google_search(self, page_from = 1, page_to = 2, delay = 0.1):
        delay = self.set1ngs.check_delay_file_type(delay)
        page_from = self.set1ngs.check_page_type(page_from, "page_from")
        page_to = self.set1ngs.check_page_type(page_to, "page_to")
        progress = 0 #needed for progress bar
        link = "https://www.google.com/search?q="
        page_from, page_to = self.set1ngs.check_values(page_from, page_to)
        for page_number in range(self.set1ngs.page_number, page_to):
            page = "&start=" + str(page_number)
            for position in range(self.set1ngs.position, len(self.set1ngs.clean_strings)):
                progress = self.progress_bar(progress)
                clean_sting = (self.set1ngs.clean_strings[position])
                r = requests.get(link + clean_sting + page)
                soup = bs4.BeautifulSoup(r.content, features="html.parser")
                self.extract_links(soup)
                with open(self.set1ngs.position_file, "w") as file:
                    file.write(str(position) + " " + str(page_number))
                time.sleep(delay)
            self.position = 1
        with open(self.set1ngs.position_file, "w") as file:
            file.write("1 1")
        self.done()

    def progress_bar(self, i) -> int:
        if i == 0:
            print("working \ō͡≡o˞̶")
        else:
            #erasing upper line
            sys.stdout.write('\x1b[1A\x1b[2K')
            #progress bar
            print("working", " " * (i % 25), "\ō͡≡o˞̶")
        i += 1
        return i
    
    def done(self):
        sys.stdout.write('\x1b[1A\x1b[2K')
        print("Done ✓")

    
