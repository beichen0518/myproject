function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
$(function () {
    $.get('/user/auths/', function (data) {
        if(data.code == 200){
            $('#real-name').val(data.id_name);
            $('#id-card').val(data.id_card);
            $('.btn-success').hide();
        }
    });

    $('#form-auth').submit(function (e) {
        e.preventDefault();
        $('.error-msg').hide();
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();
        $.ajax({
            url:'/user/auths/',
            type:'PUT',
            data:{'real_name':real_name, 'id_card':id_card},
            dataType:'json',
            success:function (data) {
                if(data.code == 200){
                    showSuccessMsg()
                    $('.btn-success').hide();
                }else if(data.code == 900){
                    $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + data.msg);
                    $('.error-msg').show()
                }else if(data.code == 1008){
                    $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + data.msg);
                    $('.error-msg').show()
                }else if(data.code == 401){
                    $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>身份证号码已存在');
                    $('.error-msg').show()
                }
            },
            error:function (data) {
                alert('请求错误')
            }

        })
    })
});

