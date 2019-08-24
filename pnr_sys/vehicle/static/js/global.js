((w, $) =>
{
    'use strict';

    w.timer = () =>
    {
        setInterval(() =>
        {
            var time = (new Date()).toLocaleTimeString();
            var date = (new Date()).toDateString();
            $('#index-time').html(time);
            $('#index-date').html(date);
        }, 1000);
    };

    timer();
})(window, jQuery);