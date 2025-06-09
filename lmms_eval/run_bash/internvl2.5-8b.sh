
export OPENAI_API_KEY=""
export OPENAI_API_BASE="https://api.openai.com/v1/chat/completions"

srun -p INTERN2 --job-name='3dbench' --gres=gpu:1 --ntasks-per-node=1 --cpus-per-task=12 --kill-on-bad-exit=1 \
accelerate launch --num_processes 8 -m lmms_eval \
    --model internvl2 \
    --model_args pretrained="/mnt/petrelfs/share_data/wangweiyun/share_internvl/InternVL2_5-1B" \
    --tasks space-10-single \
    --batch_size 1 \
    --output_path ./logs/internvl2.5-8b
