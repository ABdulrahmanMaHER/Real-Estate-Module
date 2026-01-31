/** @odoo-module */

import { Component, onWillStart, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormView } from "../formView/formView";

export class ListViewAction extends Component {
    static template = "real_estate.ListView";
    static components = { FormView }

    static props = ["*"];

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            records: [],
            loading: true,
            filter: "all",
            showformview: false,
        });

        onWillStart(this.loadRecords);

        // Uncomment if you want auto-refresh
        // this.interval_id = setInterval(() => { this.loadRecords(); }, 10000);
        // onWillUnmount(() => { clearInterval(this.interval_id); });
    }

    async loadRecords() {
        try {
            this.state.loading = true;

            let domain = [];

            if (this.state.filter === "has_garden") {
                domain.push(["garden", "=", true]);
            } else if (this.state.filter === "late") {
                domain.push(["is_late", "=", true]);
            }

            const data = await this.orm.searchRead(
                "property",
                domain,
                ['id','ref','name','bedrooms','garden','expected_selling_date','state','is_late'],
                { order: "id asc" }
            );

            this.state.records = data;

        } catch (e) {
            console.error("Error loading records:", e);
        } finally {
            this.state.loading = false;
        }
    }

    async deleteRecords(ev) {
        try {
            const id = parseInt(ev.target.dataset.id);
            await this.orm.unlink("property", [id]);
            await this.loadRecords();
        } catch (e) {
            console.error("Error deleting record:", e);
        }
    }

    loadFormView() {
        this.state.showformview = !this.state.showformview;
    }

    async onFormSave() {
        // Reload records after form save
        await this.loadRecords();
        // Close form
        this.state.showformview = false;
    }

    onFormCancel() {
        // Close form
        this.state.showformview = false;
    }
}

registry.category("actions").add("real_estate.action_list_views", ListViewAction);