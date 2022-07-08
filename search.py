import sys, requests, bs4, re
from turtle import pos

class search:
    def __init__(self, queries_file, position, start_over = False, links_file = "search.txt", position_file = "position.txt") -> None:
        self.links_file = links_file
        self.position_file = position_file
        self.queries_file = queries_file
        self.clean_strings = self.get_queries(queries_file)
        self.start_over(start_over, position)

    def start_over(self, start_over, position):
        if start_over:
            self.page_number = 1
            self.position = 1
        else:
            self.page_number = self.get_page_number(position)
            self.position = self.get_postion(position)

    def separate_position(self, file, type) -> int:
        with open(file) as f:
            string = f.read()
        list = string.split()
        if type == "position":
            type = 1
        elif type == "page":
            type = 0
        else:
            self.fatal_error("separate_position()", "wrong input")
        return int(list[type].strip())

    def separate_position_no_file(self, position, type) -> int:
        list = position.split()
        if type == "position":
            type = 0
        elif type == "page":
            type = 1
        else:
            self.fatal_error("separate_position()", "wrong input")
        return int(list[type].strip())
    
    def get_queries(self, queries_file):
        if queries_file:
            with open(queries_file) as file:
                strings = [line.rstrip() for line in file]
            #cleaning from empty strings and replacing space with +
            clean_strings = []
            for line in strings:
                if line.strip():
                    line = line.replace(' ', '+')
                    clean_strings.append(line)
            return clean_strings
        else:
            self.fatal_error("get_queries()", "wrong input")
        
    def get_page_number(self, position):
        if position:
            return self.separate_position_no_file(position, "position")
        else:
            try:
                return self.separate_position(self.position_file, "position")
            except:
                return 1

    def get_postion(self, position):
        if position:
            return self.separate_position_no_file(position, "page")
        else:
            try:
                return self.separate_position(self.position_file, "page")
            except:
                return 1

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
    
    def fatal_error(self, place, reason):
        print("error occurred in ", place.strip(), " reason: ", reason)
        sys.exit(1)

    def google_search(self, page_from = 1, page_to = 2):
        progress = 0 #needed for progress bar
        link = "https://www.google.com/search?q="

        page_from, page_to = self.check_values(page_from, page_to)

        for page_number in range(page_from, page_to):
            if page_number == page_from:
                page_number = self.page_number
                print(page_number, " ", self.page_number)
            elif page_number > page_from:
                self.position = 1
            page = "&start=" + str(page_number)
            for self.position in range(self.position, len(self.clean_strings)):
                progress = self.progress_bar(progress) #printing progress bar
                #creating a link
                clean_sting = (self.clean_strings[self.position])
                r = requests.get(link + clean_sting + page)
                #creating BeautifulSoup object, which represents html file
                soup = bs4.BeautifulSoup(r.content, features="html.parser")
                #searching for links in html response from google
                with open(self.links_file, 'a') as f:
                    links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
                    for i in range(0, len(links) - 2): #last two links are accounts.google.com, support.google.com
                            #writing links to a file
                            f.write((re.split(":(?=http)",links[i]["href"].replace("/url?q=","")))[0])
                            f.write("\n")
                #writing position to a file
                with open(self.position_file, "w") as file:
                    file.write(str(self.position) + " " + str(page_number))

    def check_values(self, page_from, page_to) -> int:
        if page_from < 0:
            page_from *= -1
        elif page_from == 0:
            page_from = -1

        if page_to < 0:
            page_to *= -1
        elif page_to == 0:
            page_to = page_to + 1

        if page_from > page_to:
            val = page_to
            page_to = page_from
            page_from = val
        elif page_from == page_to:
            page_to += 1


        if not (page_from <= self.page_number < page_to):
            self.page_number = page_from

        if self.position > len(self.clean_strings):
            self.position = 1

        return page_from, page_to