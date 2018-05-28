//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);


    $.get('/orders/orders/' , function (data) {
        if (data.code == 200){
            var myOrder = template('orders-list-tmpl', {orders:data.orders});
            $('.orders-list').html(myOrder)

            $(".order-comment").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-comment").attr("order-id", orderId);

    });
    $('.modal-comment').on('click', function () {
        var comment = $('#comment').val();
        var orderId = $('.modal-comment').attr("order-id");
        $.ajax({
            url:'/orders/comment/',
            type:'PUT',
            data:{'comment':comment, 'orderId':orderId},
            dataType:'json',
            success:function (data) {
                $('#comment-modal').modal('hide');
                $('#bu_' + orderId).hide();
                var liComment = $('<li>').html('我的评价：' + comment);
                $('#ul_' + orderId).append(liComment)
            },
            error:function (data) {
                alert('请求失败')
            }
        })
    })



        }

    })
});