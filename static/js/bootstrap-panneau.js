$(document).ready(function(){
    //Hide clear btn on page load
    //$('#clear').hide();
    
    var nombrePanneau = 0;
    var isValid = 'oui_0';
    $('#add').click(function(){
        if(isValid == ('oui_' + nombrePanneau)){

        nombrePanneau += 1;
        var prixPub = 50;
        $('#list').append('<tr id="line_' + nombrePanneau + '"><td>Panneau ' + nombrePanneau + '</td><td>x:<input class="input" type="text" name="lname"><BR>y:<input class="input" type="text" name="lname"></td><td><input id="surface_' + nombrePanneau + '" class="input" type="text" name="lname" value="1">m²</td><td id="tablePrixPub_' + nombrePanneau + '">50€</td><td><button type="button" id="valide_' + nombrePanneau + '" title="Clear checked items" class="btn btn-info col-sm-6 ">Valider</button><button type="button" id="clear_' + nombrePanneau + '" title="Clear checked items" class="btn btn-default col-sm-6">Supprimer</button></td></tr>');
        //$('#clear').show();
        
        addPubToRecap(50, nombrePanneau);

        $('#surface_' + nombrePanneau).on('input',function(){
            var data = $('#surface_' + nombrePanneau).val(); 
            var surface = parseInt(data);
            $('#pub_' + nombrePanneau).empty();
            $('#pub_' + nombrePanneau).append('<td>Pub</td><td>' + (surface * 50 )+'€</td>');
            $('#tablePrixPub_' + nombrePanneau).empty();
            $('#tablePrixPub_' + nombrePanneau).append('' + (surface * 50 )+'€');
                    
        });

        $('#clear_' + nombrePanneau).click(function(){
            $('#line_' + nombrePanneau).empty();
            $('#pub_' + nombrePanneau).empty();
        });

        $('#valide_' + nombrePanneau).click(function(){
            isValid = 'oui_' + nombrePanneau;
        });
        }
        else{
            alert('nooooon');
        }
    });

    //Checks off items as they are pressed
    /*$(document).on('click', '.item', function() {
        //Chamge list item to red
        $(this).css("color", "#cc0000");
        //Change cursor for checked item
        $(this).css("cursor","default");
        //Strike through clicked item while giving it a class of done so it will be affected by the clear
        $(this).wrapInner('<strike class="done"></strike>');
        //Add the X glyphicon
        $(this).append(" " + '<span class="glyphicon glyphicon-remove done" aria-hidden="true"></span>');
        //Stops checked off items from being clicked again
        $(this).prop('disabled', true);
    });*/
    //Removes list items with the class done
});