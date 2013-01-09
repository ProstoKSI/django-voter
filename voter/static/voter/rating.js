$(function() {
    $(document).on('click', 'a[rel="vote"]', function() {
        var link = $(this);
        $.getJSON(link.get(0).href, function(data) {
            if (data.status == 'ok')
            {
                link.parent().addClass('disable');
/*                var score = data.score;
                var mark = link.parent().find('.mark');
                mark.removeClass('positive');
                mark.removeClass('negative');
                mark.removeClass('default');
                if (score > 0)
                {
                    mark.addClass('positive');
                    score = '+' + score;
                }
                else if (score < 0)
                    mark.addClass('negative');
                else
                    mark.addClass('default');
                mark.get(0).innerHTML = score; */
            }
            add_status(data.status, data.text);
        });
        return false;
    });
});
