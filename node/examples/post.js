// axiosの準備
const axios = require("axios")
const protocol = "https"
const domain = "new.beluga.fm"
const api_version = "v1"
const request = axios.create({
	"baseURL": `${protocol}://${domain}/api/${api_version}/`,
	"headers": {
		"Content-Type": "application/json"
	},
	"responseType": "json"
})

// APIキー
const access_token = "YOUR_ACCESS_TOKEN"
const access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

// 投稿先
const hashtag_id = "5a8da737f734407078dd9583"
const text = "ふー"

// 投稿する
request
	.post("/status/update", {
		access_token,
		access_token_secret,
		hashtag_id,
		text
	})
	.then(res => {
		const { data } = res
		if (data.success == false) {
			console.error(data.error)
			return
		}
		console.log(data)
	})
	.catch(error => {
		console.error(error)
	})