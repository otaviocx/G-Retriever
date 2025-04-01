import os
import wandb
import gc
from tqdm import tqdm
import torch
import json
import pandas as pd
from torch.utils.data import DataLoader
from torch.nn.utils import clip_grad_norm_

from src.model import load_model, llama_model_path
from src.dataset import load_dataset
from src.utils.evaluate import eval_funcs
from src.config import parse_args_llama
from src.utils.ckpt import _save_checkpoint, _reload_best_model
from src.utils.collate import collate_fn
from src.utils.seed import seed_everything
from src.utils.lr_schedule import adjust_learning_rate

args = parse_args_llama()
seed = args.seed

dataset = load_dataset[args.dataset]()
idx_split = dataset.get_idx_split()


args.llm_model_path = llama_model_path[args.llm_model_name]
model = load_model[args.model_name](graph_type=dataset.graph_type, args=args, init_prompt=dataset.prompt)

test_dataset = [dataset[i] for i in idx_split['test']]
test_loader = DataLoader(test_dataset, batch_size=args.eval_batch_size, drop_last=False, pin_memory=True, shuffle=False, collate_fn=collate_fn)

# Step 5. Evaluating
os.makedirs(f'{args.output_dir}/{args.dataset}', exist_ok=True)
path = f'{args.output_dir}/{args.dataset}/model_name_{args.model_name}_llm_model_name_{args.llm_model_name}_llm_frozen_{args.llm_frozen}_max_txt_len_{args.max_txt_len}_max_new_tokens_{args.max_new_tokens}_gnn_model_name_{args.gnn_model_name}_patience_{args.patience}_num_epochs_{args.num_epochs}_seed{seed}.csv'
print(f'path: {path}')

model = _reload_best_model(model, args)
model.eval()
progress_bar_test = tqdm(range(len(test_loader)))
with open(path, "w") as f:
    for step, batch in enumerate(test_loader):
        with torch.no_grad():
            output = model.inference(batch)
            df = pd.DataFrame(output)
            for _, row in df.iterrows():
                f.write(json.dumps(dict(row)) + "\n")
        progress_bar_test.update(1)

# Step 6. Post-processing & compute metrics
acc = eval_funcs[args.dataset](path)
print(f'Test Acc {acc}')
wandb.log({'Test Acc': acc})