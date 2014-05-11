var http = require('http');

var requestStr = JSON.stringify({
    url: 'http://jianshu.io/p/e95259378a34'
});

var options = {
    hostname: '127.0.0.1',
    path: '/parse/',
    method: 'POST',
    headers: {
        'Content-Length': requestStr.length
    }
};

var req = http.request(options, function(res) {
    var result = '';
    res.on('data', function(data) {
        result += data;
    });
    res.on('end', function(){
        console.log(JSON.parse(result));
    });
});

req.end(requestStr);

req.on('error', function(err) {
    console.error(err);
});