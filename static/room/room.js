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
function clear1(){
    $('#user-list').empty()
    $('#remove-user-list').empty()
}
function remAdder(event){
    $('#remove-user-list').append(`
        <li class="list-group-item">
        <input style="position:static;margin-left: 0px;" class="form-check-input me-2" type="checkbox" value="" aria-label="..." checked onchange="gc(event)">
        ${event.path[0].textContent.trim()}
        </li>
    `)
}