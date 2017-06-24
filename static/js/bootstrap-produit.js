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
    }
    else{
        var nom = $('#nomProd_' + num).text();
        var newValue = valueParse - 1;
        $('#inputProd_' + num).val(newValue);
        $('#prod_' + num).empty();
        $('#prod_' + num).append('<td>' + nom + '</td><td>' + (newValue * prixProd )+'€</td>');
    }
}

function prodPlus(num){
    var oldValue = $('#inputProd_' + num).val();
    var valueParse = parseInt(oldValue);
    var newValue = valueParse + 1;
    var nom = $('#nomProd_' + num).text();
    if(valueParse == 0){
        $('#recapAchat').append('<tr id="prod_' + num + '"><td>' + nom + '</td><td>' + prixProd +'€</td></tr>');
    }
    $('#prod_' + num).empty();
    $('#prod_' + num).append('<td>' + nom + '</td><td>' + (newValue * prixProd )+'€</td>');
    $('#inputProd_' + num).val(newValue);
    
}

/*$.ajax('http://ponderosaproject.herokuapp.com/coucou').done(function(data){
    for(var i in data){
        $(document).on('click','#prodPlus_' + i,function(){
            /*var oldValue = $('#inputProd_' + i).val();
            var valueParse = parseInt(oldValue);
            var newValue = valueParse + 1;
            $('#inputProd_' + i).val(newValue);
            prodChange(i);
            
        });
        //alert(i);
    }
});*/

