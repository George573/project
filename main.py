import sys, os, signal, requests, re, bs4

def main() -> int:
    pid = os.fork()

    #Parent:
    if pid:
        stoped = False
        cont = True
        print("type: k - to kill, s - to suspend, c - to wake up")
        while True:
            i = input()
            if   i == 'k':
                os.kill(pid, signal.SIGKILL)
                print("killed sucsefully  (⌣́_⌣̀)")
                sys.exit(0)
            elif i == 's':
                if not stoped:
                    os.kill(pid, signal.SIGSTOP)
                    stoped = True
                    cont = False
                    print("suspended sucsefully 💤")
            elif i == 'c':
                if not cont:
                    os.kill(pid, signal.SIGCONT)
                    stoped = False
                    cont = True
                    print("awakened sucsefully ＼(o ￣∇￣o)/")

    #Child:
    else:
        with open("queries.txt") as file:
            strings = [line.rstrip() for line in file]

        clean_strings = []
        for line in strings:
            if line.strip():
                line = line.replace(' ', '+')
                clean_strings.append(line)

        try:
            with open("position.txt") as file:
                i = int(file.read().strip())
        except:
            i = 1

        while True:
            link = "https://www.google.com/search?q="
            search = (clean_strings[i % len(clean_strings)])
            r = requests.get(link + search)
            soup = bs4.BeautifulSoup(r.content,features="lxml")
            with open("search.txt", 'a') as f:
                links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
                for i in range(0, len(links) - 2):
                        f.write((re.split(":(?=http)",links[i]["href"].replace("/url?q=","")))[0])
                        f.write("\n")           
            i += 1
            with open("position.txt", "w") as file:
                file.write(str(i))

if __name__ == "__main__":
    sys.exit(main()) 