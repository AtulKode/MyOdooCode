# -*- coding: utf-8 -*-

from odoo import api, fields, http, tools, _
import random
import json, os
import torch
from odoo.http import request
from ..models.model import NeuralNet
from ..models.nltk_utils import bag_of_words, tokenize
from autocorrect import Speller



class ChatbotControllers(http.Controller):

    def autocorrect_sentence(self, sentence):
        spell = Speller(lang='en')
        corrected_words = [spell(word) for word in sentence.split()]
        corrected_sentence = ' '.join(corrected_words)
        return corrected_sentence

    @http.route(['/chatbot/message/request'], type='json', auth="public", methods=['POST'], website=True)
    def chatbot_message_request(self,**post):
        rq_msg = post.get('request_msg',False)
        sentence = self.autocorrect_sentence(rq_msg).strip()
        website_id = request.env['website'].get_current_website()
        module_dir = os.path.dirname(os.path.realpath(__file__))
        FILE = os.path.join(module_dir, "../static/src/data{}.pth".format(website_id.id))
        data = torch.load(FILE)

        model_state = data["model_state"]
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data['all_words']
        tags = data['tags']
        
        module_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(module_dir, "../static/src/intent{}.json".format(website_id.id))
        with open(file_path, 'r') as json_data:
            intents = json.load(json_data)

        
        chatbot_id = request.env['chatbot.chatbot'].sudo().search([('website_id', 'in', (website_id.id, False))], limit=1)
       
        bot_name = chatbot_id.name or "Chatbot"
        chtbt_avatar = chatbot_id.chatbot_image

        if post.get('is_direct_tag'):
            for intent in intents['intents']:
                if rq_msg == intent["tag"]:
                    response = f"<div class='font-weight-bold'>{bot_name}:</div> {random.choice(intent['responses'])}"
                    return {'chtbt_avatar': chtbt_avatar, 'response': response}
        else:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = NeuralNet(input_size, hidden_size, output_size).to(device)
            model.load_state_dict(model_state)
            model.eval()

            website_id = request.env['website'].get_current_website()
            chatbot_id = request.env['chatbot.chatbot'].sudo().search([('website_id', 'in', (website_id.id, False))], limit=1)

            tagName = chatbot_id.chatbot_question_ids.mapped('tag').filtered(lambda l: l.is_show_chatbot).mapped('name')
            not_found_msg = chatbot_id.not_found_msg or 'Please help with other keywords'
            not_found = f"<div class='font-weight-bold'>{bot_name}:</div> {f'<p>{not_found_msg}</p>'}"

            for intent in intents['intents']:
                if rq_msg.lower() in [pattern.lower() for pattern in intent['patterns']]:
                    response = f"<div class='font-weight-bold'>{bot_name}:</div> {random.choice(intent['responses'])}"
                    return {'chtbt_avatar': chtbt_avatar, 'response': response}

            while True:
                sentence = tokenize(rq_msg)
                X = bag_of_words(sentence, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(device)

                output = model(X)
                _, predicted = torch.max(output, dim=1)
                tag = tags[predicted.item()]

                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]

                if not torch.any(X):
                    return {'response':not_found, 'tag_name': tagName, 'chtbt_avatar': chtbt_avatar}
                elif prob.item() > 0.75:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            response = f"<div class='font-weight-bold'>{bot_name}:</div> {random.choice(intent['responses'])}"
                            return {'chtbt_avatar': chtbt_avatar,'response':response}
                else:
                    return {'chtbt_avatar': chtbt_avatar,'response':not_found, 'tag_name': tagName}

    @http.route(['/chatbot/details'], type='json', auth="public", methods=['POST'], website=True)
    def chatbot_details(self,**post):
        print("chatbot details")
        website_id = request.env['website'].get_current_website()
        chatbot_id = request.env['chatbot.chatbot'].sudo().search([('website_id', 'in', (website_id.id, False))], limit=1)

        tag_records = chatbot_id.chatbot_question_ids.mapped('tag').filtered(lambda l: l.is_show_chatbot)
        sorted_tags = sorted(tag_records, key=lambda tag: tag.sequence)
        tagName = [tag.name for tag in sorted_tags]
        return {'name': chatbot_id.name,'title':chatbot_id.title,
                'img': chatbot_id.chatbot_image, 'tagName':tagName,
                'chatbot_id': chatbot_id.id}
