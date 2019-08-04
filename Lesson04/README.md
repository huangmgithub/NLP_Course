### <font color="gray" size="5" face="我是微软雅黑">Assignment-04 基于维基百科的词向量构建</font> 

#### &#10084; 使用Gensim和维基百科获得词向量，并且感受词向量的基本过程。

> #### 主要包括三部分：数据预处理、Word2Vec词向量训练、词向量可视化    

+ #### 第一步：
    * WikiCorpus or wikiextractor 抽取维基百科的内容
    * langconv.py和zh_wiki.py 将繁体中文转简体中文的文件(or opencc hanziconv）
    * jieba 将维基百科内容进行分词
    * 若使用wikiextractor, 需要进行空格,英文，特殊标点字符的去除(正则)

+ #### 第二步：
    * 使用gensim工具包的LineSentence类对jieba分词完的文件进行读取
    * 读取的内容,使用gensim工具包Word2Vec进行训练，get词向量及model
    * 测试两个词相似度以及找出指定词语的近义词

+ #### 第三步：
    * 使用Kaggle给出的T-SEN进行词向量的可视化
    

####  词向量原理参考(先看看同学的，等我总结自己的 = =)：
+ https://blog.csdn.net/weixin_40547993/article/details/88773730 
+ https://blog.csdn.net/weixin_40547993/article/details/88776217  
+ https://blog.csdn.net/weixin_40547993/article/details/88779922  
+ https://blog.csdn.net/weixin_40547993/article/details/88782251  

