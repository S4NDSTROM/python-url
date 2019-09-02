document.addEventListener("DOMContentLoaded", function(event) {
    console.log("DOM fully loaded and parsed");

    document.getElementById("btn_1").addEventListener("click", function(){
        document.getElementById("display").innerHTML = "1";
    });
});
