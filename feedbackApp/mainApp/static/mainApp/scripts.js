var el_down = document.getElementById("onetimePass"); 
  
/* Function to generate combination of password */ 
function generateP() { 
    var pass = ''; 
    var str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +  
            'abcdefghijklmnopqrstuvwxyz0123456789@#$'; 
    var num = Math.floor(Math.random() * 15) + 8; 
      
    for (i = 1; i <= num; i++) { 
        var char = Math.floor(Math.random() 
                    * str.length + 1); 
          
        pass += str.charAt(char) 
    } 
    document.getElementById("id_new_password1").value = pass;
    document.getElementById("id_new_password2").value = pass;
    return pass; 
} 

function gfg_Run() { 
    el_down.innerHTML = generateP(); 
    
} 