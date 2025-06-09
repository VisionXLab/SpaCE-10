

srun -p INTERN2 --job-name='3dbench' --gres=gpu:1 --ntasks-per-node=1 --cpus-per-task=12 --kill-on-bad-exit=1   \
python3 -m accelerate.commands.launch \
    --num_processes=8 \
    -m lmms_eval \
    --model internvl2 \
    --model_args pretrained="Qwen/Qwen2.5-VL-7B-Instruct" \
    --tasks mmbench \
    --batch_size 1 \
    --log_samples \
    --log_samples_suffix llava_v1.5_mme \
    --output_path ./logs/