let app={},init=e=>{e.test=(()=>{var e=document.getElementById("sel1"),a=e.options[e.selectedIndex].value;console.log(a),console.log("hi")}),e.check_delete=(()=>{for(feedback of(e.vue.showDelete=!1,e.vue.feedbacks))!0===feedback.delete&&(e.vue.showDelete=!0)}),e.filter_feedbacks=(e=>{}),e.get_feedbacks=(()=>{$.ajax({url:"/ajax/get_feedbacks/",dataType:"json",data:{test:"last x days"},success:function(a){e.vue.feedbacks=e.reindex(e.setShow(a)),e.vue.filter_feedbacks=e.vue.feedbacks},error:function(e){console.log("failure")}})}),e.delete_feedback=(a=>{$.ajax({url:"/ajax/delete_feedback/",dataType:"json",data:{id:a.id},success:function(e){console.log("successfully deleted")},error:function(e){console.log("failure")},complete:function(a){e.init()}})}),e.delete_feedbacks=(()=>{for(feedback of e.vue.feedbacks)!0===feedback.delete&&e.delete_feedback(feedback);e.vue.showDelete=!1}),e.mark_read=(e=>{console.log(e),$.ajax({url:"/ajax/mark_read/",dataType:"json",data:{id:e.id},success:function(e){console.log("successfully marked read")},error:function(e){console.log("failure")}})}),e.setDate=(e=>{var a=new Date(e),t=(a.getDay(),a.getHours()),d=a.getMinutes();d<10&&(d="0"+d);var c="a.m.";t>12&&(t-=12,c="p.m.");var s=a.getDate();return["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][a.getMonth()]+" "+s+" "+a.getFullYear()+", "+t+":"+d+c}),e.setShow=(a=>{for(feedback of(MM=["January","February","March","April","May","June","July","August","September","October","November","December"],a))feedback.show=!1,feedback.delete=!1,feedback.created_at=e.setDate(feedback.created_at),"N/A"===feedback.salesforceOp&&(feedback.salesforceOp=!1);return a}),e.reindex=(e=>{let a=0;for(p of e)p._idx=a++;return e}),e.data={feedbacks:[],feedbacks_filtered:[],showDelete:!1,popupActivo:!1,dateRange:0},e.methods={get_feedbacks:e.get_feedbacks,delete_feedback:e.delete_feedback,mark_read:e.mark_read,delete_feedbacks:e.delete_feedbacks,check_delete:e.check_delete,test:e.test},e.vue=new Vue({el:"#vue-target",data:e.data,methods:e.methods,delimiters:["[[","]]"]}),e.init=(()=>{e.get_feedbacks()}),e.init()};init(app);