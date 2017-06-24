function prodMoins(num){
    var oldValue = $('#inputPub_' + num).val();
    var valueParse = parseInt(oldValue);
    if(valueParse == 0){

    }
    else{
        var newValue = valueParse - 1;
        $('#inputPub_' + num).val(newValue);
        alert(newValue);
    }
});

function prodPlus(num){
    var oldValue = $('#inputPub').val();
    var valueParse = parseInt(oldValue);
    var newValue = valueParse + 1;
    $('#inputPub').val(newValue);
    pubChange();
});

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

