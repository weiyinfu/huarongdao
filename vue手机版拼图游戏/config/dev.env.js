'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')
//开发环境是部署环境的超集，所以需要合并上开发环境
module.exports = merge(prodEnv, {
  NODE_ENV: '"development"'
})
