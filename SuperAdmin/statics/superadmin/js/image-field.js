// many to many image field remove photo
var images = document.getElementsByClassName('remove');
function removeImageOption() {
    var id = this.getAttribute('tag');
    var ancestor =  this.parentNode.parentNode;
    ancestor.style.display = 'none';
    var option = document.getElementById(id);
    option.removeAttribute('selected');
}
for ( var i = 0; i <images.length; i++) {
    images[i].addEventListener('click',removeImageOption, false);

}

// get cookie from form
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
// ajax
function ajaxCall() {
    var formData = new FormData(document.querySelector('form'));
    var xhr = new XMLHttpRequest();
     xhr.onreadystatechange = function () {
         if(xhr.readyState == 4) {
             console.log(xhr.responseText)
            var data = JSON.parse(xhr.responseText);
            var image = document.getElementById('pic');
            image.src = data.data;
            document.getElementsByClassName('check')[0].style.display = "block";
            document.getElementById('upload-file').style.display = "None";
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

// click remove listener
var singlePic = document.getElementById('remove');
function removeImage() {
    var ancestor =  this.parentNode.parentNode;
    ancestor.style.display = 'none';
    document.getElementById('upload-file').style.display = 'block';
    ancestor.parentNode.getElementsByTagName('input')[0].setAttribute('value', '');
}
if(singlePic) {
    singlePic.addEventListener('click', removeImage, false);
}
//trigger input when click Change button
var changeEl = document.getElementById('change');
function triggerInput() {
    var targetEl = document
        .getElementById('upload-file')
        .getElementsByTagName('input')[0];
    targetEl.click();
}
if(changeEl) {
    changeEl.addEventListener('click', triggerInput, false)

}


function displayElement(ths) {
    $(ths).find('.reupload').css({'display':'block'});
}
function hideElement(ths) {
    $(ths).find('.reupload').css({'display':'none'});
}


// toggle selected photo
function MoveOption(that, id) {
    var to_parent_id = $(that).parent().attr('id');
    console.log(to_parent_id)
    var option = "<option value='" + $(that).val() +"'ondblclick=MoveOption(this,'"+ to_parent_id +"') >" + $(that).text() +"</option>";
    $('#'+ id).append(option);
    $(that).remove();
}


