//外部js文件
$(function(){
    var BASE_URL = '../static/imgs/';
    var html = '';
    $.each(faderData,function(i,o){
        html += '<li class="slide">';
        html +=' <a href="#">';
        html += `<img src="${BASE_URL+o.img_url}" alt="">`;
        html+='<span class="imginfo">';
        html+= o.img_info;
        html+='</span></a></li>';
    });
    console.log(html);
    //将拼接好的字符串作为兄弟元素添加到fader_controls前
    $('.fader_controls').before(html);
    
    //顺序jquery-->easyfader-->index.js
    //调用jQuery.easyfader.min.js提供的函数，实现轮播功能
    $('.fader').easyFader();

});