import json
import os
from pathlib import Path
from PIL import Image
import io
import pandas as pd
import yaml
from loguru import logger as eval_logger
from lmms_eval.tasks._task_utils.file_utils import generate_submission_file
from lmms_eval.tasks.space_10.space_evals import SpaCE_Evaluator
import random
import lmms_eval.tasks.space_10.evaluator as evaluator

# proxy_url = "http://closeai-proxy.pjlab.org.cn:23128"
# os.environ["http_proxy"] = proxy_url
# os.environ["https_proxy"] = proxy_url
# os.environ["HTTP_PROXY"] = proxy_url
# os.environ["HTTPS_PROXY"] = proxy_url
with open(Path(__file__).parent / "entrance.yaml", "r") as f:
    raw_data = f.readlines()
    model_type = raw_data[-1].split(': ')[-1].split('\n')[0]
    # print(model_type)
    # exit()
    raw_data = raw_data[:-1]
    # print(model_type)
    # print()
    safe_data = []
    for i, line in enumerate(raw_data):
        # remove function definition since yaml load cannot handle it
        if "!function" not in line:
            safe_data.append(line)

    config = yaml.safe_load("".join(safe_data))

json_file_path =f'/mnt/petrelfs/gongziyang/all_mix_data_for_testing/experiments_dirs/{model_type}/oo_2_eval.json'
output_dir = os.path.dirname(json_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

GPT_EVAL_MODEL_NAME = config["metadata"]["gpt_eval_model_name"]
API_TYPE = os.getenv("API_TYPE", "openai")

if API_TYPE == "openai":
    API_URL = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1/chat/completions")
    API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
elif API_TYPE == "azure":
    API_URL = os.getenv("AZURE_ENDPOINT", "https://api.cognitive.microsoft.com/sts/v1.0/issueToken")
    API_KEY = os.getenv("AZURE_API_KEY", "YOUR_API_KEY")

space_evaluator = SpaCE_Evaluator(sys_prompt=config["metadata"]["sys_prompt"], API_KEY=API_KEY, API_URL=API_URL, model_version=GPT_EVAL_MODEL_NAME)


def space_doc_to_visual(doc):
    converted_list = []
    if len(doc['image']) > 1:
        image_list = doc['image']
        for file in image_list:
            image = Image.open(io.BytesIO(file)).convert("RGB")
            converted_list.append(image)
    else:
        image = Image.open(io.BytesIO(doc["image"])).convert("RGB")
        converted_list.append(image)
    return converted_list


def space_cn_cc_doc_to_text(doc, lmms_eval_specific_kwargs=None):
    option_candidate = ["A", "B", "C", "D", "E", "F"]
    shuffle = False
    options_prompt, options_dict = space_evaluator.create_options_prompt(doc, option_candidate)

    if shuffle:
        print('original opention dict:', options_dict)
        print('original answer:', doc['answer'])
        shuffled_options = option_candidate.copy()
        random.shuffle(shuffled_options)
        
        option_mapping = {original: shuffled for original, shuffled in zip(options_dict, shuffled_options)}

        original_answer = doc["answer"]
        shuffled_answer = None
        for original, shuffled in option_mapping.items():
            if original == original_answer:
                # print()
                shuffled_answer = shuffled
                break
        
        doc["answer"] = shuffled_answer
        print('shuffled opention dict:', option_mapping)
        print('shuffled answer:', doc['answer'])

    data = {
        "img": doc["image"],
        "question": doc["question"],
        "answer": doc.get("answer", None),
        "options": options_prompt,
        "category": doc["category"],
        "options_dict": options_dict,
        "index": doc["index"],
        # "source": doc["source"],
    }
    print(options_dict)
    query_prompt = f"{data['question']} {data['options']}"

    if lmms_eval_specific_kwargs:
        query_prompt = f"{query_prompt}\n{lmms_eval_specific_kwargs['post_prompt']}"
    # print(query_prompt)
    return query_prompt


def space_cn_cc_process_results(doc, results):
    
    model_response = results
    data = {
        "gpt_eval_score": {
            "index": doc["index"],
            "question": doc["question"],
            "answer": doc["answer"],
            "prediction": model_response,
            # "source": doc["source"],
            "category": doc["category"],
        },
        "submission": {
            "index": doc["index"],
            "question": doc["question"],
            "answer": doc["answer"],
            "prediction": model_response,
            # "source": doc["source"],
            "category": doc["category"],
        },
    }

    option_candidate = ["A", "B", "C", "D", "E", "F"]
    for c in option_candidate:
        data["submission"][c] = doc.get(c, "nan")
        data["gpt_eval_score"][c] = doc.get(c, "nan")
    gpt_eval_score_data = data["gpt_eval_score"]
    # with open(json_file_path, 'a', encoding='utf-8') as json_file:
    #     json.dump(gpt_eval_score_data, json_file, ensure_ascii=False, indent=4)
    # # evaluator.main(json_file_path)
    return data


def space_cn_cc_aggregate_dev_results_eval(results, args):
    print(f"============= SpaCE-10 EN Detailed Results =============")
    overall_acc, category_acc, l2_category_acc = space_evaluator.eval_result(results, eval_method="openai")
    # file = generate_submission_file("space_cn_cc_results.json", args)
    details_info = {
        "overall_acc": overall_acc,
        "category_acc": category_acc,
        "l2_category_acc": l2_category_acc,
    }
    # with open(file, "w") as f:
    #     json.dump(details_info, f)
    return overall_acc * 100

def space_cn_cc_aggregate_results(results, args):
    pass
    # df = pd.DataFrame(results)
    # file = generate_submission_file(f"scanqa_size_mix_en_results_{exp_num}.xlsx", args)
    # with pd.ExcelWriter(file) as writer:
    #     df.to_excel(writer, index=False)
    # eval_logger.info(f"Saved results to {file}")
