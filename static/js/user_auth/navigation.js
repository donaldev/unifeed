$(document).ready(function(){
    

    var $menuitems = $("#menuitems"); 
    $menuitems.css("display:inline-block");
    $("#heading").click(function(){
      $("#menuitems").slideToggle('200');
    });
})