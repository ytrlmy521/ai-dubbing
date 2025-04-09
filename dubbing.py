# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import time
import os
import re # 导入正则表达式库用于解析
# 移除评分相关的导入
# from rating_script import rate_translation, RATING_PROMPT_TEMPLATE
from constant import *

# --- 新增：从 rating_script 导入评分相关组件和配置 ---
from rating_script import rate_translation, RATING_PROMPT_TEMPLATE
# 显式导入评分API配置并重命名以区分
from rating_script import API_URL as RATING_API_URL
from rating_script import API_KEY as RATING_API_KEY
from rating_script import MODEL_NAME as RATING_MODEL_NAME

# --- 配置部分 ---
# 基础目录路径
# BASE_DIR = r"C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本\\电视剧"
# out_put_BASE_DIR = r"C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本"

BASE_DIR = r"E:\\Apple\\电视剧"
out_put_BASE_DIR = r"E:\\Apple"

# 翻译 API 接口地址
TRANSLATE_API_URL = "https://api.deepseek.com/v1/chat/completions"
# 翻译 API 密钥（Bearer Token格式）
TRANSLATE_API_KEY = "Bearer sk-9e2f9bc9546d4d0ca0631cca3ffe819e"
# 翻译使用的模型名称
TRANSLATE_MODEL_NAME = "deepseek-chat"

# API_URL = "https://cloud.infini-ai.com/maas/v1/chat/completions"
# # API密钥（Bearer Token格式）
# API_KEY = "Bearer sk-daz7idir52x7kash"
# # 使用的模型名称
# MODEL_NAME = "deepseek-v3"

# --- 修改：批量翻译提示词模板 (带索引) ---
BATCH_TRANSLATION_PROMPT_TEMPLATE = """
You are an expert translator specializing in translating Chinese scripts (dialogue, narration) for TV shows and movies into natural-sounding American English suitable for dubbing.
Context: This script is from the series/movie "{series_name}". Please maintain the tone, style, and character voices consistent with this context. {specific_instructions}

Translate the following Chinese lines into English. Each line below starts with its original index number followed by a colon and a space (e.g., "123: text").
**Crucially, your response MUST preserve this index prefix for each translated line.**
Return *only* the translated English lines, each prefixed with its corresponding original index, colon, and space (e.g., "123: translation"), each on a new line. Maintain the exact same order.
Do not add any extra text, explanations, greetings, or numbering other than the required index prefix.

Chinese Lines (with index prefix):
{combined_texts}
"""

# --- 翻译函数 (现在明确使用翻译配置) ---
def translate_text(text, model_name, api_key, api_url, prompt):
    """
    调用大模型API进行文本翻译
    """
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': api_key # 使用传入的 API Key
    }
    payload = json.dumps({
        "model": model_name, # 使用传入的模型名称
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "temperature": 0.7, 
        "max_tokens": 8192 
    })
    try:
        response = requests.post(api_url, headers=headers, data=payload, timeout=300)
        response.raise_for_status()
        data = response.json()
        translation = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        translation = translation.strip()
        print(f"翻译 API 返回原始内容 (前200字符): {translation[:200]}...")
        return translation
    except requests.exceptions.RequestException as e:
        print(f"翻译 API 请求错误: {e}")
        if isinstance(e, requests.exceptions.Timeout):
            return "ERROR: 请求超时"
        return f"ERROR: 请求失败 ({e})"
    except json.JSONDecodeError:
        print(f"翻译 JSON 解析错误: {response.text}")
        return "ERROR: 无效的JSON响应"
    except KeyError as e:
        print(f"翻译响应结构错误: {e}")
        return f"ERROR: 意外的响应结构 ({e})"
    except Exception as e:
        print(f"翻译过程中发生意外错误: {e}")
        return f"ERROR: 意外错误 ({e})"

# --- 获取剧集上下文信息 (不变) ---
def get_prompt_context_by_path(file_path):
    """
    根据文件路径获取剧集名称和对应的原始提示词模板 (作为 specific_instructions)
    返回: 一个元组 (series_name, prompt_template_as_instruction)
    """
    path_lower = file_path.lower()
    if "何以笙箫默" in path_lower: return "何以笙箫默", Sheng_Xiao_Mo_PROMPT_TEMPLATE
    elif "锦衣夜行" in path_lower: return "锦衣夜行", Jin_Yi_Ye_Xing_PROMPT_TEMPLATE
    elif "好事成双" in path_lower: return "好事成双", Good_Things_PROMPT_TEMPLATE
    elif "亲爱的热爱的" in path_lower: return "亲爱的热爱的", Qing_Ai_De_PROMPT_TEMPLATE
    elif "宇宙护卫队" in path_lower: return "宇宙护卫队", YuZhouHuWeiDui_PROMPT_TEMPLATE
    elif "神隐" in path_lower: return "神隐", ShenYing_PROMPT_TEMPLATE
    elif "青云志" in path_lower: return "青云志", QingYunZhi_PROMPT_TEMPLATE
    elif "与君初相识" in path_lower: return "与君初相识", YuJunChuXiangShi_PROMPT_TEMPLATE
    elif "西游降魔篇" in path_lower: return "西游降魔篇", XiYouXiangMoPian_PROMPT_TEMPLATE
    elif "雪王" in path_lower: return "雪王", XueWang_PROMPT_TEMPLATE
    elif "妖神记" in path_lower: return "妖神记", YaoShenJi_PROMPT_TEMPLATE
    elif "开心超人之英雄的心" in path_lower: return "开心超人之英雄的心", KaiXinChaoRen_PROMPT_TEMPLATE
    elif "开心超人之时空营救" in path_lower: return "开心超人之时空营救", KaiXinChaoRenShiKongYingJiu_PROMPT_TEMPLATE
    elif "喜羊羊虎虎生威" in path_lower: return "喜羊羊虎虎生威", XiYangYang_PROMPT_TEMPLATE
    elif "以爱为营" in path_lower: return "以爱为营", YiAiWeiYing_PROMPT_TEMPLATE
    elif "大头儿子小头爸爸1" in path_lower: return "大头儿子小头爸爸1", DaTouErZi_PROMPT_TEMPLATE
    elif "大头儿子小头爸爸2" in path_lower: return "大头儿子小头爸爸2", DaTouErZi2_PROMPT_TEMPLATE
    elif "鹿鼎记" in path_lower: return "鹿鼎记", LuDingJi_PROMPT_TEMPLATE
    elif "宁安如梦" in path_lower: return "宁安如梦", NingAnRuMeng_PROMPT_TEMPLATE
    else: return "Unknown Series", Good_Things_PROMPT_TEMPLATE

# --- 重构：处理单个文件（翻译 + 评分）---
def process_file(file_path):
    """
    处理单个CSV或XLSX文件，进行批量翻译，然后逐行评分，并保存结果
    """
    print(f"\n开始处理文件: {file_path}")
    print(f"使用翻译模型: {TRANSLATE_MODEL_NAME} @ {TRANSLATE_API_URL}")
    print(f"使用评分模型: {RATING_MODEL_NAME} @ {RATING_API_URL}")

    try:
        # --- 文件读取 --- 
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        if file_extension == '.csv':
            try: df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError: df = pd.read_csv(file_path, encoding='gbk')
        elif file_extension in ['.xlsx', '.xls']: df = pd.read_excel(file_path)
        else: print(f"错误: 不支持的文件类型 {file_extension}"); return

        # --- 列检查 --- 
        required_cols_strict = ['speaker', 'start_time', 'end_time', 'transcription']
        if not all(col in df.columns for col in required_cols_strict):
            print(f"错误: 文件缺少必需列: {required_cols_strict}"); return
        if 'translation' not in df.columns: df['translation'] = ''
        df['target-translation'] = '' # 初始化翻译列

        # --- 批量翻译 --- 
        series_name, specific_instructions = get_prompt_context_by_path(file_path)
        texts_to_translate_with_index = []
        original_indices = []
        for index, row in df.iterrows():
            chinese_text = str(row['transcription']) if pd.notna(row['transcription']) else ''
            chinese_text = chinese_text.rstrip(',').strip()
            if not chinese_text: chinese_text = "[无需翻译]"
            if chinese_text and chinese_text != '1' and chinese_text != "[无需翻译]":
                texts_to_translate_with_index.append(f"{index}: {chinese_text}")
                original_indices.append(index)
        
        num_to_translate = len(texts_to_translate_with_index)
        print(f"共找到 {num_to_translate} 行有效文本需要翻译")

        if num_to_translate > 0:
            combined_texts = "\n".join(texts_to_translate_with_index)
            full_prompt = BATCH_TRANSLATION_PROMPT_TEMPLATE.format(
                series_name=series_name,
                specific_instructions=specific_instructions,
                combined_texts=combined_texts
            )
            print(f"准备调用翻译 API 翻译 {num_to_translate} 行文本...")
            # print(f"使用的提示词 (部分): {full_prompt}[:600]...") # 调试时可以取消注释

            translation_result = translate_text(
                "", TRANSLATE_MODEL_NAME, TRANSLATE_API_KEY, TRANSLATE_API_URL, full_prompt
            )
            
            print(f"翻译 API 原始返回 (前500字符): {translation_result[:500]}...")
            
            # 基于索引处理翻译结果
            if translation_result and not translation_result.startswith("ERROR"):
                translated_lines = translation_result.strip().split('\n')
                processed_indices = set()
                parse_errors = 0
                line_pattern = re.compile(r"^(\d+):\s?(.*)$")
                for line in translated_lines:
                    line = line.strip(); 
                    if not line: continue
                    match = line_pattern.match(line)
                    if match:
                        try:
                            parsed_index = int(match.group(1))
                            parsed_translation = match.group(2).strip()
                            if parsed_index in original_indices:
                                df.loc[parsed_index, 'target-translation'] = parsed_translation
                                processed_indices.add(parsed_index)
                            else: parse_errors += 1 # 记录未请求的索引错误
                        except ValueError: parse_errors += 1 # 记录索引转换错误
                    else: parse_errors += 1 # 记录格式不匹配错误
                print(f"翻译结果映射完成。共成功映射 {len(processed_indices)} 行。解析错误/警告数: {parse_errors}")
                missing_indices = set(original_indices) - processed_indices
                if missing_indices:
                    print(f"警告: 以下请求的翻译缺失或无法解析: {sorted(list(missing_indices))}")
                    for index in missing_indices:
                        df.loc[index, 'target-translation'] = "ERROR: Translation missing or unparsable"
            else:
                print(f"翻译API调用失败: {translation_result}")
                for index in original_indices:
                    df.loc[index, 'target-translation'] = f"ERROR: API call failed ({translation_result})"

        # --- 逐行评分 --- 
        print("\n开始逐行调用评分 API...")
        accuracy_scores = []
        fluency_scores = []
        contextual_scores = []
        lipsync_scores = []
        localization_scores = []
        total_rows = len(df)
        rated_count = 0

        for index, row in df.iterrows():
            chinese_text = str(row['transcription']) if pd.notna(row['transcription']) else ''
            chinese_text = chinese_text.rstrip(',').strip()
            english_translation = str(row['target-translation']) if pd.notna(row['target-translation']) else ''

            # 检查原文和译文是否有效，译文不能是错误标记
            should_rate = (chinese_text and chinese_text != '1' and chinese_text != "[无需翻译]" and 
                           english_translation and not english_translation.startswith("ERROR"))

            if should_rate:
                print(f"  正在评分第 {index + 1}/{total_rows} 行: 原文='{chinese_text[:30]}...', 译文='{english_translation[:30]}...'", end='')
                # 调用评分函数 (使用 rating_script 的配置)
                scores = rate_translation(
                    chinese_text,
                    english_translation,
                    RATING_MODEL_NAME, # 使用评分模型
                    RATING_API_KEY,    # 使用评分 API Key
                    RATING_API_URL,    # 使用评分 API URL
                    RATING_PROMPT_TEMPLATE
                )
                print(f" -> 评分: {scores}")
                accuracy_scores.append(scores.get('accuracy', 0))
                fluency_scores.append(scores.get('fluency', 0))
                contextual_scores.append(scores.get('contextual', 0))
                lipsync_scores.append(scores.get('lipsync', 0))
                localization_scores.append(scores.get('localization', 0))
                rated_count += 1
                time.sleep(1) # 添加1秒延时，避免过于频繁请求评分 API
            else:
                # 对于无效数据或翻译失败的行，填充0分
                if not should_rate:
                     print(f"  跳过评分第 {index + 1}/{total_rows} 行 (无效原文/译文或翻译错误)")
                accuracy_scores.append(0)
                fluency_scores.append(0)
                contextual_scores.append(0)
                lipsync_scores.append(0)
                localization_scores.append(0)
        
        print(f"\n评分完成。共对 {rated_count} 行进行了有效评分。")

        # --- 添加评分列到 DataFrame --- 
        if len(accuracy_scores) == len(df): # 安全检查
            df['accuracy'] = accuracy_scores
            df['fluency'] = fluency_scores
            df['contextual'] = contextual_scores
            df['lipsync'] = lipsync_scores
            df['localization'] = localization_scores
        else:
            print(f"错误: 评分结果数量 ({len(accuracy_scores)}) 与 DataFrame 行数 ({len(df)}) 不匹配! 将不添加评分列。")
            # 可以选择填充0或者抛出错误
            df['accuracy'] = 0
            df['fluency'] = 0
            df['contextual'] = 0
            df['lipsync'] = 0
            df['localization'] = 0

        # --- 文件保存 --- 
        # 更新最终列列表以包含评分
        final_columns = [
            'speaker', 'start_time', 'end_time', 'transcription', 
            'translation', # 保留原始翻译列（如果存在）
            'target-translation', # 新的翻译列
            'accuracy', 'fluency', 'contextual', 'lipsync', 'localization' # 新的评分列
        ]
        # 确保所有选择的列都实际存在于DataFrame中
        final_columns = [col for col in final_columns if col in df.columns]
        df_output = df[final_columns]

        base, _ = os.path.splitext(file_path)
        rel_path = os.path.relpath(base, BASE_DIR)
        output_dir = os.path.join(out_put_BASE_DIR, 'translated_rated', os.path.dirname(rel_path))
        os.makedirs(output_dir, exist_ok=True)
        # 文件名后缀保持不变 (虽然评分了，但为了兼容之前的逻辑)
        output_file_path = os.path.join(output_dir, f"{os.path.basename(base)}_translated_rated.csv")
        
        df_output.to_csv(output_file_path, index=False, encoding='utf-8-sig')

        print(f"\n翻译与评分处理完成！")
        print(f"结果已保存至: {output_file_path}")

    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
    except pd.errors.EmptyDataError:
        print(f"错误: 文件为空或格式不正确 {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生意外错误: {e}")
        import traceback
        traceback.print_exc()

# --- 查找并处理文件 (不变) ---
def find_and_process_files(base_dir):
    processed_files = 0
    skipped_files = 0
    error_files = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(('.csv', '.xlsx', '.xls')):
                file_path = os.path.join(root, file)
                try:
                    process_file(file_path)
                    processed_files += 1
                except Exception as e:
                    print(f"处理文件 {file_path} 时捕获到顶层错误: {e}")
                    error_files += 1
            else: skipped_files += 1
    print(f"\n--- 文件处理统计 ---")
    print(f"成功处理文件数: {processed_files}")
    print(f"处理失败文件数: {error_files}")
    print(f"跳过非目标文件数: {skipped_files}")

# --- 主程序入口 (不变) ---
if __name__ == "__main__":
    if not os.path.exists(BASE_DIR): print(f"错误: 找不到目录 {BASE_DIR}"); exit()
    if not os.path.exists(out_put_BASE_DIR):
        print(f"输出目录 {out_put_BASE_DIR} 不存在，将尝试创建。")
        try:
            os.makedirs(out_put_BASE_DIR, exist_ok=True)
            os.makedirs(os.path.join(out_put_BASE_DIR, 'translated_rated'), exist_ok=True)
        except Exception as e: print(f"错误: 创建输出目录失败: {e}"); exit()
    print(f"开始在目录中查找并处理文件: {BASE_DIR}")
    find_and_process_files(BASE_DIR)
    print("\n所有文件翻译与评分处理任务已尝试完成！")
