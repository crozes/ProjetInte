var prixProd = 5;

function prodMoins(num){
    var oldValue = $('#inputProd_' + num).val();
    var valueParse = parseInt(oldValue);
    if(valueParse == 0){
    }
    else if(valueParse == 1){
        $('#prod_' + num).remove();
        var newValue = valueParse - 1;
        $('#inputProd_' + num).val(newValue);
         modifSolde();
    }
    else{
        var nom = $('#nomProd_' + num).text();
        var newValue = valueParse - 1;
        $('#inputProd_' + num).val(newValue);
        $('#prod_' + num).empty();
        $('#prod_' + num).append('<td>' + nom + '</td><td id="prixProd_' + num + '">' + (newValue * prixProd )+'€</td>');
        modifSolde();
    }
}

function prodPlus(num){
    var oldValue = $('#inputProd_' + num).val();
    var valueParse = parseInt(oldValue);
    var newValue = valueParse + 1;
    var nom = $('#nomProd_' + num).text();
    if(valueParse == 0){
        $('#recapAchat').append('<tr id="prod_' + num + '"><td>' + nom + '</td><td id="prixProd_' + num + '">' + prixProd +'€</td></tr>');
    }

    var prixglobal = newValue * prixProd;
    $('#prod_' + num).empty();
    $('#prod_' + num).append('<td>' + nom + '</td><td id="prixProd_' + num + '">' + prixglobal +'€</td>');
    $('#inputProd_' + num).val(newValue);
    modifSolde();
    
}

function modifSolde(nombrePanneau){
    /*
    //ancienne valeur du solde
    $('#achatTotal').empty();
    var soldeParse = parseInt(oldSolde);

    //Valeur calculé
    for(var i = 0; i < 100; i++){
        $('#pub_' + i).val();
    }
    var newsolde = soldeParse + addVal - sousVal;
    $('#achatTotal').text(newsolde);

    var budget = $('#recapBudget').text();
    $('#budgetTotal').text(budget);
    var budgetParse = parseInt(budget);
    var resultat = budgetParse - newsolde;
    $('#resultat').text(resultat);*/
    var total = 0;
    for(var i = 0 ; i < 30 ; i++){
        var valuePub = $('#prixPub_' + i).text();
        var pubParse = parseInt(valuePub);
        if(pubParse){
            total += pubParse;
        }
        
        var valueProd = $('#prixProd_' + i).text();
        var prodParse = parseInt(valueProd);

        if(prodParse){
            total += prodParse;
        }
    }
    //alert(total);

    $('#achatTotal').text(total);

    var budget = $('#recapBudget').text();
    var budgetParse = parseInt(budget);
    $('#budgetTotal').text(budgetParse);

    var resultat = budgetParse - total;
    $('#resultat').text(resultat);

}

