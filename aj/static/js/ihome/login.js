function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        $.ajax({
            url:'/user/login/',
            type:'POST',
            data:{'mobile': mobile, 'password': passwd},
            dataType:'json',
            success:function (data) {
                if (data.code == 200){
                    location.href='/user/my/'
                }else if (data.code == 900){
                    alert(data.msg)
                }else if (data.code == 1001 || data.code == 1004){
                    $("#mobile-err span").html(data.msg);
                    $("#mobile-err").show();
                }else if (data.code == 1005){
                    $("#password-err span").html(data.msg);
                    $("#password-err").show();
                }
            },
            error:function (data) {
                alert('请求失败')
            }

        })
        // if (!mobile) {
        //     $("#mobile-err span").html("请填写正确的手机号！");
        //     $("#mobile-err").show();
        //     return;
        // }
        // if (!passwd) {
        //     $("#password-err span").html("请填写密码!");
        //     $("#password-err").show();
        //     return;
        // }
    });
})