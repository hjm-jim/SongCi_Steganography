import hashlib
import math


# coding = utf-8
def Str_encode(s: str, rule='utf-8'):
    sc = s.encode(rule)
    bc = [bin(int(i))[2:].rjust(8, '0') for i in sc]
    rtn = ''.join(bc)
    return rtn


def myxor(a, b):  # a,b are bitstrings
    if len(a) != len(b):
        print("data type error")
        return None
    l = [ord(c) ^ ord(d) for c, d in zip(a, b)]
    return "".join(map(str, l))


def hex2bin(s):
    hexdic = {"0": "0000", "1": "0001", "2": "0010", "3": "0011",
              "4": "0100", "5": "0101", "6": "0110", "7": "0111",
              "8": "1000", "9": "1001", "a": "1010", "b": "1011",
              "c": "1100", "d": "1101", "e": "1110", "f": "1111"}
    str = ""
    for i in s:
        if i in hexdic:
            str = str + hexdic[i]
    return str


def mask_gen(seed, length):  # SHA256产生mask,大于256的呈现周期性。
    hash = hex2bin(hashlib.sha256(seed.encode('utf-8')).hexdigest())
    l = length % 256
    c = length // 256
    return c * hash + hash[0:l:1]


def encode_with_cipai(type, plaintext, start, cnt):
    # cnt:number of generated text
    # with type,encode from start pointer of plaintext,directly write back to file,number with "#+cipai"
    # return number of bytes been encoded in the cipai
    # hash of plaintext also reflects to ten types of topics

    cipher = ""

    # first we need to get appropriate pattern for the cipai type

    image_dic = {"0000": "江城子", "0001": "忆王孙", "0010": "如梦令", "0011": "相见欢",
                 "0100": "点绛唇", "0101": "浣溪沙", "0110": "菩萨蛮", "0111": "卜算子",
                 "1000": "清平乐", "1001": "鹧鸪天", "1010": "虞美人", "1011": "南乡子",
                 "1100": "蝶恋花", "1101": "一剪梅", "1110": "临江仙", "1111": "渔家傲"
                 }

    """
    image_split = {"0000": []
    
    }
    
    """
    path1 = "..//pattern//" + "#" + type + ".txt"
    path2 = "..//dic//" + "#"
    path3 = "..//output//" + "#"
    hash_tmp = hashlib.sha256(plaintext.encode('utf-8')).hexdigest()
    topic = str(int(hash_tmp[-1], base=16) % 10)

    with open(path1, encoding="utf-8") as file1:
        content = file1.read().rstrip()
        list1 = content.split("/")  # 将pattern内容划分为若干单音节，如”平仄平“
        for l in list1:
            type_accent = ""
            accent_dic = {"平": "0", "仄": "1", "中": "2"}
            for i in l:
                if i in accent_dic:
                    type_accent = type_accent + accent_dic[i]
                else:
                    print("pattern file format error")
                    return

            path4dic = path2 + topic + "//#" + type_accent + ".txt"  # 先根据hash of plaintext索引主题文件夹，再根据每一个音节，索引dic文件夹里面的音节字典文件
            with open(path4dic, encoding="utf-8") as file2:
                # 根据字典的大小决定编码长度，bits为编码长度
                lines = file2.readlines()
                bits = int(math.log2(len(lines)))
                # if start + bits <= len(plaintext):
                NR_pl = int(plaintext[start:start + bits:1], base=2)
                cipher = cipher + "/" + lines[NR_pl].rstrip()
                start = start + bits
                # elif start <= len(plaintext)-1:            #需要修改

    # write back with cipher
    path3_1 = path3 + str(cnt) + image_dic[type] + ".txt"
    file = open(path3_1, 'w')
    file.write(cipher)
    file.close()
    return start


def encrypt(plaintext, seed):
    # 补齐短块！
    # 补齐算法为：如果明文最末一位为0，填充1，如果明文最末尾一位为1，填充0
    # 直接补满整个plaintext一个最长的byte位数，保存原有的长度。
    ori_len = len(plaintext)
    NR_types = 4
    NR_paddling = 200  # 用最长的词牌加密之后得到的比特串长度
    ori_byte = 1 - int(plaintext[-1], base=2)
    # plaintext is bitstring

    plaintext = plaintext + str(ori_byte) * NR_paddling
    length = len(plaintext)
    length2 = len(seed)

    mask = mask_gen(seed, length)  # hide data patterns, including all the paddlings
    pl = myxor(plaintext, mask)

    j = 0
    i = 0
    cnt = 1
    # totally 2^NR_types of cipais

    while j < ori_len:
        if i + NR_types > length2:
            type = seed[i::1] + seed[0:(i + NR_types) % length2:1]
        else:
            type = seed[i:i + NR_types:1]
        # 按照type值索引字典里面的词牌，接下来按照词牌编码
        j = encode_with_cipai(type, pl, j, cnt)
        i = (i + NR_types) % length2  # 循环获得种子
        cnt = cnt + 1


def main():
    f = open("..//input//input.txt", 'r', encoding="utf-8")
    plaintext = Str_encode(f.read().rstrip())
    f.close()
    print("get plaintext ok")
    seed = "1101011010101110101101"
    print("start of encryption")
    encrypt(plaintext, seed)
    print("end of encryption")


main()
