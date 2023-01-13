import math
import gensim
import numpy as np
import gc
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# coding = utf-8


punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·"""
dicts = {i: '#' for i in punctuation}
punc_table = str.maketrans(dicts)

def choose_cipai(path1, cipai):
    with open("..//pattern//"+path1, encoding="utf-8") as file1:
        content1 = file1.read().rstrip()
        list1 = content1.split("/")
    file1.close()
    alpha = len(content1) - len(list1) + 1
    # print(content1)
    with open("..//pattern//Song Ci.txt", encoding="utf-8") as f:
        content_split = f.read().splitlines()
    # print(f.readline(100))
    content_nian = ""
    content_word = []
    for i in range(len(content_split)):
        if content_split[i] == cipai:
            content_nian = "\n".join([content_nian, content_split[i + 2]])
            content_word.append(content_split[i + 2])
    # print(content_nian)
    for i in range(len(content_word)):
        content_word[i] = content_word[i].translate(punc_table)

    # print(content_word)
    # 获取指定长度的词

    content_word1 = content_word
    tem_content_word = content_word
    content_word2 = []
    for i in tem_content_word:
        content_word2.append(i.replace("#", ""))

    # print(content_word2)
    content_word = []
    for i in range(len(content_word2)):
        if len(content_word2[i]) == alpha:
            content_word.append(content_word1[i])
    # print(content_word)
    # print(len(content_word))
    # print(content_word)

    str_content = ""
    # print(str_content)
    # print(content1)

    for sentence in content_word:
        j = 0
        for i in range(len(content1)):
            if content1[i] == "/" and sentence[j] != "#":
                str_content = "".join([str_content, "/"])
            elif i == len(content1) - 1:
                str_content = "".join([str_content, sentence[j]])
                str_content = "".join([str_content, "#"])
            else:
                str_content = "".join([str_content, sentence[j]])
                j = j + 1
    # print(str_content)

    list2 = str_content.split("#")
    # print(list2)

    list3 = []
    for i in list2:
        a = i.split("/")
        if len(a) >= 2:
            list3.append(a)
    return list3

#NLP方法精简字典：首先输入句子，交给word2vec模型分析，然后利用kmeans聚类的方法和手肘法得到（*10*）个类的中心词和词簇
def NLP_start():
    a = choose_cipai("#0000.txt", "江城子")
    b = choose_cipai("#0001.txt", "忆王孙")
    c = choose_cipai("#0010.txt", "如梦令")
    d = choose_cipai("#0011.txt", "相见欢")
    e = choose_cipai("#0100.txt", "点绛唇")
    f = choose_cipai("#0101.txt", "浣溪沙")
    g = choose_cipai("#0110.txt", "菩萨蛮")
    h = choose_cipai("#0111.txt", "卜算子")
    i = choose_cipai("#1000.txt", "清平乐")
    j = choose_cipai("#1001.txt", "鹧鸪天")
    k = choose_cipai("#1010.txt", "虞美人")
    l = choose_cipai("#1011.txt", "南乡子")
    m = choose_cipai("#1100.txt", "蝶恋花")
    n = choose_cipai("#1101.txt", "一剪梅")
    o = choose_cipai("#1110.txt", "临江仙")
    p = choose_cipai("#1111.txt", "渔家傲")
    sentences = a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p
    #print(sentences)
    print("sentence generate ok")
    #训练模型
    model = gensim.models.Word2Vec(sentences=sentences, vector_size=50, min_count=2, window=3)
    words = []
    for lis in sentences:
        for i in lis:
            if i in model.wv:
                words.append(i)
    print(len(words))
    print("model train ok")

    dataset = []                          #开始Kmeans聚类
    for i in words:
        v = model.wv[i]
        #pca.fit(v)
        #dataset.append(pca.transform(v))
        dataset.append(v)

    data_refined = np.asarray(dataset)
    #print(type(data_refined))
    del dataset
    gc.collect()
    """
    inertia = []
    for k in range(4,20):
        estimator = KMeans(n_clusters=k, n_init=10, random_state=0).fit(data_refined)
        inertia.append(np.sqrt(estimator.inertia_))
    plt.plot(range(4,20),inertia,"o-")
    plt.xlabel("k")
    plt.show()
    """#确定聚类数目
    estimator = KMeans(n_clusters=10, max_iter=300, n_init=10).fit(data_refined)  # 构造聚类器
    centroids = estimator.cluster_centers_                    #获得中心点坐标列表
    #print(centroids)
    del data_refined
    gc.collect()

    for array in centroids:
        print(model.wv.similar_by_vector(array, topn=1024))   #获得词语簇

    del centroids
    del model
    gc.collect()
    print("KMeans clustering ok")
    #print(model.wv.most_similar(positive=["明月"], topn=20))
    #print(model.wv["明月"])


NLP_start()