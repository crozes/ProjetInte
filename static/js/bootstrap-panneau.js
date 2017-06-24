var nombrePanneau = 0;
var prix = 50;

function addPanneau(num){

    nombrePanneau += 1;
    var prixPub = 50;
    $('#list').append('<tr id="line_' + nombrePanneau + '"><td>Panneau ' + nombrePanneau + '</td><td>x:<input id="x_' + nombrePanneau + '" value="10" class="input" type="text" name="lname"><BR>y:<input value="10" id="y_' + nombrePanneau + '" class="input" type="text" name="lname"></td><td><input id="surface_' + nombrePanneau + '" onkeypress="inputClick(' + nombrePanneau + ')" class="input" type="text" name="lname" value="1">m²</td><td id="tablePrixPub_' + nombrePanneau + '">50€</td><td><button type="button" id="clear_' + nombrePanneau + '" onclick="deletePanneau(' + nombrePanneau + ')" title="Clear checked items" class="btn btn-default col-sm-12">Supprimer</button></td></tr>');
        
    //
    addPubToRecap(nombrePanneau);

}

function addPubToRecap(index){
    //On ajoute l'achat du panneau dans le recap
    $('#recapAchat').append('<tr id="pub_' + index + '"><td>Pub</td><td>' + prix +'€</td></tr>');
}

function inputClick(num){
    //Ici on refait un test pour récupérer la dernière valeur de l'input          
    $('#surface_' + num).on('input',function(){
        var data = $('#surface_' + num).val(); 
        var surface = parseInt(data);

        //On modifie le récap pour ce panneau
        $('#pub_' + num).empty();
        $('#pub_' + num).append('<td>Pub</td><td>' + (surface * 50 )+'€</td>');

        //On modifie le prix dans le tableau de l'achat du panneau
        $('#tablePrixPub_' + num).empty();
        $('#tablePrixPub_' + num).append('' + (surface * 50 )+'€');
    });
}

function deletePanneau(num){
    //On vide la ligne du panneau et le recap
    $('#line_' + num).empty();
    $('#pub_' + num).empty();
}
