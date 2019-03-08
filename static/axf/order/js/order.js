$(function () {
    $(".delete").click(function () {
       var $btn = $(this);
       var order_item_id = $btn.parents("li").attr("order_item_id");
       var order_id = $("h3").text().split(":")[1]
       $.ajax({
           url: "/api/client/v1/orderitem/" + order_item_id,
           method:"delete",
           data:{
               order_id: order_id
           },
           success:function (res) {
               console.log(res)
               if (res.code == 0){
               //    更新总价
                   $(".pay_msg").text("待付款金额：￥" + res.data.sum_money)
               //    删除li
                   $btn.parents("li").remove();
               }
           }
       });
    })
})