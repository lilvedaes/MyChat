$(function(){
    var url = "http://127.0.0.1:5000/messages";


    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url , //get
            insertUrl: url , //post
            updateUrl: url , //put
            deleteUrl: url , //delete
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        editing: {
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },
        remoteOperations: {
            sorting: true,
            paging: true
        },
        paging: {
            pageSize: 12
        },
        pager: {
            showPageSizeSelector: true,
            allowedPageSizes: [8, 12, 20]
        },
        columns: [{
            dataField: "id",
            dataType: "number",
            allowEditing: true
        }, {
            dataField: "message"
        }, {
            dataField: "sendby"
        }, {
            dataField: "receiveby"
        }, ],
    }).dxDataGrid("instance");
});
