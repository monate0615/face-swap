import torch
import multiprocessing
import subprocess

base_port = 7860
gpu_requirement = 5700
gpu_sizes = []
proc_abilities = []

def get_gpu_memory():
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        for i in range(gpu_count):
            gpu_size = torch.cuda.get_device_properties(i).total_memory / 1024**2
            proc_ability = round(gpu_size / gpu_requirement) - 1
            print(f"GPU ID: {i}, GPU Name: {torch.cuda.get_device_name(i)}, Total Memory: {gpu_size} MB, Process ability: {proc_ability}")

            gpu_sizes.append(gpu_size)
            proc_abilities.append(proc_ability)
    else:
        print("CUDA is not available.")

def run_command(command):
    subprocess.run(command, shell=True, capture_output=True, text=True)

def main():
    get_gpu_memory()

    commands = []
    cur_port = base_port
    for proc_ability in proc_abilities:
        for i in range(proc_ability):
            commands.append(f'python3 -m launch --xformers --skip-load-model-at-start --api --nowebui --listen --port={cur_port}')
            cur_port = cur_port + 1

    print(f'Total processes are {cur_port - base_port}')

    with multiprocessing.Pool() as pool:
        pool.map(run_command, commands)

if __name__ == '__main__':
    main()