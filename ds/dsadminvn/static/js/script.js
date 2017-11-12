/*
* Update counts new sentenses
* */

var my_ajax_req ={

    updInterval: 10000,
    url: '/ctr/ajax/newsentcount/',
    elem: $('#count_new_sentences'),
    init: function(){
        var self = my_ajax_req;
        setInterval($.proxy(my_ajax_req.requestData, self), self.updInterval);
    },

    requestData: function(){
        var self = my_ajax_req;

        $.ajax({
            url: self.url,
            type: 'GET',
            dataType: 'json',
            success: function(data){ self.update(data) },
            error: function(data){ self.error(data) },
        });
    },

    update: function(data) {
        var self = my_ajax_req;
        if (data.status){
            self.elem.text(data.count);
        }

    },
    error: function(Data){
        var self = my_ajax_req;
        console.log('Failed to get data');
    },
};
//my_ajax_req.init();
