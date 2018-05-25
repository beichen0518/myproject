// 页面加载准备好了     就是页面基本结构加载完成
$(function () {
    cartTotal();
    $('.addShopping').on('click', function () {
        var goodsid = $(this).attr('goodsid');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url:'/axf/createcart/',
            type:'POST',
            data:{'goodsid': goodsid},
            dataType:'json',
            headers:{'X-CSRFToken': csrf},
            success:function (msg) {
                cartTotal();
                $('#num_'+ goodsid).html(msg.c_num)
            },
            error:function () {
                alert('请求失败')
            }
        })

    });

    $('.subShopping').on('click', function () {
        var goodsid = $(this).attr('goodsid');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url:'/axf/subcart/',
            type:'POST',
            data:{'goodsid': goodsid},
            dataType:'json',
            headers:{'X-CSRFToken': csrf},
            success:function (msg) {
                cartTotal();
                $('#num_'+ goodsid).html(msg.c_num)
            },
            error:function () {
                alert('请求失败')
            }
        })

    });
    function selectSpan(goodsid, is_select){
        if (is_select==1) {
            $('#sel_' + goodsid).html('√');
        }else  {
            $('#sel_' + goodsid).html('&nbsp;')
        }
    }

    $('.is_choose span').on('click', function () {
        var goodsid = $(this).attr('is_select');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var select = $(this).html();
        if (select=='√'){
            var is_select = 0
        }else {
            var is_select = 1
        }
        $.ajax({
            url:'/axf/cart/',
            type:'POST',
            data:{'is_select': is_select, 'goodsid': goodsid},
            dataType: 'json',
            headers: {'X-CSRFToken': csrf},
            success:function (msg) {
                selectSpan(goodsid, msg.is_select);
                cartTotal();

            },
            error:function () {
                alert('请求失败')
            }
        })

    });
    $('#all_select').on('click', function () {
       var csrf = $('input[name="csrfmiddlewaretoken"]').val();
       var select = $(this).html();
        if (select=='√'){
            var all_select = 0
        }else {
            var all_select = 1
        }
       $.ajax({
           url: '/axf/cart/',
           type: 'POST',
           data: {'all_select': all_select},
           dataType: 'json',
           headers: {'X-CSRFToken': csrf},
           success:function (msg) {
               cartTotal();
               for (var i = 0; i < msg.goods_id.length; i += 1) {
                   selectSpan(msg.goods_id[i], msg.all_select)
               }
               if (msg.all_select == 1){
                    $('#all_select').html('√')
                }else {
                    $('#all_select').html('&nbsp;')
                }
           },
           error:function () {
               alert('请求失败')
           }
       });

    });
    function cartTotal() {
       $.ajax({
           url: '/axf/carttotal/',
           type: 'GET',
           dataType: 'json',
           success:function (msg) {
               $('#total').text('总价:' + msg.carttotal)
           },
           error:function () {
               alert('请求失败')
           }
       })
    }
});
