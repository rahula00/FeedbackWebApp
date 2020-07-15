let app = {};

let init = (app) => {

    // This is the Vue data.
    app.data = {
        feedbacks: [],
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

    app.mark_read = (data) => {
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

   app.methods = {
        get_feedbacks: app.get_feedbacks,
        delete_feedback: app.delete_feedback,
        mark_read: app.mark_read,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
        delimiters: ['[[', ']]']
    });

    app.init = () => {
        app.get_feedbacks();
    };

    app.init();
};

init(app);

