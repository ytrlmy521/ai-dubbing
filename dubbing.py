# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import time
import os # 用于构建输出文件路径
from rating_script import rate_translation, RATING_PROMPT_TEMPLATE # 导入评分函数和模板

# --- 配置部分 ---
# CSV文件路径 CSV_FILE_PATH = r"C:\Users\User\Downloads\AI配音中翻英台本 0320\AI配音中翻英台本\电视剧\好事成双\14-01_TJ.csv"
CSV_FILE_PATH = r"C:\Users\User\Downloads\AI配音中翻英台本 0320\AI配音中翻英台本\电视剧\14-01_TJ.csv"
# API接口地址
API_URL = "https://cloud.infini-ai.com/maas/v1/chat/completions"
# API密钥（Bearer Token格式）
API_KEY = "Bearer sk-daz7idir52x7kash"
# 使用的模型名称
MODEL_NAME = "deepseek-v3"

# --- 翻译提示词模板 ---
PROMPT_TEMPLATE = """
翻译要求：将电视剧《好事成双》中文剧本译为美式英语配音稿。需确保：
1）角色身份准确，与第10项的任务身份一致（林双-前顶尖高材生/全职主妇，顾许-海归精英/林双同学，江喜-职场女性/林双闺蜜） 
2）译文行数与原文逐行对应 
3）口语化表达符合角色身份 
4）专业术语保持语境一致 
5）保留5%行数弹性空间 
6）使用当代美式英语表达习惯 
7）确保口型同步适配 
8）PG级语言规范。注意人物关系表述的自然流畅，职场场景用词需符合硅谷科技公司背景设定。
9) 剧情背景介绍：Lin Shuang, once a top university graduate, became a full-time mom after marriage—only to face betrayal. Fighting for custody of her daughter, she returns to the workforce, where she stumbles upon Gu Xu, her former classmate now a high-achieving returnee. Shocked to see her abandon her hard-earned skills for marriage, he is frustrated yet drawn to her resilience. With support from friend Jiang Xi, Lin Shuang overcomes challenges in love, career, and family, proving her worth. As she transforms from homemaker to professional, she also finds love with Gu Xu. Both Lin Shuang and Jiang Xi grow through rivalry and camaraderie, forging new futures. Please translate this modern TV show's script into American English for lip sync dubbing.
10) 人物身份：林双：曾是天之骄女的林双在怀孕生子后，辞去工作成为全职主妇，每日围绕家庭大小事宜奔波不停，直到她发现丈夫卫明的背叛，婚姻危机一触即发。为了在离婚时能顺利夺下女儿的抚养权，林双必须重返职场实现经济独立，以证明自己有养育孩子的能力。但她在对家庭孤注一掷的10年里，也被迫失去了自我，逐渐走向了人生窄路。顾许：出身普通城市家庭，从小开明的教育让尊重他人和换位思考刻在骨子里。顾许性格木讷不善言谈，当得知林双毕业后就放弃专业做了家庭主妇，顾许替她不甘，也气她不争气。随着林双的成长，顾许的钦佩和保护欲逐渐变成爱恋，这些年他尊重林双的决定，选择退出和祝福，但他承认自己从没忘记过林双。江喜：出身小镇，赌徒父亲四处躲债让她毫无安全感，重男轻女的母亲只会在她身上吸血，将教育资源严重向儿子江海倾斜。江喜毕业后来到大城市打拼，她一面努力生活，一面包装自己。从小城市的大公司，到大城市的小公司，再从方舟的前台，内部转岗到市场部做商务拓展，她利用一切机会去攀附各路大佬，刷新自己的行业经验。卫明：出身小城市，父母是小生意人，他的出身环境也养成了他利益至上的人生信条。自小习惯了斤斤计较，形成了以自我利益为中心的自私性格。但是眼力见儿极好善于见风使舵，也让他对女人的情绪非常敏感，假意温柔，在一开始就将林双和江喜哄得团团转。可当发现原本被自己哄得团团转的林双和江喜心生反意，便睚眦必报地打击报复。黄嘉仪：出生豪门千金，自小在外留学缺乏家庭温暖，父母因此对她过度保护弥补导致心事单纯涉事未深。黄嘉仪虽是空降公司，但她履历和能力都很出众，对自己所负责的工作也兢兢业业，不遗余力的去完成。但是人际关系的处理却不尽如人意，团队协作经验不足，过于直接的沟通方式引起同事高度不满和抵制，导致工作举步维艰。

请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
{text_to_translate}
"""

# 翻译函数
def translate_text(text, model_name, api_key, api_url, prompt_template):
    """
    调用大模型API进行文本翻译
    
    参数:
        text: 需要翻译的中文文本
        model_name: 使用的模型名称
        api_key: API密钥
        api_url: API接口地址
        prompt_template: 翻译提示词模板
    
    返回:
        翻译后的英文文本
    """
    # 检查输入文本是否为空
    if not text or pd.isna(text):
        return ""

    # 设置请求头
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': api_key
    }

    # 构建完整的提示词
    full_prompt = prompt_template.format(text_to_translate=text)

    # 构建请求体
    payload = json.dumps({
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "stream": False,
        "temperature": 0.7,
    })

    try:
        # 发送API请求
        response = requests.post(api_url, headers=headers, data=payload, timeout=60)
        response.raise_for_status()  # 检查响应状态码

        # 解析响应数据
        data = response.json()
        translation = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        translation = translation.strip()  # 清理首尾空白字符

        return translation

    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {e}")
        return f"ERROR: 请求失败 ({e})"
    except json.JSONDecodeError:
        print(f"JSON解析错误: {response.text}")
        return "ERROR: 无效的JSON响应"
    except KeyError as e:
        print(f"响应结构错误: {e}")
        return f"ERROR: 意外的响应结构 ({e})"
    except Exception as e:
        print(f"翻译过程中发生意外错误: {e}")
        return f"ERROR: 意外错误 ({e})"

if __name__ == "__main__":
    print(f"开始处理文件: {CSV_FILE_PATH}")
    print(f"使用模型: {MODEL_NAME}")

    # 检查文件是否存在
    if not os.path.exists(CSV_FILE_PATH):
        print(f"错误: 找不到文件 {CSV_FILE_PATH}")
        exit()

    try:
        # 尝试使用UTF-8编码读取CSV文件
        try:
            df = pd.read_csv(CSV_FILE_PATH, encoding='utf-8')
        except UnicodeDecodeError:
            print("UTF-8解码失败，尝试使用GBK编码...")
            df = pd.read_csv(CSV_FILE_PATH, encoding='gbk')

        # 检查必要的列是否存在
        required_cols = ['speaker', 'start_time', 'end_time', 'transcription']
        if not all(col in df.columns for col in required_cols):
            print(f"错误: CSV文件必须包含以下列: {required_cols}")
            exit()

        # 初始化翻译结果列表和评分结果列表
        translations = []
        ratings = []
        total_rows = len(df)
        print(f"共发现 {total_rows} 行需要处理")

        # 逐行处理翻译和评分
        for index, row in df.iterrows():
            chinese_text = row['transcription'].rstrip(',')
            print(f"正在处理第 {index + 1}/{total_rows} 行: '{str(chinese_text)[:100]}...'")

            # 调用翻译函数
            english_translation = translate_text(
                chinese_text,
                MODEL_NAME,
                API_KEY,
                API_URL,
                PROMPT_TEMPLATE
            )
            translations.append(english_translation)

              # 添加延时以避免API限制
            time.sleep(5)

            # 对翻译结果进行评分
            if english_translation and not english_translation.startswith("ERROR"):
                print(f"正在对翻译结果进行评分...")
                rating = rate_translation(
                    chinese_text,
                    english_translation,
                    MODEL_NAME,
                    API_KEY,
                    API_URL,
                    RATING_PROMPT_TEMPLATE
                )
                ratings.append(rating)
            else:
                ratings.append("评分失败")  # 如果翻译失败，评分也标记为失败
            
            time.sleep(5)
          

        # 添加翻译结果列和评分结果列
        df['translation'] = translations
        df['rating'] = ratings

        # 构建输出文件路径
        base, ext = os.path.splitext(CSV_FILE_PATH)
        output_file_path = f"{base}_translated_rated{ext}"
        
        # 保存结果到新文件（使用utf-8-sig编码以确保Excel能正确显示中文）
        df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

        print(f"\n翻译和评分完成！")
        print(f"结果已保存至: {output_file_path}")

    except FileNotFoundError:
        print(f"错误: 找不到文件 {CSV_FILE_PATH}")
    except pd.errors.EmptyDataError:
        print(f"错误: CSV文件为空 {CSV_FILE_PATH}")
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
