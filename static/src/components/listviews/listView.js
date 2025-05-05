/** @odoo-module **/

import { Component, useState , onWillUnmount} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "TEST_APP.listview";

    setup() {
        this.state = useState({ 'records': [] });
        this.orm = useService('orm');
        // this.rpc = useService("rpc");
        this.load_records();
        this.interval=setInterval(() => this.load_records(), 3000);
        onWillUnmount(()=> clearInterval(this.interval));
    }

    async load_records() {
        const result = await this.orm.searchRead('property', [], ['id','ref', 'name', 'date_availability', 'is_late', 'bedrooms', 'state']);
        this.state.records = result;
    }

    // async load_records() {
    //     const result = await this.rpc("/web/dataset/call_kw/property/search_read", {
    //         params: {
    //             model: "property",
    //             method: "search_read",
    //             args: [[]],
    //             kwargs: {
    //                 fields: ["id", "ref", "name", "date_availability", "is_late", "bedrooms", "state"],
    //             },
    //         }
    //     });
    //     this.state.records = result;
    // }

    async delete_record(recordId) {
        try {
            await this.orm.call("property", "unlink", [[recordId]]);
            // Refresh list after delete
            await this.load_records();
        } catch (error) {
            console.error("Failed to delete record:", error);
        }
    }

}

registry.category("actions").add("TEST_APP.action_list_view", ListViewAction);
