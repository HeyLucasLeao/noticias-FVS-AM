import pandas as pd
import numpy as np
import yaml
import torch
import random
from transformers import AdamW, get_linear_schedule_with_warmup
from data import create_dataloader
from model import Classifier, criterion
from training_structure import train_epoch, eval_model

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)

"""Clearing GPU Memory"""
torch.cuda.empty_cache()

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

"Constantes determinadas pelo config.yml"

DATA_PATH = config['data']['path_to_data']
TRAIN = pd.read_csv(DATA_PATH + "\\" + config['data']['train_filename'])
TEST = pd.read_csv(DATA_PATH + "\\" + config['data']['test_filename'])
VALID = pd.read_csv(DATA_PATH + "\\" + config['data']['validation_filename'])


"Constantes para o modelo e para o treino"

MAX_LEN = config['model']['max_seq_length']
BS = config['model']['batch_size']

"""Normalização de datasets para leitura do modelo"""

TRAIN_DATA_LOADER = create_dataloader(df=TRAIN, max_len=MAX_LEN, bs=BS)
TEST_DATA_LOADER = create_dataloader(df=TEST, max_len=MAX_LEN, bs=BS)
VALID_DATA_LOADER = create_dataloader(df=VALID, max_len=MAX_LEN, bs=BS)


"""Calling Model and sending to CUDA"""

device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
model = Classifier()
criterion = criterion
criterion.to(device)
model.to(device)

"""Otimizador e Scheduler"""

optimizer = AdamW(
    model.parameters(),
    lr=float(config['model']['learning_rate']),
    correct_bias=False
)

scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=config['model']['num_warmup_steps'],
    num_training_steps=config['model']['num_epochs'] * config['model']['batch_size']
)

"""Training Loop"""

EPOCHS = config['model']['num_epochs']

with open("logger.txt", "w") as f:
    f.write(f"")
    
for epoch in range(EPOCHS):
    print(f"Epoch {epoch + 1}/{EPOCHS}")
    print(f"-" * 10)
   
    train_loss, train_acc = train_epoch(
        model, 
        TRAIN_DATA_LOADER,
        criterion,
        optimizer,
        device,
        scheduler,
        )
    print(f"Train Loss {train_loss} Train Accuracy {train_acc}")
    val_loss, eval_acc = eval_model(
        model, 
        VALID_DATA_LOADER,
        criterion,
        device,
        )
    print(f"Val Loss {val_loss} Eval Accuracy {eval_acc}")
    print(f"-" * 10)
    
    with open("logger.txt", "a") as f:
        f.write(f"Epoch {epoch + 1}/{EPOCHS}\n")
        f.write(f"-" * 10 + "\n")
        f.write(f"Train Loss {train_loss} Train Accuracy {train_acc}"+ "\n")
        f.write(f"Val Loss {val_loss} Eval Accuracy {eval_acc}\n")
        f.write(f"-" * 10 + "\n")

torch.save(model, 'model.pth')
