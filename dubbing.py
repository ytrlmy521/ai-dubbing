# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import time
import os
import re # 导入正则表达式库用于解析
import random # 导入random用于随机选择API密钥
from itertools import cycle # 导入cycle用于循环迭代API密钥
# 移除评分相关的导入
# from rating_script import rate_translation, RATING_PROMPT_TEMPLATE
from constant import *

# --- 新增：从 rating_script 导入评分相关组件和配置 ---
from rating_script import rate_translation, RATING_PROMPT_TEMPLATE, batch_rate_translations
# 显式导入评分API配置并重命名以区分
from rating_script import API_URL as RATING_API_URL
from rating_script import API_KEYS as RATING_API_KEYS
from rating_script import MODEL_NAME as RATING_MODEL_NAME
# 导入轮询相关函数
from rating_script import get_next_api_key as get_next_rating_api_key

# --- 配置部分 ---
# 基础目录路径
BASE_DIR = r"C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本\\电视剧"
out_put_BASE_DIR = r"C:\\Users\\User\\Downloads\\AI配音中翻英台本 0320\\AI配音中翻英台本"

# BASE_DIR = r"E:\\Apple\\电视剧"
# out_put_BASE_DIR = r"E:\\Apple"

# API密钥配置文件路径
API_KEYS_CONFIG_FILE = "api_keys.json"

# 默认翻译 API 接口地址
TRANSLATE_API_URL = "https://cloud.infini-ai.com/maas/v1/chat/completions"
# 默认翻译 API 密钥
DEFAULT_TRANSLATE_API_KEYS = [
    "Bearer sk-daz7idir52x7kash",  # 原始密钥作为第一个
]

# 尝试从配置文件加载API密钥
def load_api_keys():
    """从配置文件加载API密钥"""
    global TRANSLATE_API_KEYS, RATING_API_KEYS
    
    try:
        if os.path.exists(API_KEYS_CONFIG_FILE):
            with open(API_KEYS_CONFIG_FILE, 'r', encoding='utf-8') as f:
                keys_config = json.load(f)
                
                # 加载翻译API密钥
                translate_keys = keys_config.get('translate_api_keys', [])
                if translate_keys and isinstance(translate_keys, list) and len(translate_keys) > 0:
                    # 确保每个密钥都有Bearer前缀
                    translate_keys = ["Bearer " + k.replace("Bearer ", "") if not k.startswith("Bearer ") else k for k in translate_keys]
                    TRANSLATE_API_KEYS = translate_keys
                    print(f"已从配置文件加载 {len(TRANSLATE_API_KEYS)} 个翻译API密钥")
                else:
                    TRANSLATE_API_KEYS = DEFAULT_TRANSLATE_API_KEYS
                    print(f"配置文件中未找到有效的翻译API密钥，使用默认密钥")
                
                # 加载评分API密钥 (如果存在)
                rating_keys = keys_config.get('rating_api_keys', [])
                if rating_keys and isinstance(rating_keys, list) and len(rating_keys) > 0:
                    # 确保每个密钥都有Bearer前缀
                    rating_keys = ["Bearer " + k.replace("Bearer ", "") if not k.startswith("Bearer ") else k for k in rating_keys]
                    # 更新rating_script.py中的API_KEYS
                    import rating_script
                    rating_script.API_KEYS = rating_keys
                    # 同时更新本地引用
                    globals()['RATING_API_KEYS'] = rating_keys
                    print(f"已从配置文件加载 {len(rating_keys)} 个评分API密钥")
    except Exception as e:
        print(f"加载API密钥配置文件时出错: {e}")
        TRANSLATE_API_KEYS = DEFAULT_TRANSLATE_API_KEYS
        print("使用默认API密钥配置")

# 创建示例配置文件（如果不存在）
def create_example_config_file():
    """创建示例API密钥配置文件（如果不存在）"""
    if not os.path.exists(API_KEYS_CONFIG_FILE):
        example_config = {
            "translate_api_keys": [
                "sk-daz7idir52x7kash",  # 默认不带Bearer前缀，程序会自动添加
                # 可以添加更多密钥
            ],
            "rating_api_keys": [
                "sk-daz7idir52x7kash",
                # 可以添加更多密钥
            ]
        }
        
        try:
            with open(API_KEYS_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(example_config, f, indent=4)
            print(f"已创建示例API密钥配置文件: {API_KEYS_CONFIG_FILE}")
            print("请编辑此文件添加您的API密钥。")
        except Exception as e:
            print(f"创建示例配置文件时出错: {e}")

# 初始化API密钥配置
create_example_config_file()  # 如果文件不存在，则创建示例配置
load_api_keys()  # 尝试加载配置

# 设置翻译API密钥和当前索引
TRANSLATE_API_KEYS = TRANSLATE_API_KEYS if 'TRANSLATE_API_KEYS' in locals() else DEFAULT_TRANSLATE_API_KEYS
current_translate_api_key_index = 0

# 翻译使用的模型名称
TRANSLATE_MODEL_NAME = "deepseek-v3"

# --- API密钥轮询功能 ---
def get_next_translate_api_key():
    """获取下一个翻译API密钥，实现轮询机制"""
    global current_translate_api_key_index
    
    # 如果只有一个API密钥，则直接返回
    if len(TRANSLATE_API_KEYS) <= 1:
        return TRANSLATE_API_KEYS[0]
    
    # 循环使用下一个API密钥
    current_translate_api_key_index = (current_translate_api_key_index + 1) % len(TRANSLATE_API_KEYS)
    return TRANSLATE_API_KEYS[current_translate_api_key_index]

def get_random_translate_api_key():
    """随机获取一个翻译API密钥"""
    return random.choice(TRANSLATE_API_KEYS)

# --- 修改：批量翻译提示词模板 (带索引) ---
BATCH_TRANSLATION_PROMPT_TEMPLATE = """
You are an expert translator specializing in translating Chinese scripts (dialogue, narration) for TV shows and movies into natural-sounding American English suitable for dubbing.
Context: This script is from the series/movie "{series_name}". Please maintain the tone, style, and character voices consistent with this context. {specific_instructions}

Translate the following Chinese lines into English. Each line below starts with its original index number followed by a colon and a space (e.g., "123: text").
**Crucially, your response MUST preserve this index prefix for each translated line.**
Return *only* the translated English lines, each prefixed with its corresponding original index, colon, and space (e.g., "123: translation"), each on a new line. Maintain the exact same order.
Do not add any extra text, explanations, greetings, or numbering other than the required index prefix.

IMPORTANT: You MUST translate ALL provided lines and keep ALL original index numbers in your response. Verify that each source line's index appears in your response exactly once.

Chinese Lines (with index prefix):
{combined_texts}

Required index numbers that MUST appear in your response: {required_indices}
"""

# --- 翻译函数 (添加轮询逻辑) ---
def translate_text(text, model_name, api_key=None, api_url=None, prompt=None):
    """
    调用大模型API进行文本翻译，支持API密钥轮询
    
    参数:
        text: 要翻译的文本（可以为空，因为prompt中已包含完整内容）
        model_name: 使用的模型名称
        api_key: API密钥，如不指定则自动轮询选择
        api_url: API接口地址，如不指定则使用默认地址
        prompt: 完整的提示词
    """
    # 如果未指定API密钥，则轮询获取下一个
    if api_key is None:
        api_key = get_next_translate_api_key()
        print(f"使用翻译API密钥: {api_key[:15]}... (轮询选择)")
    
    # 如果未指定API地址，则使用默认地址
    if api_url is None:
        api_url = TRANSLATE_API_URL
        
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': api_key # 使用传入的或轮询选择的 API Key
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
        "temperature": 0.5, # 降低温度以获得更确定性的结果
        "max_tokens": 8192 
    })
    try:
        # 增加重试逻辑
        max_retries = min(3, len(TRANSLATE_API_KEYS))  # 最多重试次数，不超过可用API密钥数
        retries = 0
        
        while retries < max_retries:
            try:
                response = requests.post(api_url, headers=headers, data=payload, timeout=300)
                response.raise_for_status()
                break  # 请求成功，跳出重试循环
            except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                retries += 1
                if retries >= max_retries:
                    raise  # 达到最大重试次数，抛出异常
                
                print(f"翻译API请求失败 (第{retries}次): {e}")
                # 切换API密钥再试
                api_key = get_next_translate_api_key()
                headers['Authorization'] = api_key
                print(f"尝试使用新翻译API密钥: {api_key[:15]}...")
                time.sleep(1)  # 稍等一下再重试
        
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

# --- 添加：尝试恢复丢失的翻译索引 ---
def try_recover_missing_translations(translation_result, expected_indices, original_texts):
    """
    尝试从翻译结果中恢复缺失的索引翻译
    
    参数:
        translation_result: 完整的翻译结果文本
        expected_indices: 期望包含的索引列表
        original_texts: 原始待翻译文本列表，格式为 "索引: 文本内容"
    
    返回:
        recovered: 字典，键为成功恢复的索引，值为对应的翻译文本
    """
    recovered = {}
    
    # 创建索引到原始文本的映射
    index_to_original = {}
    for text in original_texts:
        parts = text.split(":", 1)
        if len(parts) == 2:
            try:
                idx = int(parts[0].strip())
                content = parts[1].strip()
                index_to_original[idx] = content
            except ValueError:
                continue
                
    if not expected_indices or not translation_result:
        return recovered
    
    # 先尝试使用标准格式解析（可能带有额外空格、标点等干扰）
    pattern1 = re.compile(r'(?:^|\n)\s*(\d+)\s*[:.：]\s*(.*?)(?=\n\s*\d+\s*[:.：]|\s*$)', re.DOTALL)
    matches = pattern1.findall(translation_result)
    for idx_str, content in matches:
        try:
            idx = int(idx_str)
            if idx in expected_indices and idx not in recovered:
                recovered[idx] = content.strip()
        except ValueError:
            continue
    
    # 尝试查找包含索引的完整行，但格式可能有变化
    pattern2 = re.compile(r'(?:^|\n)\s*(\d+)[^:：\n]*[:.：](.*?)(?=\n|$)', re.MULTILINE)
    matches = pattern2.findall(translation_result)
    for idx_str, content in matches:
        try:
            idx = int(idx_str)
            if idx in expected_indices and idx not in recovered:
                recovered[idx] = content.strip()
        except ValueError:
            continue
    
    # 尝试顺序匹配策略（基于行的位置）
    lines = [line.strip() for line in translation_result.split('\n') if line.strip()]
    ordered_indices = sorted(list(index_to_original.keys()))
    
    # 计算有多少行可能是翻译结果（排除空行、注释行等）
    potential_translation_lines = []
    for line in lines:
        # 排除明显不是翻译的行
        if not line or line.startswith('#') or line.startswith('//') or re.match(r'^[a-zA-Z\s]+:$', line):
            continue
        
        # 检查是否已经是标准格式（索引:翻译）
        if re.match(r'^\d+\s*[:.：]', line):
            continue
            
        potential_translation_lines.append(line)
    
    # 如果潜在翻译行数量与缺失索引数量接近，尝试按顺序匹配
    missing_indices = [idx for idx in expected_indices if idx not in recovered]
    
    if len(potential_translation_lines) > 0 and len(missing_indices) > 0:
        # 按索引的顺序排列
        missing_indices.sort()
        
        # 尝试按顺序匹配缺失的索引和可能的翻译行
        for i, idx in enumerate(missing_indices):
            if i < len(potential_translation_lines):
                content = potential_translation_lines[i]
                if idx not in recovered:
                    recovered[idx] = content.strip()
    
    # 使用内容相似度匹配（针对较短文本）
    missing_indices = [idx for idx in expected_indices if idx not in recovered]
    if missing_indices and len(potential_translation_lines) > 0:
        for idx in missing_indices:
            if idx in index_to_original:
                original = index_to_original[idx]
                # 只对较短的文本使用此策略，避免长文本的误匹配
                if len(original) < 100:  
                    for line in potential_translation_lines:
                        # 如果翻译后的行长度与原文相对接近，可能是对应的翻译
                        if 0.5 <= len(line) / max(1, len(original)) <= 2.0:
                            recovered[idx] = line.strip()
                            potential_translation_lines.remove(line)  # 已匹配的行不再重复使用
                            break
    
    return recovered

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
            # 将文本分批处理，每批次最多30条
            batch_size = 30
            total_batches = (num_to_translate + batch_size - 1) // batch_size  # 向上取整
            
            print(f"将分成 {total_batches} 个批次进行翻译，每批次最多 {batch_size} 条文本")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, num_to_translate)
                current_batch = texts_to_translate_with_index[start_idx:end_idx]
                current_indices = original_indices[start_idx:end_idx]
                
                print(f"\n处理第 {batch_idx + 1}/{total_batches} 批翻译 (共 {len(current_batch)} 条)...")
                
                combined_texts = "\n".join(current_batch)
                full_prompt = BATCH_TRANSLATION_PROMPT_TEMPLATE.format(
                    series_name=series_name,
                    specific_instructions=specific_instructions,
                    combined_texts=combined_texts,
                    required_indices=", ".join(map(str, current_indices))
                )
                
                # 尝试最多3次翻译，直到成功或达到最大尝试次数
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        print(f"批次 {batch_idx + 1}/{total_batches} - 尝试翻译 (第 {attempt + 1}/{max_attempts} 次)...")
                        translation_result = translate_text(
                            "", TRANSLATE_MODEL_NAME, None, None, full_prompt
                        )
                        
                        if translation_result and not translation_result.startswith("ERROR"):
                            # 翻译成功，处理这个批次的结果
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
                                        if parsed_index in current_indices:
                                            df.loc[parsed_index, 'target-translation'] = parsed_translation
                                            processed_indices.add(parsed_index)
                                        else: parse_errors += 1 # 记录未请求的索引错误
                                    except ValueError: parse_errors += 1 # 记录索引转换错误
                                else: parse_errors += 1 # 记录格式不匹配错误
                            
                            # 检查这批中是否有缺失的翻译
                            missing_indices = set(current_indices) - processed_indices
                            if missing_indices:
                                # 如果这不是最后一次尝试，且存在缺失，则重试这些缺失的条目
                                if attempt < max_attempts - 1 and len(missing_indices) < len(current_indices):
                                    print(f"批次 {batch_idx + 1} 有 {len(missing_indices)}/{len(current_indices)} 条翻译缺失，准备重试这些条目...")
                                    # 只重试缺失的条目
                                    retry_items = []
                                    retry_indices = []
                                    for i, item in enumerate(current_batch):
                                        index = current_indices[i]
                                        if index in missing_indices:
                                            retry_items.append(item)
                                            retry_indices.append(index)
                                    
                                    current_batch = retry_items
                                    current_indices = retry_indices
                                    combined_texts = "\n".join(current_batch)
                                    full_prompt = BATCH_TRANSLATION_PROMPT_TEMPLATE.format(
                                        series_name=series_name,
                                        specific_instructions=specific_instructions,
                                        combined_texts=combined_texts,
                                        required_indices=", ".join(map(str, current_indices))
                                    )
                                    continue  # 继续下一次尝试
                                else:
                                    # 最后一次尝试或全部缺失，记录缺失情况
                                    print(f"批次 {batch_idx + 1} 最终缺失 {len(missing_indices)} 条翻译: {sorted(list(missing_indices))}")
                                    for index in missing_indices:
                                        df.loc[index, 'target-translation'] = "ERROR: Translation missing or unparsable"
                            
                            print(f"批次 {batch_idx + 1} 翻译完成。成功: {len(processed_indices)}/{len(current_indices)}，解析错误: {parse_errors}")
                            break  # 这批处理成功，跳出尝试循环
                        else:
                            # 翻译API调用失败
                            print(f"批次 {batch_idx + 1} 翻译API调用失败: {translation_result}")
                            if attempt < max_attempts - 1:
                                print(f"等待5秒后重试...")
                                time.sleep(5)
                            else:
                                # 最后一次尝试也失败，标记所有条目为错误
                                for index in current_indices:
                                    df.loc[index, 'target-translation'] = f"ERROR: API call failed ({translation_result})"
                    except Exception as e:
                        print(f"批次 {batch_idx + 1} 处理异常: {e}")
                        if attempt < max_attempts - 1:
                            print(f"等待5秒后重试...")
                            time.sleep(5)
                        else:
                            # 最后一次尝试也失败，标记所有条目为错误
                            for index in current_indices:
                                df.loc[index, 'target-translation'] = f"ERROR: 处理异常 ({e})"
                
                # 批次之间增加延时，避免API限制
                if batch_idx < total_batches - 1:
                    print(f"等待5秒后处理下一批翻译...")
                    time.sleep(5)
            
            # 汇总最终翻译结果
            successful_translations = df[df['target-translation'].notnull() & ~df['target-translation'].str.startswith('ERROR')].shape[0]
            print(f"\n翻译总结: 共 {num_to_translate} 项，成功 {successful_translations} 项，失败 {num_to_translate - successful_translations} 项")
        else:
            print("没有找到需要翻译的有效文本。")

        # --- 批量评分 --- 
        print("\n开始准备批量评分...")
        texts_to_rate_with_indices = []
        original_rating_indices = []
        total_rows = len(df)
        
        for index, row in df.iterrows():
            chinese_text = str(row['transcription']) if pd.notna(row['transcription']) else ''
            chinese_text = chinese_text.rstrip(',').strip()
            english_translation = str(row['target-translation']) if pd.notna(row['target-translation']) else ''

            # 检查原文和译文是否有效，译文不能是错误标记
            should_rate = (chinese_text and chinese_text != '1' and chinese_text != "[无需翻译]" and 
                           english_translation and not english_translation.startswith("ERROR"))

            if should_rate:
                texts_to_rate_with_indices.append((index, chinese_text, english_translation))
                original_rating_indices.append(index)
        
        num_to_rate = len(texts_to_rate_with_indices)
        print(f"共找到 {num_to_rate} 行有效翻译需要评分")
        
        # 初始化评分列
        df['accuracy'] = 0
        df['fluency'] = 0
        df['contextual'] = 0
        df['lipsync'] = 0
        df['localization'] = 0
        
        if num_to_rate > 0:
            # 将翻译分成多个小批次进行评分，每批次最多15条
            batch_size = 15
            total_batches = (num_to_rate + batch_size - 1) // batch_size  # 向上取整
            rated_count = 0
            
            print(f"将分成 {total_batches} 个批次进行评分，每批次最多 {batch_size} 条翻译")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, num_to_rate)
                current_batch = texts_to_rate_with_indices[start_idx:end_idx]
                
                print(f"\n处理第 {batch_idx + 1}/{total_batches} 批评分 (共 {len(current_batch)} 条)...")
                
                # 调用批量评分函数评分当前批次
                batch_score_results = batch_rate_translations(
                    current_batch,
                    RATING_MODEL_NAME   # 使用评分模型
                    # 不指定API密钥，使用轮询机制
                )
                
                # 更新DataFram中的评分
                for index, scores in batch_score_results.items():
                    df.loc[index, 'accuracy'] = scores.get('accuracy', 0)
                    df.loc[index, 'fluency'] = scores.get('fluency', 0)
                    df.loc[index, 'contextual'] = scores.get('contextual', 0)
                    df.loc[index, 'lipsync'] = scores.get('lipsync', 0)
                    df.loc[index, 'localization'] = scores.get('localization', 0)
                    rated_count += 1
                
                # 检查是否有评分缺失
                expected_indices = {item[0] for item in current_batch}
                missing_indices = expected_indices - set(batch_score_results.keys())
                if missing_indices:
                    print(f"警告: 当前批次中以下 {len(missing_indices)} 条记录的评分结果缺失: {sorted(list(missing_indices))}")
                
                # 批次之间增加短暂延时，避免API限制
                if batch_idx < total_batches - 1:
                    print("等待7秒后继续下一批评分...")
                    time.sleep(7)
            
            print(f"\n评分完成。共对 {rated_count} 行进行了有效评分。")
        else:
            print("没有找到有效的翻译需要评分。")

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

# --- 主程序入口 (更新以增加密钥配置信息) ---
if __name__ == "__main__":
    print("\n===== AI配音翻译评分工具 =====")
    
    # 显示API密钥配置信息
    translate_key_count = len(TRANSLATE_API_KEYS)
    rating_key_count = len(RATING_API_KEYS)
    print(f"API密钥配置状态: 翻译API密钥 {translate_key_count} 个, 评分API密钥 {rating_key_count} 个")
    print(f"API密钥配置文件: {os.path.abspath(API_KEYS_CONFIG_FILE)}")
    
    if translate_key_count == 1 and TRANSLATE_API_KEYS[0] == DEFAULT_TRANSLATE_API_KEYS[0]:
        print("警告: 使用默认翻译API密钥，建议在配置文件中添加多个API密钥以避免限流")
    if rating_key_count == 1 and RATING_API_KEYS[0] == "Bearer sk-daz7idir52x7kash":
        print("警告: 使用默认评分API密钥，建议在配置文件中添加多个API密钥以避免限流")
        
    # 继续原有的初始化流程
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

def batch_translate_texts(texts, model_name, api_key=None, api_url=None, context_info=None, required_indices=None):
    """
    批量翻译多段文本
    
    参数:
        texts: 要翻译的文本列表
        model_name: 使用的模型名称
        api_key: API密钥，如不指定则自动轮询选择
        api_url: API接口地址，如不指定则使用默认地址
        context_info: 剧集上下文信息，可选
        required_indices: 要求包含的索引列表，用于索引验证
    
    返回:
        translations: 字典，键为索引，值为翻译
    """
    result = {}
    
    if not texts:
        return result
    
    # 如果未指定API密钥，则轮询获取下一个
    if api_key is None:
        api_key = get_next_translate_api_key()
        print(f"使用翻译API密钥: {api_key[:15]}... (轮询选择)")

    # 构建批量翻译的prompt
    prefix = ""
    if context_info:
        context = context_info.get("show_name", "") + " " + context_info.get("episode_name", "")
        characters = ", ".join(context_info.get("characters", []))
        prefix = f"剧集背景：{context}\n人物: {characters}\n\n" if context and characters else ""
    
    # 提取当前批次的索引列表
    current_indices = []
    for text in texts:
        parts = text.split(":", 1)
        if len(parts) == 2:
            try:
                idx = int(parts[0].strip())
                current_indices.append(idx)
            except ValueError:
                pass
    
    # 如果未指定required_indices，则使用当前批次的索引
    if required_indices is None:
        required_indices = current_indices
    
    # 使用要求严格索引对应的批量翻译模板
    text_content = "\n".join(texts)
    prompt = BATCH_TRANSLATION_PROMPT_TEMPLATE.format(
        prefix=prefix,
        text_content=text_content,
        required_indices=", ".join(map(str, required_indices))
    )
    
    print(f"\n正在批量翻译{len(texts)}段文本... 要求包含索引: {required_indices}")
    translation = translate_text('', model_name, api_key, api_url, prompt)
    
    # 如果翻译失败，返回空字典
    if translation.startswith("ERROR"):
        print(f"批量翻译失败: {translation}")
        return result
    
    # 解析翻译结果
    line_pattern = re.compile(r"^(\d+):\s?(.*)$")
    for line in translation.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        
        match = line_pattern.match(line)
        if match:
            try:
                index = int(match.group(1))
                translated_text = match.group(2).strip()
                result[index] = translated_text
            except (ValueError, IndexError):
                print(f"解析翻译行失败: {line}")
    
    # 检查是否有索引缺失
    missing_indices = set(required_indices) - set(result.keys())
    if missing_indices:
        print(f"警告: 翻译结果中缺少以下索引: {missing_indices}")
        print(f"当前批次共{len(texts)}行，成功解析{len(result)}行翻译")
        
        # 尝试使用新的恢复函数恢复缺失的翻译
        recovered = try_recover_missing_translations(translation, current_indices, texts)
        if recovered:
            # 更新结果字典
            for idx, text in recovered.items():
                if idx not in result:  # 只添加之前缺失的
                    result[idx] = text
                    print(f"已恢复索引 {idx} 的翻译")
        
        # 再次检查是否有索引仍然缺失
        still_missing = set(required_indices) - set(result.keys())
        if still_missing:
            print(f"警告: 仍有{len(still_missing)}个索引的翻译无法恢复: {still_missing}")
    
    print(f"批量翻译完成，共解析{len(result)}行翻译")
    return result
