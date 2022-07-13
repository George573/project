import filehandler

class Settings:
    def __init__(self, queries_file,attempts, position, start_over, links_file, position_file) -> None:
        self.attempts = self.set_attempts_value(attempts)
        self.file_handler = filehandler.FileHandler(attempts)
        self.set_file_names(links_file, position_file)
        self.file_handler.set_links_file(self.links_file)
        self.file_handler.set_position_file(self.position_file)
        self.clean_strings = self.file_handler.get_queries(queries_file)
        self.start_over(start_over, position)

    def start_over(self, start_over, position):
        if start_over:
            self.page_number = 1
            self.position = 1
        else:
            self.page_number = self.file_handler.get_page_number(position)
            self.position = self.file_handler.get_postion(position)

    def set_file_names(self, links_file, position_file):
        if self.check_file_name(links_file):
            self.links_file = links_file
        else:
            self.links_file = "./files/search.txt"
        if self.check_file_name(position_file):
            self.position_file = position_file
        else:
            self.position_file = "./files/position.txt"

    def set_attempts_value(self, attempts) -> int:
        if isinstance(attempts, (int, bool)):
            return int(attempts)
        else:
            filehandler.warning("set_attempts_value", "wrong input type (has to be int)")
            return 5

    def check_file_name(self, file_name) -> bool:
        try:
            self.file_handler.read_file(file_name)
            return True
        except:
            try:
                self.file_handler.write_file(file_name,"")
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
                filehandler.warning("check_delay_file_type()", "Delay value can't be smaller than 0")
                return float(delay * -1)
            else:
                return float(delay)
        elif isinstance(delay, (str)):
            filehandler.warning("check_delay_file_type()", "Delay must be float or int")
            delay = float(delay.strip())
            if delay < 0:
                filehandler.warning("check_delay_file_type()", "Delay value can't be smaller than 0")
                return float(delay * -1)
            else:
                return float(delay)
        else:
            return 0.1

    def check_page_type(self, page, type) -> int:
        if isinstance(page, (int, float)):
            return int(page)
        elif isinstance(page, (str)):
            filehandler.warning("check_page_type()", "Page value must be int")
            return int(page.strip())
        else:
            if type == "page_from":
                return 1
            elif type == "page_to":
                return 2
            else:
                filehandler.fatal_error("check_page_type()", "wrong type")

    def check_values(self, page_from, page_to) -> int:
        if page_from < 0:
            page_from *= -1
            filehandler.warning("check_values()", "page_from can't be smaller than 0")
        elif page_from == 0:
            page_from = 1
            filehandler.warning("check_values()", "page_from can't be equal to 0")

        if page_to < 0:
            page_to *= -1
            filehandler.warning("check_values()", "page_to can't be smaller than 0")
        elif page_to == 0:
            page_to = page_to + 1
            filehandler.warning("check_values()", "page_to can't be equal to 0")

        if page_from > page_to:
            val = page_to
            page_to = page_from
            page_from = val
            filehandler.warning("check_values()", "pafe_from can't be bigger than page_to")
        elif page_from == page_to:
            page_to += 1
            filehandler.warning("check_values()", "pafe_from and page_to can't be equal")

        if not (page_from <= self.page_number < page_to):
            self.page_number = page_from
            filehandler.warning("check_values()", "page number must be in range of page_from to page_to")

        if self.position >= len(self.clean_strings):
            self.position = 1
            filehandler.warning("check_values()", "position can't be bigger than amount of queries")

        return int(page_from), int(page_to)