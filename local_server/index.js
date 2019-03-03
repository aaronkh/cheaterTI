var express = require('express')
var app = express()

app.use(express.json({limit: '15mb'}))

var getCam = false
var getCamf = false
var resp = undefined
var thread = undefined

app.get('/cam', function(req, res){
	tgetCam = getCam
	getCam = true
	while(!resp){
		console.log(on)
	}
	tresp = resp
	resp = undefined
	res.json({resp:tresp})
})

app.get('/camf', function(req, res){
	tgetCam = getCamf
	getCamf = true
	while(!resp){
		console.log(on)
	}
	tresp = resp
	resp = undefined
	res.json({resp:tresp})
})

app.get('/camstat', function(req, res){
	tgetCam = getCam
	getCam = false
	res.json({cam:tgetCam})
})

app.get('/camstatf', function(req, res){
	tgetCam = getCamf
	getCamf = false
	res.json({cam:tgetCam})
})

app.post('/resp', function(req, res){
	resp = req.body.resp
	res.json({resp:resp})
})

app.post('/thread', function(req, res){
	thread = req.body.thread
	res.json({thread:thread})
})

app.get('/thread', function(req, res){
	res.json({thread:thread})
})

app.listen(3000)