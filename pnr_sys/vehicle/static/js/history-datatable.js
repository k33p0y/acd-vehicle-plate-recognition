$(function (){
    // error function
    var showError = function(error){
        Swal.fire({
            type: 'error',
            title: 'Oops...',
            text: error,
        })
    };

    // filter history function
    var filterHistory = function(){
        var date_from = $('#date_from').val();
        var date_to = $('#date_to').val();

        if(!date_from || !date_to) { // show error if date_from or date_to is empty
            showError('Dates from and to are required.')
        } else {
            if(moment(date_from).isSameOrBefore(date_to)) { // if dates are valid, run ajax request
                getHistoryLogJson(date_from, date_to)
            } else showError('Date To must come after date From.'); // show error if date_to comes before date_from
        }
    };
    
    // get history list as JSON via ajax request
    var getHistoryLogJson = function(date_from, date_to){
        $.ajax({
            url: '/history-list/json/',
            data: {
                'date_from': date_from,
                'date_to': date_to,
            },
            success: function(response){
                // call createDataTable function
                createDataTable(response)
            },
            error: function(a, b, error){
                showError(error);
            }
        });
    }

    // create datatable after ajax success
    var createDataTable = function(response) {
        // if patient utilization datatable exist, destroy datatable
        if ($.fn.DataTable.isDataTable( '#table-history')) {
            $('#table-history').DataTable().destroy();
        }

        $('#table-history').DataTable({
            order: [[3, 'desc']],
            searching: true,
            data: response,
            processing: true,
            language: {
                loadingRecords: '&nbsp;',
                processing: '<div class="fas fa-cog fa-spin text-primary"></div>',
            },
            columns: [
                { // vehicle plate
                    data: "vehicle__plate",
                },
                { // vehicle type
                    data: "vehicle__v_type"},
                { // vehicle color
                    data: "vehicle__color",
                },
                { // Date time-in
                    data: "datetime_in",
                    render: function(data, type, row, meta){
                        if(type === 'display'){
                            data = moment(row.datetime_in).format('MM-DD-YYYY HH:mm');
                        }
                        return data;
                    }
                },
                { // Date time-out
                    data: "datetime_out",
                    render: function(data, type, row, meta){
                        if(type === 'display'){
                            data = moment(row.datetime_out).format('MM-DD-YYYY HH:mm');
                        }
                        return data;
                    }
                },
                { // Purpose
                    data: "reason",
                },
                { // // Logged by
                    data: "edited_by__last_name",
                    render: function(data, type, row, meta){
                        if(type === 'display'){
                            data = '';
                            if (row.edited_by__last_name) data += `${row.edited_by__last_name}, `
                            if (row.edited_by__first_name) data += `${row.edited_by__first_name}`
                        }
                        return data;
                    }
                }, 
            ],
            columnDefs: [
                {
                    searchable: false,
                    targets: [3, 4]
                },
            ],
            // dom: 'Bfrtip', // export to excel
            // buttons: [
            //     {
            //         extend: 'excelHtml5',
            //         title: `Patient Utilization`,
            //         // messageTop: `<span>The quick brown fox</span>`,
            //         text: `<i class="fas fa-download text-primary fa-lg"></i> <span class='text-primary font-weight-bold'>Export to Excel</span>`,
            //         exportOptions: {
            //             columns: [12, 0, 1, 2, 4, 3, 5, 6, 8, 7, 10],
            //             format: {
            //                 header: function (data, columnIndex) {
            //                     if (columnIndex === 12) {
            //                         return 'No.'
            //                     } else if (columnIndex === 0) {
            //                         return 'Date Utilization'
            //                     } else if (columnIndex === 1) {
            //                         return 'Control Number'
            //                     } else if (columnIndex === 2) {
            //                         return 'Patient'
            //                     } else if (columnIndex === 4) { 
            //                         return 'Address'
            //                     } else if (columnIndex === 5) { 
            //                         return 'Assistance'
            //                     } else return data;
            //                 },
            //                 body: function (data, rowIndex, columnIndex, node) {
            //                     if (columnIndex === 0) { // No. column
            //                         return data = rowIndex+1;
            //                     } else return data;
            //                 }
            //             },
            //         }
            //     }
                    
            // ],
        });
    };

    // execute on page load
    var startOfMonth = moment().startOf('month').format('YYYY-MM-DD');
    var endOfMonth = moment().endOf('month').format('YYYY-MM-DD');
    getHistoryLogJson(startOfMonth, endOfMonth)

    $('#btn-filter-history').on('click', filterHistory)
});