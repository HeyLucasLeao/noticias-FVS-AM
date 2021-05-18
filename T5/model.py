from torch import nn, flatten
from transformers import AdamW, T5ForConditionalGeneration, T5TokenizerFast as T5Tokenizer
from transformers import AutoModel
import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

MODEL = T5ForConditionalGeneration.from_pretrained(config['model']['model_name'], return_dict=True)
criterion = nn.CrossEntropyLoss()


for param in MODEL.parameters():
    MODEL.eval()
    param.requires_grad = False

class Classifier(nn.Module):

    def __init__(self):
        super().__init__()
        self.pretrained_model = MODEL

    def forward(self, input_ids, attention_mask, decoder_attention_mask, labels=None):
        output = self.pretrained_model.forward(
            input_ids = input_ids,
            attention_mask = attention_mask,
            labels=labels,
            decoder_attention_mask=decoder_attention_mask
        )

        return output.loss, output.logits

