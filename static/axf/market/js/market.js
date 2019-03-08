$(function () {
    var types_menu_is_down = true;
    var sort_menu_is_down = true;
    $("#all_type").click(function () {
        sub_type_toggle();
    })
    $("#sub_types").click(function () {
        sub_type_toggle();
    })

    $("#all_sort").click(function () {
            sort_toggle();
    });
    $("#sort").click(function () {
            sort_toggle();
    });
    function sort_toggle() {
        $("#sort").toggle();
        if (sort_menu_is_down) {
            $("#all_sort").find("span").find("span").removeClass("glyphicon glyphicon-menu-down").addClass("glyphicon glyphicon-menu-up");
            sort_menu_is_down = false
        } else {
            $("#all_sort").find("span").find("span").removeClass("glyphicon glyphicon-menu-up").addClass("glyphicon glyphicon-menu-down");
            sort_menu_is_down = true
        }

    }
    function sub_type_toggle() {
        $("#sub_types").toggle();
        if (types_menu_is_down) {
            $("#all_type").find("span").find("span").removeClass("glyphicon glyphicon-menu-down").addClass("glyphicon glyphicon-menu-up");
            types_menu_is_down = false
        } else {
            $("#all_type").find("span").find("span").removeClass("glyphicon glyphicon-menu-up").addClass("glyphicon glyphicon-menu-down");
            types_menu_is_down = true
        }
    };

//    商品添加到购物车
    $(".addShopping").click(function () {
    //    要知道商品的ID
        var goods_id = $(this).attr("goods_id");
        var $current_btn = $(this);
        // console.log(goods_id);
    //    发送请求
        $.ajax({
            url: "/api/client/v1/cart-item",
            data:{
                goods: goods_id,
                num: 1,
            },
            method:"post",
            success:function (res) {
                console.log(res)
                if (res.code == 1){
                    //如果没登录 我们要跳转到登录页
                    window.open(res.data, target="_self")
                } else if (res.code == 0 ){
                    // 如果成功了 我们要更新商品显示的数量
                    $current_btn.prev().html(res.data.num);
                } else{
                    alert(res.msg);
                }
            }
        })
    //    如果成功了 我们要更新商品显示的数量
    //    如果没登录 我们要跳转到登录页
    //    如果其他失败的情况 我们就弹窗
    });
    $(".subShopping").click(function () {
    //    要知道商品的ID
        var goods_id = $(this).attr("goods_id");
        var $current_btn = $(this);
        //如果当前显示的数量是0 那么就不发送请求了
        if ($current_btn.next().text() == "0"){
            return;
        }
        // console.log(goods_id);
    //    发送请求
        $.ajax({
            url: "/api/client/v1/cart-item",
            data:{
                goods: goods_id,
                num: 1,
            },
            method:"put",
            success:function (res) {
                console.log(res)
                if (res.code == 1){
                    //如果没登录 我们要跳转到登录页
                    window.open(res.data, target="_self")
                } else if (res.code == 0 ){
                    // 如果成功了 我们要更新商品显示的数量
                    $current_btn.next().html(res.data);
                } else{
                    alert(res.msg);
                }
            }
        })
    //    如果成功了 我们要更新商品显示的数量
    //    如果没登录 我们要跳转到登录页
    //    如果其他失败的情况 我们就弹窗
    })
})