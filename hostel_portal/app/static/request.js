var addUser=function(rollno,token)
{
	 $.ajax({
                async:false,
                url:"http://127.0.0.1:5000/admin/addUser",
                method:"POST",
                data:{roll:rollno,csrf_token:token},
                success:function(response){alert("User is successfully added");
                            console.log(response);},
                error:function(response){alert("new user not added");
                            console.log(response);},
                });
     location.reload();
}
var delUser=function(rollno,token)
{
     $.ajax({
                async:false,
                url:"http://127.0.0.1:5000/admin/delUser",
                method:"POST",
                data:{roll:rollno,csrf_token:token},
                success:function(response){alert("successfully removed");
                            console.log(response);},
                error:function(response){alert("not removed");
                            console.log(response);},
                });
     location.reload();
}

var showSelected = function(a,b){
    document.getElementById('username').innerText = a;
    document.getElementById('userval').innerText = b;
    document.getElementById('request_process').style.display = "block";
}
