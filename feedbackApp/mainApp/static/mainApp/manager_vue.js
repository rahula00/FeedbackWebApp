
let app = {};

let init = (app) => {

    // This is the Vue data.

    app.sel_or_del = () => {
        if(app.vue.checkAll){
            app.select_all()
        }
        else{
            app.deselect_all()
        }
    };

    app.select_all = () => {
        for (feedback of app.vue.feedbacks){
            if(feedback.in_range === true){
                feedback.delete = true
            }
        }
    };

    app.deselect_all = () => {
        for (feedback of app.vue.feedbacks){
            if(feedback.in_range === true){
                feedback.delete = false
            }
        }
    };

    app.check_sel = () => {
        var all = true
        for (feedback of app.vue.feedbacks){
            if(feedback.in_range === true){
                if(feedback.delete === false){
                    all = false
                }
            }
        }
        app.vue.checkAll = all
    }


    // Loops through feedback array to determine 
    // if delete button should be highlighted
    app.check_delete = () => {
        app.vue.showDelete = false
        for (feedback of app.vue.feedbacks){
            if(feedback.in_range === true){
                if(feedback.delete === true){
                    app.vue.showDelete = true
                }
            }
        }
    };


    // Sets new date range (after dropdown selection changed)
    app.set_range = () => {
        var id = document.getElementById("sel1")
        // newRange = value of dropdown
        var newRange = id.options[id.selectedIndex].value;
        app.vue.dateRange = newRange
        //console.log(app.vue.dateRange === '0')
        app.check_range()
    };

    // Displays/hides feedback depending on selected date range
    app.check_range = () => {
        var range = app.vue.dateRange
        if(range !== '0'){
            var today = new Date()
            today.setDate(today.getDate()-app.vue.dateRange)
            today.setHours(0, 0, 0, 0)
            var check_against = today
            for (feedback of app.vue.feedbacks){
                var date = new Date(feedback.created_at)
                if (date >= check_against){
                    feedback.in_range = true
                }
                else{
                    feedback.in_range = false
                    feedback.delete = false
                }
                // console.log(feedback.in_range)
            }
        }
        else{
            for (feedback of app.vue.feedbacks){
                feedback.in_range = true
            }
        }
        app.vue.showDelete = false
        app.check_delete()
    };


    // AJAX request to GET all feedback entries from db
    app.get_feedbacks = () => {
        $.ajax({
            url: '/ajax/get_feedbacks/',
            dataType: 'json',
            data:{'test': "last x days"},
            success: function (data) {

                app.vue.feedbacks = app.setShow(data)
                app.check_range()

            },
            error: function (data) {
                //console.log("failure")
            }
        })
    };

    // AJAX request to delete a single feedback entry based on id
    app.delete_feedback = (data) => {
            // data = feedback entry
            $.ajax({
                url: '/ajax/delete_feedback/',
                dataType: 'json',
                data:{
                    'id':data.id
                },
                // data.id = feedbackEntry.id
                success: function (data) {
                    //console.log("successfully deleted")
                },
                error: function (data) {
                    //console.log("failure")
                },
                complete: function(data){
                    app.init()
                }
            })
    };

    // Calls delete function on all selected feedbacks
    app.delete_feedbacks = () => {
        // delete confirmation
        var result = confirm("Are you sure you want to delete this?"); 
        if (result) {
            for (feedback of app.vue.feedbacks){
                if(feedback.delete === true){
                    app.delete_feedback(feedback)
                }
            }
            app.vue.showDelete = false
        }
        
    };

    // AJAX request to mark a single feedback entry as read
    app.mark_read = (data) => {
        //console.log(data)
        $.ajax({
            url: '/ajax/mark_read/',
            dataType: 'json',
            data:{
                'id':data.id
            },
            success: function (data) {
                //console.log("successfully marked read")
            },
            error: function (data) {
                //console.log("failure")

            }
        })
    };

    // Formats date from Django's iso-8601 format to something legible
    app.setDate = (data) => {
        var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        var d = new Date(data);
        var day = days[d.getDay()];
        var hr = d.getHours();
        var min = d.getMinutes();
        if (min < 10) {
            min = "0" + min;
        }
        var ampm = "a.m.";
        if( hr > 12 ) {
            hr -= 12;
            ampm = "p.m.";
        }
        var date = d.getDate();
        var month = months[d.getMonth()];
        var year = d.getFullYear();
        var x = month + " " + date + " " + year + ", " + hr + ":" + min + ampm
        //var x = day + " " + hr + ":" + min + ampm + " " + date + " " + month + " " + year;
        return x;
    }


    // Adds a new variable to each fb entry
    // feedback.show = show popup
    // feedback.show_date = formatted date
    // feedback.in_range = show feedback based on dropdown
    app.setShow = (data) => {
        MM = ["January", "February","March","April","May","June","July","August","September","October","November", "December"]

        for (feedback of data){
            feedback.show = false;
            feedback.delete = false;
            feedback.show_date = app.setDate(feedback.created_at);
            feedback.in_range = false;
            // Will hide SalesForceOp link if there is none
            // 'N/A' = default value in DB (models.py)
            if(feedback.salesforceOp==="N/A"){
                feedback.salesforceOp=false;
            };

        }
        return data  
    };


    // Global Vue vars
    app.data = {
        // Array of feedbacks in JSON format(GET from AJAX req)
        feedbacks: [],
        // Show/Hide delete button
        showDelete: false,
        // How far back to show feedback entries in days
        // Default is 7 days
        dateRange:7,
        checkAll: false,
    };

    // Methods called from within manager.html
    app.methods = {
        get_feedbacks: app.get_feedbacks,
        set_range: app.set_range,
        mark_read: app.mark_read,
        delete_feedbacks: app.delete_feedbacks,
        check_delete: app.check_delete,
        sel_or_del: app.sel_or_del,
        select_all: app.select_all,
        deselect_all: app.deselect_all,
        check_sel: app.check_sel,
    };

    // Changed delimiters to '[[',']]' from '{{','}}'
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
        delimiters: ['[[', ']]'],

    });

    // Initialize page with GET request for feedbacks
    app.init = () => {
        app.get_feedbacks();
    };

    // Call init() on page load
    app.init();
};

init(app);

