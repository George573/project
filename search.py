import sys, requests, bs4, re

class search:
    def __init__(self, queries_file, position = "", start_over = False, links_file = "search.txt", position_file = "position.txt") -> None:
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

    def separate_position(self, file, type) -> int:
        with open(file) as f:
            string = f.read()
        list = string.split()
        if type == "position":
            type = 0
        elif type == "page":
            type = 1
        else:
            raise Exception(self.fatal_error("separate_position()", "wrong input", fix="automatically handled 🔧" ,exit=False))
        if (len(list)) != 2:
            self.position_warning("separate_position()", "Too many arguments")
        return int(list[type].strip())

    def separate_position_no_file(self, position, type) -> int:
        list = position.split()
        if type == "position":
            type = 0
        elif type == "page":
            type = 1
        else:
            raise Exception(self.fatal_error("separate_position_no_file()", "wrong input", fix="automatically handled 🔧",exit=False))
        if (len(list)) != 2:
            self.position_warning("separate_position_no_file()", "Too many arguments")
        return int(list[type].strip())
        
    def get_page_number(self, position):
        if position:
            try:
                return self.separate_position_no_file(position, "page")
            except:
                self.position_warning("get_page_number")
                return self.get_postion(position=0)
        else:
            try:
                return self.separate_position(self.position_file, "page")
            except:
                return 1

    def get_postion(self, position):
        if position:
            try:
                return self.separate_position_no_file(position, "position")
            except:
                self.position_warning("get_position()")
                return self.get_postion(position=0)
        else:
            try:
                return self.separate_position(self.position_file, "position")
            except:
                return 1

    def check_values(self, page_from, page_to) -> int:
        if page_from < 0:
            page_from *= -1
            self.warning("check_values()", "page_from can't be smaller than 0")
        elif page_from == 0:
            page_from = 1
            self.warning("check_values()", "page_from can't be equal to 0")

        if page_to < 0:
            page_to *= -1
            self.warning("check_values()", "page_to can't be smaller than 0")
        elif page_to == 0:
            page_to = page_to + 1
            self.warning("check_values()", "page_to can't be equal to 0")

        if page_from > page_to:
            val = page_to
            page_to = page_from
            page_from = val
            self.warning("check_values()", "pafe_from can't be bigger than page_to")
        elif page_from == page_to:
            page_to += 1
            self.warning("check_values()", "pafe_from and page_to can't be equal")


        if not (page_from <= self.page_number < page_to):
            self.page_number = page_from
            self.warning("check_values()", "page number must be in range of page_from to page_to")

        if self.position >= len(self.clean_strings):
            self.position = 1
            self.warning("check_values()", "position can't be bigger than amount of queries")

        return page_from, page_to
    
    def extract_links(self, soup):
        with open(self.links_file, 'a') as f:
            links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
            for i in range(0, len(links) - 2): #last two links are accounts.google.com, support.google.com
                    #writing links to a file
                    f.write((re.split(":(?=http)",links[i]["href"].replace("/url?q=","")))[0])
                    f.write("\n")
    
    def google_search(self, page_from = 1, page_to = 2):
        progress = 0 #needed for progress bar
        link = "https://www.google.com/search?q="
        page_from, page_to = self.check_values(page_from, page_to)
        for page_number in range(self.page_number, page_to):
            page = "&start=" + str(page_number)
            for position in range(self.position, len(self.clean_strings)):
                progress = self.progress_bar(progress)
                clean_sting = (self.clean_strings[position])
                r = requests.get(link + clean_sting + page)
                soup = bs4.BeautifulSoup(r.content, features="html.parser")
                self.extract_links(soup)
                with open(self.position_file, "w") as file:
                    file.write(str(position) + " " + str(page_number))
            self.position = 1

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

    def fatal_error(self, place, reason, fix = "", exit = True):
        print("Error occurred in ", place.strip(), ",\n reason: ", reason, "\n fix:", fix)
        if exit:
            sys.exit(1)
        
    def warning(self, place, reason, fix="Fixed by the professional team of robots 🤖"):
        print("Warning: in ", place.strip(), ",\n reason:", reason, "\n fix:", fix)

    def position_warning(self, place, reason="Wrong imput."):
        self.warning(place, reason, 
                "Position need to be string in form: 'position page' ('1 1'). Where 'position' is position(int) inside of file and 'page' is page number(int)")
