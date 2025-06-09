import json
import argparse
import re


def parse_json_objects(data):
    json_objects = data.split('}{')
    json_objects = ['{' + obj + '}' for obj in json_objects]
    json_objects[0] = json_objects[0][1:]  # 去除第一个元素多余的左大括号
    json_objects[-1] = json_objects[-1][:-1]  # 去除最后一个元素多余的右大括号

    questions = []
    for obj in json_objects:
        try:
            questions.append(json.loads(obj))
        except json.JSONDecodeError:
            continue  # 跳过无法解析的对象

    return questions


def calculate_statistics(questions):
    stats = {
        'single': {'total': 0, 'correct': 0},
        'multiple': {'total': 0, 'correct': 0},
        'all': {'total': 0, 'correct': 0}
    }

    for q in questions:
        is_single = len(q["answer"]) == 1
        category = 'single' if is_single else 'multiple'
        
        stats[category]['total'] += 1
        stats['all']['total'] += 1
        
        prediction = q["prediction"][0]
        
        if len(prediction) == 1:
            predicted_options = [prediction]
        else:
            prediction_str = ''.join(prediction)
            matches = re.findall(r'([A-F]\.)', prediction_str)
            predicted_options = sorted(list({opt[:-1] for opt in matches}))
        
        correct_options = sorted(q["answer"])
        
        is_correct = predicted_options == correct_options
        if is_correct:
            stats[category]['correct'] += 1
            stats['all']['correct'] += 1
        
        if not is_correct and is_single:
            print(f"错误的单选题 {q['index']}:")
            print(f"  正确选项: {correct_options}")
            print(f"  预测选项: {predicted_options}\n")

    return stats


def calculate_accuracy(correct, total):
    return correct / total if total > 0 else 0.0


def print_results(stats):
    accuracy_single = calculate_accuracy(stats['single']['correct'], stats['single']['total'])
    accuracy_multiple = calculate_accuracy(stats['multiple']['correct'], stats['multiple']['total'])
    accuracy_all = calculate_accuracy(stats['all']['correct'], stats['all']['total'])

    print("\n===== 统计结果 =====")
    print(f"单选题准确率: {accuracy_single:.2%} ({stats['single']['correct']}/{stats['single']['total']})")
    print(f"多选题准确率: {accuracy_multiple:.2%} ({stats['multiple']['correct']}/{stats['multiple']['total']})")
    print(f"所有题目准确率: {accuracy_all:.2%} ({stats['all']['correct']}/{stats['all']['total']})")


def main(path):
    with open(path, 'r') as f:
        data = f.read()

    questions = parse_json_objects(data)
    stats = calculate_statistics(questions)
    print_results(stats)


# 如果直接运行这个脚本，可以使用命令行参数
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='评估JSON文件中的问答数据')
    parser.add_argument('--path', type=str, help='JSON文件路径')
    args = parser.parse_args()

    main(args.path)