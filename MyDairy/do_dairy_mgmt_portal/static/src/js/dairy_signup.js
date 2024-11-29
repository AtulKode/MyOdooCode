/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.DairyWidget = publicWidget.Widget.extend({
    selector: '#grad1',

    events: {
        'click .next': '_nextButtonClick',
        'click .previous': '_previousButtonClick',
        'click #owner_add' : 'fillOwnerAddress',
        'change #incharge_add' : 'fillInchargeAddress',
        'change #owner_is_incharge' : 'ownerIsIncharge'
    },

    ownerIsIncharge() {
        var isChecked = $("#owner_is_incharge").is(":checked");
        var hideform = $(".incharge_form");
        if(isChecked){
            hideform.hide();
        }
        else{
            hideform.show();
        }
    },

    fillOwnerAddress()
    {
        var check_bool=$("#owner_add").is(":checked");
        if(check_bool==true){
            var addr = document.getElementById("d_address").value;
            var copyaddr = addr;
            document.getElementById("o_address").value = copyaddr;           
        }
        else{
            document.getElementById("o_address").value = '';           
        }
    },

    fillInchargeAddress()
    {
        var selected = $('option:selected', '#incharge_add').attr('class');
        if(selected == "copy_d_add"){
            var d_addr = document.getElementById("d_address").value;
            var copyd_addr = d_addr;
            document.getElementById("inc_address").value = copyd_addr;
        }
        else if(selected == "copy_o_add"){
            var o_addr = document.getElementById("o_address").value;
            var copyd_o_addr = o_addr;
            document.getElementById("inc_address").value = copyd_o_addr;            
        }
    },

_nextButtonClick(ev) {
    var current_fs = $(ev.currentTarget).parent();
    var next_fs = current_fs.next();
    var missing_vals = [];
    var isCheck = $("#owner_is_incharge").is(":checked");

    current_fs.find('input').each(function (idx, inp) {
        if (!inp.value) {
            missing_vals.push(inp.name);
            $(inp).css('border', '2px solid red');
        }
        else if(inp.value.length<4 && inp.type!='checkbox'){
            missing_vals.push(inp.name);
            $(inp).css('border', '2px solid red');
            alert("length must be greater than 4");
        }
        else if (inp.type == 'tel' && (!$.isNumeric(inp.value) || inp.value.length < 6 || inp.value.length > 12)) {
            missing_vals.push(inp.name);
            $(inp).css('border', '2px solid red');
        
            alert("Contact No should be a digit and its length should be between 6 to 12 characters");
        }
        else {
            $(inp).css({ 'border': '', 'opacity': '' });
        }
    });

    if (!isCheck && missing_vals.length) {
        ev.preventDefault();
        return;
    }

    // Add Class Active
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    next_fs.show();

    // Hide the current fieldset with style
    current_fs.animate({ opacity: 0 }, {
        step: function (now) {
            // For making fieldset appear animation
            var opacity = 1 - now;

            current_fs.css({
                'display': 'none',
                'position': 'relative'
            });
            next_fs.css({ 'opacity': opacity });
        },
        duration: 600
    });
},


    _previousButtonClick(ev) {
        var current_fs = $(ev.currentTarget).parent();
        var previous_fs = current_fs.prev();

        // Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        // Show the previous fieldset
        previous_fs.show();

        // Hide the current fieldset with style
        current_fs.animate({ opacity: 0 }, {
            step: function (now) {
                // For making fieldset appear animation
                var opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({ 'opacity': opacity });
            },
            duration: 600
        });
    },
});
