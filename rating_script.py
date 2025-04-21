# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd # translate_text 函数依赖 pandas.isna
import time # 虽然评分本身可能不需要，但 translate_text 里有，保持一致
import os # 虽然评分本身可能不需要，但 translate_text 里有，保持一致
import re # 导入正则表达式库用于解析批量评分结果
import random # 导入random用于随机选择API密钥
from itertools import cycle # 导入cycle用于循环迭代API密钥

# --- API 配置 ---
API_URL = "https://api.x.ai/v1/chat/completions"
# 多个API密钥配置
API_KEYS = [
    "Bearer xai-0rkRDFt2xe041BgWMaf9o7naR1cdrcd8i0yJyzCzh0KXacUpxj5nHpjbMYgguUy8N0X0GJkeXLJUkmJY",  # 原始密钥作为第一个
    # 以下可以添加更多API密钥
    # "Bearer sk-your_key_2",
    # "Bearer sk-your_key_3",
    # 等等...
]
# 使用第一个密钥作为默认密钥
API_KEY = API_KEYS[0]  
# 创建一个循环迭代器
api_key_cycle = cycle(API_KEYS)
# 当前使用的API密钥索引
current_api_key_index = 0

# 定义代理服务器
proxies = {
        'http': 'http://10.252.27.1:8888',
        'https': 'http://10.252.27.1:8888', # 假设HTTPS也走这个代理
}

MODEL_NAME = "grok-3-beta" # 或者其他适合评分任务的模型

# --- API密钥轮询功能 ---
def get_next_api_key():
    """获取下一个API密钥，实现轮询机制"""
    global current_api_key_index
    
    # 如果只有一个API密钥，则直接返回
    if len(API_KEYS) <= 1:
        return API_KEYS[0]
    
    # 循环使用下一个API密钥
    current_api_key_index = (current_api_key_index + 1) % len(API_KEYS)
    return API_KEYS[current_api_key_index]

def get_random_api_key():
    """随机获取一个API密钥"""
    return random.choice(API_KEYS)

# --- 评分标准 Prompt 模板 ---
RATING_PROMPT_TEMPLATE = """
你是一个专业的影视剧译制翻译质量评估员，对翻译质量要求非常严格。请根据以下评分标准，对提供的中文原文和英文译文进行认真评估。

重要说明：每个评分维度都有明确的标准，请严格按照标准评分，不要无故给满分！即使翻译看起来不错，也请仔细分析各个维度可能存在的问题。好的翻译可能得到较高分数，但极少有完美的翻译能在所有维度都得满分。

注意：评分标准（每个维度分值都不一样）:
     准确性 (Accuracy) - 30分
     流畅度 (Fluency) - 25分
     语境适应性 (Contextual Appropriateness) - 20分
     对口型匹配度 (Lip-Sync Compatibility) - 15分
     文化适用性 (Localization) - 10分

1.  准确性 (Accuracy) - 30分: 是否准确传达原文含义，无遗漏或曲解。
    - 27-30 分: 翻译完全准确，无任何错误。仅在译文完美捕捉原文全部含义且无任何偏差时给予。
    - 20-26 分: 翻译基本准确，存在轻微偏差但不影响理解。这是大多数好翻译应得的分数。
    - 10-19 分: 翻译有明显错误，但核心意思尚存。
    - 0-9 分: 翻译严重失真，原文意思丧失。
        - 示例: 
        - 原文: "你别逼我动手。" 
        - 翻译: "Don't force me to act." (25 分，准确但"动手"的威胁性稍有弱化)
        - 翻译: "Don't make me use force." (28 分，更准确地传达了威胁意味)
        - 翻译: "You don't make me move."  (10 分，误解了原文含义)

2.  流畅度 (Fluency) - 25分: 是否符合英语母语者表达习惯，语法正确流畅。
      - 22-25 分: 翻译自然流畅，如英语母语者表达。仅当表达非常地道，完全符合英语习惯时才给满分。
      - 15-21 分: 翻译较自然，但有轻微不地道之处。这是大多数好翻译的正常分数。
      - 8-14 分: 翻译可理解，但明显非母语风格。
      - 0-7 分: 翻译生硬，语法或表达严重不当。
        - 示例: 
        - 原文: "这事儿没那么简单。" 
        - 翻译: "It's not that simple." (23 分，自然流畅)
        - 翻译: "This matter is not so simple." (18 分，语法正确但不够地道)
        - 翻译: "This matter not so simple." (5 分，语法错误)

3.  语境适应性 (Contextual Appropriateness) - 20分: 是否符合影视剧场景、角色语气、情绪、性格和剧情。
      - 18-20 分: 翻译完美契合语境，语气和角色一致。需要译文特别符合场景和角色特点才给满分。
      - 12-17 分: 翻译基本符合语境，但语气稍有偏差。这是大多数好翻译的常见得分。
      - 6-11 分: 翻译与语境脱节，角色性格体现不足。
      - 0-5 分: 翻译完全无视语境，语气或含义不符。
        - 示例: 
        - 场景: 武侠片中高手对决 
        - 原文: "来吧，决一死战。"
        - 翻译: "Come on, fight to the death." (17 分，基本符合语境)
        - 翻译: "Come, let us duel to the death." (19 分，更符合武侠片风格)
        - 翻译: "Let's have a meeting." (0 分，完全不符)

4.  对口型匹配度 (Lip-Sync Compatibility) - 15分: 英文单词数、音节数和节奏是否与中文口型接近（考虑语流节奏）。
      - 13-15 分: 翻译音节和节奏高度匹配，配音几乎无缝。需要音节数和重音位置都非常匹配才给满分。
      - 9-12 分: 翻译基本匹配，需轻微调整口型。这是好翻译的常见分数。
      - 5-8 分: 翻译勉强可用，但节奏或音节明显不符。
      - 0-4 分: 翻译完全无法对口型，音节数或节奏严重偏离。
        - 示例: 
        - 原文: "我不会让你走。" (6 个音节) 
        - 翻译: "I won't let you go."  (6 个音节，13 分，音节数一致但重音位置稍有差异)
        - 翻译: "I will not allow you to leave." (11 个音节, 5 分，音节数明显不匹配)

5.  文化适用性 (Localization) - 10分: 是否适应目标语英语观众文化背景，避免直译障碍。
      - 9-10 分: 翻译充分本地化，符合英语文化习惯。只有真正考虑了文化差异并巧妙本地化的翻译才给满分。
      - 6-8 分: 翻译基本适配，但有些细节未优化。这是大多数好翻译的正常分数。
      - 3-5 分: 翻译未完全本地化，可能引发轻微误解。
      - 0-2 分: 翻译忽视文化差异，显得突兀或费解。
       - 示例: 
        - 原文: "晒黑了不好看。" 
        - 翻译: "Too much sun will hurt your skin." (9 分，巧妙规避了文化差异)
        - 翻译: "Getting tan doesn't look good." (7 分，直译但能理解)
        - 翻译: "Dark skin isn't attractive." (0 分，忽视文化差异和价值观问题)

评估以下内容：
中文原文: "{source_text}"
英文译文: "{translation_text}"

请根据上述标准进行严格评分，并按照以下格式返回评分结果：
accuracy:XX,fluency:XX,contextual:XX,lipsync:XX,localization:XX

例如：accuracy:25,fluency:20,contextual:15,lipsync:10,localization:5

注意：
1. 所有分值必须是0-30之间的整数
2. 严格按照上述格式返回，不要包含任何其他文字
3. 使用英文逗号分隔各个评分
4. 不要无故给满分，每个满分都需要有充分理由
"""

# --- 批量评分提示词模板 ---
BATCH_RATING_PROMPT_TEMPLATE = """
你是一个专业的翻译评分专家，任务是根据以下评分标准对翻译文本进行评分。评分需严格遵循用户提供的标准，综合评估翻译质量。每项评分满分10分，总分由各评分项加权计算（具体权重由用户决定，或默认均等）。请确保评分逻辑透明，包含详细的评分依据和计算过程，并在评分中提供示例说明。以下是评分标准和提示词要求：

#### 1. 是否按照Prompt设定的术语表翻译（满分10分）
- **评分标准**：
  - 翻译必须严格遵循Prompt中指定的术语表，确保术语一致性和准确性。
  - 若术语表中的术语未被正确使用，每出现一次错误扣1分（最多扣10分）。
  - 若原文中未涉及术语表内容，但译文擅自引入不一致的术语，扣2分/次。
  - 若术语表未提供，但译文使用了不恰当或不一致的术语，酌情扣分（基于目标语言的惯用表达）。
- **评分步骤**：
  1. 对比原文和译文，检查术语表中指定的术语是否出现在原文中。
  2. 验证译文是否使用术语表中的对应翻译。
  3. 记录术语使用错误的数量，计算扣分。
- **示例**：
  - 术语表：英文"machine learning"应翻译为法语"apprentissage automatique"。
  - 原文：The system uses machine learning.
  - 译文：Le système utilise l'apprentissage automatique.（10分）
  - 译文：Le système utilise l'intelligence artificielle.（8分，术语错误扣2分）
  - 译文：Le système utilise machine learning.（6分，未翻译术语扣4分）

#### 2. 是否按照Prompt设定的tu/vous关系翻译（仅限法语和葡萄牙语，英语和斯洛文尼亚语不涉及）（满分10分）
- **评分标准**：
  - 法语和葡萄牙语翻译必须遵循Prompt中指定的tu（亲密）或vous（正式）关系。
  - 每出现一次tu/vous使用错误，扣2分（最多扣10分）。
  - 若原文语境未明确指定关系，但译文未遵循Prompt默认设置，扣1分/次。
  - 若Prompt未指定tu/vous关系，译文需根据目标语言语境选择合理的关系，错误扣1分/次。
- **评分步骤**：
  1. 检查Prompt中是否指定tu/vous关系。
  2. 对比原文语境和译文，验证tu/vous的使用是否符合要求。
  3. 记录错误次数，计算扣分。
- **示例**：
  - Prompt指定：使用vous（正式）。
  - 原文：Can you help me?（英语）
  - 译文（法语）：Pouvez-vous m'aider ?（10分）
  - 译文（法语）：Peux-tu m'aider ?（8分，tu/vous错误扣2分）
  - 译文（葡萄牙语）：Pode me ajudar?（10分）
  - 译文（葡萄牙语）：Podes me ajudar?（8分，tu/vous错误扣2分）

#### 3. 是否按照Prompt设定的语言分级翻译（满分10分）
- **评分标准**：
  - 翻译必须符合Prompt中指定的语言分级（如正式、口语化、专业术语等）。
  - 若译文语言风格与指定分级不符，每出现一次错误扣2分（最多扣10分）。
  - 若Prompt未明确指定语言分级，译文需根据原文语境选择适当风格，错误扣1分/次。
- **评分步骤**：
  1. 确定Prompt中指定的语言分级。
  2. 分析译文语言风格是否符合要求（如用词、句式、语气）。
  3. 记录不符合分级的实例，计算扣分。
- **示例**：
  - Prompt指定：口语化。
  - 原文：Let's get started!
  - 译文（法语）：Allez, on commence !（10分）
  - 译文（法语）：Procédons au commencement.（6分，过于正式，扣4分）
  - Prompt未指定，原文为口语：
  - 译文（法语）：On y va !（10分）
  - 译文（法语）：Veuillez débuter.（8分，风格不符，扣2分）

#### 4. 是否遵照Prompt设定的计量单位翻译（满分10分）
- **评分标准**：
  - 翻译需遵循Prompt中指定的计量单位规则（以原文单位为准或以目标语惯用单位为准）。
  - 若Prompt指定以原文单位为准，译文需保留原文单位（如"miles"不转为"kilometers"）。
  - 若Prompt指定以目标语为准，译文需转换为目标语言惯用单位（如英语"miles"转为法语"kilomètres"）。
  - 每出现一次计量单位错误，扣2分（最多扣10分）。
  - 若原文未涉及计量单位，则此项得满分。
- **评分步骤**：
  1. 确认Prompt中计量单位规则。
  2. 检查原文中的计量单位及其在译文中的表达。
  3. 记录单位转换或保留的错误，计算扣分。
- **示例**：
  - Prompt指定：以目标语为准。
  - 原文：The distance is 5 miles.
  - 译文（法语）：La distance est de 8 kilomètres.（10分）
  - 译文（法语）：La distance est de 5 miles.（8分，未转换单位，扣2分）
  - Prompt指定：以原文为准。
  - 译文（法语）：La distance est de 5 miles.（10分）
  - 译文（法语）：La distance est de 8 kilomètres.（8分，错误转换，扣2分）

#### 5. 源语言到目标语的翻译完整度（以英语到法语为例）（满分10分）
- **评分标准**：
  - 翻译需100%将源语言（英语）翻译为目标语言（法语）。
  - 评分公式：得分 = 10 × (1 - 未翻译行数 / 总行数)。
  - 若译文完全翻译为法语，得10分。
  - 若部分英语未翻译，按未翻译行数比例扣分。
  - 若整行未翻译，每行扣2分（最多扣10分）。
- **评分步骤**：
  1. 计算原文总行数。
  2. 统计译文中未翻译为法语的行数（包括保留原文或缺失翻译的行）。
  3. 按公式计算得分。
- **示例**：
  - 原文（3行）：
    - I love coffee.
    - It's a sunny day.
    - Let's go for a walk.
  - 译文：
    - J'aime le café.
    - It's a sunny day.
    - Allons nous promener.
  - 评分：未翻译1行，总行数3行，得分 = 10 × (1 - 1/3) = 6.67分（四舍五入得7分）。
  - 译文（全翻）：
    - J'aime le café.
    - C'est une journée ensoleillée.
    - Allons nous promener.
  - 评分：10分。

#### 6. 开闭口匹配（每句话开头和结尾的单词开闭口需匹配）（满分10分）
- **评分标准**：
  - 每句话的开头和结尾单词的开闭口音需与原文一致（开声/闭声）。
  - 开声：以元音或无声辅音开头/结尾；闭声：以辅音（特别是爆破音）开头/结尾。
  - 每句不符合开闭口匹配的，扣2分/句（最多扣10分）。
  - 若译文句数与原文不一致，按原文句数为准，未翻译的句子视为错误，扣2分/句。
- **评分步骤**：
  1. 分析原文每句的开头和结尾单词的开闭口特征。
  2. 对比译文每句的开闭口是否匹配。
  3. 记录不匹配的句子，计算扣分。
- **示例**：
  - 原文：嗯嗯！（开声：/m/，闭声：/m/）
  - 译文：Mhmm.（开声：/m/，闭声：/m/，10分）
  - 译文：Uh-huh.（开声：/ʌ/，闭声：/h/，0分，开闭口不匹配）
  - 原文：Let's go!（开声：/l/，闭声：/g/）
  - 译文：Allons-y !（开声：/a/，闭声：/i/，6分，开声不匹配，扣4分）

#### 7. 音节数匹配（结合语速和音节数）（满分10分）
- **评分标准**：
  - 译文的音节数需与原文音节数匹配，同时考虑语速（每秒音节数）。
  - 语速参考：
    - 英语：150单词/分钟（2.5单词/秒），约4.4音节/秒（中位数）。
    - 法语/葡萄牙语：150-160单词/分钟（2.5单词/秒），250-300音节/分钟（约4.58音节/秒）。
  - 音节数评分：
    - 译文音节数完全匹配原文，得10分。
    - 译文音节数偏差1个，得8分；偏差2个，得6分；偏差3个，得4分；偏差4个及以上，得0分。
  - 若提供视频或语速信息，需根据实际语速调整音节数匹配（如快速语速需压缩音节）。
- **评分步骤**：
  1. 计算原文的音节数（逐词分析元音核心）。
  2. 根据语速（默认或视频提供）估算每秒音节数。
  3. 计算译文的音节数，验证是否匹配原文。
  4. 根据音节数偏差计算得分。
- **示例**：
  - 原文：千万别和你妈妈讲！（8个音节，语速4.4音节/秒，约1.82秒）
  - 译文：Don't tell this to your mom, okay?（8个音节，10分）
  - 译文：Don't tell your mom about this.（7个音节，8分，偏差1个）
  - 译文：This is our secret.（5个音节，4分, 偏差3个）
  - 译文：Shhh!（1个音节，0分，偏差7个）
  - 若视频显示语速为5音节/秒：
    - 原文8音节需1.6秒，译文需调整为接近8音节且适合1.6秒的表达。

下面是需要评分的翻译内容，每行以索引号开头，格式为"[索引号] 英文原文 ||| 法语译文"：

{combined_texts}

请对每个翻译配对进行严格评分，确保区分不同翻译的质量差异，并按照以下格式返回评分结果：
[索引号] 术语表一致性:XX,tu/vous关系:XX,语言分级:XX,计量单位:XX,翻译完整度:XX,开闭口匹配:XX,音节数匹配:XX

例如：
[123] 术语表一致性:9,tu/vous关系:10,语言分级:10,计量单位:10,翻译完整度:10,开闭口匹配:10,音节数匹配:10

请确保:
1. 每个评分结果前必须有原始索引号，格式为 [索引号]，与输入的索引号完全一致
2. 所有分值必须是0-10之间的整数
3. 每行评分结果独立成行
4. 使用英文逗号分隔各个评分
5. 不要添加任何额外的解释文字
6. 必须根据翻译质量的不同，给出相应的不同分数，避免所有翻译评分都完全相同
"""

# --- 从笔记中复制的 translate_text 函数，添加轮询逻辑 ---
def translate_text(prompt_content, model_name, api_key=None, api_url=None):
    """
    调用大模型API执行任务（翻译或评分）。
    支持API密钥轮询，如果未指定api_key，则自动轮询选择密钥。

    参数:
        prompt_content: 发送给大模型的完整提示内容。
        model_name: 使用的模型名称。
        api_key: API密钥，如果不指定，则使用轮询机制获取。
        api_url: API接口地址，如果不指定，则使用默认地址。

    返回:
        大模型的响应内容。
    """
    if not prompt_content: # 检查输入prompt是否为空
        return "ERROR: Prompt content is empty"
    
    # 如果未指定API密钥，则轮询获取下一个
    if api_key is None:
        api_key = get_next_api_key()
        print(f"使用API密钥: {api_key[:15]}... (轮询选择)")
    
    # 如果未指定API地址，则使用默认地址
    if api_url is None:
        api_url = API_URL
    
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': api_key
    }

    payload = json.dumps({
      "model": model_name,
      "messages": [
        {
          "role": "user",
          "content": prompt_content
        }
      ],
      "stream": False,
      "temperature": 0.7, # 提高温度，增加输出的随机性，以获得更差异化的评分
    })

    try:
        # 增加重试逻辑
        max_retries = min(3, len(API_KEYS))  # 最多重试次数，不超过可用API密钥数
        retries = 0
        
        while retries < max_retries:
            try:
                response = requests.post(api_url, headers=headers, data=payload, timeout=90, proxies=proxies)
                response.raise_for_status()
                break  # 请求成功，跳出重试循环
            except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                retries += 1
                if retries >= max_retries:
                    raise  # 达到最大重试次数，抛出异常
                
                print(f"API请求失败 (第{retries}次): {e}")
                # 切换API密钥再试
                api_key = get_next_api_key()
                headers['Authorization'] = api_key
                print(f"尝试使用新API密钥: {api_key[:15]}...")
                # time.sleep(1)  # 稍等一下再重试
        
        data = response.json()
        # 提取模型返回的内容
        result = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # 清理响应内容
        result = result.strip()
        
        # 如果响应不是有效的JSON，尝试修复
        if not result.startswith('{'):
            # 尝试找到第一个 { 和最后一个 }
            start = result.find('{')
            end = result.rfind('}')
            if start != -1 and end != -1:
                result = result[start:end+1]
        
        # 再次清理
        result = result.strip()
        
        print(f"评分结果: {result}")
        return result

    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {e}")
        return f"ERROR: 请求失败 ({e})"
    except json.JSONDecodeError:
        print(f"JSON解析错误: Response text: {response.text}")
        return "ERROR: 无效的JSON响应"
    except KeyError as e:
        print(f"响应结构错误: Missing key {e}. Response data: {data}")
        return f"ERROR: 意外的响应结构 ({e})"
    except Exception as e:
        print(f"处理过程中发生意外错误: {e}")
        return f"ERROR: 意外错误 ({e})"

# --- 新增的评分函数 ---
def rate_translation(source_text, translation_text, model_name, api_key=None, api_url=None, rating_prompt_template=None):
    """
    调用大模型对翻译质量进行评分。

    参数:
        source_text: 中文原文。
        translation_text: 英文译文。
        model_name: 使用的模型名称。
        api_key: API密钥，如果不指定，则使用轮询机制获取。
        api_url: API接口地址，如果不指定，则使用默认地址。
        rating_prompt_template: 包含评分标准的提示词模板，如不指定则使用默认模板。

    返回:
        包含五个维度评分的字典。
    """
    # 使用默认模板（如果未指定）
    if rating_prompt_template is None:
        rating_prompt_template = RATING_PROMPT_TEMPLATE
        
    # 构建完整的评分prompt
    rating_prompt = rating_prompt_template.format(
        source_text=source_text,
        translation_text=translation_text
    )

    # 调用 translate_text 函数获取评分结果
    score_text = translate_text(rating_prompt, model_name, api_key, api_url)
    
    # 如果返回错误，直接返回默认值
    if score_text.startswith("ERROR"):
        print(f"API返回错误: {score_text}")
        return get_default_scores()
    
    try:
        # 清理响应文本
        score_text = score_text.strip()
        
        # 解析评分结果
        scores = {}
        for item in score_text.split(','):
            if ':' in item:
                key, value = item.split(':')
                try:
                    value = int(value.strip())
                    if 0 <= value <= 100:
                        scores[key.strip()] = value
                    else:
                        print(f"分值超出范围: {key}={value}")
                        scores[key.strip()] = 0
                except ValueError:
                    print(f"无效的分值: {key}={value}")
                    scores[key.strip()] = 0
        
        # 确保所有必需的评分都存在
        required_scores = {
            'accuracy': 0,
            'fluency': 0,
            'contextual': 0,
            'lipsync': 0,
            'localization': 0
        }
        
        # 更新默认值
        for key in required_scores:
            if key in scores:
                required_scores[key] = scores[key]
        
        return required_scores
        
    except Exception as e:
        print(f"解析评分结果时发生错误: {e}")
        return get_default_scores()

# --- 新增的批量评分函数 ---
def batch_rate_translations(texts_with_indices, model_name, api_key=None, api_url=None):
    """
    批量调用大模型对多个翻译配对进行评分。

    参数:
        texts_with_indices: 包含索引、原文和译文的列表，每项格式为(index, source_text, translation_text)
        model_name: 使用的模型名称。
        api_key: API密钥，如果不指定，则使用轮询机制获取。
        api_url: API接口地址，如果不指定，则使用默认地址。

    返回:
        字典，键为索引，值为包含五个维度评分的子字典。
    """
    if not texts_with_indices:
        print("警告: 没有有效的翻译需要评分")
        return {}
        
    # 构建合并的评分文本
    combined_texts = []
    for index, source, translation in texts_with_indices:
        combined_texts.append(f"[{index}] {source} ||| {translation}")
    
    combined_text_str = "\n".join(combined_texts)
    
    # 构建完整的评分提示词
    full_prompt = BATCH_RATING_PROMPT_TEMPLATE.format(
        combined_texts=combined_text_str
    )
    
    # 调用API获取评分结果
    score_text = translate_text(full_prompt, model_name, api_key, api_url)
    
    # 如果返回错误，返回空字典
    if score_text.startswith("ERROR"):
        print(f"批量评分API返回错误: {score_text}")
        return {}
    
    # 解析评分结果
    scores_by_index = {}
    try:
        # 按行分割结果
        lines = score_text.strip().split('\n')
        # 更新正则表达式以匹配新的评分格式
        line_pattern = re.compile(r"^\[(\d+)\]\s*术语表一致性:(\d+),tu/vous关系:(\d+),语言分级:(\d+),计量单位:(\d+),翻译完整度:(\d+),开闭口匹配:(\d+),音节数匹配:(\d+)$")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = line_pattern.match(line)
            if match:
                try:
                    index = int(match.group(1))
                    # 提取新的评分维度值
                    terminology_score = int(match.group(2))
                    tu_vous_score = int(match.group(3))
                    language_level_score = int(match.group(4))
                    units_score = int(match.group(5))
                    completeness_score = int(match.group(6))
                    lip_sync_open_close_score = int(match.group(7))
                    syllable_score = int(match.group(8))

                    # 验证分值范围 (所有维度都是 0-10)
                    if all(0 <= score <= 10 for score in [
                        terminology_score, tu_vous_score, language_level_score,
                        units_score, completeness_score, lip_sync_open_close_score,
                        syllable_score
                    ]):
                        # 使用新的键名存储评分结果
                        scores_by_index[index] = {
                            '术语表一致性': terminology_score,
                            'tu/vous关系': tu_vous_score,
                            '语言分级': language_level_score,
                            '计量单位': units_score,
                            '翻译完整度': completeness_score,
                            '开闭口匹配': lip_sync_open_close_score,
                            '音节数匹配': syllable_score
                        }
                    else:
                        print(f"警告: 索引 {index} 的部分分值超出范围 (0-10)")
                        scores_by_index[index] = get_default_scores() # 使用更新后的默认值
                except ValueError:
                    print(f"警告: 索引或分值解析失败: {line}")
            else:
                # 尝试匹配旧格式以提供兼容性或更详细的警告
                old_pattern = re.compile(r"^\[(\d+)\]\s*accuracy:(\d+),fluency:(\d+),contextual:(\d+),lipsync:(\d+),localization:(\d+)$")
                old_match = old_pattern.match(line)
                if old_match:
                     print(f"警告: 评分结果格式不匹配，似乎是旧格式: {line}")
                else:
                    print(f"警告: 评分结果格式无法识别: {line}")

        # 检查是否所有索引都有对应的评分
        indices_with_scores = set(scores_by_index.keys())
        expected_indices = set(index for index, _, _ in texts_with_indices)
        missing_indices = expected_indices - indices_with_scores
        
        if missing_indices:
            print(f"警告: 以下索引的评分结果缺失: {missing_indices}")
            # 为缺失的索引添加默认分数
            for index in missing_indices:
                scores_by_index[index] = get_default_scores()
                
        return scores_by_index
        
    except Exception as e:
        print(f"解析批量评分结果时发生错误: {e}")
        return {}

def get_default_scores():
    """返回默认的评分字典 (使用新的键名)"""
    return {
        '术语表一致性': 0,
        'tu/vous关系': 0,
        '语言分级': 0,
        '计量单位': 0,
        '翻译完整度': 0,
        '开闭口匹配': 0,
        '音节数匹配': 0
    }

# --- 主执行部分 ---
if __name__ == "__main__":
    # --- 示例 ---
    example_source = "你别逼我动手。"
    example_translation = "Don't force me to act."
    # example_translation = "You don't make me move." # 可以换用这个测试低分情况

    print(f"正在对以下翻译进行评分:")
    print(f"  原文: {example_source}")
    print(f"  译文: {example_translation}")
    print("-" * 30)

    # 调用评分函数
    final_score = rate_translation(
        example_source,
        example_translation,
        MODEL_NAME
        # 不指定API密钥，使用轮询机制
    )

    print(f"评分结果: {final_score}")

    print("-" * 30)
    # --- 批量评分示例 ---
    example_pairs = [
        (0, "你别逼我动手。", "Don't force me to act."),
        (1, "我想上厕所", "I want to go to the toilet"),
        (2, "这事儿没那么简单。", "It's not that simple.")
    ]
    
    print(f"正在对 {len(example_pairs)} 个翻译配对进行批量评分...")
    batch_scores = batch_rate_translations(
        example_pairs,
        MODEL_NAME
        # 不指定API密钥，使用轮询机制
    )
    
    for index, scores in batch_scores.items():
        print(f"索引 {index} 的评分结果: {scores}") 