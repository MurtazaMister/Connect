function resetter(){
    $('#inputbox').html('Enter your message...')
}
function checkKey(e){
    if(e.key == "Enter"){
        $("#sub").click()
    }
}