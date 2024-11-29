/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

  // var ajax = require('web.ajax');
  var running = false;
  var global_img;

  publicWidget.registry.ChatbotFunc = publicWidget.Widget.extend({
    selector: '#chatbot',
    events: {
      'click .chatbot_icon_btn': '_OnclickChatbot',
      'click .chatbot_close_icon': '_OnclickChatbot',
      'click #input_send_request': '_OnclickChatSend',
      'keyup .input-message': '_onChatInputMessageKeyUp',
      'click .btn_tag_secondary': '_OnTagButton',
    },

    start: function() {
      var title_msg = false
      this._replaceSpanText(title_msg);
      return this._super.apply(this, arguments);
    },
    _replaceSpanText: function(title_msg) {
      jsonrpc("/chatbot/details")
        .then(function(result) {
          if (result) {
            if (title_msg == false) {
              var div = document.createElement("div");
              global_img = '<img src="/web/image/chatbot.chatbot/'+ result['chatbot_id'] + '/chatbot_image" alt="Chatbot" style="height: 27px;width: 27px;"/>'
              var imgAvatar = '<img src="/web/image/chatbot.chatbot/'+ result['chatbot_id'] + '/chatbot_image" alt="Chatbot" style="height: 27px;width: 27px;"/>'
              div.innerHTML = "<div class='chatbot_avatar'><span class='avatar'>" + imgAvatar + "</span></div><div class='chat-message-received'><div class='font-weight-bold'>" + result['name'] + ":</div>" + "<p>" + result['title'] + "</p>" + "</div>";
              div.className = "chat-message-div";
              document.getElementById("message-box").appendChild(div);
              document.getElementById("message-box").scrollTop = document.getElementById(
                "message-box"
              ).scrollHeight;
              running = false;

              var outerdiv = document.createElement("div");
              outerdiv.id = "content_area";
              document.getElementById("message-box").appendChild(outerdiv);
              var inndiv = document.createElement("div");
              var frag = document.createDocumentFragment();
              for (var i = 0; i < result['tagName'].length; i++) {
                var button = document.createElement("button");
                button.className = "btn_tag_secondary"
                button.value = result['tagName'][i];
                button.name = result['tagName'][i];
                button.innerHTML = result['tagName'][i];
                frag.appendChild(button);
              }
              document.getElementById("content_area").appendChild(frag);
            }
          }
        });
    },
    _OnclickChatbot: function(ev) {
      var chatbot_card = $('.chatbot_card');
      if(chatbot_card.hasClass('collapsed')){
        chatbot_card.removeClass('collapsed');
        $('#my-custom-open').addClass('my-custom-open');
        $('.chatbot_icon').addClass('d-none');
        $('.chatbot_close_icon').removeClass('d-none');
        chatbot_card.removeClass('d-none');
      }
      else {
        chatbot_card.addClass('collapsed');
        $('#my-custom-open').removeClass('my-custom-open');
        $('.chatbot_icon').removeClass('d-none');
        $('.chatbot_close_icon').addClass('d-none');
        chatbot_card.addClass('d-none');
      }
    },
    _OnclickChatSend: function(ev) {
      if (running == true) return;
      var msg = document.getElementById("message").value;
      if (msg == "") return;
      running = true;
      this._addMsg(msg);
      window.setTimeout(this._addResponseMsg, 1000, msg);
    },

    _onChatInputMessageKeyUp: function(ev) {
      if (ev.which === 13) {
        this._OnclickChatSend();
        ev.preventDefault();
      }
    },
    _addMsg: function(msg) {
      var div = document.createElement("div");
      div.innerHTML =
        "<span style='flex-grow:1'></span><div class='chat-message-sent'>" +
        msg +
        "</div>";
      div.className = "chat-message-div";
      document.getElementById("message-box").appendChild(div);
      document.getElementById("message").value = "";
      document.getElementById("message-box").scrollTop = document.getElementById(
        "message-box"
      ).scrollHeight;
    },
    
    _addResponseMsg: function(msg) {
      jsonrpc("/chatbot/message/request",{
          'request_msg': msg,
          'is_direct_tag': false
          
        })
        .then(function(modal) {
          if (modal) {
              var div = document.createElement("div");
              var imgAvatar = '<img src="data:image/png;base64,' + modal['chtbt_avatar'] + '" alt="My Avatar" style="height: 27px;width: 27px;"/>'
              div.innerHTML = "<div class='chatbot_avatar'><span class='avatar'>" + imgAvatar + "</span></div><div class='chat-message-received'>" + modal['response'] + "</div>";
              div.className = "chat-message-div";
              document.getElementById("message-box").appendChild(div);
              document.getElementById("message-box").scrollTop = document.getElementById(
                "message-box"
              ).scrollHeight;
              running = false;

              if(modal['tag_name']){
                  var outerdiv = document.createElement("div");
                  outerdiv.className = "content_area1";
                  document.getElementById("message-box").appendChild(outerdiv);
                  var inndiv = document.createElement("div");
                  var frag = document.createDocumentFragment();
                  for (var i = 0; i < modal['tag_name'].length; i++) {
                    var button = document.createElement("button");
                    button.className = "btn_tag_secondary"
                    button.style.width = "auto"
                    button.style.margin = "2px 3px 3px"
                    button.value = modal['tag_name'][i];
                    button.name = modal['tag_name'][i];
                    button.innerHTML = modal['tag_name'][i];
                    frag.appendChild(button);
                  }
                  outerdiv.appendChild(frag);
              }
            }
        });
    },
    _OnTagButton: function(ev) {
      var tag_value = $(ev.currentTarget).getAttributes().name;
      this._addMsg(tag_value)
      jsonrpc("/chatbot/message/request",{
          'request_msg': tag_value,
          'is_direct_tag': true

        })
        .then(function(modal) {
          if (modal) {
            var div = document.createElement("div");
            var imgAvatar = '<img src="data:image/png;base64,' + modal['chtbt_avatar'] + '" alt="My Avatar" style="height: 27px;width: 27px;"/>'
            div.innerHTML = "<div class='chatbot_avatar'><span class='avatar'>" + imgAvatar + "</span></div><div class='chat-message-received'>" + modal['response'] + "</div>";
            div.className = "chat-message-div";
            document.getElementById("message-box").appendChild(div);
            document.getElementById("message-box").scrollTop = document.getElementById(
              "message-box"
            ).scrollHeight;
            running = false;
          }
        });
    },
  });
