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

评分标准（总分100分）:
1.  准确性 (Accuracy) - 30 分: 是否准确传达原文含义，无遗漏或曲解。
    - 27-30: 完全准确
    - 20-26: 基本准确，轻微偏差
    - 10-19: 明显错误，核心意思尚存
    - 0-9: 严重失真
2.  流畅度 (Fluency) - 25 分: 是否符合英语母语者表达习惯，语法正确流畅。
    - 22-25: 自然流畅
    - 15-21: 较自然，轻微不地道
    - 8-14: 可理解，非母语风格
    - 0-7: 生硬，语法/表达严重不当
3.  语境适应性 (Contextual Appropriateness) - 20 分: 是否符合影视剧场景、角色语气、情绪、性格和剧情。
    - 18-20: 完美契合语境
    - 12-17: 基本符合，语气稍有偏差
    - 6-11: 与语境脱节，角色体现不足
    - 0-5: 完全无视语境
4.  对口型匹配度 (Lip-Sync Compatibility) - 15 分: 英文单词数、音节数和节奏是否与中文口型接近（考虑语流节奏）。
    - 13-15: 高度匹配
    - 9-12: 基本匹配，需轻微调整
    - 5-8: 勉强可用，明显不符
    - 0-4: 完全无法对口型
5.  文化适用性 (Localization) - 10 分: 是否适应目标语英语观众文化背景，避免直译障碍。
    - 9-10: 充分本地化
    - 6-8: 基本适配，细节未优化
    - 3-5: 未完全本地化，可能误解
    - 0-2: 忽视文化差异

评估以下内容：
中文原文: "{source_text}"
英文译文: "{translation_text}"

请根据上述标准进行综合评分，并**直接返回最终的总分数值，格式为 'XX分'**，不要包含任何评分细则、解释或其他文字。例如，如果评分是90分，就只返回 "90分"。
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
        大模型的响应内容（预期是翻译结果或评分分数）。
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
          "content": prompt_content # 这里是完整的评分prompt
        }
      ],
      "stream": False,
      "temperature": 0.1, # 评分任务通常需要更确定的输出，降低温度
    })

    try:
        response = requests.post(api_url, headers=headers, data=payload, timeout=90) # 增加超时时间
        response.raise_for_status()

        data = response.json()
        # 提取模型返回的内容
        result = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        result = result.strip()

        # 简单验证是否符合 "XX分" 格式 (可选，但有助于调试)
        # import re
        # if not re.match(r"^\d+分$", result):
        #    print(f"Warning: LLM response format might be incorrect: {result}")
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
        LLM返回的评分结果 (预期格式: "XX分")。
    """
    # 构建完整的评分prompt
    rating_prompt = rating_prompt_template.format(
        source_text=source_text,
        translation_text=translation_text
    )

    # 调用 translate_text 函数（实际执行的是评分任务）
    score = translate_text(rating_prompt, model_name, api_key, api_url)

    return score

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