var exportData = new Vue({
    delimiters: ['{[', ']}'],
    el: '#export-modal',
    data: {
        selectValue: 1
    },
    methods: {
        exportDataEvent: function () {
            $('#export-modal').modal('hide');
            zlajax.post({
                'url': '/export_data/',
                'data': {
                    'exportType': exportData.selectValue,
                },
                'success': function (result) {
                    var data = result.data;
                    exportFileInfo.fileInfo.name = data.filename;
                    exportFileInfo.fileInfo.url = 'http://lock.huangtongx.cn/' + data.fileurl;
                    $('#download-export-data').modal('show');
                }
            })
        }
    }

});

var exportFileInfo = new Vue({
    delimiters: ['{[', ']}'],
    el: '#download-export-data',
    data: {
        fileInfo: {
            name: '',
            size: 0,
            url: ''
        }
    },
    methods: {
        downloadFilEvent: function () {
            window.location = exportFileInfo.fileInfo.url;
            $('#download-export-data').modal('hide');
        }
    }
});