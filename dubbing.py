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

# --- 配置部分 ---
# 基础目录路径
# BASE_DIR = r"C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本\\电视剧"
# out_put_BASE_DIR = r"C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本"

BASE_DIR = r"E:\\Apple\\电视剧"
out_put_BASE_DIR = r"E:\\Apple"


# API接口地址
API_URL = "https://api.deepseek.com/v1/chat/completions"
# API密钥（Bearer Token格式）
API_KEY = "Bearer sk-9e2f9bc9546d4d0ca0631cca3ffe819e"
# 使用的模型名称
MODEL_NAME = "deepseek-chat"

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

# --- 翻译函数 (基本不变) ---
def translate_text(text, model_name, api_key, api_url, prompt):
    """
    调用大模型API进行文本翻译 (现在接收完整的提示词)
    
    参数:
        text: 需要翻译的文本 (在此函数中未使用，因为已包含在prompt中)
        model_name: 使用的模型名称
        api_key: API密钥
        api_url: API接口地址
        prompt: 完整的请求提示词
    
    返回:
        翻译后的文本 (可能包含多行，且应带有索引前缀)
    """
    # 设置请求头
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': api_key
    }

    # 构建请求体 - 使用传入的完整prompt
    payload = json.dumps({
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt # 直接使用构建好的完整提示词
            }
        ],
        "stream": False,
        "temperature": 0.7, # 可以根据需要调整
        "max_tokens": 8192 # 根据模型限制和预期输出长度考虑是否需要设置
    })

    try:
        # 发送API请求，增加超时时间以应对长文本翻译
        response = requests.post(api_url, headers=headers, data=payload, timeout=300) # 增加超时到300秒
        response.raise_for_status()  # 检查响应状态码

        # 解析响应数据
        data = response.json()
        translation = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        translation = translation.strip()  # 清理首尾空白字符

        # 打印部分返回内容用于调试
        print(f"API返回原始内容 (前200字符): {translation[:200]}...")
        return translation

    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {e}")
        # 对于超时错误，可以给出更具体的提示
        if isinstance(e, requests.exceptions.Timeout):
            return "ERROR: 请求超时"
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

# --- 修改：获取剧集上下文信息 (使用 PROMPT_TEMPLATE 而非 INSTRUCTIONS) ---
def get_prompt_context_by_path(file_path):
    """
    根据文件路径获取剧集名称和对应的原始提示词模板 (作为 specific_instructions)
    
    参数:
        file_path: 文件的完整路径
    
    返回:
        一个元组 (series_name, prompt_template_as_instruction)
    """
    path_lower = file_path.lower()
    
    # 返回剧集名称和对应的原始 PROMPT_TEMPLATE 常量
    # 这些 PROMPT_TEMPLATE 常量现在作为 BATCH_TRANSLATION_PROMPT_TEMPLATE 中的 specific_instructions 部分
    if "何以笙箫默" in path_lower:
        print(f"检测到《何以笙箫默》")
        return "何以笙箫默", Sheng_Xiao_Mo_PROMPT_TEMPLATE 
    elif "锦衣夜行" in path_lower:
        print(f"检测到《锦衣夜行》")
        return "锦衣夜行", Jin_Yi_Ye_Xing_PROMPT_TEMPLATE
    elif "好事成双" in path_lower:
        print(f"检测到《好事成双》")
        return "好事成双", Good_Things_PROMPT_TEMPLATE
    elif "亲爱的热爱的" in path_lower:
        print(f"检测到《亲爱的热爱的》")
        return "亲爱的热爱的", Qing_Ai_De_PROMPT_TEMPLATE
    elif "宇宙护卫队" in path_lower:
        print(f"检测到《宇宙护卫队》")
        # 注意：这里之前错误地返回了 YuJunChuXiangShi_PROMPT_TEMPLATE
        return "宇宙护卫队", YuZhouHuWeiDui_PROMPT_TEMPLATE 
    elif "神隐" in path_lower:
        print(f"检测到《神隐》")
        return "神隐", ShenYing_PROMPT_TEMPLATE
    elif "青云志" in path_lower:
        print(f"检测到《青云志》")
        return "青云志", QingYunZhi_PROMPT_TEMPLATE
    elif "与君初相识" in path_lower:
        print(f"检测到《与君初相识》")
        return "与君初相识", YuJunChuXiangShi_PROMPT_TEMPLATE
    elif "西游降魔篇" in path_lower:
        print(f"检测到《西游降魔篇》")
        return "西游降魔篇", XiYouXiangMoPian_PROMPT_TEMPLATE
    elif "雪王" in path_lower:
        print(f"检测到《雪王》")
        return "雪王", XueWang_PROMPT_TEMPLATE
    elif "妖神记" in path_lower:
        print(f"检测到《妖神记》")
        return "妖神记", YaoShenJi_PROMPT_TEMPLATE
    elif "开心超人之英雄的心" in path_lower:
        print(f"检测到《开心超人之英雄的心》")
        return "开心超人之英雄的心", KaiXinChaoRen_PROMPT_TEMPLATE
    elif "开心超人之时空营救" in path_lower:
        print(f"检测到《开心超人之时空营救》")
        return "开心超人之时空营救", KaiXinChaoRenShiKongYingJiu_PROMPT_TEMPLATE
    elif "喜羊羊虎虎生威" in path_lower:
        print(f"检测到《喜羊羊虎虎生威》")
        return "喜羊羊虎虎生威", XiYangYang_PROMPT_TEMPLATE
    elif "以爱为营" in path_lower:
        print(f"检测到《以爱为营》")
        return "以爱为营", YiAiWeiYing_PROMPT_TEMPLATE
    elif "大头儿子小头爸爸1" in path_lower:
        print(f"检测到《大头儿子小头爸爸1》")
        return "大头儿子小头爸爸1", DaTouErZi_PROMPT_TEMPLATE
    elif "大头儿子小头爸爸2" in path_lower:
        print(f"检测到《大头儿子小头爸爸2》")
        return "大头儿子小头爸爸2", DaTouErZi2_PROMPT_TEMPLATE
    elif "鹿鼎记" in path_lower:
        print(f"检测到《鹿鼎记》")
        return "鹿鼎记", LuDingJi_PROMPT_TEMPLATE
    elif "宁安如梦" in path_lower:
        print(f"检测到《宁安如梦》")
        return "宁安如梦", NingAnRuMeng_PROMPT_TEMPLATE 
    else:
        # 默认返回通用名称和《好事成双》的模板
        print(f"未检测到特定剧集，使用默认上下文信息")
        return "Unknown Series", Good_Things_PROMPT_TEMPLATE 

# --- 重构：处理单个文件（CSV 或 XLSX）---
def process_file(file_path):
    """
    处理单个CSV或XLSX文件，进行批量翻译，并使用索引精确映射结果
    
    参数:
        file_path: 文件的完整路径
    """
    print(f"\n开始处理文件: {file_path}")
    print(f"使用模型: {MODEL_NAME}")

    try:
        # 根据文件扩展名读取文件
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension == '.csv':
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                print("UTF-8解码失败，尝试使用GBK编码...")
                df = pd.read_csv(file_path, encoding='gbk')
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            print(f"错误: 不支持的文件类型 {file_extension}，跳过文件: {file_path}")
            return

        # 检查必要的列
        required_cols_strict = ['speaker', 'start_time', 'end_time', 'transcription']
        if not all(col in df.columns for col in required_cols_strict):
            print(f"错误: 文件必须至少包含以下列: {required_cols_strict}，找到的列: {df.columns.tolist()}")
            return
        if 'translation' not in df.columns:
            df['translation'] = '' # 如果原始文件没有，添加空列

        # 获取剧集上下文信息 (现在 specific_instructions 是原始的提示模板)
        series_name, specific_instructions = get_prompt_context_by_path(file_path)

        # --- 修改：收集带索引的待翻译文本 ---
        texts_to_translate_with_index = []
        original_indices = [] # 仍然需要这个列表来跟踪哪些行被请求了翻译
        total_rows = len(df)
        print(f"共发现 {total_rows} 行需要检查")

        for index, row in df.iterrows():
            chinese_text = str(row['transcription']) if pd.notna(row['transcription']) else ''
            chinese_text = chinese_text.rstrip(',').strip()
            
            # 处理空文本情况 (给一个特殊标记让模型知道不用翻译)
            if not chinese_text:
                chinese_text = "[无需翻译]" # 使用特殊标记而非"不用翻译"
            
            # 检查是否需要翻译 (不为空, 不是 '1', 不是特殊标记)
            if chinese_text and chinese_text != '1' and chinese_text != "[无需翻译]":
                # 添加带索引前缀的文本
                texts_to_translate_with_index.append(f"{index}: {chinese_text}")
                original_indices.append(index)
            # elif chinese_text == "[无需翻译]":
            #     # 如果原文就是无需翻译标记，则也记录索引，以便后续填充空字符串
            #     original_indices.append(index)

        num_to_translate = len(texts_to_translate_with_index)
        print(f"共找到 {num_to_translate} 行有效文本需要翻译 (索引: {original_indices[:10]}...)")

        # 初始化翻译结果列
        df['target-translation'] = ''

        if num_to_translate == 0:
            print("没有需要翻译的文本。")
        else:
            # 构建批量翻译的提示词 (使用带索引的文本)
            combined_texts = "\n".join(texts_to_translate_with_index)
            full_prompt = BATCH_TRANSLATION_PROMPT_TEMPLATE.format(
                series_name=series_name,
                specific_instructions=specific_instructions, # 这里是原始的模板
                combined_texts=combined_texts
            )
            
            print(f"准备调用API翻译 {num_to_translate} 行文本...")
            print(f"使用的提示词 (部分): {full_prompt}[:600]...") # 调试时可以取消注释

            # 调用翻译函数
            translation_result = translate_text(
                "", 
                MODEL_NAME,
                API_KEY,
                API_URL,
                full_prompt
            )

            # time.sleep(5) # 如果需要，可以取消注释
            print(f"翻译API原始返回 (前500字符): {translation_result[:500]}...")

            # --- 修改：基于索引处理翻译结果 ---
            if translation_result and not translation_result.startswith("ERROR"):
                translated_lines = translation_result.strip().split('\n')
                print(f"API成功返回了 {len(translated_lines)} 行响应。开始基于索引映射...")
                
                processed_indices = set()
                parse_errors = 0
                
                # 使用正则表达式提取索引和翻译
                # 匹配模式：行首的数字 + 冒号 + 可选空格 + 任意字符直到行尾
                line_pattern = re.compile(r"^(\d+):\s?(.*)$")

                for line in translated_lines:
                    line = line.strip()
                    if not line:
                        continue # 跳过空行
                    
                    match = line_pattern.match(line)
                    if match:
                        try:
                            # 提取索引和翻译文本
                            parsed_index = int(match.group(1))
                            parsed_translation = match.group(2).strip()
                            
                            # 检查提取的索引是否在我们请求的索引列表中
                            if parsed_index in original_indices:
                                # 如果索引有效，填入DataFrame
                                df.loc[parsed_index, 'target-translation'] = parsed_translation
                                processed_indices.add(parsed_index) # 标记此索引已处理
                                # print(f"  成功映射索引 {parsed_index}") # 调试时可取消注释
                            else:
                                print(f"  警告: API返回了未请求的索引 {parsed_index}，内容: '{parsed_translation}'")
                                parse_errors += 1
                        except ValueError:
                            print(f"  错误: 无法将提取的索引 '{match.group(1)}' 转换为整数，行: '{line}'")
                            parse_errors += 1
                        except Exception as e:
                             print(f"  错误: 处理行 '{line}' 时发生未知错误: {e}")
                             parse_errors += 1
                    else:
                        # 如果行不匹配格式，记录警告
                        print(f"  警告: API返回的行未使用预期格式 (index: text): '{line}'")
                        parse_errors += 1

                print(f"映射完成。共成功映射 {len(processed_indices)} 行。解析错误/警告数: {parse_errors}")

                # 检查是否有请求的索引未被处理 (即API没有返回对应的翻译)
                missing_indices = set(original_indices) - processed_indices
                if missing_indices:
                    print(f"警告: 以下请求的索引在API响应中缺失或无法解析: {sorted(list(missing_indices))}")
                    # 在缺失的行中标记错误
                    for index in missing_indices:
                        df.loc[index, 'target-translation'] = "ERROR: Translation missing or unparsable in API response"
                
            else:
                print(f"翻译API调用失败或返回错误: {translation_result}")
                # 在所有请求翻译的行中标记错误
                error_message = f"ERROR: API call failed ({translation_result})"
                for index in original_indices:
                    df.loc[index, 'target-translation'] = error_message

        # --- 文件保存逻辑 (基本不变) ---
        final_columns = ['speaker', 'start_time', 'end_time', 'transcription']
        if 'translation' in df.columns:
            final_columns.append('translation')
        final_columns.append('target-translation')
        final_columns = [col for col in final_columns if col in df.columns]
        df_output = df[final_columns]

        base, _ = os.path.splitext(file_path)
        rel_path = os.path.relpath(base, BASE_DIR)
        output_dir = os.path.join(out_put_BASE_DIR, 'translated_rated', os.path.dirname(rel_path))
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, f"{os.path.basename(base)}_translated_rated.csv")
        
        df_output.to_csv(output_file_path, index=False, encoding='utf-8-sig')

        print(f"\n处理完成！")
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
    """
    递归查找并处理所有CSV和XLSX文件
    
    参数:
        base_dir: 基础目录路径
    """
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
            else:
                skipped_files += 1

    print(f"\n--- 文件处理统计 ---")
    print(f"成功处理文件数: {processed_files}")
    print(f"处理失败文件数: {error_files}")
    print(f"跳过非目标文件数: {skipped_files}")

# --- 主程序入口 (不变) ---
if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        print(f"错误: 找不到目录 {BASE_DIR}")
        exit()
    
    if not os.path.exists(out_put_BASE_DIR):
        print(f"输出目录 {out_put_BASE_DIR} 不存在，将尝试创建。")
        try:
            os.makedirs(out_put_BASE_DIR, exist_ok=True)
            os.makedirs(os.path.join(out_put_BASE_DIR, 'translated_rated'), exist_ok=True)
        except Exception as e:
            print(f"错误: 创建输出目录 {out_put_BASE_DIR} 失败: {e}")
            exit()

    print(f"开始在目录中查找并处理文件: {BASE_DIR}")
    find_and_process_files(BASE_DIR)
    print("\n所有文件处理任务已尝试完成！")
