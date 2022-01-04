function resetter(){
    $('#inputbox').html('Enter your message...')
}
function checkKey(e){
    if(e.key == "Enter"){
        $("#sub").click()
    }
}
$(document).ready(function() {
    $(document).on('show.bs.modal', '.modal', function () {
        $(this).appendTo('body');
      });
});
function gc(event){
    event.path[1].remove()
}