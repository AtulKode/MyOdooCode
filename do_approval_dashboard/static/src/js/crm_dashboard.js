/** @odoo-module */
import { registry} from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, onMounted} = owl
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { WebClient } from "@web/webclient/webclient";
export class SMSDashboard extends Component {

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");

        // Variables for filters
        this.selectedDate = null;
        this.selectedStage = null;
        this.selectedApprovalType = null;

        // Variables for counts and average times
        this.my_request_count = 0;
        this.sub_requests_count =0;
        this.approve_requests_count=0;
        this.inprogress_requests_count=0;
        this.paid_requests_count=0;
        this.rejected_requests_count=0;

        this.my_request_review_count = 0;
        this.my_request_all_count = 0;
        this.my_request_deleted_count = 0;

        // Variables for Average Times
        this.avg_time_submit_to_paid = 0;
        this.avg_time_submit_to_all_approved = 0;
        this.avg_time_submit_to_first_approval = 0;

        onWillStart(async () => {
            await this.fetchRequestCounts();
            await this.fetchAverageTimes();
        });

        onMounted(this.onMounted);
    }

    // Method to update filters and refetch data
    updateFilters() {
        this.selectedStage = $('#stageFilter').val();
        this.selectedDate = $('#dateFilter').val();
        this.selectedApprovalType = $('#approvalTypeFilter').val();
        this.fetchAverageTimes();
        this.fetchRequestCounts();
    }

    // Fetch request counts
    async fetchRequestCounts() {
        const result = await jsonrpc('/web/dataset/call_kw/approval.request/get_all_req_count', {
            model: "approval.request",
            method: "get_all_req_count",
            args: [{}],
            kwargs: {},
        });
        this.my_request_count = result['my_request_count'];
        this.my_request_review_count = result['my_request_review_count'];
        this.my_request_all_count = result['my_request_all_count'];
        this.my_request_deleted_count = result['my_request_deleted_count'];

        const result_submitted = await jsonrpc('/web/dataset/call_kw/approval.request/get_submitted_requests', {
            model: "approval.request",
            method: "get_submitted_requests",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.sub_requests_count = result_submitted;

        const result_approved = await jsonrpc('/web/dataset/call_kw/approval.request/get_approved_requests', {
            model: "approval.request",
            method: "get_approved_requests",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.approve_requests_count = result_approved;

        const result_inprogress = await jsonrpc('/web/dataset/call_kw/approval.request/get_inprogress_requests', {
            model: "approval.request",
            method: "get_inprogress_requests",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.inprogress_requests_count = result_inprogress;

        const result_paid = await jsonrpc('/web/dataset/call_kw/approval.request/get_paid_requests', {
            model: "approval.request",
            method: "get_paid_requests",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.paid_requests_count = result_paid;

        const result_rejected = await jsonrpc('/web/dataset/call_kw/approval.request/get_rejected_requests', {
            model: "approval.request",
            method: "get_rejected_requests",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.rejected_requests_count = result_rejected;
        this.render();
    }

    // Fetch average times based on the selected filters
    async fetchAverageTimes() {
        const resultPaid = await jsonrpc('/web/dataset/call_kw/approval.request/get_avg_time_submit_to_paid', {
            model: "approval.request",
            method: "get_avg_time_submit_to_paid",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.avg_time_submit_to_paid = resultPaid;

        const resultAllApproved = await jsonrpc('/web/dataset/call_kw/approval.request/get_avg_time_submit_to_all_approved', {
            model: "approval.request",
            method: "get_avg_time_submit_to_all_approved",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.avg_time_submit_to_all_approved = resultAllApproved;
        const resultFirstApproval = await jsonrpc('/web/dataset/call_kw/approval.request/get_avg_time_submit_to_first_approval', {
            model: "approval.request",
            method: "get_avg_time_submit_to_first_approval",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        });
        this.avg_time_submit_to_first_approval = resultFirstApproval;
        this.render();
    }

    // On mounted, render graphs
    async onMounted() {
        this.render_sales_activity_graph();
        this.render_annual_chart_graph();
    }

    exportReport(){
        return
    }

    all_approval(e){

    var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/get_all_requests_review', {
            model: "approval.request",
            method: "get_all_requests_review",
            args: [{}],
            kwargs: {},
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });



    }

    view_approved_req(e){

        var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/view_approved_request', {
            model: "approval.request",
            method: "view_approved_request",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });       
    }

    view_in_progress_req(e){

        var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/view_in_progress_request', {
            model: "approval.request",
            method: "view_in_progress_request",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });       
    }


    view_paid_req(e){

        var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/view_paid_request', {
            model: "approval.request",
            method: "view_paid_request",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });       
    }

    view_rejected_req(e){

        var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/view_rejected_request', {
            model: "approval.request",
            method: "view_rejected_request",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });       
    }

    view_submitted_req(e){

        var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/view_submitted_request', {
            model: "approval.request",
            method: "view_submitted_request",
            args: [],
            kwargs: {
                'date': this.selectedDate,
                'stage': this.selectedStage,
                'approval_type': this.selectedApprovalType
            },
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });       
    }
    approval_to_review(e){

          var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/get_my_requests_review', {
            model: "approval.request",
            method: "get_my_requests_review",
            args: [{}],
            kwargs: {},
        }).then(function(result) {
            self.action.doAction({
            name: _t("Approval Requests To Review"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })
    });
    }

    deleted_approval_req(e){
    var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/deleted_my_requests', {
            model: "approval.request",
            method: "deleted_my_requests",
            args: [{}],
            kwargs: {},
        }).then(function(result) {
            self.action.doAction({
            name: _t("Deleted Requests"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })

        });


    }


    total_message(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        jsonrpc('/web/dataset/call_kw/approval.request/get_my_requests', {
            model: "approval.request",
            method: "get_my_requests",
            args: [{}],
            kwargs: {},
        }).then(function(result) {
            self.action.doAction({
            name: _t("My Requests"),
            type: 'ir.actions.act_window',
            res_model: 'approval.request',
            view_mode: 'tree',
            views: [
                [false, 'list'],
            ],
            domain: result,
            target: 'current',
        })

        });

    }

        render_sales_activity_graph() {
        var self = this
        var ctx = $(".sales_activity");
        jsonrpc('/web/dataset/call_kw/approval.request/get_request_by_stage', {
            model: "approval.request",
            method: "get_request_by_stage",
            args: [{}],
            kwargs: {},
        }).then(function(arrays) {
            var data = {
                labels: arrays[1],
                datasets: [{
                    label: "",
                    data: arrays[0],
                    backgroundColor: [
                        "#003f5c",
                        "#2f4b7c",
                        "#f95d6a",
                        "#665191",
                        "#d45087",
                        "#ff7c43",
                        "#ffa600",
                        "#a05195",
                        "#6d5c16"
                    ],
                    borderColor: [
                        "#003f5c",
                        "#2f4b7c",
                        "#f95d6a",
                        "#665191",
                        "#d45087",
                        "#ff7c43",
                        "#ffa600",
                        "#a05195",
                        "#6d5c16"
                    ],
                    borderWidth: 1
                }, ]
            };
            //options
            var options = {
                responsive: true,
                title: false,
                legend: {
                    display: true,
                    position: "right",
                    labels: {
                        fontColor: "#333",
                        fontSize: 16
                    }
                },
                scales: {
                    yAxes: [{
                        gridLines: {
                            color: "rgba(0, 0, 0, 0)",
                            display: false,
                        },
                        ticks: {
                            min: 0,
                            display: false,
                        }
                    }]
                }
            };
            //create Chart class object
            var chart = new Chart(ctx, {
                type: "doughnut",
                data: data,
                options: options
            });
        });
    }




    render_annual_chart_graph() {
        var self = this
        var ctx = $(".annual_target");
        jsonrpc('/web/dataset/call_kw/approval.request/get_request_by_stage', {
            model: "approval.request",
            method: "get_request_by_stage",
            args: [{}],
            kwargs: {},
        }).then(function(arrays) {
            var data = {
                labels: arrays[1],
                datasets: [{
                    label: "",
                    data: arrays[0],
                    backgroundColor: [
                        "#003f5c",
                        "#f95d6a",
                        "#ff7c43",
                        "#6d5c16"
                    ],
                    borderColor: [
                        "#003f5c",
                        "#f95d6a",
                        "#ff7c43",
                        "#6d5c16"
                    ],
                    borderWidth: 1
                }, ]
            };
            //options
            var options = {
                responsive: true,
                title: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 0
                        }
                    }]
                }
            };
            //create Chart class object
            var chart = new Chart(ctx, {
                type: "bar",
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false //This will do the task
                    },
                }
            });
        });
    }
}

SMSDashboard.template = "SMSDashboard"
registry.category("actions").add("approval_dashboard", SMSDashboard);