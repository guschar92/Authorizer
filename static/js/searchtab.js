function search(keyword){
    var items =  document.getElementsByClassName('tbrow');
    var key = event.keyCode || event.charCode;
    if( key == 8 || key == 46 ){
        $(items).each(function(index){
            if (!($(items[index]).text().toLowerCase().includes(keyword.toLowerCase()))){
                $(items[index]).hide();
            }
            else{
                 $(items[index]).show();
            }
        });
    }
    else{
        $(items).each(function(index){
            if (!($(items[index]).text().toLowerCase().includes(keyword.toLowerCase()))){
                $(items[index]).hide();
            }
            else{
                $(items[index]).show();
            }
        });
    }
}