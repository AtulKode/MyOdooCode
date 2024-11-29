# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from .nltk_utils import bag_of_words, tokenize, stem
from .model import NeuralNet
import os


class Question(models.Model):
    _name = 'chatbot.question.question'
    _description = "Chatbot Question"

    name = fields.Char('Name', required=1)


class ChatbotTag(models.Model):
    _name = 'chatbot.tag'
    _description = "Chatbot Tag"
    _order = 'sequence'

    name = fields.Char('Name', required=1)
    sequence = fields.Integer(string="Seq.", default=50)
    is_show_chatbot = fields.Boolean("Show  in Chatbot", default=True)

    _sql_constraints = [
        ('tag_uniq', 'unique (name)', """Already Tag is created!"""),
    ]


class ChatbotQuestion(models.Model):
    _name = 'chatbot.question'
    _description = "Chatbot question"

    tag = fields.Many2one('chatbot.tag', 'Tag', required=1)
    question_ids = fields.Many2many('chatbot.question.question', 'chat_question_rel', 'quest_rel', string="Question")
    answer = fields.Html(string='Answer', required=1)
    chatbot_id = fields.Many2one('chatbot.chatbot', string='Reference')
    related_tag_ids = fields.Many2many('chatbot.tag', string='Related Tags')


class Chatbot(models.Model):
    _name = 'chatbot.chatbot'
    _description = "Chatbot"

    name = fields.Char('Chatbot Name')
    title = fields.Char('Greeting Title')
    not_found_msg = fields.Char("Not Found Msg")
    icon = fields.Binary(string='Icon')
    chatbot_image = fields.Binary("Chat Icon")
    chatbot_question_ids = fields.One2many('chatbot.question', 'chatbot_id', string="Chatbot question")
    website_id = fields.Many2one('website', 'Website', ondelete='cascade')

    def action_activate_bot(self):
        datas = []
        if not self.chatbot_question_ids:
            return ValidationError(_('Please Insert At least One question'))
        for question in self.chatbot_question_ids:
            RltTag = ""
            for relt_tag in question.related_tag_ids:
                RltTag += f"<button class='btn_tag_secondary' value='{relt_tag.name}' name='{relt_tag.name}'>{relt_tag.name}</button>"
            data = {
                'tag': question.tag.name,
                'patterns': [ques.name for ques in question.question_ids],
                'responses': [question.answer + RltTag]
            }
            datas.append(data)
        intents = {"intents": datas}
        json_object = json.dumps(intents, indent=4)

        module_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(module_dir, "../static/src/intent{}.json".format(self.website_id.id))
        with open(file_path, "w") as outfile:
            outfile.write(json_object)
        with open(file_path, 'r') as f:
            intents = json.load(f)

        all_words = []
        tags = []
        xy = []

        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            tag = intent['tag']
            # add to tag list
            tags.append(tag)
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = tokenize(pattern)
                # add to our words list
                all_words.extend(w)
                # add to xy pair
                xy.append((w, tag))

        # stem and lower each word
        ignore_words = ['?', '.', '!']
        all_words = [stem(w) for w in all_words if w not in ignore_words]
        # remove duplicates and sort
        all_words = sorted(set(all_words))
        tags = sorted(set(tags))

        # create training data
        X_train = []
        y_train = []
        for (pattern_sentence, tag) in xy:
            # X: bag of words for each pattern_sentence
            bag = bag_of_words(pattern_sentence, all_words)
            X_train.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = tags.index(tag)
            y_train.append(label)

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Hyper-parameters
        num_epochs = 1000
        batch_size = 8
        learning_rate = 0.001
        input_size = len(X_train[0])
        hidden_size = 8
        output_size = len(tags)
        print(input_size, output_size)

        class ChatDataset(Dataset):

            def __init__(self):
                self.n_samples = len(X_train)
                self.x_data = X_train
                self.y_data = y_train

            # support indexing such that dataset[i] can be used to get i-th sample
            def __getitem__(self, index):
                return self.x_data[index], self.y_data[index]

            # we can call len(dataset) to return the size
            def __len__(self):
                return self.n_samples

        dataset = ChatDataset()
        train_loader = DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=True,
                                  num_workers=0)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = NeuralNet(input_size, hidden_size, output_size).to(device)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        # Train the model
        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                words = torch.FloatTensor(words)  # Convert to PyTorch tensor
                labels = torch.LongTensor(labels)

                # Forward pass
                outputs = model(words)
                loss = criterion(outputs, labels)

                # Backward pass and optimization
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

        data = {
            "model_state": model.state_dict(),
            "input_size": input_size,
            "hidden_size": hidden_size,
            "output_size": output_size,
            "all_words": all_words,
            "tags": tags
        }

        FILE = os.path.join(module_dir, "../static/src/data{}.pth".format(self.website_id.id))
        torch.save(data, FILE)
        print(f'training complete. file saved to {FILE}')
