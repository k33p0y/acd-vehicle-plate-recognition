((w, $) =>
{
    // 'use strict';
    w.xhr = new XMLHttpReques();

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

    w.ajax = () => { };

    w.timer();
})(window, jQuery);