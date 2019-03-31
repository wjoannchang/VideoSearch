'use strict';

module.exports = function(app) {
    var server = require('../controllers/controller');

    app.route('/searchTranscription')
        .get(server.searchTranscription);
    app.route('/searchVideo')
        .get(server.searchVideo);

}