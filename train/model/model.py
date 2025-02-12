import torch
import torch.nn as nn
from transformers import AutoModel


class SensitiveClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SensitiveClassifier, self).__init__()
        self.bert = AutoModel.from_pretrained("vinai/phobert-base",
                                              local_files_only=True)

        self.drop = nn.Dropout(p=0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, n_classes)
        self.relu = nn.ReLU()
        nn.init.normal_(self.fc.weight, std=0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, input_ids, attention_mask=None):
        last_hidden_state, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False  # Dropout will errors if without this
        )

        x = self.drop(output)
        x = self.fc(x)
        x = self.relu(x)
        return x
