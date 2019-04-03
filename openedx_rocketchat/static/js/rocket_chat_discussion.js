
class RocketChatNavigation {

    constructor(url_change_role) {
        this.pageContentMain = $(".page-content-main");
        this.pageContentSecondary = $(".page-content-secondary");
        this.url_change_role = url_change_role;

        this.loadComponents(this.pageContentMain, this.pageContentSecondary);

        $(window).bind('hashchange', $.proxy(function(){
            this.loadComponents(this.pageContentMain, this.pageContentSecondary);
        },this));

        $(".change-role-rocketchat").unbind().click($.proxy(function() {
            this.change_role(this.url_change_role);
        }, this))
    }


    change_role(url_change_role){
        var input = $(".rocket-chat-user-input")
        var username = input.val();
        var role = "coach";
        $.ajax({
            type: "POST",
            url: url_change_role,
            data: {"username": username, "role": role},
            success: function(){
                input.val("");
                alert("The role has been changed");
            },
            error: function (request, status, error) {
                alert(request.responseText);
            },
        });
    }


    loadComponents(pageContentMain, pageContentSecondary){

        var navigationOptions = $(".rocket-chat-options").children();

        if(window.location.hash == "#main"){
            pageContentSecondary.hide();
            $(navigationOptions[1]).removeClass("active");
            pageContentMain.fadeIn("slow");
            $(navigationOptions[0]).addClass("active");

        }else if (window.location.hash == "#settings"){
            pageContentMain.hide();
            $(navigationOptions[0]).removeClass("active");
            pageContentSecondary.fadeIn("slow")
            $(navigationOptions[1]).addClass("active");
        }
    }
}

class RocketChatLogout {

    constructor(urlLogout, beacon){
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
}
