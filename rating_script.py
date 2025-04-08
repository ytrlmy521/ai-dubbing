# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd # translate_text 函数依赖 pandas.isna
import time # 虽然评分本身可能不需要，但 translate_text 里有，保持一致
import os # 虽然评分本身可能不需要，但 translate_text 里有，保持一致

# --- API 配置 ---
API_URL = "https://cloud.infini-ai.com/maas/v1/chat/completions"
API_KEY = "Bearer sk-daz7idir52x7kash" # 请确保这是有效的Key
MODEL_NAME = "deepseek-v3" # 或者其他适合评分任务的模型

# --- 评分标准 Prompt 模板 ---
RATING_PROMPT_TEMPLATE = """
你是一个专业的影视剧译制翻译质量评估员。请根据以下评分标准，对提供的中文原文和英文译文进行评估。


注意：评分标准（每个维度分值都不一样）:
     准确性 (Accuracy) - 30分
     流畅度 (Fluency) - 25分
     语境适应性 (Contextual Appropriateness) - 20分
     对口型匹配度 (Lip-Sync Compatibility) - 15分
     文化适用性 (Localization) - 10分

1.  准确性 (Accuracy) - 30分: 是否准确传达原文含义，无遗漏或曲解。
    - 27-30 分: 翻译完全准确，无任何错误。
    - 20-26 分: 翻译基本准确，存在轻微偏差但不影响理解。
    - 10-19 分: 翻译有明显错误，但核心意思尚存。
    - 0-9 分: 翻译严重失真，原文意思丧失。
        - 示例: 
        - 原文: "你别逼我动手。" 
        - 翻译: "Don’t force me to act." (30 分)
        - 翻译: "You don’t make me move."  (10 分)
2.  流畅度 (Fluency) - 25分: 是否符合英语母语者表达习惯，语法正确流畅。
      - 22-25 分: 翻译自然流畅，如英语母语者表达。
      - 15-21 分: 翻译较自然，但有轻微不地道之处。
      - 8-14 分: 翻译可理解，但明显非母语风格。
      - 0-7 分: 翻译生硬，语法或表达严重不当。
        - 示例: 
        - 原文: "这事儿没那么简单。" 
        - 翻译: "It’s not that simple." (25 分)
        - 翻译: "This matter not so simple." (5 分)
3.  语境适应性 (Contextual Appropriateness) - 20分: 是否符合影视剧场景、角色语气、情绪、性格和剧情。
      - 18-20 分: 翻译完美契合语境，语气和角色一致。
      - 12-17 分: 翻译基本符合语境，但语气稍有偏差。
      - 6-11 分: 翻译与语境脱节，角色性格体现不足。
      - 0-5 分: 翻译完全无视语境，语气或含义不符。
        - 示例: 
        - 场景: 武侠片中高手对决 
        - 原文: "来吧，决一死战。"
        - 翻译: "Come on, fight to the death." (20 分)
        - 翻译: "Let’s have a meeting." (0 分)
4.  对口型匹配度 (Lip-Sync Compatibility) - 15分: 英文单词数、音节数和节奏是否与中文口型接近（考虑语流节奏）。
      - 13-15 分: 翻译音节和节奏高度匹配，配音几乎无缝。
      - 9-12 分: 翻译基本匹配，需轻微调整口型。
      - 5-8 分: 翻译勉强可用，但节奏或音节明显不符。
      - 0-4 分: 翻译完全无法对口型，音节数或节奏严重偏离。
        - 示例: 
        - 原文: "我不会让你走。" (6 个音节) 
        - 翻译: "I won’t let you go."  (6 个音节，15 分)
        - 翻译: "I will not allow you to leave." (9 个音节，5 分)
5.  文化适用性 (Localization) - 10分: 是否适应目标语英语观众文化背景，避免直译障碍。
      - 9-10 分: 翻译充分本地化，符合英语文化习惯。
      - 6-8 分: 翻译基本适配，但有些细节未优化。
      - 3-5 分: 翻译未完全本地化，可能引发轻微误解。
      - 0-2 分: 翻译忽视文化差异，显得突兀或费解。
       - 示例: 
        - 原文: "晒黑了不好看。" 
        - 翻译: "Too much sun will hurt your skin." (10 分)
        - 翻译: "Dark skin isn’t attractive." (0 分)

评估以下内容：
中文原文: "{source_text}"
英文译文: "{translation_text}"

请根据上述标准进行评分，并按照以下格式返回评分结果：
accuracy:XX,fluency:XX,contextual:XX,lipsync:XX,localization:XX

例如：accuracy:25,fluency:20,contextual:15,lipsync:10,localization:5

注意：
1. 所有分值必须是0-30之间的整数
2. 严格按照上述格式返回，不要包含任何其他文字
3. 使用英文逗号分隔各个评分
准确性 (Accuracy) - 30分
流畅度 (Fluency) - 25分
语境适应性 (Contextual Appropriateness) - 20分
对口型匹配度 (Lip-Sync Compatibility) - 15分
文化适用性 (Localization) - 10分

"""

# --- 从笔记中复制的 translate_text 函数 ---
# 注意：此函数现在用于发送评分请求，其 'text' 参数将是包含评分说明和待评分内容的完整prompt
def translate_text(prompt_content, model_name, api_key, api_url):
    """
    调用大模型API执行任务（翻译或评分）。

    参数:
        prompt_content: 发送给大模型的完整提示内容。
        model_name: 使用的模型名称。
        api_key: API密钥。
        api_url: API接口地址。

    返回:
        大模型的响应内容。
    """
    if not prompt_content: # 检查输入prompt是否为空
        return "ERROR: Prompt content is empty"

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
      "temperature": 0.1, # 评分任务通常需要更确定的输出，降低温度
    })

    try:
        response = requests.post(api_url, headers=headers, data=payload, timeout=90)
        response.raise_for_status()

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
def rate_translation(source_text, translation_text, model_name, api_key, api_url, rating_prompt_template):
    """
    调用大模型对翻译质量进行评分。

    参数:
        source_text: 中文原文。
        translation_text: 英文译文。
        model_name: 使用的模型名称。
        api_key: API密钥。
        api_url: API接口地址。
        rating_prompt_template: 包含评分标准的提示词模板。

    返回:
        包含五个维度评分的字典。
    """
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
        MODEL_NAME,
        API_KEY,
        API_URL,
        RATING_PROMPT_TEMPLATE
    )

    print(f"评分结果: {final_score}")

    print("-" * 30)
    # --- 另一个示例 ---
    example_source_2 = "我想上厕所"
    example_translation_2 = "I want to go to the toilet"
    print(f"正在对以下翻译进行评分:")
    print(f"  原文: {example_source_2}")
    print(f"  译文: {example_translation_2}")
    print("-" * 30)
    final_score_2 = rate_translation(
        example_source_2,
        example_translation_2,
        MODEL_NAME,
        API_KEY,
        API_URL,
        RATING_PROMPT_TEMPLATE
    )
    print(f"评分结果: {final_score_2}") 