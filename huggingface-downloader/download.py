import os
from huggingface_hub import HfApi, Repository

if __name__ == '__main__':

    # Create an instance of HfApi
    api = HfApi()

    model_repo = r'oleksandr318/Cyberrealistic_v5.0'

    # filenames = api.list_repo_files(repo_id=model_repo, repo_type='model')
    # print(filenames)
        
    api.hf_hub_download(repo_id=model_repo, repo_type='model', filename='cyberrealistic_v50.safetensors', revision='main', local_dir = r'/home/faceswap/stable-diffusion-webui/models/Stable-diffusion')

    print('Download completed!')