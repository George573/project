import sys

class settings:
    def __init__(self, queries_file, position, start_over, links_file, position_file) -> None:
        self.queries_file = queries_file
        self.clean_strings = self.get_queries(queries_file)
        self.set_file_names(links_file, position_file)
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

    def set_file_names(self, links_file, position_file):
        if self.check_file_name(links_file):
            self.links_file = links_file
        else:
            self.links_file = "search.txt"
        if self.check_file_name(position_file):
            self.position_file = position_file
        else:
            self.position_file = "position.txt"
        
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

    def check_file_name(self, file_name) -> bool:
        try:
            with open(file_name, "r") as f:
                return True
        except:
            try:
                with open(file_name, "w") as f:
                    return True
            except:
                return False
        '''list = str(file_name).split(".")
        if len(list) == 2 and list[1] == "txt":
            return True
        else:
            self.warning("check_file_name()", "Wrong input file")
            return False'''

    def check_delay_file_type(self, delay) -> float:
        if isinstance(delay, (int, float)):
            if delay < 0:
                self.warning("check_delay_file_type()", "Delay value can't be smaller than 0")
                return float(delay * -1)
            else:
                return float(delay)
        elif isinstance(delay, (str)):
            self.warning("check_delay_file_type()", "Delay must be float or int")
            delay = float(delay.strip())
            if delay < 0:
                self.warning("check_delay_file_type()", "Delay value can't be smaller than 0")
                return float(delay * -1)
            else:
                return float(delay)
        else:
            return 0.1

    def check_page_type(self, page, type) -> int:
        if isinstance(page, (int, float)):
            return int(page)
        elif isinstance(page, (str)):
            self.warning("check_page_type()", "Page value must be int")
            return int(page.strip())
        else:
            if type == "page_from":
                return 1
            elif type == "page_to":
                return 2
            else:
                self.fatal_error("check_page_type()", "wrong type")

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

    def fatal_error(self, place, reason, fix = "", exit = True):
        print("Error occurred in ", place.strip(), ",\n reason: ", reason, "\n fix:", fix)
        if exit:
            sys.exit(1)
        
    def warning(self, place, reason, fix="Fixed by the professional team of robots 🤖"):
        print("Warning: in ", place.strip(), ",\n reason:", reason, "\n fix:", fix)

    def position_warning(self, place, reason="Wrong input."):
        self.warning(place, reason, 
                "Position need to be string in form: 'position page' ('1 1'). Where 'position' is position(int) inside of file and 'page' is page number(int)")