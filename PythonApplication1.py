
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import sys
import codecs
import os
import shutil
import re
import collections
import math
#import enchant
import numpy as np
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
import importlib

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


# 遍历文件夹
def funfolder(path):
    filesArray = []
    for root, dirs, files in os.walk(path):
        for file in files:
            each_file = str(root + "//" + file)
            filesArray.append(each_file)
    return filesArray


# 新建文件夹
def buildfolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    print("成功创建文件夹！")


# 读取txt
def readtxt(path):
    with codecs.open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        f.close()
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
    content = re.sub(pattern, '', content)
    content = content.lower()
    return content


# 写入文件
def out_file(path, content_list):
    with codecs.open(path, "a", encoding="utf-8") as f:
        for content in content_list:
            f.write(str(content[0]) + ":" + str(content[1]) + "\r\n")
    print("well done!")
    f.close()


# 分词+统计词频
def count_word(content):
    # 分词
    tokens = word_tokenize(content)
    # tokens = [t for t in content.split()]
    # 删除停止词及拼写检查
    clean_tokens = tokens[:]
   # chk = enchant.Dict("en_US")
    for token in tokens:
        if  token in stopwords.words('english'):
            clean_tokens.remove(token)
    wordList = clean_tokens
    # 单词还原
    porter_stemmer = PorterStemmer()  
    lemmatizer = WordNetLemmatizer()
    for token in tokens:
        token = lemmatizer.lemmatize(token, pos="n")
        wordList.append(token)
    # 统计词频
    freq = nltk.FreqDist(wordList)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))
    return freq



# 计算TF-IDF
def count_tfidf(word_dic, words_dic, files_Array):
    word_idf = {}
    word_tfidf = {}
    num_files = len(files_Array)
    for word in word_dic:
        for words in words_dic:
            if word in words:
                if word in word_idf:
                    word_idf[word] = word_idf[word] + 1
                else:
                    word_idf[word] = 1
    for key, value in word_dic.items():
        if key != " ":
            word_tfidf[key] = value * math.log(num_files / (word_idf[key] + 1))
    return word_tfidf



# pdf2txt
def readPDF(path, toPath):
    # 以二进制形式打开pdf文件
    with open(path, "rb") as f:
        parser = PDFParser(f)
        pdfFile = PDFDocument()
        # 链接分析器与文档对象
        parser.set_document(pdfFile)
        pdfFile.set_parser(parser)
        # 提供初始化密码
        pdfFile.initialize()
        # 检测文档是否提供txt转换
        if not pdfFile.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            manager = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(manager, laparams=laparams)
            # 解释器对象
            interpreter = PDFPageInterpreter(manager, device)

            # 开始循环处理，每次处理一页
            for page in pdfFile.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        with open(toPath, "a", encoding='utf-8') as f1:
                            f1_str = x.get_text()
                            f1.write(f1_str + '\n')


def findmonth(txt):
    # 分词
    global result
    words_list = re.split(',|[ \]]', txt)
    # 目标词
    for str in words_list:
        if "9\r1\r0\r2\r\rr\rp\r\ra\r" in str:
            result = 4
            break
        elif "9\r1\r0\r2\r\ry\ra\r\rm\r" in str:
            result = 5
            break
        elif "9\r1\r0\r2\r\rn\ru\r\rj\r" in str:
            result = 6
            break
        elif "9\r1\r0\r2\r\rl\ru\r\rj\r" in str:
            result = 7
            break
        elif "9\r1\r0\r2\r\rg\ru\r\ra\r" in str:
            result = 8
            break
        else:
            result = 0
    return result


def merge_dict(x, y):
    for k,v in dict.items(x):
        if k in y.keys():
            dict[k]+=v
        else:
            dict[k] = v
    return dict


def word_cloud(wordsCnt,i):
    mask = np.array(Image.open('wordcloud.jpg'))  # 定义词云背景
    wc = wordcloud.WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
        mask=mask,  # 设置背景图
        max_words=200,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )
    wc.generate_from_frequencies(wordsCnt)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
    wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像
    wc.to_file('WordCloud' + str(i))  # 输出文件 设置文件名

def main():
    # pdf2txt
    folder_path = r'S:\共享资料库\THU_Hackthon2019\all'
    files_array = funfolder(folder_path)
    i = 0
    txt_folder = r"C:/Users/ALin/test1"
    buildfolder(txt_folder)
    for file_path in files_array:
        files_path = files_array[i].split(r"//")
        print(files_path)
        outfile_name = files_path[1]
        print(outfile_name)
        out_path = r"%s//%s.txt" % (txt_folder, outfile_name)
        readPDF(file_path, out_path)
        i = i + 1

    # 读取txt得到词汇统计dict
    newfiles_array = funfolder(txt_folder)
    files_dic = [] # 生成语料库
    for file_path in newfiles_array:
        file = readtxt(file_path)
        word_dic = count_word(file)
        files_dic.append(word_dic)

    files_dic4 = collections.Counter()
    files_dic5 = collections.Counter()
    files_dic6 = collections.Counter()
    files_dic7 = collections.Counter()
    files_dic8 = collections.Counter()

    i = 0
    for file in files_dic:
        tf_idf = count_tfidf(file, files_dic, newfiles_array)
        wordsCnt = collections.Counter(tf_idf)
        files_path = newfiles_array[i]
        print(files_path)
        new_file = readtxt(files_path)
        month = findmonth(new_file)
        if month is 4:
            files_dic4 +=(wordsCnt)
        elif month is 5:
            files_dic5 +=(wordsCnt)
        elif month is 6:
            files_dic6 +=(wordsCnt)
        elif month is 7:
           files_dic7 +=(wordsCnt)
        elif month is 8:
            files_dic8+=(wordsCnt)
        i = i + 1

    # 生成词云
    word_cloud(files_dic4,4)
    word_cloud(files_dic5,5)
    word_cloud(files_dic6,6)
    word_cloud(files_dic7,7)
    word_cloud(files_dic8,8)
if __name__ == '__main__':
    main()
