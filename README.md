# solutionTo-1

create by Alin, hezy18

## 一、运行环境
python3.7
### pip freeze:
astroid==2.2.5
atomicwrites==1.3.0
attrs==19.1.0
backcall==0.1.0
beautifulsoup4==4.8.0
bleach==3.1.0
colorama==0.4.1
cycler==0.10.0
decorator==4.4.0
defusedxml==0.6.0
entrypoints==0.3
importlib-metadata==0.19
inexactsearch==1.0.2
ipykernel==5.1.2
ipython==7.7.0
ipython-genutils==0.2.0
ipywidgets==7.5.1
isort==4.3.21
jedi==0.15.1
jieba==0.39
Jinja2==2.10.1
jsonschema==3.0.2
jupyter==1.0.0
jupyter-client==5.3.1
jupyter-console==6.0.0
jupyter-core==4.5.0
kiwisolver==1.1.0
lazy-object-proxy==1.4.2
MarkupSafe==1.1.1
matplotlib==3.1.1
mccabe==0.6.1
mistune==0.8.4
more-itertools==7.2.0
mpmath==1.1.0
nbconvert==5.6.0
nbformat==4.4.0
nltk==3.4.5
nose==1.3.7
notebook==6.0.1
numpy==1.17.0
packaging==19.1
pandas==0.25.1
pandocfilters==1.4.2
parso==0.5.1
pdfminer3k==1.3.1
pickleshare==0.7.5
Pillow==6.1.0
pluggy==0.12.0
ply==3.11
prometheus-client==0.7.1
prompt-toolkit==2.0.9
py==1.8.0
Pygments==2.4.2
pylint==2.3.1
pyparsing==2.4.2
pyrsistent==0.15.4
pytest==5.1.1
python-dateutil==2.8.0
pytz==2019.2
pywinpty==0.5.5
pyzmq==18.1.0
qtconsole==4.5.4
scipy==1.3.1
Send2Trash==1.5.0
silpa-common==0.3
six==1.12.0
soundex==1.1.3
soupsieve==1.9.3
spellchecker==0.4
sympy==1.4
terminado==0.8.2
testpath==0.4.2
tornado==6.0.3
traitlets==4.3.2
typed-ast==1.4.0
wcwidth==0.1.7
webencodings==0.5.1
widgetsnbextension==3.5.1
wordcloud==1.5.0
wrapt==1.11.2
zipp==0.5.2

## 二、运行操作：
### 1、用户需修改绝对路径：
205行路径为待读文件夹（内含pdf文件）的路径
</br>208行路径为新建文件夹的路径
### 2、所用相对路径：
在与py文件同级文件夹下需要一张图片作为词云背景图，这里使用了'wordcloud.jpg'（即下图所示小熊图案），该选项可以在源代码第189行进行修改
![wordcloud.jpg](https://i.loli.net/2019/08/23/a4STwhO6qU81ipM.jpg)

## 三、选题
#1	AI技术趋势分析与展示
1.针对提供的ArXiv网站论文集数据，编写程序自动遴选出AI/ML主题的论文集合
</br> 2.针对遴选出的AI/ML主题的论文集合进行分析，编写程序自动提取AI/ML相关的技术关键词，如“deep learning”或“random forest”等
</br> 3.编写程序分析并采用数据可视化方法展示上述AI/ML技术关键词，随时间变化的趋势

## 四、选题分析
本题主要是对PDF格式的论文数据集进行分析，筛选符合条件的论文并提取其关键词，并以可视化的形式将提取出的关键词展示出来，同时展示论文中关键词随时间变化的趋势。
### 难点分析：
本题主要有以下几个难点需要攻克：
</br> 1.如何将PDF格式文件转化为程序可直接读取的文件类型
</br> 2.如何提取文档的关键词，并排除无关词的的干扰
</br> 3.如何使用可视化的方法展示提取出的关键词

## 五、数据处理
使用pdfminer遍历数据集，将pdf文件转换为程序可直接读取的txt格式文件；
</br> 对转换后的txt格式文件进行清洗，使用正则表达式去掉标点和多余空行，并读取文本内容判断论文发表时间；
</br> 读取初步清洗后的文档，对文档内容进行分词，清除掉介词等无意义单词后对剩余单词进行词根化并使用tf-idf计算词频；
</br> 统计和整合相同发表时间的论文的词频（以月为单位）；
</br> 以月为单位，依照词频制作词云，完成关键词的可视化。
