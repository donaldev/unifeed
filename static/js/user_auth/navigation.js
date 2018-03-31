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
    


    $('.btn-startFeed').click(function(){

      var form_name = $(this).attr("data-id")

      $('#formname').val(form_name);
      $('#modcodefeed1').html(form_name);
      
    })

    $('.btn-post').click(function(){

      var mod_code = $(this).attr("data-id");
      
      $('#module_from_id').val(mod_code);
      $('#modcodefeed').html(mod_code);

    })

    $('.btn-feedback').click(function(){

      var mod_code = $(this).attr("data-id");

      
      $('#module_from_id2').val(mod_code);
      $('#modcodefeed').html(mod_code);

    })

 
    $('input:radio[name="attend"]').change(function(){
      if(this.value == "No")
      {
        $('#studentFeedbackModal').modal('toggle');
        location.reload();
      }
    })


      $('input[type="range"]').on("change", function() {
        var value;
        if($(this).val() >=0 && $(this).val() < 2)
        {value = "Very Poor"}
        if($(this).val() >=2 && $(this).val() < 6)
        {value = "Poor"}
        if($(this).val() == 5)
        {value = "Average"}
        if($(this).val() >=6 && $(this).val() < 9)
        {value = "Good"}
        if($(this).val() >=9 && $(this).val() <= 11)
        {value = "Very Good"}
        $(this).next().html(value);
      })
         
   
    



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




      // $('#module2').keyup(function(){
      //   var inputModule = $(this).val();
      //   inputModule = inputModule.toUpperCase();
      //   console.log(inputModule);
      //   data = {
      //     module : inputModule
      //   };

      //   console.log(data);
      //   $.ajax({
      //       data : data,
      //       type : 'POST',
      //       url : '/checkModules'
      //   }).done(function(data){
      //       if (data == 'success'){
      //         $(this).css('border','2px solid green');
      //       }
      //       else{
      //         $(this).css('border','2px solid red');
      //       }
      //   });
      //   event.preventDefault();
      // });

      // var delay = (function(){
      //   var timer = 0;
      //   return function(callback, ms){
      //     clearTimeout (timer);
      //     timer = setTimeout(callback, ms);
      //   };
      // })();

      

     
      var validMods = [];
      $('.module1').on('input',function(event){
        // delay(function(){

        var module1 = $(this).val();

        var $self = $(this);

         var selectedModules = [module1];

        data = {
          module1 :  module1

        }; 
        $.ajax({
            data : data,
            type : 'POST',
            url : '/checkModules'
        }).done(function(data){
          var correctMods = data.allModules[0].correct;
          

          if (module1 == correctMods[0]){
          $self.css('border','2px solid green');
          validMods.push(module1); 
          
          }
          else{
            $self.css('border','2px solid red');
          }
          $('#modules').val(validMods);
          });
          event.preventDefault();

          
        
      });
      





              //  for(j=0;j<incorrectMods.length;j++){
              //      if( selectedModules[i].toUpperCase() == incorrectMods[j].toUpperCase())
              //         {
              //             var position = i+1
              //            if(selectedModules[i] != "")
              //             $('#module'+ position).css('border','2px solid red');
              //         }
              //       }
              //       for(k=0;k<correctMods.length;k++){
              //         if( selectedModules[i].toUpperCase() == correctMods[k].toUpperCase())
              //            {
              //                var position = i+1
                            
              //                $('#module'+ position).css('border','2px solid green');
              //               //  $('.validMods').append("<li class='login loginButton'>"+ selectedModules[i]+ "</li>");
                            

              //            }
              //          }

                
                    
                  // else 
                  //  {
                  //   if (selectedModules[i] != ""){
                  //   $('#module'+ i).css('border','1px solid green');
                  //   $('.validMods').append("<li class='login loginButton'>"+ selectedModules[i]+ "</li>");
                  //   console.log("correct : " + selectedModules[i])
                  //   }
                  // }
             

        
            

            // console.log(data)
            // if (data.allModules[0].incorrect){
            //     console.log("incorrect modules : " + data.allModules[0].incorrect[0]);
            // }
            // else {
            //   console.log("Good to go : " + data.allModules[1].correct);
            // }
        
      });
