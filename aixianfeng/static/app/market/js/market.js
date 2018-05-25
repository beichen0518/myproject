$(function () {

    $("#all_types").click(function () {

        $("#all_types_container").show();
        $("#all_type_logo").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
        $("#sort_container").hide();
        $("#sort_rule_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");
    });


    $("#all_types_container").click(function () {
        $(this).hide();
        $("#all_type_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");

    });


    $("#sort_rule").click(function () {
        $("#sort_container").show();
        $("#sort_rule_logo").addClass("glyphicon-chevron-up").removeClass("glyphicon-chevron-down");
        $("#all_types_container").hide();
        $("#all_type_logo").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    });

    $("#sort_container").click(function () {
        $(this).hide();
        $("#sort_rule_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");
    });

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
                if (msg.code == 200) {
                    $('#num_' + goodsid).html(msg.c_num)
                }else if (msg.code == 400) {
                    window.open('/axf/login/', target='_self')
                }
                
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
               if (msg.code == 200) {
                    $('#num_' + goodsid).html(msg.c_num)
                }else if (msg.code == 400) {
                    window.open('/axf/login/', target='_self')
                }
            },
            error:function () {
                alert('请求失败')
            }
        })

    });

});