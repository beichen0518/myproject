function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$(function () {
     $("#form-avatar").submit(function(e){
         e.preventDefault();
         $(this).ajaxSubmit({
             url:'/user/user/',
             type:'PUT',
             dataType:'json',
             success:function (data) {
                 if (data.code == 200) {
                     $('#user-avatar').attr('src', data.url);
                 }else if (data.code == 1006){
                     alert(data.msg)
                 }

             }
         })
         // $.ajax({
         //     url:'/user/user/',
         //     type:'PUT',
         //     data: new FormData($('#form-avatar')[0]),
         //     cache: false,
         //     processData: false,// 告诉jQuery不要去处理发送的数据
         //     contentType: false,// 告诉jQuery不要去设置Content-Type请求头
         //     success:function (data){
         //         if (data.code == 200) {
         //             $('#user-avatar').attr('src', data.url);
         //         }
         //     },
         //     error:function (data) {
         //        alert('请求失败')
         //     }
         // })
     });

    $('#form-name').submit(function (e) {
        $('.error-msg').hide();
        e.preventDefault();
        var name = $('#user-name').val();
        $.ajax({
            url:'/user/user/',
            type:'PUT',
            data:{'name': name},
            dataType:'json',
            success:function (data) {
                if (data.code == 200) {
                    showSuccessMsg()
                }else if (data.code == 1007){
                    $('.error-msg').show()
                }
            },
            error:function (data) {
                alert('请求失败')
            }
        })
    })
});
