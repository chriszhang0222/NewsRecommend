var jayson = require('jayson');

var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

function add(a, b, callback) {
    client.request('add', [a,b], function (err, error, response) {
       if(err) throw err;
       console.log(response);
       callback(response);
    });
}

let getNewsSummarierForUser = (user_id, page_num, callback) =>{
    client.request('getNewsSummariesForUser', [user_id, page_num], (err, resp) =>{
        if(err){
            throw err;
            return;
        }
        console.log(resp.result);
        callback(resp.result);
    })
}

let logNewsClickForUser = (user_id, news_id) => {
    client.request('logNewsClickForUser', [user_id, news_id], (err, resp) => {
        if(err){
            throw err;
        }
        console.log(resp.result);
    })
}

function searchNews(keyword, page_num, callback) {
    client.request(
        'searchNews', [keyword, page_num], (err,error, response) => {
            if (err) {
                throw err;
            }

            console.log('[+] Search results received:');
            console.log(response);
            callback(response);
        }
    );
}

module.exports = {
    add:add,
    getNewsSummarierForUser: getNewsSummarierForUser,
    logNewsClickForUser: logNewsClickForUser,
    searchNews : searchNews

}
