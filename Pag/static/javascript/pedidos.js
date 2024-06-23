var data = [
    [
        '1',
        '02/04/2018',
        'Cancelado',
        '345263774',
        '3500.00',
    ],
    [
        '2',
        '06/05/2018',
        'Completado',
        '7364536363',
        '700.00',
    ],
    [
        '3',
        '12/07/2018',
        'Pendiente',
        '09364526378',
        '9500.00',
    ],
    [
        '4',
        '24/08/2018',
        'Completado',
        '4536473652',
        '2600.00',
    ],
    [
        '5',
        '06/03/2018',
        'Completado',
        '77463564537u',
        '8600.00',
    ],
    [
        '6',
        '16/04/2018',
        'Completado',
        '345263774',
        '2799.00',
    ],
];
var modalData = [
    ['1234','Nombre del producto creo', 'Descripción del producto creo', 'Almacén del producto','PRecio por unidad', '220','200','20','1000']
];

var minDate = null;
var maxDate = null;
var modalTable = null;
var table = null;

function openModalDetails() {
    modalTable.clear();
    modalTable.rows.add(modalData);
    modalTable.draw();
    $('#detail_modal').modal();
}

$(document).ready(function () {
    // Configura el texto a mostrar en los recuadros de búsqueda de la tabla
    $('#report_ordes_table thead th').each(function () {
        var title = $(this).text();
        $(this).html('<h3>' + title + '</h3>' + '<input type="text" placeholder="Buscar" />');
    });

    // Declaración de la tabla de estatus de pedidos
    table = $('#report_ordes_table').DataTable({
        data: data,
        language: {
            lengthMenu: 'Mostrar _MENU_ elementos por página',
            zeroRecords: 'No se encontraron registros',
            info: 'Mostrando página _PAGE_ de _PAGES_',
            infoEmpty: 'No cuentas con ningún registro',
            infoFiltered: '(Filtrado del total de registros : _MAX_  )'
        },
        columnDefs: [{
            targets: -1,
            data: null,
            defaultContent: '<a id="open_modal_details" class="link">Abrir detalle</a>'
        }]
    });

    // Declaración de la tabla del detalle del pedido
    modalTable = $('#detail_table_modal').DataTable({
        data: [],
        language: {
            lengthMenu: 'Mostrar _MENU_ elementos por página',
            zeroRecords: 'No se encontraron registros',
            info: 'Mostrando página _PAGE_ de _PAGES_',
            infoEmpty: 'No cuentas con ningún registro',
            infoFiltered: '(Filtrado del total de registros : _MAX_    )'
        }
    });

    // Agrega los campos para filtrar en las columnas
    table.columns().every(function () {
        var that = this;

        $('input', this.header()).on('keyup change', function () {
            if (that.search() !== this.value) {
                that
                    .search(this.value)
                    .draw();
            }
        });
    });

    // Valida los rangos de fechas dados por el usuario
    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
            var date = new Date(data[1]).getTime() || null; 

            if (minDate === null && maxDate === null) {
                return true;
            } else if (minDate !== null && maxDate === null) {
                if (date >= minDate) {
                    return true;
                }
            } else if (minDate === null && maxDate !== null) {
                if (date <= maxDate) {
                    return true;
                }
            } else if (date >= minDate && date <= maxDate) {
                return true;
            }

            return false;
        }
    );

    // Función que se encarga del filtrado de los registros
    $("#filter_button").click(function () {
        minDate = new Date($('#begin_date').val()).getTime() || null;
        maxDate = new Date($('#end_date').val()).getTime() || null;

        table.draw();
    });

    // Abrir el modal de detalles al hacer clic en el enlace
    $('#report_ordes_table').on('click', '#open_modal_details', function () {
        openModalDetails();
    });
});



(function($) {
    $.fn.menumaker = function(options) {  
      var cssmenu = $(this), settings = $.extend({
        format: "dropdown",
        sticky: false
      }, options);
  
      return this.each(function() {
        $(this).find(".button").on('click', function(){
          $(this).toggleClass('menu-opened');
          var mainmenu = $(this).next('ul');
          
          if (mainmenu.hasClass('open')) { 
            mainmenu.slideToggle().removeClass('open');
          }
          
          else {
            mainmenu.slideToggle().addClass('open');
            if (settings.format === "dropdown") {
              mainmenu.find('ul').show();
            }
          }
        });
  
        cssmenu.find('li ul').parent().addClass('has-sub');
      
        multiTg = function() {
          cssmenu.find(".has-sub").prepend('<span class="submenu-button"></span>');
          cssmenu.find('.submenu-button').on('click', function() {
            $(this).toggleClass('submenu-opened');
            
            if ($(this).siblings('ul').hasClass('open')) {
              $(this).siblings('ul').removeClass('open').slideToggle();
            }
  
            else {
              $(this).siblings('ul').addClass('open').slideToggle();
            }
          });
        };
  
        if (settings.format === 'multitoggle') multiTg();
        else cssmenu.addClass('dropdown'); 
        if (settings.sticky === true) cssmenu.css('position', 'fixed');
        
        resizeFix = function() {
          var mediasize = 1000;
          
          if ($( window ).width() > mediasize) {
            cssmenu.find('ul').show();
          }
  
          if ($(window).width() <= mediasize) {
            cssmenu.find('ul').hide().removeClass('open');
          }
        };
  
      resizeFix();
        return $(window).on('resize', resizeFix);
      });
    };
  })(jQuery);
  
  (function($){
    $(document).ready(function(){
      $("#cssmenu").menumaker({
        format: "multitoggle"
      });
    });
  })(jQuery);