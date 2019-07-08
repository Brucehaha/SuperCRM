    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function ajaxCall() {
        var formData = new FormData(document.querySelector('form'));
        var xhr = new XMLHttpRequest();
         xhr.onreadystatechange = function () {
             if(xhr.readyState == 4) {
                 console.log(xhr.responseText)
                var data = JSON.parse(xhr.responseText);
                var image = document.getElementById('pic');
                image.src = data.data;
                document.getElementsByClassName('check')[0].style.display = "block"
                document.getElementsByClassName('upload-file')[0].style.display = "None"
                var inputs = document.getElementsByTagName('input');
                for(index in inputs) {
                    if(inputs[index].type=='text') {
                        inputs[index].value = data.file_name.split('.')[0];
                    }
                }

            }
        }
        xhr.open('POST', '/superadmin/ajax-upload.html/');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

        xhr.send(formData)

     }


    function updateImage(ths) {
        var loading = document.getElementsByClassName('initLoading')[0]
        loading.style.display = 'block';
        ajaxCall()
        setInterval(function() {
            loading.style.display = 'none';

        }, 1000)
    }
    function removeImg(ths) {

        var pic=$(ths).parent().parent();
        $(pic).parent().find('.upload-file').css({'display':'block'});
        $(pic).parent().find('input').val('')
        $(pic).css({'display':'none'});



    }
    function triggerInput() {
        $('.upload-file').find('input').trigger('click');


    }
    function displayElement(ths) {
        $(ths).find('.reupload').css({'display':'block'});
    }
    function hideElement(ths) {
        $(ths).find('.reupload').css({'display':'none'});
    }

    function MoveOption(that, id) {
        var to_parent_id = $(that).parent().attr('id');
        console.log(to_parent_id)
        var option = "<option value='" + $(that).val() +"'ondblclick=MoveOption(this,'"+ to_parent_id +"') >" + $(that).text() +"</option>";
        $('#'+ id).append(option);
        $(that).remove();
    }
    function SelectOption() {
        $("select[tag] option").prop('selected', true);
    }