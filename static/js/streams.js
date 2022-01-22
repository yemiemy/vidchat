const APP_ID = '9a50aed5dc584f3bb27c5bd40e4a69ce'
const TOKEN = "0069a50aed5dc584f3bb27c5bd40e4a69ceIAB/w140XJoppDzz1sHbsnEKB3BxIMxKhC9s8VZ1zaaKwmTNKL8AAAAAEABLPQ3JWNXtYQEAAQBX1e1h"
const CHANNEL = "main"

const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" })

let localTracks = []
let remoteUsers = {}

let UID;

let joinAndDisplayLocalStream = async () => {

    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    let player = `  <div class="video-container" id="user-container-${UID}">
                        <div class="username-wrapper"><span class="user-name">My Name</span></div>
                        <div class="video-player" id="user-${UID}"></div>
                    </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0], localTracks[1]])
}