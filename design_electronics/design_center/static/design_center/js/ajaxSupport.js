(function($) {
  $.fn.autosubmit = function() {
    this.submit(function(event) {
      event.preventDefault();
      var form = $(this);
      $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(json){
            var toReturn = ""
            for(i = 0; i < json.length; i++){
                toReturn += json[i][0] + ", " + json[i][1] + " Value: ";
                if (json[i][4].length == 0){
                    toReturn += "<br><br>";
                }else{
                    toReturn += json[i][3]+ " &micro;"+ json[i][4] +"<br><br>";
                }
            };
            $("#ee-content-rec-comps-ajax").html(toReturn);
            $("#ee-content-rec-comps-ajax-errors").html("");
        },
        error: function(list){
            var response = JSON.parse(list.responseText);
            var toReturn = "";
            for(var key in response.errors){
                if (response.errors.hasOwnProperty(key)) {
                    toReturn += response.errors[key][0] + "<br>";
                }
            };
            toReturn += "<br>";

            $("#ee-content-rec-comps-ajax-errors").html(toReturn);
        }
      }).done(function(data) {

      }).fail(function(data) {
        // Optionally alert the user of an error here...
      });
    });
    return this;
  }
})(jQuery)

$(function() {
    $('form[data-autosubmit]').autosubmit();
});

(function($) {
  $.fn.analysissubmit = function() {
    this.submit(function(event) {
      event.preventDefault();
      var form = $(this);
      $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(json){
            var toReturn = ""
            for(i = 0; i < json.length; i++){
                toReturn += json[i][0] + ": " + json[i][1];
                if (json[i][2] == "None"){
                    toReturn += "<br><br>";
                }else{
                    toReturn += " " + json[i][2] + "<br><br>";
                }
            };
            $("#ee-content-analysis-ajax").html(toReturn);
            $("#ee-content-analysis-ajax-errors").html("");
        },
        error: function(list){
            var response = JSON.parse(list.responseText);
            var toReturn = "";
            for(var key in response.errors){
                if (response.errors.hasOwnProperty(key)) {
                    toReturn += response.errors[key][0] + "<br>";
                }
            };
            toReturn += "<br>";

            $("#ee-content-analysis-ajax-errors").html(toReturn);
        }
      }).done(function(data) {

      }).fail(function(data) {
        // Optionally alert the user of an error here...
      });
    });
    return this;
  }
})(jQuery)

$(function() {
    $('form[data-analysissubmit]').analysissubmit();
});

(function($) {
  $.fn.openloopbode = function() {
    this.submit(function(event) {
      event.preventDefault();
      var form = $(this);
      $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(json){
            //Update each bode plots mags and phases data
            // with updated data from analysis.
            graphs.forEach(function(element){
                for(i = 0; i <json.length; i++){
                    var div = json[i][0];
                    var bode;
                    if(element.mag_plot_div == div){
                        bode = element;
                        bode.mags = json[i][1];
                        bode.mags_min = json[i][2];
                        bode.mags_max = json[i][3];
                        bode.phases = json[i][4];
                        bode.phases_min = json[i][5];
                        bode.phases_max = json[i][6];
                        bode.redraw();

                                $("#ee-open-bode-ajax-errors").html("");
                            }
                        };
                    });
                },
                error: function(list){
                    var response = JSON.parse(list.responseText);
                    var toReturn = "";
                    for(var key in response.errors){
                        if (response.errors.hasOwnProperty(key)) {
                            toReturn += response.errors[key] + "<br>";
                        }
                    };

                    $("#ee-open-bode-ajax-errors").html(toReturn);
                }
                }).done(function(data) {
    
        }).fail(function(data) {
        // Optionally alert the user of an error here...
      });
    });
    return this;
  }
})(jQuery)
    
$(function() {
    $('form[gen-openloop-bodeplot]').openloopbode();
});