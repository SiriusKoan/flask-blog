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