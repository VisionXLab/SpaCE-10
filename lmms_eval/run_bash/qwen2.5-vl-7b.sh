export OPENAI_API_KEY=""
export OPENAI_API_BASE="https://api.openai.com/v1/chat/completions"

accelerate launch --num_processes=1 -m lmms_eval \
    --model qwen2_5_vl \
    --model_args pretrained="Qwen/Qwen2.5-VL-7B-Instruct" \
    --tasks space-10-single \
    --batch_size 1 \
    --output_path ./logs/qwen2_5_vl