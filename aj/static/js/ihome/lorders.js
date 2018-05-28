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
    

    $.get('/orders/showlorders/', function (data) {
        if (data.code == 200){
            var showLorders = template('show-lorders', {lorders:data.lorders});
            $('.orders-list').html(showLorders);

            $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
            $(window).on('resize', centerModals);
            $(".order-accept").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
            });
            
            $(".modal-accept").on("click", function () {

            var orderId = $(this).attr("order-id");
            $.ajax({
                url:'/orders/changeorder/' + orderId +'/',
                type:'PATCH',
                data:{ 'status':"WAIT_PAYMENT"},
                dataType:'json',
                success:function (data) {
                    if (data.code == 200){
                        // 可以在选择确认接单之后隐藏，并且去掉后面的灰色背景
                    //$('#accept-modal').modal('hide')
                    location.href = "/orders/lorders/"
                    }
                },
                error:function (data) {
                    alert('请求失败')
                }
                })
                });
            
                $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
                });

                $(".modal-reject").on("click", function () {
                    var orderId = $(this).attr("order-id");
                    var comment = $('#reject-reason').val();
                    $.ajax({
                        url:'/orders/changeorder/' + orderId +'/',
                        type:'PATCH',
                        data:{ 'status':"REJECTED", 'comment': comment},
                        dataType:'json',
                        success:function (data) {
                            if(data.code == 200){
                                location.href = "/orders/lorders/"
                            }

                            },
                        error:function (data) {
                            alert('访问失败')
                        }
                        })
                });
        }
    })
});
