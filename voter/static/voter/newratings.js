objs = $('.{{ identifier }}')
for(var i = 0; i < objs.length; i++)
{
    objs[i].onclick = function() {
        var el = $(this)[0];
        value = el.getAttribute("value");
         $.getJSON("{% url ratings_set obj_type.pk obj_id %}?value=" + value, function(data) {
            add_status(data.status, data.text);
            var ch = $('#{{ identifier }}')[0].children;
            for(var i = 0; i < ch.length; i++)
            {
                if (ch[i].children[0].getAttribute("value") <= data.score)
                    $(ch[i].children[0]).addClass("star_marked");
                else
                    $(ch[i].children[0]).addClass("star_unmarked");
                ch[i].children[0].onmouseover = null;
                ch[i].children[0].onmouseout = null;
                $(ch[i].children[0]).removeClass("star_selected");
            }
        });
    };
    objs[i].onmouseover = function() {
        var el = $(this)[0];
        var ch = el.parentNode.parentNode.children;
        for (var i = 0; i < ch.length; i++)
            if (ch[i].children[0].getAttribute("value") <= el.getAttribute("value"))
            {
                $(ch[i].children[0]).removeClass("star_marked");
                $(ch[i].children[0]).removeClass("star_unmarked");
                $(ch[i].children[0]).addClass("star_selected");
            }
    };
    objs[i].onmouseout = function() {
        var ch = $(this)[0].parentNode.parentNode.children;
        for (var i = 0; i < ch.length; i++)
        {
                if (ch[i].children[0].getAttribute("marked") == "1")
                    $(ch[i].children[0]).addClass("star_marked");
                else
                    $(ch[i].children[0]).addClass("star_unmarked");
                $(ch[i].children[0]).removeClass("star_selected");
        }
    };
}
