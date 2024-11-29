/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted} from  "@odoo/owl";

class DairyKiosk extends Component {
    setup(){
        this.orm = useService("orm");
        this.current_date = new Date().toLocaleString();
        this.actionService = useService("action");
        this.user = session.name;
        this.selected_dairy_id = null;
        this.mydairy = null;
        this.myAnimal = [];
        this.dairies = [];
        this.confButtonAdded = false;
        this.animalRate = {};
        
        onWillStart(async () => {
            await this.getdairy()
    
        });

        onMounted(() => {
          setTimeout(async () => {
                if (this.dairies.length === 1) {
                    this.selected_dairy_id = this.dairies[0].id;
                    this.mydairy = this.dairies[0].name;
                    const AnimalIds = this.dairies[0].supported_animal_ids;
                    const sup_Animals = await this.orm.call(
                        "animal.animal",
                        "read",
                        [AnimalIds, ['name']],
                    );
                    this.myAnimal = sup_Animals.map(animal => animal.name);
                    await this.getRatePerFat();
                    if(!this.confButtonAdded){
                        this.addConfirmButton();
                        this.confButtonAdded = true;
                    }
                }
            }, 100);
        });

    }

    exit_kiosk(ev) {
        window.location.href = '/web#action=do_dairy_management.action_milk_intake_management';
    }

    exit(ev) {
        this.env.config.historyBack();
    }
    
    async getdairy() {
        const dairies = await this.orm.call(
            "milk.intake.management",
            "get_dairies",
        );
        this.dairies = dairies;
    } 

    async getRatePerFat() {
        const ratePerFatData = await this.orm.call(
            "rate.management",
            "get_rate_per_fat",
            [this.selected_dairy_id]
        );
        this.animalRate = ratePerFatData;
    }

    async handleDairySelection(event) {
        this.selected_dairy_id = parseInt(event.target.value);
        const selectedDairy = this.dairies.find(dairy => dairy.id === this.selected_dairy_id);
        if (selectedDairy) {
            this.mydairy = selectedDairy.name;
            const supportedAnimalIds = selectedDairy.supported_animal_ids;
            const supportedAnimals = await this.orm.call(
                "animal.animal",
                "read",
                [supportedAnimalIds, ['name']],
            );
            this.myAnimal = supportedAnimals.map(animal => animal.name);
            await this.getRatePerFat();
            if(!this.confButtonAdded){
                this.addConfirmButton();
                this.confButtonAdded = true;
            }
        }
        else {
            this.removeConfirmButton();
        }
    }

    addConfirmButton() {
        const conf_button = document.createElement("button");
        conf_button.innerHTML = "Next (Rate)";
        conf_button.className = "btn btn-block btn-primary m-1 w-50";
        conf_button.onclick = () => {
            this.actionService.doAction('do_dairy_mgmt.customer_dairy_action', {
                additionalContext: {dairy_id : this.selected_dairy_id ,dairy: this.mydairy , 
                animals: this.myAnimal, milkRate: this.animalRate},
        });
        };
        console.log("do_dairy_mgmt",this.animalRate,this.myAnimal);
		document.querySelector(".confirm").appendChild(conf_button);
    }


    removeConfirmButton() {
        const btn = document.querySelector(".confirm button");
        if (btn) {
            btn.remove();
            this.confButtonAdded = false;
        }
    }
}

DairyKiosk.template = "do_dairy_mgmt.clientaction";

registry.category("actions").add("do_dairy_mgmt.DairyKioskModeAction", DairyKiosk);
export default DairyKiosk;