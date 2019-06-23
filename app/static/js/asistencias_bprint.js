function asistenciasElements(e) {

  if ($('#tblistarReuniones').length != 0) {
    $(tblistarReuniones).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }

  if ($('#tblistarAsistencias').length != 0) {
    $(tblistarAsistencias).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      },
      dom: 'Bfrtip',
      select: {
        style: 'multi'
      },
      buttons: [{
          text: 'Seleccionar todo',
          action: function () {
            this.rows().select();
          }
        },
        {
          text: 'Quitar seleccionados',
          action: function () {
            this.rows().deselect();
          }
        }
      ]
    });
  }

  function after_asistencias_submitted(data) {
    if (data.status == 'val') {
      document.getElementById("formerrors").innerHTML = data.errors;
    } else {
      window.location.href = data.url;
    }
  }


  $(document).on('click', '#btnRegistrarAsistencia', function (e) {
    e.preventDefault();

    let oTab = $('#tblistarAsistencias').DataTable();
    const id = $('#id_reunion').val();
    let dataArr = [];
    let rowData = oTab.rows('.selected').data();

    $.each($(rowData), function (key, value) {
        dataArr.push(value[0]); //"name" being the value of your first column.
    });
    $('#id_miembros').val(dataArr);
    console.log($('#id_miembros').val());

    const url = '/asistencias/registrar/' + id
      $.ajax({
        type: "POST",
        url: url,
        data: $('#frmRegistrarAsistencia').serialize(),
        success: after_asistencias_submitted,
        dataType: 'json'
      });
  });

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

window.addEventListener("load", asistenciasElements, false);