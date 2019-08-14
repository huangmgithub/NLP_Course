# # max_font_size 调低最大字体
# # width,height,margin可以设置图片属性
# # font_path参数来设置字体集
# # background_color参数为设置背景颜色,默认颜色为黑色
# etc.......

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba,os

BASE_DIR = "../data/word_cloud"

# 固定词列表
# userdict_list = ['阿Ｑ', '孔乙己', '单四嫂子']

def processing_txt_by_jieba(text, stopwords_path):
    """
    中文分词
    :param text: 待分词文本
    :return:
    """

    # 增加固定词（保证不被再次分割）
    # for word in userdict_list:
    #     jieba.add_word(word)

    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)


    liststr = "/ ".join(seg_list)

    with open(stopwords_path, encoding='utf-8') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.splitlines()

    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)


def generate_word_cloud(text_path, image_path, font_path, stopwords_path, save_path):
    """
    生成词云
    :param text_path:  文本
    :param image_path: 图片
    :param font_path:  字体
    :param stopwords_path: 停用词
    :param save_path: 保存文件名
    :return:
    """
    # 读取文本
    text = open(text_path,encoding='utf-8').read()

    # 读取mask image
    alice_mask = np.array(Image.open(image_path))

    # 设置停用词，可添加到WordCloud中作为参数stopwords的值
    # stop_words = set(STOPWORDS)
    # stop_words.add('said')

    word_cloud = WordCloud(background_color='white',
                           max_words=2000,
                           mask=alice_mask,
                           contour_width=3,
                           contour_color='steelblue',
                           font_path=font_path).generate(processing_txt_by_jieba(text, stopwords_path))

    # 颜色
    # image_colors_byImg = ImageColorGenerator(alice_mask)

    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # 保存图片
    word_cloud.to_file(save_path)

if __name__ == "__main__":
    stopwords_path = os.path.join(BASE_DIR, 'stopwords_cn_en.txt')
    text_path = os.path.join(BASE_DIR, 'words.txt')
    image_path = os.path.join(BASE_DIR, 'animal.PNG')
    font_path = os.path.join(BASE_DIR, 'msyh.ttf')
    save_path = os.path.join(BASE_DIR, 'word_cloud.png')

    generate_word_cloud(text_path, image_path, font_path, stopwords_path, save_path)
