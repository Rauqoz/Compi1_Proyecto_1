// pathl: /home/user/output/js/
// pathw: c:\user\output\js\


/******************************************************************
 * ============================================================== *
 * ============================================================== *
 * ============================================================== *
 * ===================archivo de prueba de js==================== *
 * ============================================================== *
 * ================pathl -> /home/user/output/js/================ *
 * =================pathw -> c:\user\output\js\================== *
 * ============================================================== *
 * ============================================================== *
 * ============================================================== *
 ******************************************************************/



        /*********************************************
         *  dentro de un archivo de tipo javascript  *
         *  pueden encontrarse comentarios de tipo   *
         *   multilinea o de tipo unilinea, estos    *
         *  pueden aparecer en cualquier parte del   *
         * archivo de entrada tomando en cuenta que, *
         * el primero es el que contiene el path del *
         *  directorio al cual se enviara la salida  *
         *        ya analizada y limpiada.           *
         *********************************************/


function session(){

    var success = sessionstorage.getitem("session-user");

    if(success == null){
        window.location.href = "login.html";
    }
    
}


function obtener(){
    session();

    var f = new date();

    var date = f.getfullyear() + "" + ( f.getmonth() + 1 ) + "" + f.getdate(); // yyymmdd

    var nit = document.getelementbyid("nit").value;

    var datos = {
        fecha: parseint(date,"10"), // fecha de pedido
        nit: nit,                   // nit del cliente
    };

    var url = 'http://ejemplo_sitio_web/endpoint1/';

    ajax({url,
        type: 'post',
        datatype: 'json',
        data: datos,
        async: true,
        success: function(response){
            addproducts(response); // prueba
        }
    });

}



function addproducts(data){

    var tojson = json.parse(json.stringify(data));

    var tbody = document.getelementbyid('body');

    var inputtotal = document.getelementbyid("total");

    var total = 0.0
    tojson.foreach(function(element) {
        total = total + parsefloat(element.precio);
    });

    inputtotal.value = total;

    return '200';
}



function facturar(){

    var doc = new jspdf();

    var nit = document.getelementbyid("nit").value;

    var total = document.getelementbyid("total").value;
    

    var specialelementhandlers = {
        '#elementh': function (element, renderer) {
            return true;
        }
    };


    doc.fromhtml(elementhtml, 15, 15, {
        'width': 170,
        'elementhandlers': specialelementhandlers
    });


    doc.save('factura.pdf');
}


function logout(){

    sessionstorage.clear();

    window.location.href = "login.html";
}


function datavalidation(){
    var dataincache = sessionstorage.getitem("data-in-cache");

    if(!dataincache){
        sessionstorage.setitem("data-in-cache",false);
    }
}


function saveincache(data){
    sessionstorage.setitem("data-in-cache",true);

    sessionstorage.setitem("data-products",json.stringify(data));

    return;
}


function addproducts(data){

    var tojson = json.parse(json.stringify(data)).items;
    var lista = document.getelementbyid('listadoproductos');

    tojson.foreach(function(element) {
        //id del producto
        var divproducto = document.createelement("div");
        divproducto.setattribute("class","product");&
        divproducto.setattribute('id',element.id.n);

        //seccion de imagen
        var divimagen = document.createelement("div");
        divimagen.setattribute("align","center");

        var img = document.createelement("img");
        img.setattribute('src',element.url.s);
        img.setattribute('alt','');
        img.setattribute('height','200px');
        img.setattribute('width','200px');
        divimagen.appendchild(img);

        //seccion de datos
        var divdata = document.createelement("div");
        divdata.setattribute('class','product-body');

        var pcategoria = document.createelement("p");
        pcategoria.setattribute('class','product-category');
        pcategoria.innerhtml = element.categoria.s;
        pcategoria.innertext = element.categoria.s;

        var hnombre = document.createelement("h3");
        hnombre.setattribute('class','product-name');
        hnombre.innerhtml = element.nombre.s;
        hnombre.innertext = element.nombre.s;

        var hprecio = document.createelement("h4");
        hprecio.setattribute('class','product-price');
        hprecio.innerhtml = "q"+element.precio.s;
        hprecio.innertext = "q"+element.precio.s;

        divdata.appendchild(pcategoria);
        divdata.appendchild(hnombre);
        divdata.appendchild(hprecio);


        //seccion del boton de compra
        var divcart = document.createelement("div");
        divcart.setattribute('class','add-to-cart');

        var button1 = document.createelement("button");
        button1.setattribute("class","add-to-cart-btn");
        button1.setattribute('id',element.id.n);
        var namebtn=element.id.n+","+element.categoria.s+","+element.nombre.s+","+element.precio.s;
        button1.setattribute('name',namebtn);
        button1.setattribute('onclick','agregarcarrito(this);');
        button1.innerhtml = "agregar al carrito";/
        button1.innertext = "agregar al carrito";

        var i1 = document.createelement("i");
        i1.setattribute("class","fa fa-shopping-cart");

        button1.appendchild(i1);
        divcart.appendchild(button1);

        divproducto.appendchild(divimagen);
        divproducto.appendchild(divdata);
        divproducto.appendchild(divcart);

        lista.appendchild(divproducto);
    });

    return '200';
}

var lista = new array();

function linkedlist(pestana, nombre) {
    var obj = new object();
    obj.pestana = pestana;
    obj.nombre = nombre;
    lista.push(obj);
}


        /**************************
         *  posibles caracteres   *
         * que deberan reportados *
         *      como error        *
         *                        *
         *     $ @ # % & ^ ? ~    *
         **************************/
