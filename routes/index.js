/*
 * Connect all of your endpoints together here.
 */
module.exports = function (app, router) {
    app.use('/api', require('./home.js')(router));

    app.use('/api', require('./fragments.js')(router));
    app.use('/api', require('./fragmentsId.js')(router));

};
