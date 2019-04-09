

function rocketChatNavigation(url_change_role) {
    pageContentMain = $(".page-content-main");
    pageContentSecondary = $(".page-content-secondary");
    url_change_role = url_change_role;
    loadComponents(pageContentMain, pageContentSecondary);
    $(window).bind("hashchange", function() {
        loadComponents(pageContentMain, pageContentSecondary);
    });
    $(".change-role-rocketchat").unbind().click( function() {
        change_role(url_change_role);
    })
}


function change_role(url_change_role) {
    var input = $(".rocket-chat-user-input")
    var username = input.val();
    var role = "coach";
    $.ajax({
        type: "POST",
        url: url_change_role,
        data: {"username": username, "role": role},
        success: function() {
            input.val("");
            alert("The role has been changed");
        },
        error: function (request, status, error) {
            alert(request.responseText);
        },
    });
}

function loadComponents(pageContentMain, pageContentSecondary) {
    var navigationOptions = $(".rocket-chat-options").children();
    if(window.location.hash == "#main") {
        pageContentSecondary.hide();
        $(navigationOptions[1]).removeClass("active");
        pageContentMain.fadeIn("slow");
        $(navigationOptions[0]).addClass("active");
    }else if (window.location.hash == "#settings") {
        pageContentMain.hide();
        $(navigationOptions[0]).removeClass("active");
        pageContentSecondary.fadeIn("slow")
        $(navigationOptions[1]).addClass("active");
    }
}

function rocketChatLogout(urlLogout, beacon) {
    var beacon_rc = localStorage.getItem("beacon_rc");
    if (beacon_rc != null && beacon_rc != beacon) {
        $.ajax({
            type: "GET",
            url: urlLogout,
            data: {"beacon_rc": beacon_rc},
        });
        localStorage.setItem("beacon_rc", beacon);
    } else {
        localStorage.setItem("beacon_rc", beacon);
    }
}
