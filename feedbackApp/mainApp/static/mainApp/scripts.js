var el_down=document.getElementById("onetimePass");function generateP(){var e="",n="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$",t=Math.floor(15*Math.random())+8;for(i=1;i<=t;i++){var a=Math.floor(Math.random()*n.length+1);e+=n.charAt(a)}return document.getElementById("id_new_password1").value=e,document.getElementById("id_new_password2").value=e,e}function gfg_Run(){el_down.innerHTML=generateP()}