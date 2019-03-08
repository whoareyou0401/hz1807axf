$(function () {
    $("button").click(function () {
    //    获取数据
        var name = $("#uname").val();
        var pwd = $("#pwd").val();
    //    校验数据
        if (name.length==0 || pwd.length==0){
            alert("用户名或密码不能为空");
            return;

        }
    //    做md5
        var enc_pwd = md5(pwd);
    //    上传数据
        $.ajax({
            url:"/api/client/v1/login",
            data:{
                uname: name,
                pwd: enc_pwd,

            },
            method: "post",
            success:function (res) {

                if (res.code == 0){
                    window.open(res.data, target="_self")
                } else {
                    alert(res.msg);
                }
            },
            fail:function (res) {

            },
            complete:function (res) {

            }
        })
    })
})