import { config } from "dotenv";
// import { sendChatMessage } from "./chat";
import { checkVideoStatus } from "./videoProcess";
// import { processVideo } from "./videoProcess";

config(); // Load environment variables from .env file

async function main(videoId: string){
    const status = await checkVideoStatus(videoId)
    // const process_status = await processVideo(videoId)
    // const chat_status = await sendChatMessage({
    //     "query": "What is going to be the growth on AI industry according to in dLe0U-98ECY and explain the images u recieved in structured manner",
    //     "video_id":videoId,
    //     "user_id":"c2c23e89-3a2f-4da6-9035-af29b4da31b2"
    // })
    // console.log(chat_status)
    // console.log(process_status)
    console.log(status)
    console.log(status?.status)
}

main("dLe0U-98ECY")