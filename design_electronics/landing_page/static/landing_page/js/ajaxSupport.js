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
                      }
                  };
              });
          },

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