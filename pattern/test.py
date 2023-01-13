def main():
    l = [0] * 27
    for i in range(0,15):
        tmp = bin(i)[2::]
        j = "0" * (4 - len(tmp)) + tmp
        path = "#" + j + ".txt"
        with open(path, encoding="utf-8") as file:
            accent_dic = {"平": "0", "仄": "1", "中": "2"}
            content = file.read().rstrip()
            list = content.split("/")
            for k in list:
                s = ""
                for char in k:
                    s = s + accent_dic[char]
                t = int(s,base = 3)
                l[t] = l[t] + 1
    for i in range(0,27):
        if l[i] != 0:
            print(i)
            print("\n")


main()