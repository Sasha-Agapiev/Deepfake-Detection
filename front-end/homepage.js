// takes user-uploaded image and b64 encodes it into reader
function encodeImageFileAsURL(element){
    var file = element.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(file);
}