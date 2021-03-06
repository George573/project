import re
import sys
import time

import bs4
import requests
from filehandler import FileHandler
from settings import Settings


class Search:
    def __init__(
        self,
        queries_file: str,
        attempts=5,
        position="",
        start_over=False,
        links_file="./files/search.txt",
        position_file="./files/position.txt",
    ) -> None:
        # self.setings = Settings(queries_file, attempts, position, start_over, links_file, position_file)
        filehandler = FileHandler(links_file, position_file, queries_file)
        self.setings = Settings(attempts, position, start_over, filehandler)

    def extract_links(self, soup: bs4.BeautifulSoup):
        links = soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
        for i in range(
            0, len(links) - 2
        ):  # last two links are accounts.google.com, support.google.com
            # writing links to a file
            self.setings.file_handler.append_to_links_file(
                (re.split(":(?=http)", links[i]["href"].replace("/url?q=", "")))[0]
            )
            self.setings.file_handler.append_to_links_file("\n")

    def google_search(self, page_from=1, page_to=2, delay=0.1):
        delay = self.setings.check_delay_file_type(delay)
        page_from = self.setings.check_page_type(page_from, "page_from")
        page_to = self.setings.check_page_type(page_to, "page_to")
        progress = 0  # needed for progress bar
        link = "https://www.google.com/search?q="
        page_from, page_to = self.setings.check_values(page_from, page_to)
        for page_number in range(self.setings.page_number, page_to):
            page = "&start=" + str(page_number)
            for position in range(
                self.setings.position, len(self.setings.clean_strings)
            ):
                progress = self.progress_bar(progress)
                clean_sting = self.setings.clean_strings[position]
                r = requests.get(link + clean_sting + page)
                soup = bs4.BeautifulSoup(r.content, features="html.parser")
                self.extract_links(soup)
                self.setings.file_handler.write_to_position_file(
                    str(position) + " " + str(page_number)
                )
                time.sleep(delay)
            self.position = 1
        self.setings.file_handler.write_to_position_file("1 1")
        self.done()

    def progress_bar(self, i: int) -> int:
        if i == 0:
            print("working \???????o????")
        else:
            # erasing upper line
            sys.stdout.write("\x1b[1A\x1b[2K")
            # progress bar
            print("working", " " * (i % 25), "\???????o????")
        i += 1
        return i

    def done(self):
        sys.stdout.write("\x1b[1A\x1b[2K")
        print("Done ???")
