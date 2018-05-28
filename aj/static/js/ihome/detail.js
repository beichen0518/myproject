function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function swiper(){
    var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
    });
}

$(document).ready(function(){
    $.get('/house/housedetail/' + window.location.search, function (data) {
        if (data.code == 200){
            // template.js模板引擎
            var detail_house = template('house_detail_list',{ohouse: data.house_dict})
            $('.container').append(detail_house);
            swiper();

            if (data.booking == 0){
                $(".book-house").hide();
            }else{
                $(".book-house").show();
            }
        }
    });
});