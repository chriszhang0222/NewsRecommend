var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next){
    info = [
        {
            "name":"Name",
            "Info":"Info"
        }
    ]
    res.json(info);
});

module.exports = router;