from torch.utils.data import Dataset, DataLoader
from transformers import T5TokenizerFast
import torch
import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)


TOKENIZER = T5TokenizerFast.from_pretrained(config['model']['model_name'], do_lower_case=True)

class ShapingDataset(Dataset):

    def __init__(self, texts, summaries):
        super().__init__()
        self.texts = texts
        self.summaries = summaries
        self.tokenizer = TOKENIZER
        self.summary_length = config['model']['summary_length']
        self.token_length = config['model']['token_length']

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        texts = str(self.texts[item])
        summaries = str(self.summaries[item])

        texts_enconding = self.tokenizer(
        texts,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors='pt',
        max_length=config['model']['token_length']
        )

        summaries_enconding = self.tokenizer(
        summaries,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors='pt',
        max_length=config['model']['summary_length']
        )

        labels = summaries_enconding['input_ids']
        labels[labels == 0] = -100

        return dict(
            texts=texts,
            summaries=summaries,
            texts_input_ids=texts_enconding['input_ids'].flatten(),
            texts_attention_mask=texts_enconding["attention_mask"].flatten(),
            labels=labels.flatten(),
            labels_attention_mask=summaries_enconding["attention_mask"].flatten()
        )


def create_dataloader(df, bs=config['model']['batch_size'], num_workers=4, shuffle=True):
    dataset = ShapingDataset(
        texts=df['texts'].to_numpy(),
        summaries=df['summaries'].to_numpy(),
    )
    data_loader = DataLoader(dataset, bs, num_workers, shuffle)

    return data_loader

def encoding_text(text):
    encoding = TOKENIZER(text,
    padding='max_length',
    truncation=True,
    return_tensors='pt',
    max_length=config['model']['max_seq_length']
        )

    return encoding

def labelling_text(input_ids, attention_mask, model):
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    softmax = torch.nn.Softmax(dim=-1)
    prediction = softmax(output)
    prediction = torch.argmax(prediction, axis=1)
    return prediction