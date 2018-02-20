$(document).ready(function(){
    

    var $menuitems = $("#menuitems"); 
    $menuitems.css("display:inline-block");
    $("#heading").click(function(){
      $("#menuitems").slideToggle('200');
    });

    $("a[href*='" + location.pathname + "']").addClass("nav_active");

    function errorCheck(){
    var error = window.error;
    console.log(error);
      $('.error').append("Error: "+ error);
      $('.error').css('visibilty','visible');
      
    }
    
    // $('.validate').on('click',function(){
    //   var selectedModules = $('.moduleInput');
    //   console.log(selectedModules);
    //   $.ajax({
    //     url: '/checkModulesL',
    //     data: selectedModules,
    //     type: 'POST',
    //     success: function(response) {
    //         var correctMods = response.correctMods;
    //         var incorrectMods = response.incorrectMods;

    //         console.log(correctMods + " Incorrect : " + incorrectMods)
    //     },
    //     error: function(error) {
    //         console.log(error);
    //     }
    // });


        // var dbModules = appConfig.modulesDBinfo;
        // dbModules = dbModules.replace(/&#39;/g,"'");
        // // dbModules = dbModules.replace(/\[/g, '{')
        // // dbModules = dbModules.replace(/]/g, '}');
        // dbModules = JSON.stringify(dbModules);
        // // dbModules = JSON.parse(dbModules);
        // console.log("Sorted it : " + dbModules)
        // console.log(typeof dbModules)
        // for (i=0;i<selectedModules.length;i++)
        //    {
        //   if (selectedModules[i] == dbModules.mod_code){
        //     console.log(selectedModules[i])
        //   }
        // }



      $('.checkModules').on('click', function(event){

        var module1 = $('#module1').val();
        var module2 = $('#module2').val();
        var module3 = $('#module3').val();
        var module4 = $('#module4').val();
        var module5 = $('#module5').val();
        var module6 = $('#module6').val();
        var selectedModules = [module1,module2,module3,module4,module5,module6];
        
        $.ajax({
            data : {
                 module1 :  module1,
                 module2 :  module2,
                 module3 :  module3,
                 module4 :  module4,
                 module5 :  module5,
                 module6 :  module6
            },
            type : 'POST',
            url : '/checkModules'
        }).done(function(data){
          var incorrectMods = data.allModules[0].incorrect;
          var correctMods = data.allModules[0].correct;
          
          console.log(incorrectMods)
           for (i=0;i<selectedModules.length;i++){

               for(j=0;j<incorrectMods.length;j++){
                   if( selectedModules[i].toUpperCase() == incorrectMods[j].toUpperCase())
                      {
                          var position = i+1
                         if(selectedModules[i] != "")
                          $('#module'+ position).css('border','2px solid red');
                      }
                    }
                    for(k=0;k<correctMods.length;k++){
                      if( selectedModules[i].toUpperCase() == correctMods[k].toUpperCase())
                         {
                             var position = i+1
                            
                             $('#module'+ position).css('border','2px solid green');
                            //  $('.validMods').append("<li class='login loginButton'>"+ selectedModules[i]+ "</li>");

                         }
                       }
                
                    
                  // else 
                  //  {
                  //   if (selectedModules[i] != ""){
                  //   $('#module'+ i).css('border','1px solid green');
                  //   $('.validMods').append("<li class='login loginButton'>"+ selectedModules[i]+ "</li>");
                  //   console.log("correct : " + selectedModules[i])
                  //   }
                  // }
             

          }
            

            // console.log(data)
            // if (data.allModules[0].incorrect){
            //     console.log("incorrect modules : " + data.allModules[0].incorrect[0]);
            // }
            // else {
            //   console.log("Good to go : " + data.allModules[1].correct);
            // }
        });
        event.preventDefault();
      });
    });