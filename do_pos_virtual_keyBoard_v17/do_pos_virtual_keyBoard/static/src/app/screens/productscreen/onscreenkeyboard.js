/** @odoo-module */
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Chrome } from "@point_of_sale/app/pos_app";

export class OnscreenKeyboardSimple extends Component {
    static template = "do_pos_virtual_keyBoard.OnscreenKeyboardSimple";

    setup() {
        super.setup(...arguments);
    }

    keyboardClose(event) {
        this.hide();
    }

    keyboardClick(event) {
        var self = this;
        var $this = $(event.currentTarget);
        var character = $this.html(); // If it's a lowercase letter, nothing happens to this variable

        if ($this.hasClass('left-shift') || $this.hasClass('right-shift')) {
            self.toggleShift();
            return false;
        }

        if ($this.hasClass('capslock')) {
            self.toggleCapsLock();
            return false;
        }

        if ($this.hasClass('delete')) {
            self.deleteCharacter();
            return false;
        }

        if ($this.hasClass('numlock')) {
            self.toggleNumLock();
            return false;
        }

        // Special characters
        if ($this.hasClass('symbol')) character = $('span:visible', $this).html();
        if ($this.hasClass('space')) character = ' ';
        if ($this.hasClass('tab')) character = "\t";
        if ($this.hasClass('return')) character = "\n";

        // Uppercase letter
        if ($this.hasClass('uppercase')) character = character.toUpperCase();

        // Remove shift once a key is clicked.
        self.removeShift();

        self.writeCharacter(character);
    }
    connect(target) {
        var self = this;
        this.$target = $(target);
        self.show();

        
    }
        generateEvent(type, key) {
            var event = document.createEvent("KeyboardEvent");
            var initMethod = event.initKeyboardEvent ? 'initKeyboardEvent' : 'initKeyEvent';
            event[initMethod](type,
                true, //bubbles
                true, //cancelable
                window, //viewArg
                false, //ctrl
                false, //alt
                false, //shift
                false, //meta
                ((typeof key.code === 'undefined') ? key.char.charCodeAt(0) : key.code),
                ((typeof key.char === 'undefined') ? String.fromCharCode(key.code) : key.char)
            );
            return event;

        }

        // Write a character to the input zone
        writeCharacter(character) {
            var input = this.$target[0];
            input.dispatchEvent(this.generateEvent('keypress', { char: character }));
            if (character !== '\n') {
                input.value += character;
            }
            input.dispatchEvent(this.generateEvent('keyup', { char: character }));
            input.dispatchEvent(this.generateEvent('input', { char: character }));
        }

        // Removes the last character from the input zone.
        deleteCharacter() {
            var input = this.$target[0];
            input.dispatchEvent(this.generateEvent('keypress', { code: 8 }));
            input.value = input.value.substr(0, input.value.length - 1);
            input.dispatchEvent(this.generateEvent('keyup', { code: 8 }));
        }


        show() {
            
            $('.keyboard_frame').show().css({ 'height': '235px' });
            console.log("fgfgfgfg",this);
        }

        // Makes the keyboard hide by sliding to the bottom of the screen.
        hide() {
            $('.keyboard_frame')
                .css({ 'height': '0' })
                .hide();
            this.reset();
        }
        toggleShift() {
            $('.letter').toggleClass('uppercase');
            $('.symbol span').toggle();

            this.shift = (this.shift === true) ? false : true;
            this.capslock = false;
        }

        //what happens when capslock is pressed : toggle case, set capslock
        toggleCapsLock() {
            $('.letter').toggleClass('uppercase');
            this.capslock = true;
        }

        //What happens when numlock is pressed : toggle symbols and numlock label 
        toggleNumLock() {
            $('.symbol span').toggle();
            $('.numlock span').toggle();
            this.numlock = (this.numlock === true) ? false : true;
        }

        //After a key is pressed, shift is disabled. 
        removeShift() {
            if (this.shift === true) {
                $('.symbol span').toggle();
                if (this.capslock === false) $('.letter').toggleClass('uppercase');

                this.shift = false;
            }
        }

        // Resets the keyboard to its original state; capslock: false, shift: false, numlock: false
        reset() {
            if (this.shift) {
                this.toggleShift();
            }
            if (this.capslock) {
                this.toggleCapsLock();
            }
            if (this.numlock) {
                this.toggleNumLock();
            }
        }

    }

Chrome.components = {
    ...Chrome.components,
    OnscreenKeyboardSimple,
};
