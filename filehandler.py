import settings, sys

class filehandler:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.settings.clean_strings = self.get_queries(settings.queries_file)
        self.start_over()

    def read_file(self, file_name) -> str:
        for i in range(0, self.settings.attempts):
            try:
                with open(file_name) as file:
                    return file.read()
            except:
                pass
        raise Exception("Couldn't read the file: ", file_name)
    
    def write_file(self, file_name, text) -> int:
        for i in range(0, self.settings.attempts):
            try:
                with open(file_name, 'w') as file:
                    file.write(text)
                    return 0
            except:
                pass
        raise Exception("Couldn't write to the file: ", file_name)

    def append_to_links_file(self, text) -> int:
        for i in range(0, self.settings.attempts):
            try:
                with open(self.settings.links_file, 'a') as file:
                    file.write(text)
                    return 0
            except:
                pass
        raise Exception("Couldn't write to the file: ", self.settings.links_file)

    def read_from_position_file(self) -> str:
        for i in range(0, self.settings.attempts):
            try:
                with open(self.settings.position_file) as file:
                    return file.read()
            except:
                pass
        raise Exception("Couldn't read the file: ", settings.position_file)
    
    def write_to_position_file(self, text) -> int:
        for i in range(0, self.settings.attempts):
            try:
                with open(self.settings.position_file, 'w') as file:
                    file.write(text)
                    return 0
            except:
                pass
        raise Exception("Couldn't write to the file: ", self.settings.position_file)

    def start_over(self):
        if self.settings.start_over:
            self.settings.page_number = 1
            self.settings.position = 1
        else:
            self.settings.page_number = self.get_page_number(settings.position)
            self.settings.position = self.get_postion(settings.position)


    def separate_position(self, type) -> int:
        string = self.read_file()
        list = string.split()
        if type == "position":
            type = 0
        elif type == "page":
            type = 1
        else:
            raise Exception("separate_position()", "wrong input")
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

    def fatal_error(self, place, reason, fix = "", exit = True):
        print("Error occurred in ", place.strip(), ",\n reason: ", reason, "\n fix:", fix)
        if exit:
            sys.exit(1)
        
    def warning(self, place, reason, fix="Fixed by the professional team of robots 🤖"):
        print("Warning: in ", place.strip(), ",\n reason:", reason, "\n fix:", fix)

    def position_warning(self, place, reason="Wrong input."):
        self.warning(place, reason, 
                "Position need to be string in form: 'position page' ('1 1'). Where 'position' is position(int) inside of file and 'page' is page number(int)")