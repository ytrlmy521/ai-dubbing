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
API_URL = "https://cloud.infini-ai.com/maas/v1/chat/completions"
# 多个API密钥配置
API_KEYS = [
    "Bearer sk-daz7idir52x7kash",  # 原始密钥作为第一个
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

MODEL_NAME = "deepseek-v3" # 或者其他适合评分任务的模型

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
你是一个专业的影视剧译制翻译质量评估员，对翻译质量要求非常严格。请根据以下评分标准，对提供的一批中文原文和英文译文配对进行认真评估。

重要说明：每个评分维度都有明确的标准，请严格按照标准评分，不要无故给满分！即使翻译看起来不错，也请仔细分析各个维度可能存在的问题。好的翻译可能得到较高分数，但极少有完美的翻译能在所有维度都得满分。你必须对不同的翻译给出不同的评分！

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

2.  流畅度 (Fluency) - 25分: 是否符合英语母语者表达习惯，语法正确流畅。
      - 22-25 分: 翻译自然流畅，如英语母语者表达。仅当表达非常地道，完全符合英语习惯时才给满分。
      - 15-21 分: 翻译较自然，但有轻微不地道之处。这是大多数好翻译的正常分数。
      - 8-14 分: 翻译可理解，但明显非母语风格。
      - 0-7 分: 翻译生硬，语法或表达严重不当。

3.  语境适应性 (Contextual Appropriateness) - 20分: 是否符合影视剧场景、角色语气、情绪、性格和剧情。
      - 18-20 分: 翻译完美契合语境，语气和角色一致。需要译文特别符合场景和角色特点才给满分。
      - 12-17 分: 翻译基本符合语境，但语气稍有偏差。这是大多数好翻译的常见得分。
      - 6-11 分: 翻译与语境脱节，角色性格体现不足。
      - 0-5 分: 翻译完全无视语境，语气或含义不符。

4.  对口型匹配度 (Lip-Sync Compatibility) - 15分: 英文单词数、音节数和节奏是否与中文口型接近（考虑语流节奏）。
      - 13-15 分: 翻译音节和节奏高度匹配，配音几乎无缝。需要音节数和重音位置都非常匹配才给满分。
      - 9-12 分: 翻译基本匹配，需轻微调整口型。这是好翻译的常见分数。
      - 5-8 分: 翻译勉强可用，但节奏或音节明显不符。
      - 0-4 分: 翻译完全无法对口型，音节数或节奏严重偏离。

5.  文化适用性 (Localization) - 10分: 是否适应目标语英语观众文化背景，避免直译障碍。
      - 9-10 分: 翻译充分本地化，符合英语文化习惯。只有真正考虑了文化差异并巧妙本地化的翻译才给满分。
      - 6-8 分: 翻译基本适配，但有些细节未优化。这是大多数好翻译的正常分数。
      - 3-5 分: 翻译未完全本地化，可能引发轻微误解。
      - 0-2 分: 翻译忽视文化差异，显得突兀或费解。

下面是需要评分的翻译内容，每行以索引号开头，格式为"[索引号] 中文原文 ||| 英文译文"：

{combined_texts}

请对每个翻译配对进行严格评分，确保区分不同翻译的质量差异，并按照以下格式返回评分结果：
[索引号] accuracy:XX,fluency:XX,contextual:XX,lipsync:XX,localization:XX

例如：
[123] accuracy:25,fluency:20,contextual:15,lipsync:10,localization:5

请确保:
1. 每个评分结果前必须有原始索引号，格式为 [索引号]，与输入的索引号完全一致
2. 所有分值必须是0-30之间的整数
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
                response = requests.post(api_url, headers=headers, data=payload, timeout=90)
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
                time.sleep(1)  # 稍等一下再重试
        
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
        line_pattern = re.compile(r"^\[(\d+)\]\s*accuracy:(\d+),fluency:(\d+),contextual:(\d+),lipsync:(\d+),localization:(\d+)$")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match = line_pattern.match(line)
            if match:
                try:
                    index = int(match.group(1))
                    accuracy = int(match.group(2))
                    fluency = int(match.group(3))
                    contextual = int(match.group(4))
                    lipsync = int(match.group(5))
                    localization = int(match.group(6))
                    
                    # 验证分值范围
                    if 0 <= accuracy <= 30 and 0 <= fluency <= 25 and 0 <= contextual <= 20 and 0 <= lipsync <= 15 and 0 <= localization <= 10:
                        scores_by_index[index] = {
                            'accuracy': accuracy,
                            'fluency': fluency,
                            'contextual': contextual,
                            'lipsync': lipsync,
                            'localization': localization
                        }
                    else:
                        print(f"警告: 索引 {index} 的分值超出范围: accuracy={accuracy}, fluency={fluency}, contextual={contextual}, lipsync={lipsync}, localization={localization}")
                        scores_by_index[index] = get_default_scores()
                except ValueError:
                    print(f"警告: 索引或分值解析失败: {line}")
            else:
                print(f"警告: 评分结果格式不匹配: {line}")
        
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
    """返回默认的评分字典"""
    return {
        'accuracy': 0,
        'fluency': 0,
        'contextual': 0,
        'lipsync': 0,
        'localization': 0
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