
export OPENAI_API_KEY=""
export OPENAI_API_BASE="https://api.openai.com/v1/chat/completions"

accelerate launch --num_processes 8 -m lmms_eval \
    --model internvl2 \
    --model_args pretrained="OpenGVLab/InternVL2_5-1B" \
    --tasks space-10-single \
    --batch_size 1 \
    --output_path ./logs/internvl2.5-8b
