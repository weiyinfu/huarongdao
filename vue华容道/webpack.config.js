const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: __dirname + '/src/main.js',
    output: {
        path: __dirname + '/dist',
        // 这里使用了hash，从而每次编译生成的结果都是不一样的，
        // 从而可以保留多份代码进行比较
        filename: 'bundle-[hash].js'
    },
    devServer: {
        open: true,
        host: 'localhost'
    },
    /**
     * 使用正则表达式设定不同类型的文件的loader（加载器）
     * */
    module: {
        rules: [{
            test: /\.js$/,
            use: 'babel-loader'
        }, {
            /**
             * 这个地方是至关重要的，vue类型的文件html，js，css混在一起
             * 这就需要一个强大的loader去理解vue，.vue文件中的less就是通过vue-loader
             * 调用less解析器进行解析的
             * */
            test: /\.vue$/,
            use: 'vue-loader'
        }]
    },
    plugins: [
        /**
         * htmlWebpackPlugin的唯一作用是给index.tpl.html添加script标签
         * 让它引用生成的bundle.js
         * */
        new HtmlWebpackPlugin({template: __dirname + '/index.tpl.html'}),
        /**
         * 使用js丑化插件，压缩bundle.js
         * 此插件是webpack自带的
         * */
        new webpack.optimize.UglifyJsPlugin()
    ]
}
