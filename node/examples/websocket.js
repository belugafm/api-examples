const WebSocket = require("ws")

const ascii_red = "\u001b[1;31m"
const ascii_green = "\u001b[1;32m"
const ascii_cyan = "\u001b[1;36m"
const ascii_reset = "\u001b[0m"

const console_green_bold = text => {
	return `${ascii_green}${text}${ascii_reset}`
}
const console_cyan_bold = text => {
	return `${ascii_cyan}${text}${ascii_reset}`
}
const console_red_bold = text => {
	return `${ascii_red}${text}${ascii_reset}`
}

// 再接続を自動的に行う
class WebSocketClient {
	constructor(protocol, domain, port, endpoint) {
		this.protocol = protocol
		this.port = port
		this.domain = domain
		this.endpoint = endpoint
		this.listeners = []
		this.initial_reconnect_interval = 1000	// ミリ秒
		this.max_reconnect_interval = 30000		// ミリ秒
		this.reconnect_decay = 1.5
		this.reconnect_interval = this.initial_reconnect_interval
		this.timer_id = 0
		this.init()
	}
	init() {
		if (this.ws) {
			for (const listener of this.listeners) {
				this.ws.removeEventListener(listener.name, listener.callback)
			}
		}
		const url = `${this.protocol}://${this.domain}:${this.port}/${this.endpoint}`
		const ws = new WebSocket(url)
		ws.onclose = event => {
			console.log(console_red_bold("closed websocket connection"))
			clearTimeout(this.timer_id)
			this.timer_id = setTimeout(() => {
				this.init()
			}, this.reconnect_interval);
			this.reconnect_interval = Math.min(this.max_reconnect_interval, this.reconnect_interval * this.reconnect_decay)
		}
		ws.onopen = event => {
			console.log(console_cyan_bold("connected websocket server"))
			this.reconnect_interval = this.initial_reconnect_interval
		}
		ws.onerror = event => {
			console.error("websocket error", event)
		}
		for (const listener of this.listeners) {
			ws.addEventListener(listener.name, listener.callback)
		}
		this.ws = ws
	}
	addEventListener(name, callback) {
		this.listeners.push({ name, callback })
		this.ws.addEventListener(name, callback)
	}
}

const protocol = "wss"
const domain = "new.beluga.fm"
const port = 8080

// どのページにユーザーが滞在しているかをサーバーに教える
// この情報を元にオンライン一覧が更新されるため、載りたくない場合は空にする
const endpoint = "server/beluga/public"

const client = new WebSocketClient(protocol, domain, port, endpoint)

client.addEventListener("message", event => {
	const data = JSON.parse(event.data)

	// 新しい投稿
	if (data.status_updated) {
		const { status } = data
		console.log(console_green_bold("status_updated"), status.id)
		return
	}

	// 投稿削除
	if (data.status_deleted) {
		const { id } = data
		console.log(console_green_bold("status_deleted"), id)
		return
	}

	// ふぁぼの更新
	if (data.favorites_updated) {
		const { status } = data
		console.log(console_green_bold("favorites_updated"), status.id)
		return
	}

	// いいね
	if (data.like_created) {
		const { status } = data
		console.log(console_green_bold("like_created"), status.id)
		return
	}

	// リアクション
	if (data.reaction_added) {
		const { status } = data
		console.log(console_green_bold("reaction_added"), status.id)
		return
	}
})