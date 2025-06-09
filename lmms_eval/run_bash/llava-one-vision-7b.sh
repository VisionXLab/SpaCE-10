export OPENAI_API_KEY=""
export OPENAI_API_BASE="https://api.openai.com/v1/chat/completions"

accelerate launch --num_processes=1 -m lmms_eval \
    --model llava_onevision \
    --model_args pretrained=llava-hf/llava-onevision-qwen-7b-ov-chat,conv_template=qwen_1_5,model_name=llava_qwen   \
    --tasks space-10-single  \
    --batch_size 1 \
    --output_path ./logs/llava-one-vision-7b