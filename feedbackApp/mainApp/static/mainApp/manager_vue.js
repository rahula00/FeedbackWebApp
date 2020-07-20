let app = {};

let init = (app) => {

    // This is the Vue data.
    

    app.check_delete = () => {
        app.vue.showDelete = false
        for (feedback of app.vue.feedbacks){
            if(feedback.delete === true){
                app.vue.showDelete = true;

            }
        }
    };

    app.get_feedbacks = () => {
        $.ajax({
            url: '/ajax/get_feedbacks/',
            dataType: 'json',
            success: function (data) {

                app.vue.feedbacks = app.reindex(app.setShow(data))

            },
            error: function (data) {
                console.log("failure")
            }
        })
    };

    app.delete_feedback = (data) => {
        $.ajax({
            url: '/ajax/delete_feedback/',
            dataType: 'json',
            data:{
                'id':data.id
            },
            success: function (data) {
                console.log("successfully deleted")
            },
            error: function (data) {
                console.log("failure")
            },
            complete: function(data){
                app.init()
            }
        })
    };

    app.delete_feedbacks = () => {
        for (feedback of app.vue.feedbacks){
            if(feedback.delete === true){
                app.delete_feedback(feedback)
            }
        }
        app.vue.showDelete = false
    };

    app.mark_read = (data) => {
        console.log(data)
        $.ajax({
            url: '/ajax/mark_read/',
            dataType: 'json',
            data:{
                'id':data.id
            },
            success: function (data) {
                console.log("successfully marked read")
            },
            error: function (data) {
                console.log("failure")

            }
        })
    };

    app.setShow = (data) => {
        for (feedback of data){
            feedback.show = false;
            feedback.delete = false;
            if(feedback.salesforceOp==="N/A"){
                feedback.salesforceOp=false;
            }
        }
        return data  
    };

    app.reindex = (a) => {
        let idx = 0;
        for (p of a) {
            p._idx = idx++;
        }
        return a;
    };

    app.data = {
        feedbacks: [],
        showDelete: false,
        popupActivo:false,
    };

   app.methods = {
        get_feedbacks: app.get_feedbacks,
        delete_feedback: app.delete_feedback,
        mark_read: app.mark_read,
        delete_feedbacks: app.delete_feedbacks,
        check_delete: app.check_delete,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
        delimiters: ['[[', ']]'],

    });

    app.init = () => {
        app.get_feedbacks();
    };

    app.init();
};

init(app);

