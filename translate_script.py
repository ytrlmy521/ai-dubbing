# -*- coding: utf-8 -*-
import pandas as pd
import http.client
import json
import time
import csv

def translate_text(text, api_key):
    """
    调用API进行翻译
    """
    conn = http.client.HTTPSConnection("cloud.infini-ai.com")
    
    # 构建翻译提示词
    prompt = f"""翻译要求：将电视剧《好事成双》中文剧本译为美式英语配音稿。需确保：
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

    原文：{text}"""

    payload = {
        "model": "deepseek-v3",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 10000
    }

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {api_key}"
    }

    try:
        conn.request("POST", "/maas/v1/chat/completions", json.dumps(payload), headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        else:
            return "Translation failed"
            
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return "Translation error"
    finally:
        conn.close()

def main():
    # 设置API密钥
    API_KEY = "sk-daz7idir52x7kash"  # 请替换为你的实际API密钥
    
    # 文件路径
    input_file = "C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本\\电视剧\\好事成双\\14-01_TJ.csv"
    output_file = input_file.replace(".csv", "_translated.csv")
    
    try:
        # 读取CSV文件
        rows = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            fieldnames = reader.fieldnames + ['translation']
            
            # 创建输出文件
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                
                # 逐行处理
                for i, row in enumerate(reader):
                    print(f"Translating line {i + 1}")
                    translation = translate_text(row['transcription'], API_KEY)
                    row['translation'] = translation
                    writer.writerow(row)
                    
                    # 添加延时以避免API限制
                    time.sleep(1)
        
        print(f"Translation completed. Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        print("Please check if the file exists and has the correct format.")

if __name__ == "__main__":
    main() 