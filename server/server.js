/*
 * import sys
 * import base64
 * import requests
 * import json
 *
 * file_path = "integral.jpg"
 * image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read()).decode()
 * r = requests.post("https://api.mathpix.com/v3/latex",
 *     data=json.dumps({'src': image_uri, 'ocr': ["math", "text"]}),
 *         headers={"app_id": "trial", "app_key": "34f1a4cea0eaca8540c95908b4dc84ab",
 *                 "Content-type": "application/json"})
 *                 print(r.text)
 **/

const fetch = require('node-fetch')
const express = require('express')
const app = express()
app.use(express.json())

const MATHPIX_ID = process.env.MATHPIX_ID
const MATHPIX_KEY = process.env.MATHPIX_KEY
const WOLFRAM_ID = process.env.WOLFRAM_ID

let latex = undefined
let results = ""

function sendMathPix(img, cb) {
    fetch('https://api.mathpix.com/v3/latex', {
        method: 'post',
        headers: {
            "app_id": MATHPIX_ID, "app_key": MATHPIX_KEY,
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            'src': img,
            'ocr': ['math', 'text']
        })
    }).then((res) =>{ 
        latex = res.body.latex || undefined
        cb()
    }).catch((err) => { throw err })
}

function sendWolfram() {
    // parse wolfram results
    let encoded_latex = encodeURIComponent(latex)
    let call = `https://api.wolframalpha.com/v2/query?input=${encoded_latex}&format=image,plaintext&output=JSON&appid=${WOLFRAM_ID}`
    fetch(call).then(e=>
        e.json()
    ).then(d=>{
        if (d.queryresult.success && d.queryresult.numpods > 0)
            results = d.queryresult.pods[0].subpods[0].plaintext
    })
}

// get image
app.post('/image', (req, res) => {
    try {
        sendMathPix(res.body.image, () => sendWolfram()) // promises are overrated
        res.json({ success: "image received" })
    } catch {
        res.status(500).send({ message: "error processing image" })
    }
})

// get latex
app.get('/latex', (req, res) => {
    let temp = latex
    latex = undefined
    if (temp) res.send(temp)
    res.status(404).send({ message: "No latex found" })
})
app.post('/latex', (req, res) => {
    latex = req.body.latex
    res.json({ success: true })
})

// get wolfram results
app.get('/results', (req, res) => {
    let temp = results
    results = ""
    if (temp > 0)
        res.json({ results: temp })
    res.status(404).send({ message: "No results found" })
})

app.listen(process.env.PORT || 3000, (req, res) => {
    console.log(`listening on port ${process.env.PORT || 3000}`)
})