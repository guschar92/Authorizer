    function passwordToggler(id){
    console.log(id);
        if ($('#password').attr('type') == 'password'){
            $('#password').attr('type','text');
            $('#password2').attr('type','text');
            document.getElementById(id).style.color = '#007bff';
        }
        else{
            $('#password').attr('type','password');
            $('#password2').attr('type','password');
            document.getElementById(id).style.color = 'gray';
        }
    }


    function clipboard(e){
        var copyText = e.parentElement.innerText;
        var textArea = document.createElement("INPUT");
        textArea.setAttribute("type", "text");
        document.body.appendChild(textArea);
        textArea.value = copyText;
        textArea.select();
        document.execCommand("Copy");
        //textArea.remove();
        textArea.parentElement.removeChild(textArea);
    }

    function clipboardUrl(url){
        var copyText = url;
        var textArea = document.createElement("INPUT");
        textArea.setAttribute("type", "text");
        document.body.appendChild(textArea);
        textArea.value = copyText;
        textArea.select();
        document.execCommand("Copy");
        //textArea.remove();
        textArea.parentElement.removeChild(textArea);
    }