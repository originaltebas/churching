function seguimientosElements(e) {

  // EXTRAS -> Estados Civiles
  if ($('#tblistarSeguimientos').length != 0) {
    $(tblistarSeguimientos).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }

  if ($('#nomyape').length != 0) {

    $(function() {
      $("#nomyape").autocomplete({
        source:function(request, response) {
            $.getJSON("/seguimientos/autocomplete",{
                q: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                response($.map(data, function (item) {
                  return {
                    value: item.name,
                    label: item.name,
                    id: item.id
                  }
                }));
              }
          )
        },
        minLength: 2,
        select: function (event, ui) {
          $('#id_miembro').val(ui.item.id);
          console.log(ui.item.id)
        }
      });
    })
  }

}

window.addEventListener("load", seguimientosElements, false);