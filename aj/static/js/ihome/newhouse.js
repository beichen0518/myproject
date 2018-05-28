function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('#form-house-info').hide();
    // $('#form-house-image').show()
    $.get('/house/area_facility/',function (data) {
        var area_html_list = '';
        for (var i = 0; i<data.area_list.length; i += 1) {

            area_html = '<option value="' + data.area_list[i].id + '">' + data.area_list[i].name + '</option>';
            area_html_list += area_html
        }
        $('#area-id').html(area_html_list);

        var facility_html_list = '';
        for(var i = 0; i < data.facility_list.length; i += 1){
            facility_html = '<li><div class="checkbox"><label>';
            facility_html += '<input type="checkbox" name="facility" value="' + data.facility_list[i].id + '">' + data.facility_list[i].name ;
            facility_html += '</label></div></li>';
            facility_html_list += facility_html
        }
        $('.house-facility-list').html(facility_html_list)
    })
});

$('#form-house-info').submit(function (e) {
    e.preventDefault();
    // $(this）.serialize 可以序列化form表单的数据，在后端可以to.dict()将它转化成字典
    // $.post('/house/createhouse', $(this).serialize(), function (data) {
    //
    // });
    $(this).ajaxSubmit({
        url:'/house/createhouse/',
        type:'POST',
        dataType:'json',
        success:function (data) {
            if (data.code == 200){
                $('#house-id').val(data.houseid);
                $('#form-house-info').hide();
                $('#form-house-image').show();

            }
        },
        error:function (data) {
            alert('失败')
        }

    })
});

$('#form-house-image').submit(function (e) {
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/house/addimage/',
        type:'POST',
        dataType:'json',
        success:function (data) {
            if (data.code == 200){
                var img = $('<img>').attr('src', data.url);
                $('.house-image-cons').append(img)

            }else if (data.code == 2002){
                alert(data.msg);
            }
        },
        error:function (data) {
            alert('失败')
        }

    })
});

