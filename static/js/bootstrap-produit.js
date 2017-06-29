
function prodMoins(num){
    var oldValue = $('#inputProd_' + num).val();
    var prix = $('#PrixProduit_' + num).text();
    var prixProd = parseFloat(prix);
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
        var prixglobal = newValue * prixProd;
        prixglobal = prixglobal.toFixed(2);
        $('#inputProd_' + num).val(newValue);
        $('#prod_' + num).empty();
        $('#prod_' + num).append('<td>' + nom + '</td><td id="prixProd_' + num + '">' + prixglobal +'€</td>');
        modifSolde();
    }
}

function prodPlus(num){
    var oldValue = $('#inputProd_' + num).val();
    var prix = $('#PrixProduit_' + num).text();
    var prixProd = parseFloat(prix);
    prixProd = prixProd.toFixed(2);
    var valueParse = parseInt(oldValue);
    var newValue = valueParse + 1;
    var nom = $('#nomProd_' + num).text();
    if(valueParse == 0){
        $('#recapAchat').append('<tr id="prod_' + num + '"><td>' + nom + '</td><td id="prixProd_' + num + '">' + prixProd +'€</td></tr>');
    }

    var prixglobal = newValue * prixProd;
    prixglobal = prixglobal.toFixed(2);
    $('#prod_' + num).empty();
    $('#prod_' + num).append('<td>' + nom + '</td><td id="prixProd_' + num + '">' + prixglobal +'€</td>');
    $('#inputProd_' + num).val(newValue);
    modifSolde();
}

function modifSolde(){

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

    $('#achatTotal').text(total);

    var budget = $('#recapBudget').text();
    var budgetParse = parseInt(budget);
    $('#budgetTotal').text(budgetParse);

    var resultat = budgetParse - total;
    $('#resultat').text(resultat);
}

