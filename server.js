var express = require('express')
var path = require('path')
var app = express()

var config = require('./config')

var port = process.env.PORT || 3000

app.get('/', function (req, res) {
  res.sendFile(config.build.index)
})

// serve pure static assets
var staticPath = path.join(config.build.assetsPublicPath, config.build.assetsSubDirectory)

app.use(staticPath, express.static('./dist/static'))

module.exports = app.listen(port, function (err) {
  if (err) {
    console.log(err)
    return
  }
  console.log('Listening at ' + port)
})
