import logging # 日志记录
from utils.ltp import LTP  # 文本处理(分词，词性分析，词性标注，命名实体识别，依存句法分析)
from bin.get_doc_similarity import compare_txt_similarity  # 比较文本相似度
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(lineno)d -  %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = './data'
LTP_MODEL_DIR = './model/ltp_data_v3.4.0'

def get_opinion_from_news(news, words_like_say_list, f_w=None):
    """
    获得新闻任务观点
    :param news: 一段新闻
    :param words_like_say_list: 与“说”相近的词列表
    :param f_w:   写入文件
    :return:
    """
    # ltp处理文本
    ltp = LTP(model_path=LTP_MODEL_DIR)
    # sentence_list = ltp.sentence_split(news)  # 分句
    words_list = ltp.word_split(news)  # 分词
    postags_list = ltp.word_tag(words_list)  # 词性标注
    entity_list = ltp.name_entity_recognize(words_list, postags_list) # 命名实体识别

    full_point_list = [index for index, word in enumerate(words_list) if word == "。"]  # 句号的位置

    res = [] # 返回新闻文本抽取处理结果

    if not full_point_list:
        full_point_list.append(len(words_list) - 1)

    if full_point_list[-1] != len(words_list) - 1:
        full_point_list.append(len(words_list) - 1)

    arcs, relation, heads = ltp.dependence_parse(words_list, postags_list)  # 依存句法分析
    for a, r, w, h, e in zip(arcs, relation, words_list, heads, entity_list):
        if 'S-Ns' != e[1] and 'S-Ni' != e[1] and 'S-Nh' != e[1]: # 判断新闻中是否包含人名，机构名等
            continue
        if r == "SBV": # 过滤出SBV的主谓结构
            if h in words_like_say_list:
                head = a.head  # 父节点词的索引
                print('{0}({1},{2},{3})'.format(r, w, h, head))
                logger.info("找到符合的===> {0}：{1}".format(w, h))
                end_point = len(words_list) - 1
                for point in full_point_list:
                    if point > head - 1:
                        end_point = point  # 谓词所在句子的句号位置
                        break
                if words_list[head] in [',','，',':','：','?','？','!','！']:
                    head += 1

                if len(words_list[head:end_point + 1]) < 5:
                    ob = []
                else:
                    ob = words_list[head:end_point + 1]
                if len(full_point_list) - full_point_list.index(end_point) == 1:
                    pass
                elif len(full_point_list) - full_point_list.index(end_point) == 2:
                    next_end_point = full_point_list[-1]
                    if len(words_list[end_point + 1: next_end_point + 1]) >= 3:
                        print(end_point+1, next_end_point+1)
                        ob += words_list[end_point + 1: next_end_point + 1]
                else:
                    next_sentence_count = len(full_point_list) - full_point_list.index(end_point) - 1
                    for i in range(next_sentence_count):
                        cur_sentence_start = full_point_list[full_point_list.index(end_point) - 1]
                        cur_sentence_stop = end_point
                        cur_sentence = words_list[cur_sentence_start + 1:cur_sentence_stop + 1]
                        compare_sentence_stop = full_point_list[full_point_list.index(end_point) + 1]
                        compare_sentence = words_list[cur_sentence_stop + 1:compare_sentence_stop + 1]
                        if compare_txt_similarity(cur_sentence, compare_sentence):
                            ob += compare_sentence
                        else:
                            break
                        end_point = full_point_list[full_point_list.index(end_point) + 1]
                if ob == []:
                    continue
                logger.info("写入ing")
                res.append((w, h, ''.join(ob)))  # 待返回内容
                # f_w.write("{0} {1} {2}".format(w, h, ''.join(ob)) + '\n')

    # f_w.write("\n++++++++++++++++++++++++++++++++++++ 分割线 ++++++++++++++++++++++++++++++++++++\n")
    return res


if __name__ == "__main__":

    # 获得与说相近的词 f1
    # 新闻存储文本
    # 创建txt文件保存结果 f_w
    with open(os.path.join(BASE_DIR, 'words.txt'), 'r', encoding='utf-8') as f1, \
        open(os.path.join(BASE_DIR, 'filter_news.txt'), 'r', encoding='utf-8') as f2, \
            open(os.path.join(BASE_DIR, 'result.txt'), 'w', encoding='utf-8') as f_w:

            # 获得与“说”相近的词列表
            words_like_say_list = f1.read().split(' ')

            for news in f2:
                res = get_opinion_from_news(news, words_like_say_list, f_w)





