const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    console.log("Setting up proxy...");
    app.use(
        '/search',
        createProxyMiddleware({
            target: 'http://127.0.0.1:8000/',
            changeOrigin: true,
        })
    );
};
