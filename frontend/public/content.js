function extractVideoId(url) {
  try {
    const params = new URLSearchParams(new URL(url).search)
    return params.get("v");
  } catch (e) {
    console.error('Could not parse URL: ', url, e);
    return null;
  }
}

let lastVideoId = null;
let currentVideoElement = null;
let lastTimeUpdateSent = 0;
const THROTTLE_INTERVAL = 2000;

let retryCount = 0;
const MAX_RETRIES = 5;

/**
 * Sends a throttled time update
 */
function sendTimeUpdate() {
  if (!chrome.runtime || !chrome.runtime.sendMessage) {
    console.warn("Context invalidated, stopping time updates.");
    if (currentVideoElement) {
      currentVideoElement.removeEventListener("timeupdate", sendTimeUpdate);
    }
    return;
  }

  const now = Date.now(); 
  if(now - lastTimeUpdateSent < THROTTLE_INTERVAL) {
    return;
  }
  lastTimeUpdateSent = now;

  if (currentVideoElement) {
    console.log("sending time update: ", currentVideoElement.duration, currentVideoElement.currentTime)
    chrome.runtime.sendMessage({
      type: "TIME_UPDATE",
      currentTime: currentVideoElement.currentTime,
      duration: currentVideoElement.duration,
    });
  }
}

/**
 * Finds the video element and attaches the "timeupdate" listener.
 */
function setupVideoListener(){
  // remove old listener if exists
  if (currentVideoElement) {
    currentVideoElement.removeEventListener("timeupdate", sendTimeUpdate);
  }

  currentVideoElement = document.querySelector(".video-stream.html5-main-video");

  if(currentVideoElement) {
    currentVideoElement.addEventListener("timeupdate", sendTimeUpdate);
    console.log("Attached timeupdate listener to video");
    lastTimeUpdateSent = 0;
  } else {
    console.warn("Could not find video element to attach time listener");
  }
}


/**
 * Main function to check and send video details
 * Retries, if DOM isn't ready.
 */
function checkVideoDetails(){
  if (!chrome.runtime || !chrome.runtime.sendMessage) {
    console.warn("Context invalidated, stopping video detail check.");
    return;
  }

  const videoId = extractVideoId(location.href);

  if(!videoId || videoId === lastVideoId) {
    return;
  }

  const videoTitle = document.querySelector("h1.ytd-watch-metadata")?.innerText;
  const videoChannel = document.querySelector("#channel-name a")?.innerText;

  if (!videoTitle || !videoChannel) {
    if (retryCount < MAX_RETRIES) {
      retryCount++;
      console.log(`Video ID found {${videoId}}, but metadata not ready. Retrying..`);
      setTimeout(checkVideoDetails, 1000);
      return;
    } else {
      console.warn(`Max retries reached, Sending videoId without metadata.`);
    }
  }

  console.log("Video change detected: ", videoId, videoTitle, videoChannel);
  lastVideoId = videoId;
  retryCount = 0;

  setupVideoListener();

  try {
    chrome.runtime.sendMessage({
      type: 'VIDEO_ID_UPDATE',
      video_id: videoId,
      video_title: videoTitle,
      video_channel: videoChannel,
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Error sending video ID update:", chrome.runtime.lastError.message);
      }
    });
  } catch (error) {
    console.error("Failed to send video ID Update:", error);
  }
}


// Initialize the observer
const observer = new MutationObserver(()=> {
  checkVideoDetails();
})

try {
  const titleElement = document.querySelector("title");
  if (titleElement) {
    observer.observe(titleElement, {
      childList: true,
    });
    console.log("Youtube video observer initialized");
  } else {
    console.error("Could not find title element to observe");
  }
} catch (error) {
  console.error("Failed to initialize video observer:", error);
}


// Run the check once on initial script load
// We use a small delay to give the DOM a chance to load.
setTimeout(checkVideoDetails, 500);

// Send video coordinates to capture screen shot
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_VIDEO_COORDS") {
    console.log("Recieved request for video coordinates");

    const video = document.querySelector('.video-stream.html5-main-video')

     if (video) {
      const rect = video.getBoundingClientRect();

      sendResponse({
        x: Math.round(rect.left),
        y: Math.round(rect.top),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      })
    }
    else {
      console.error("Could not find video element to get coordinates");
      sendResponse(null);
    }
  }
  return true;
})