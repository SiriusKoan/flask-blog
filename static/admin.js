function del_post(post_id) {
    $.ajax({
        url: "/admin_dashboard_posts_backend",
        type: "delete",
        data: JSON.stringify({ "post_id": post_id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                alert("OK.", "success");
            }
            else {
                alert("Error.", "alert");
            }
        })
}

function del_comment(comment_id) {
    $.ajax({
        url: "/admin_dashboard_comments_backend",
        type: "delete",
        data: JSON.stringify({ "comment_id": comment_id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                alert("OK.", "success");
            }
            else {
                alert("Error.", "alert");
            }
        })
}

function del_user(user_id) {
    $.ajax({
        url: "/manage_user_backend",
        type: "delete",
        data: JSON.stringify({ "user_id": user_id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                alert("OK.", "success");
            }
            else {
                alert("Error.", "alert");
            }
        })
}

function update_user(element) {
    var parent = element.parentElement;
    var user_id = parent.children[0].innerText;
    var email = parent.children[2].value;
    var is_admin = parent.children[3].checked;
    var data = { "user_id": user_id, "username": username, "email": email, "is_admin": is_admin }
    $.ajax({
        url: "/manage_user_backend",
        type: "patch",
        data: JSON.stringify(data),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                alert("OK.", "success");
            }
            else {
                alert("Error.", "alert");
            }
        })
}