$(function () {

    $(".subCart").click(function () {
    //    要知道点击的是哪个按钮
        var $btn = $(this);
    //    知道点击的是哪个数据
        var cid = $btn.parents("li").attr("cart_id");

    //    发送请求
        $.ajax({
            url:"/api/client/v1/cart/options",
            data:{
                cid:cid,
                option:"sub"
            },
            method:"put",
            success:function (res) {
                if (res.code == 0){
                    //数量更新
                    if(res.data.current_num != 0){
                        $btn.next().text(res.data.current_num);
                    } else {
                        //如果删除到0 那么移除掉li
                        $btn.parents("li").remove();
                    }
                //    更新总价
                    $("#sum_money").text(res.data.sum_money);
                } else{
                    alert(res.msg);
                }
            //    更新全选按钮的状态
                var text = res.data.is_select_all?"√":"";
                $(".all_select>span>span").text(text);
            }
        })
    //    更新对应的信息
    });
    $(".addCart").click(function () {
    //    要知道点击的是哪个按钮
        var $btn = $(this);
    //    知道点击的是哪个数据
        var cid = $btn.parents("li").attr("cart_id");

    //    发送请求
        $.ajax({
            url:"/api/client/v1/cart/options",
            data:{
                cid:cid,
                option:"add"
            },
            method:"put",
            success:function (res) {
                if (res.code == 0){
                    //数量更新
                    $btn.prev().text(res.data.current_num);
                //    更新总价
                    $("#sum_money").text(res.data.sum_money);
                } else{
                    alert(res.msg);
                }
            }
        })
    //    更新对应的信息
    });
    //全选按钮的点击状态
    $(".all_select").click(function () {
        $.ajax({
           url: "/api/client/v1/cart-status",
           success:function (res) {
            if (res.code == 0){
                //     更新全选按钮的状态
                var text = res.data.is_select_all?"√":"";
                $(".all_select>span>span").text(text);
                //    更新总价
                $("#sum_money").text(res.data.sum_money);
                //    更新商品的选中按钮的状态
                $(".confirm").each(function () {
                    $(this).find("span").find("span").text(text);
                })
            }
           }
        });
    })

    $(".confirm").click(function () {
        var $current_btn = $(this);
        var cid =$current_btn.parents("li").attr("cart_id");
        $.ajax({
            url: "/api/client/v1/cart/status",
            data:{
                cid: cid
            },
            method:"put",
            success:function (res) {
                if (res.code == 0){
                //    修改全选选中状态
                    if (res.data.is_select_all){
                        $(".all_select>span>span").html("√");
                    } else {
                        $(".all_select>span>span").html("");
                    }

                //    更新总价
                    $("#sum_money").html(res.data.money);

                //    修改当前的数据的选中状态
                    if (res.data.current_item_status){
                        $current_btn.find("span").find("span").html("√");
                    } else {
                        $current_btn.find("span").find("span").html("");
                    }
                } else{
                    alert(res.msg);
                }
            }
        })
    });
})