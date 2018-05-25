function check_input() {
    var password = $("#password").val();
    $("#password").val(md5(password));

    return true
}
function register() {
       window.open('/axf/register/', target='_self')
};