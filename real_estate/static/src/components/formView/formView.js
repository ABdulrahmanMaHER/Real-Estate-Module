/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FormView extends Component {
    static template = "real_estate.FormView";

    static props = {
        onSave: { type: Function, optional: true },
        onCancel: { type: Function, optional: true },
    };

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            name: "",
            postcode: "",
            date_availability: ""
        });
    }

    async createRecords() {
        try {
            await this.orm.create("property", [{
                name: this.state.name,
                post_code: this.state.postcode,
                date_availability: this.state.date_availability
            }]);

            // Clear form after successful creation
            this.Cancel();

            // Notify parent to reload records
            if (this.props.onSave) {
                await this.props.onSave();
            }

        } catch (e) {
            console.error("Error Creating records:", e);
        }
    }

    Cancel() {
        this.state.name = "";
        this.state.postcode = "";
        this.state.date_availability = "";

        // Notify parent to close form
        if (this.props.onCancel) {
            this.props.onCancel();
        }
    }
}