'use strict';
let {PythonShell} = require('python-shell')
var videoDict = {"HCf2oDXFypY" : ["gs://la-hacks-236102-lcm/basketball.mp4", "https://www.youtube.com/watch?v=HCf2oDXFypY", "basketball"], "GKZp1jbcg_s": ["gs://la-hacks-236102-lcm/beach.mp4", "https://www.youtube.com/watch?v=GKZp1jbcg_s", "beach"], "OCDS5L7mW1s" : ["gs://la-hacks-236102-lcm/admission.mp4", "https://www.youtube.com/watch?v=OCDS5L7mW1s", "admission"]};

exports.searchTranscription = function(req, res){
    var video = req.query.video;
    var keyword = req.query.keyword;
    console.log(video);
    console.log(keyword);
    var returnJson = {};
    var options ={args:[videoDict[video][2], keyword]}
    PythonShell.run('api/python/transcription.py', options, function (err, data) {
        if (err) throw err;
        data = JSON.parse(data.toString());
        returnJson["transcriptionCandidate"] = [];
        data[keyword].forEach(function(element){
            var temp = {};
            temp["sentence"] = element["sentence"];
            temp["time"] = element["time"];
            temp["url"] = element["img"];
            returnJson["transcriptionCandidate"].push(temp);
        });
        res.send(returnJson);
    });
}

exports.searchVideo = function (req, res){
    var video = req.query.video;
    var keyword = req.query.keyword;
    console.log(video);
    console.log(keyword);
    var returnJson = {};
    var options ={args:[videoDict[video][0], keyword]}
    PythonShell.run('api/python/video.py', options, function (err, data) {
        if (err) throw err;
        data = JSON.parse(data.toString());
        returnJson["videoCandidate"] = [];
        data[keyword].forEach(function(element){
            var temp  = {};
            temp["time"] = element["time"];
            temp["url"] = element["img"];
            returnJson["videoCandidate"].push(temp);
        });
        res.send(returnJson);
    });
}



