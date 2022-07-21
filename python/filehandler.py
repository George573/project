import sys

class FileHandler:
    def __init__(self, links_file : str, position_file : str, queries_file : str) -> None:
        self.links_file = links_file
        self.position_file = position_file
        self.queries_file = queries_file
 
    def read_file(self, file_name : str) -> str:
        for i in range(0, self.attempts):
            try:
                with open(file_name) as file:
                    return file.read()
            except:
                pass
        raise Exception("Couldn't read the file: ", file_name)

    def write_file(self, file_name : str, text : str) -> int:
        for i in range(0, self.attempts):
            try:
                with open(file_name, 'w') as file:
                    file.write(text)
                    return 0
            except:
                pass
        raise Exception("Couldn't write to the file: ", file_name)

    def append_to_links_file(self, text : str) -> int:
        for i in range(0, self.attempts):
            try:
                with open(self.links_file, 'a') as file:
                    file.write(text)
                    return 0
            except:
                pass
        raise Exception("Couldn't write to the file: ", self.links_file)

    def read_from_position_file(self) -> str:
        for i in range(0, self.attempts):
            try:
                with open(self.position_file) as file:
                    return file.read()
            except:
                pass  
        raise Exception("Couldn't read the file: ", self.position_file)

    def write_to_position_file(self, text : str) -> int:
        for i in range(0, self.attempts):
            try:
                with open(self.position_file, 'w') as file:
                    file.write(text)
                    return 0
            except:
                pass
        raise Exception("Couldn't write to the file: ", self.position_file)

    def separate_position(self, type : str) -> int:
        string = self.read_from_position_file()
        list = string.split()
        if (len(list)) != 2:
            raise Exception("separate_position()", "Too many arguments")
        if type == "position":
            return int(list[0].strip())
        elif type == "page":
            return int(list[1].strip())
        else:
            raise Exception("separate_position()", "wrong input")

    def separate_position_no_file(self, position : str, type : str) -> int:
        list = position.split()
        if type == "position":
            type = 0
        elif type == "page":
            type = 1
        else:
            raise Exception("separate_position_no_file()", "wrong input")
        if (len(list)) != 2:
            position_warning("separate_position_no_file()", "Too many arguments")
        return int(list[type].strip())

    def get_postion(self, position : str):
        if position:
            try:
                return self.separate_position_no_file(position, "position")
            except:
                position_warning("get_position()")
                return self.get_postion(position=0)
        else:
            try:
                return self.separate_position(self.position_file, "position")
            except:
                return 1

    def get_page_number(self, position : str):
        if position:
            try:
                return self.separate_position_no_file(position, "page")
            except:
                position_warning("get_page_number")
                return self.get_postion(position=0)
        else:
            try:
                return self.separate_position(self.position_file, "page")
            except:
                return 1

    def get_queries(self):
        if self.queries_file:
            with open(self.queries_file) as file:
                strings = [line.rstrip() for line in file]
            #cleaning from empty strings and replacing space with +
            clean_strings = []
            for line in strings:
                if line.strip():
                    line = line.replace(' ', '+')
                    clean_strings.append(line)
            return clean_strings
        else:
            fatal_error("get_queries()", "wrong input")

def fatal_error(place, reason : str, fix="", exit=True):
    print("Error occurred in ", place.strip(), ",\n reason: ", reason, "\n fix:", fix)
    if exit:
        sys.exit(1)

def warning(place, reason, fix="Fixed by the professional team of robots 🤖"):
    print("Warning: in ", place.strip(), ",\n reason:", reason, "\n fix:", fix)

def position_warning(place, reason="Wrong input."):
    warning(place, reason, 
            "Position need to be string in form: 'position page' ('1 1'). Where 'position' is position(int) inside of file and 'page' is page number(int)")