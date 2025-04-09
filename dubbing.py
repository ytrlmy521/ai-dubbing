# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import time
import os
from rating_script import rate_translation, RATING_PROMPT_TEMPLATE
from constant import *

# --- 配置部分 ---
# 基础目录路径
BASE_DIR = r"C:\Users\User\Downloads\AI配音中翻英台本 0320\AI配音中翻英台本\电视剧"
out_put_BASE_DIR = r"C:\Users\User\Downloads\AI配音中翻英台本 0320\AI配音中翻英台本"

# BASE_DIR = r"E:\Apple\电视剧"
# out_put_BASE_DIR = r"E:\Apple"


# API接口地址
API_URL = "https://api.deepseek.com/v1/chat/completions"
# API密钥（Bearer Token格式）
API_KEY = "Bearer sk-9e2f9bc9546d4d0ca0631cca3ffe819e"
# 使用的模型名称
MODEL_NAME = "deepseek-chat"

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

def get_prompt_template_by_path(file_path):
    """
    根据文件路径选择合适的翻译提示词模板
    
    参数:
        file_path: 文件的完整路径
    
    返回:
        对应的提示词模板
    """
    # 将路径转换为小写以便不区分大小写进行匹配
    path_lower = file_path.lower()
    
    # 根据路径中的关键词选择对应的提示词模板
    if "何以笙箫默" in path_lower:
        print(f"检测到《何以笙箫默》，使用对应提示词模板")
        return Sheng_Xiao_Mo_PROMPT_TEMPLATE
    elif "锦衣夜行" in path_lower:
        print(f"检测到《锦衣夜行》，使用对应提示词模板")
        return Jin_Yi_Ye_Xing_PROMPT_TEMPLATE
    elif "好事成双" in path_lower:
        print(f"检测到《好事成双》，使用对应提示词模板")
        return Good_Things_PROMPT_TEMPLATE
    elif "亲爱的热爱的" in path_lower:
        print(f"检测到《亲爱的热爱的》，使用对应提示词模板")
        return Qing_Ai_De_PROMPT_TEMPLATE
    elif "宇宙护卫队" in path_lower:
        print(f"检测到《宇宙护卫队》，使用对应提示词模板")
        return YuZhouHuWeiDui_PROMPT_TEMPLATE
    elif "神隐" in path_lower:
        print(f"检测到《神隐》，使用对应提示词模板")
        return ShenYing_PROMPT_TEMPLATE
    elif "青云志" in path_lower:
        print(f"检测到《青云志》，使用对应提示词模板")
        return QingYunZhi_PROMPT_TEMPLATE
    elif "与君初相识" in path_lower:
        print(f"检测到《与君初相识》，使用对应提示词模板")
        return YuJunChuXiangShi_PROMPT_TEMPLATE
    elif "西游降魔篇" in path_lower:
        print(f"检测到《西游降魔篇》，使用对应提示词模板")
        return XiYouXiangMoPian_PROMPT_TEMPLATE
    elif "雪王" in path_lower:
        print(f"检测到《雪王》，使用对应提示词模板")
        return XueWang_PROMPT_TEMPLATE
    elif "妖神记" in path_lower:
        print(f"检测到《妖神记》，使用对应提示词模板")
        return YaoShenJi_PROMPT_TEMPLATE
    elif "开心超人之英雄的心" in path_lower:
        print(f"检测到《开心超人之英雄的心》，使用对应提示词模板")
        return KaiXinChaoRen_PROMPT_TEMPLATE
    elif "开心超人之时空营救" in path_lower:
        print(f"检测到《开心超人之时空营救》，使用对应提示词模板")
        return KaiXinChaoRenShiKongYingJiu_PROMPT_TEMPLATE
    elif "喜羊羊虎虎生威" in path_lower:
        print(f"检测到《喜羊羊虎虎生威》，使用对应提示词模板")
        return XiYangYang_PROMPT_TEMPLATE
    elif "以爱为营" in path_lower:
        print(f"检测到《以爱为营》，使用对应提示词模板")
        return YiAiWeiYing_PROMPT_TEMPLATE
    elif "大头儿子小头爸爸1" in path_lower:
        print(f"检测到《大头儿子小头爸爸1》，使用对应提示词模板")
        return DaTouErZi_PROMPT_TEMPLATE
    elif "大头儿子小头爸爸2" in path_lower:
        print(f"检测到《大头儿子小头爸爸2》，使用对应提示词模板")
        return DaTouErZi2_PROMPT_TEMPLATE 
    elif "鹿鼎记" in path_lower:
        print(f"检测到《鹿鼎记》，使用对应提示词模板")
        return LuDingJi_PROMPT_TEMPLATE
    elif "宁安如梦" in path_lower:
        print(f"检测到《宁安如梦》，使用对应提示词模板")
        return NinAnRuMeng_PROMPT_TEMPLATE
    else:
        # 默认使用《好事成双》的提示词模板
        print(f"未检测到特定剧集，使用默认提示词模板")
        return Good_Things_PROMPT_TEMPLATE


def process_csv_file(csv_path):
    """
    处理单个CSV文件
    
    参数:
        csv_path: CSV文件的完整路径
    """
    print(f"\n开始处理文件: {csv_path}")
    print(f"使用模型: {MODEL_NAME}")

    try:
        # 尝试使用UTF-8编码读取CSV文件
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            print("UTF-8解码失败，尝试使用GBK编码...")
            df = pd.read_csv(csv_path, encoding='gbk')

        # 检查必要的列是否存在
        required_cols = ['speaker', 'start_time', 'end_time', 'transcription']
        if not all(col in df.columns for col in required_cols):
            print(f"错误: CSV文件必须包含以下列: {required_cols}")
            return

        # 根据文件路径选择合适的提示词模板
        prompt_template = get_prompt_template_by_path(csv_path)

        # 初始化翻译结果列表和评分结果列表
        translations = []
        accuracy_scores = []
        fluency_scores = []
        contextual_scores = []
        lip_sync_scores = []
        localization_scores = []
        total_rows = len(df)
        print(f"共发现 {total_rows} 行需要处理")

        # 逐行处理翻译和评分
        for index, row in df.iterrows():
            # 确保chinese_text是字符串类型，然后再调用rstrip方法
            chinese_text = str(row['transcription']).rstrip(',')
            print(chinese_text)
            # 检查transcription是否为空或等于'1'，如果是则跳过翻译
            if pd.isna(row['transcription']) or str(chinese_text).strip() == '' or str(chinese_text).strip() == '1':
                print(f"跳过第 {index + 1} 行: 文本为空")
                translations.append("")  # 添加空字符串作为翻译
                accuracy_scores.append(0)
                fluency_scores.append(0)
                contextual_scores.append(0)
                lip_sync_scores.append(0)
                localization_scores.append(0)
                continue
            print(f"正在处理第 {index + 1}/{total_rows} 行: '{chinese_text}'")

            print(f'使用的提示词模版是：{prompt_template[:50]}...')
            # 调用翻译函数
            english_translation = translate_text(
                chinese_text,
                MODEL_NAME,
                API_KEY,
                API_URL,
                prompt_template
            )
            translations.append(english_translation)

            # 添加延时以避免API限制
            time.sleep(1)

            # 对翻译结果进行评分
            if english_translation and not english_translation.startswith("ERROR"):
                print(f"正在对翻译结果进行评分...")
                scores = rate_translation(
                    chinese_text,
                    english_translation,
                    MODEL_NAME,
                    API_KEY,
                    API_URL,
                    RATING_PROMPT_TEMPLATE
                )
                accuracy_scores.append(scores.get('accuracy', 0))
                fluency_scores.append(scores.get('fluency', 0))
                contextual_scores.append(scores.get('contextual', 0))
                lip_sync_scores.append(scores.get('lipsync', 0))
                localization_scores.append(scores.get('localization', 0))
            else:
                # 如果翻译失败，所有评分都设为0
                accuracy_scores.append(0)
                fluency_scores.append(0)
                contextual_scores.append(0)
                lip_sync_scores.append(0)
                localization_scores.append(0)
            
           

        # 确保列表长度与数据框行数匹配
        if len(translations) != len(df) or len(accuracy_scores) != len(df):
            print(f"错误: 结果数量与数据框行数不匹配")
            return

        # 添加翻译结果列和评分结果列
        df['target-translation'] = translations
        df['accuracy_score'] = accuracy_scores
        df['fluency_score'] = fluency_scores
        df['contextual_score'] = contextual_scores
        df['lip_sync_score'] = lip_sync_scores
        df['localization_score'] = localization_scores

        # 只选择需要的列
        final_columns = [
            'speaker', 'start_time', 'end_time', 'transcription', 
            'translation', 'target-translation', 'accuracy_score', 
            'fluency_score', 'contextual_score', 'lip_sync_score', 
            'localization_score'
        ]
        df = df[final_columns]

        # 构建输出文件路径
        base, ext = os.path.splitext(csv_path)
        # 获取相对于BASE_DIR的路径
        rel_path = os.path.relpath(base, BASE_DIR)
        # 创建新的输出目录路径
        output_dir = os.path.join(out_put_BASE_DIR, 'translated_rated', os.path.dirname(rel_path))
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        # 构建完整的输出文件路径
        output_file_path = os.path.join(output_dir, f"{os.path.basename(base)}_translated_rated{ext}")
        
        # 保存结果到新文件（使用utf-8-sig编码以确保Excel能正确显示中文）
        df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

        print(f"\n翻译和评分完成！")
        print(f"结果已保存至: {output_file_path}")

    except FileNotFoundError:
        print(f"错误: 找不到文件 {csv_path}")
    except pd.errors.EmptyDataError:
        print(f"错误: CSV文件为空 {csv_path}")
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

def find_and_process_csv_files(base_dir):
    """
    递归查找并处理所有CSV文件
    
    参数:
        base_dir: 基础目录路径
    """
    # 遍历基础目录下的所有文件和子目录
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                process_csv_file(csv_path)

if __name__ == "__main__":

    
    # 检查基础目录是否存在
    if not os.path.exists(BASE_DIR):
        print(f"错误: 找不到目录 {BASE_DIR}")
        exit()

    # 开始处理所有CSV文件
    print(f"开始处理目录: {BASE_DIR}")
    find_and_process_csv_files(BASE_DIR)
    print("\n所有文件处理完成！")
