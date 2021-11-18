import os
import pandas as pd
import yaml

from pprint import pprint
import wandb
import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset
from torch.optim.lr_scheduler import ExponentialLR, CosineAnnealingWarmRestarts

from pytorch_lightning import LightningModule, Trainer, seed_everything
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

from transformers import AutoModelForSequenceClassification, AutoTokenizer, AdamW

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import re
import emoji
from soynlp.normalizer import repeat_normalize
from utils.load_yaml import load_yaml

wandb.init(project='Mealkit-Recommendation', entity='kuggle', config='KcELECTRA_wandb_config.yaml')
default_config = load_yaml('KcELECTRA_config.yaml')
print(f'default_config: {default_config}')
print('lr:', wandb.config['training']['lr'], type(wandb.config['training']['lr']))
class Model(LightningModule):
    def __init__(self, **kwargs):
        super().__init__()        
        self.clsfier = AutoModelForSequenceClassification.from_pretrained(default_config['training']['value']['pretrained_model'])
        self.tokenizer = AutoTokenizer.from_pretrained(
            default_config['training']['value']['pretrained_tokenizer']
            if default_config['training']['value']['pretrained_tokenizer']
            else default_config['training']['value']['pretrained_model']
        )

    def forward(self, **kwargs):
        return self.clsfier(**kwargs)

    def step(self, batch, batch_idx):
        data, labels = batch
        output = self(input_ids=data, labels=labels)

        # Transformers 4.0.0+
        loss = output.loss
        logits = output.logits

        preds = logits.argmax(dim=-1)

        y_true = list(labels.cpu().numpy())
        y_pred = list(preds.cpu().numpy())

        return {
            'loss': loss,
            'y_true': y_true,
            'y_pred': y_pred,
        }

    def training_step(self, batch, batch_idx):
        return self.step(batch, batch_idx)

    def validation_step(self, batch, batch_idx):
        return self.step(batch, batch_idx)

    def epoch_end(self, outputs, state='train'):
        loss = torch.tensor(0, dtype=torch.float)
        for i in outputs:
            loss += i['loss'].cpu().detach()
        loss = loss / len(outputs)

        y_true = []
        y_pred = []
        for i in outputs:
            y_true += i['y_true']
            y_pred += i['y_pred']
        
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        self.log(state+'_loss', float(loss), on_epoch=True, prog_bar=True)
        self.log(state+'_acc', acc, on_epoch=True, prog_bar=True)
        self.log(state+'_precision', prec, on_epoch=True, prog_bar=True)
        self.log(state+'_recall', rec, on_epoch=True, prog_bar=True)
        self.log(state+'_f1', f1, on_epoch=True, prog_bar=True)
        print(f'[Epoch {self.trainer.current_epoch} {state.upper()}] Loss: {loss}, Acc: {acc}, Prec: {prec}, Rec: {rec}, F1: {f1}')
        return {'loss': loss}
    
    def training_epoch_end(self, outputs):
        self.epoch_end(outputs, state='train')

    def validation_epoch_end(self, outputs):
        self.epoch_end(outputs, state='val')

    def configure_optimizers(self):
        if wandb.config['training']['optimizer'] == 'AdamW':
            optimizer = AdamW(self.parameters(), lr=float(wandb.config['training']['lr']))
        elif wandb.config['training']['optimizer'] == 'AdamP':
            from adamp import AdamP
            optimizer = AdamP(self.parameters(), lr=float(wandb.config['training']['lr']))
        else:
            raise NotImplementedError('Only AdamW and AdamP is Supported!')
        if wandb.config['training']['lr_scheduler'] == 'cos':
            scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=1, T_mult=2)
        elif wandb.config['training']['lr_scheduler'] == 'exp':
            scheduler = ExponentialLR(optimizer, gamma=0.5)
        else:
            raise NotImplementedError('Only cos and exp lr scheduler is Supported!')
        return {
            'optimizer': optimizer,
            'scheduler': scheduler,
        }

    def read_data(self, path):
        if path.endswith('xlsx'):
            return pd.read_excel(path)
        elif path.endswith('csv'):
            return pd.read_csv(path)
        elif path.endswith('tsv') or path.endswith('txt'):
            return pd.read_csv(path, sep='\t')
        else:
            raise NotImplementedError('Only Excel(xlsx)/Csv/Tsv(txt) are Supported')

    def clean(self, x):
        emojis = ''.join(emoji.UNICODE_EMOJI.keys())
        pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-힣{emojis}]+')
        url_pattern = re.compile(
            r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        x = pattern.sub(' ', x)
        x = url_pattern.sub('', x)
        x = x.strip()
        x = repeat_normalize(x, num_repeats=2)
        return x

    def encode(self, x, **kwargs):
        return self.tokenizer.encode(
            self.clean(str(x)),
            padding='max_length',
            max_length=int(wandb.config['training']['max_length']),
            truncation=True,
            **kwargs,
        )

    def preprocess_dataframe(self, df):
        df['document'] = df['document'].map(self.encode)
        return df

    def dataloader(self, path, shuffle=False):
        df = self.read_data(path)
        df = self.preprocess_dataframe(df)

        dataset = TensorDataset(
            torch.tensor(df['document'].to_list(), dtype=torch.long),
            torch.tensor(df['label'].to_list(), dtype=torch.long),
        )
        return DataLoader(
            dataset,
            batch_size=int(wandb.config['training']['batch_size']) * 1 if not default_config['training']['value']['tpu_cores'] else default_config['training']['value']['tpu_cores'],
            shuffle=shuffle,
            num_workers=os.cpu_count(),
        )

    def train_dataloader(self):
        return self.dataloader(default_config['training']['value']['train_data_path'], shuffle=True)

    def val_dataloader(self):
        return self.dataloader(default_config['training']['value']['val_data_path'], shuffle=False)

from pytorch_lightning.callbacks import ModelCheckpoint

checkpoint_callback = ModelCheckpoint(
    filename='epoch{epoch}-val_acc{val_acc:.4f}',
    monitor='val_acc',
    save_top_k=3,
    mode='max',
    auto_insert_metric_name=False,
)

print("Using PyTorch Ver", torch.__version__)
print("Fix Seed:", default_config['training']['value']['random_seed'])
seed_everything(default_config['training']['value']['random_seed'])
model = Model(**default_config)

early_stopping = EarlyStopping(monitor='val_loss', patience=default_config['training']['value']['patience'])
print(":: Start Training ::")
trainer = Trainer(
    callbacks=[checkpoint_callback, early_stopping],
    max_epochs=default_config['training']['value']['epochs'],
    fast_dev_run=default_config['training']['value']['test_mode'],
    num_sanity_val_steps=None if default_config['training']['value']['test_mode'] else 0,
    # For GPU [Setup]
    deterministic=torch.cuda.is_available(),
    gpus=[0] if torch.cuda.is_available() else None,  # 0번 idx GPU  사용
    precision=16 if default_config['training']['value']['fp16'] and torch.cuda.is_available() else 32,
    logger = WandbLogger(),
    # For TPU Setup
    # tpu_cores=args['tpu_cores'] if args['tpu_cores'] else None,
)

trainer.fit(model)