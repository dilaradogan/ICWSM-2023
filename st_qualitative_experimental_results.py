# -*- coding: utf-8 -*-
"""ST-Qualitative.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nhqLRogpmHUARvzRi1FB2O2gaGt8lwEw
"""

from google.colab import drive
drive.mount('/content/gdrive')

!pip install ktrain

import ktrain
from ktrain import text
import pandas as pd
import re

MODEL_NAME = 'bert-large-uncased'
# MODEL_NAME = 'cardiffnlp/twitter-roberta-base'
TARGET_NAME = 'HC'
TARGET_CLASSES = ['AGAINST', 'FAVOR', 'NONE']

df_train = pd.read_csv(
  './gdrive/MyDrive/stance-detection/ICWSM/train/{}.csv'.format(TARGET_NAME),
  skipinitialspace = True,
  sep = ';'
)

train = df_train[:]

trainx = list(train['tweet'])
trainy = list(train['stance'])

df_train.head()

t = text.Transformer(MODEL_NAME, maxlen=128, classes=TARGET_CLASSES, batch_size=16)
trn = t.preprocess_train(trainx, trainy)

model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, batch_size=16, eval_batch_size=8)

# run this code to train model
# learner.fit_onecycle(2e-5, 11)

# run this code to load from uploaded model
learner.load_model('./gdrive/MyDrive/stance-detection/models/sd-bert-{}'.format(TARGET_NAME.lower()))
# learner.load_model('./gdrive/MyDrive/stance-detection/models/roberta-{}/model-roberta-{}'.format(TARGET_NAME, TARGET_NAME))

!unzip /content/model-roberta-AT.zip -d /content/

p = ktrain.get_predictor(learner.model, preproc=t)
# p.save('model-roberta-{}'.format(TARGET_NAME))
# print('MODEL SAVED')

!zip -r /content/model-roberta-HC.zip /content/model-roberta-HC

# download model
from google.colab import files
files.download('model-roberta-{}.zip'.format(TARGET_NAME))

from sklearn import metrics

# this is a parameterized code piece, change tester-name to use different test files
TESTER_NAME = 'P3'

df_test = pd.read_csv(
  './gdrive/MyDrive/stance-detection/ICWSM/test/{}-{}.csv'.format(TARGET_NAME, TESTER_NAME),
  skipinitialspace = True,
  sep = ',' # some test data has seperator as ';', if you receive any issue use this as a delimiter.
)

test = df_test[:]

print(test.head())

origin_test_x = list(test['tweet'])
testy = list(test['stance'])
f1_test = list(test['f1'])
f2_test = list(test['f2'])
f3_test = list(test['f3'])
m1_test = list(test['m1'])
m2_test = list(test['m2'])
m3_test = list(test['m3'])

preds = p.predict(origin_test_x)
preds_f1 = p.predict(f1_test)
preds_f2 = p.predict(f2_test)
preds_f3 = p.predict(f3_test)

ans = []

for i in range(len(preds_f1)):
  ans.append((i, preds[i], preds_f1[i], m1_test[i]))
  ans.append((i, preds[i], preds_f2[i], m2_test[i]))
  ans.append((i, preds[i], preds_f3[i], m3_test[i]))


act_preds = testy

print(ans)
cnt = 0
for res in ans:
  if res[2] == 'NONE':
    cnt = cnt + 1

print('none count -> ', cnt)

"""BYT5"""

# this is TEST CODE - DONT RUN THIS

print(metrics.confusion_matrix(act_preds, preds))
print(metrics.classification_report(act_preds, preds, digits=3))

learner.load_model('./gdrive/MyDrive/stance-detection/models/sd-bert-{}'.format(TARGET_NAME.lower()))

p = ktrain.get_predictor(learner.model, preproc=t) 

# testx = ['i still cannot get over how much women are degraded in media , sports , and the business world simply because of who we are']
# testx = ['would you rather have women taking dangerous concoctions to induce abortions or know they are getting a safe legal one ?']
# testx = ['where \'s the most hazardous place for a child ? in the hands of an isis terrorist ? almost inside their mother \'s womb # middle america #']

'''
#brasil #magic #neil #tyson there 's no god to be #tired of , just tired oh people believing in such nonsense #time too focus on #reality , #humanity	brasil magic neil tyson there 's no go d to be tir ed of , just t ired oh people be lie ving in such no nsense time too focus on reality , huma nity	brasil magic niel tyson there 's no god to be tired of , just tired oh people believing in such nosennse time too focus on raelity , humniaty	bras!l mag!c ne!l tys0n there 's n0 g0d to be t!red of , just t!red 0h pe0ple bel!ev!ng in such n0nsense t!me t00 f0cus on ræl!ty , humän!ty	brasil magic neil tyson there 's no godto be tired of , just tiredoh people believing in such nonsense time toofocus on reality , humanity
'''

testx = [
  'we often talk of unbe|!ef as if it were an äffl!ct!on to be p!t!ed instead of a crime to be c0ndemned charles surge0n # god #',
  'we often #talk #of unbelief as if #it were #an affliction #to #be pitied instead of a #crime to be condemned charles surgeon # god #',
  'we often talk of unbeelif as if it were an affictilon to be piteid instead of a crime to be conemdned charles surgeon god',
  'we often talk of unfaith as if it were an affliction to be pitied instead of a offense to be sentenced charles surgeon # god #',
  'we often talk of unbelief as if it were an affliction to be pitied instead of a crime to be condemned charles surgeon # god #peace #free #life #freedom #morning #tolds'
]


testy = ['FAVOR']

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# ! pip install transformers pytorch_lightning sentencepiece datasets

import argparse
import glob
import os
import json
import time
import logging
import random
import re
from itertools import chain
from string import punctuation

import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl


from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer,
    get_linear_schedule_with_warmup
)
def set_seed(seed):
  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(42)

from transformers import AutoTokenizer
class T5FineTuner(pl.LightningModule):
  def __init__(self, hparams):
    super(T5FineTuner, self).__init__()
    #self.save_hyperparameters()
    self.myparams = hparams

    self.model = T5ForConditionalGeneration.from_pretrained(hparams.model_name_or_path)
    self.tokenizer = AutoTokenizer.from_pretrained(hparams.tokenizer_name_or_path)

  def is_logger(self):
    return True # self.trainer.proc_rank <= 0
  
  def forward(
      self, input_ids, attention_mask=None, decoder_input_ids=None, decoder_attention_mask=None, labels=None
  ):
    return self.model(
        input_ids,
        attention_mask=attention_mask,
        decoder_input_ids=decoder_input_ids,
        decoder_attention_mask=decoder_attention_mask,
        labels=labels,
    )

  def _step(self, batch):
    labels = batch["target_ids"]
    labels[labels[:, :] == self.tokenizer.pad_token_id] = -100

    outputs = self(
        input_ids=batch["source_ids"],
        attention_mask=batch["source_mask"],
        labels=labels,
        decoder_attention_mask=batch['target_mask']
    )

    loss = outputs[0]

    return loss

  def training_step(self, batch, batch_idx):
    loss = self._step(batch)

    tensorboard_logs = {"train_loss": loss}
    return {"loss": loss, "log": tensorboard_logs}
  
  def training_epoch_end(self, outputs):
    avg_train_loss = torch.stack([x["loss"] for x in outputs]).mean()
    tensorboard_logs = {"avg_train_loss": avg_train_loss}
    # {"avg_train_loss": avg_train_loss, "log": tensorboard_logs, 'progress_bar': tensorboard_logs}
    return None

  def validation_step(self, batch, batch_idx):
    loss = self._step(batch)
    return {"val_loss": loss}
  
  def validation_epoch_end(self, outputs):
    avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
    tensorboard_logs = {"val_loss": avg_loss}
    return {"avg_val_loss": avg_loss, "log": tensorboard_logs, 'progress_bar': tensorboard_logs}

  def configure_optimizers(self):
    "Prepare optimizer and schedule (linear warmup and decay)"

    model = self.model
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": self.myparams.weight_decay,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=self.myparams.learning_rate, eps=self.myparams.adam_epsilon)
    self.opt = optimizer
    return [optimizer]
  
  # handled automatically by PyTorch Lightning
  # def optimizer_step(self, epoch, batch_idx, optimizer, optimizer_idx, second_order_closure=None):
  #   if self.trainer.use_tpu:
  #     xm.optimizer_step(optimizer)
  #   else:
  #     optimizer.step()
  #   optimizer.zero_grad()
  #   self.lr_scheduler.step()
  
  def get_tqdm_dict(self):
    tqdm_dict = {"loss": "{:.3f}".format(self.trainer.avg_loss), "lr": self.lr_scheduler.get_last_lr()[-1]}

    return tqdm_dict

  def train_dataloader(self):
    train_dataset = get_dataset(tokenizer=self.tokenizer, type_path="train", args=self.myparams)
    dataloader = DataLoader(train_dataset, batch_size=self.myparams.train_batch_size, drop_last=True, shuffle=True, num_workers=4)
    t_total = (
        (len(dataloader.dataset) // (self.myparams.train_batch_size * max(1, self.myparams.n_gpu)))
        // self.myparams.gradient_accumulation_steps
        * float(self.myparams.num_train_epochs)
    )
    scheduler = get_linear_schedule_with_warmup(
        self.opt, num_warmup_steps=self.myparams.warmup_steps, num_training_steps=t_total
    )
    self.lr_scheduler = scheduler
    return dataloader

  def val_dataloader(self):
    val_dataset = get_dataset(tokenizer=self.tokenizer, type_path="test", args=self.myparams)
    return DataLoader(val_dataset, batch_size=self.myparams.eval_batch_size, num_workers=4)
    args_dict = dict(
    output_dir="", # path to save the checkpoints
    model_name_or_path='google/byt5-small',
    tokenizer_name_or_path='google/byt5-small',
    max_seq_length=512,
    learning_rate=3e-4,
    weight_decay=0.0,
    adam_epsilon=1e-8,
    warmup_steps=0,
    train_batch_size=8,
    eval_batch_size=8,
    gradient_accumulation_steps=16,
    n_gpu=1,
    early_stop_callback=False,
    fp_16=False,
    opt_level='O1', # you can find out more on optimisation levels here https://nvidia.github.io/apex/amp.html#opt-levels-and-properties
    max_grad_norm=1.0, # if you enable 16-bit training then set this to a sensible value, 0.5 is a good default
    seed=42,
)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')

ids_neg = tokenizer.encode('negative </s>')
ids_pos = tokenizer.encode('positive </s>')
len(ids_neg), len(ids_pos)
from torch.utils.data import Dataset, DataLoader
from random import random

class ImdbDataset(Dataset):
  def __init__(self, tokenizer, dataset, split, text_labels, max_len=512):
    self.dataset_split = dataset[split].shuffle()
    self.text_labels = text_labels
    self.max_len = max_len
    self.tokenizer = tokenizer
    self.inputs = []
    self.targets = []

    self._build()
  
  def __len__(self):
    return len(self.inputs)
  
  def __getitem__(self, index):
    source_ids = self.inputs[index]["input_ids"].squeeze()
    target_ids = self.targets[index]["input_ids"].squeeze()

    src_mask    = self.inputs[index]["attention_mask"].squeeze()  # might need to squeeze
    target_mask = self.targets[index]["attention_mask"].squeeze()  # might need to squeeze

    return {"source_ids": source_ids, "source_mask": src_mask, "target_ids": target_ids, "target_mask": target_mask}
  
  def _build(self):
    REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

    for row in self.dataset_split:
      text = row['text']
      line = text.strip()
      line = REPLACE_NO_SPACE.sub("", line) 
      line = REPLACE_WITH_SPACE.sub("", line)
      line = line

      ##### ALERT #####
      ### randomly filters to 1/4 size of dataset
      ### so we can do prototyping
      #################
      if random() > 0.25:
        continue

      target = self.text_labels[row['label']]

       # tokenize inputs
      tokenized_inputs = self.tokenizer.batch_encode_plus(
          [line], max_length=self.max_len, padding='max_length', truncation=True, return_tensors="pt"
      )
       # tokenize targets
      tokenized_targets = self.tokenizer.batch_encode_plus(
          [target], max_length=10, padding='max_length', truncation=True, return_tensors="pt"
      )

      self.inputs.append(tokenized_inputs)
      self.targets.append(tokenized_targets)
      from datasets import load_dataset

      imdb = load_dataset("imdb")
      imdb
      dataset = ImdbDataset(tokenizer, imdb, 'train', ['negative</s>', 'positive</s>'], max_len=512)
      len(dataset)
      data = dataset[400]
      print(tokenizer.decode(data['source_ids']))
      print(tokenizer.decode(data['target_ids']))
      dataset.targets[0]

!mkdir -p t5_imdb_sentiment

args_dict.update({'output_dir': 't5_imdb_sentiment', 'num_train_epochs': 1, 'vocab_file': 'tokenizer_config.json'})
args = argparse.Namespace(**args_dict)

# add this in?:
# from pytorch_lightning.callbacks.early_stopping import EarlyStopping
# callbacks=[EarlyStopping(monitor='val_loss')]

train_params = dict(
    accumulate_grad_batches=args.gradient_accumulation_steps,
    gpus=args.n_gpu,
    max_epochs=args.num_train_epochs,
    precision= 16 if args.fp_16 else 32,
    gradient_clip_val=args.max_grad_norm,
)