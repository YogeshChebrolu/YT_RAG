// Store the latest video ID in background script
let currentVideoId = null;
let currentVideoTitle = null;
let currentVideoChannel = null;

let sidePanelPort = null;


async function cropImage(dataUrl, coords) {
  console.log("Cropping image with coords: ", coords);

  // const img = new Image();
  // await new Promise(r => { img.onload = r; img.src = dataUrl; })

  // const canvas = new OffscreenCanvas(coords.width, coords.height);
  // const ctx = canvas.getContext("2d");

  // ctx.drawImage(
  //   img,
  //   coords.x,
  //   coords.y,
  //   coords.width,
  //   coords.height,
  //   0,0,
  //   coords.width,
  //   coords.height
  // );
  
  // const blob = await canvas.convertToBlob({ type: "image/jpeg", quality: 0.9 });
  // const croppedDataUrl = await new Promise(resolve => {
  //   const reader = new FileReader();
  //   reader.onload = () => resolve(reader.result);
  //   reader.readAsDataURL(blob);
  // });

  if (sidePanelPort) {
    sidePanelPort.postMessage({
      type: "CAPTURE_COMPLETE",
      dataUrl: dataUrl,
    });
    console.log("Sent cropped image to side panel");
  } else {
    console.warn("Side panel not connected, could not end screenshot.");
  }  
}


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "VIDEO_ID_UPDATE") {
    console.log("Background got new video_id:", message.video_id);
    
    // Store the video ID in background script
    currentVideoId = message.video_id;
    currentVideoTitle = message.video_title;
    currentVideoChannel = message.video_channel;
    // Store in chrome storage for side panel to access
    try {
      chrome.storage.local.set({ 
        currentVideoId: message.video_id,
        currentVideoTitle: message.video_title,
        currentVideoChannel: message.video_channel,
        lastUpdate: Date.now()
      }, () => {
        if (chrome.runtime.lastError) {
          console.error("Failed to store video ID:", chrome.runtime.lastError.message);
        } else {
          console.log("Video ID stored successfully:", message.video_id);
        }
      });
    } catch (error) {
      console.error("Failed to store video ID:", error);
    }
    
    // Send response back to content script
    sendResponse({ success: true });
  }
  else if (message.type === "TIME_UPDATE") {
    if (sidePanelPort) {
      try {
        sidePanelPort.postMessage(message);
      } catch (e) {
        console.warn("Cound not send time update to side panel, it might be closed", e);
      }
    }
  }
  
  else if(message.type === "CAPTURE_REQUEST") {
    console.log("Received capture request");

    // 1. Get the current active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs[0] || !tabs[0].id) {
        console.error("Could not find active tab");
        return;
      }
      const targetTabId = tabs[0].id;
      const targetWindowId = tabs[0].windowId;

      //2. Ask content script for video's position
      chrome.tabs.sendMessage(
        targetTabId,
        { type: "GET_VIDEO_COORDS"},
        (coords) => {
          if (chrome.runtime.lastError) {
            console.error("Error getting coords: ", chrome.runtime.lastError.message);
            return;
          }

          if (!coords) {
            console.error("Did not receive coordinates from content script")
          }

          // 3. Capture the visible tab
          chrome.tabs.get(targetTabId, (tab) => {
            if (chrome.runtime.lastError || !tab) {
                console.error("Tab no longer exists.", chrome.runtime.lastError?.message);
                return;
            }

            if (!tab.active) {
                console.error("Tab is no longer active. Capture aborted.");
                // Optionally, send a message back to React:
                // if (sidePanelPort) sidePanelPort.postMessage({ type: "CAPTURE_FAILED", reason: "Tab not active" });
                return;
            }

            // 4. Capture the VISIBLE tab in the correct window
            chrome.tabs.captureVisibleTab(
                targetWindowId, // <-- PASS THE CORRECT WINDOW ID
                { format: "jpeg", quality: 90 },
                (dataUrl) => {
                    if (chrome.runtime.lastError || !dataUrl) {
                        console.error("Failed to capture tab:", chrome.runtime.lastError?.message);
                        return;
                    }
                    // 5. Crop the image
                    cropImage(dataUrl, coords);
                }
              );
            });
        }
      );
    });
  }
  // Return true to indicate we will send a response asynchronously
  return true;
});

// Handle side panel connection and send current video ID
chrome.runtime.onConnect.addListener((port) => {
  if (port.name === "sidepanel") {
    console.log("Side panel connected");
    sidePanelPort = port;
    
    // Send current video ID to side panel when it connects
    if (currentVideoId) {
      port.postMessage({
        type: "VIDEO_ID_UPDATE",
        video_id: currentVideoId,
        video_title: currentVideoTitle,
        video_channel: currentVideoChannel
      });
    }
    
    port.onDisconnect.addListener(() => {
      console.log("Side panel disconnected");
      sidePanelPort = null;
    });
  }
});


// Add this code instead:
chrome.runtime.onInstalled.addListener(() => {
  // Clear any existing rules
  chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
    // Add a new rule
    let rule = {
      conditions: [
        new chrome.declarativeContent.PageStateMatcher({
          pageUrl: { hostEquals: 'www.youtube.com', pathPrefix: '/watch' },
        })
      ],
      actions: [new chrome.declarativeContent.ShowAction()]
    };
    // Register the rule
    chrome.declarativeContent.onPageChanged.addRules([rule]);
  });
});


// Handle extension icon click to open side panel
chrome.action.onClicked.addListener(async (tab) => {
  try {
    // Open the side panel for the current tab
    await chrome.sidePanel.open({ tabId: tab.id });
    console.log("Side panel opened for tab:", tab.id);
  } catch (error) {
    console.error("Failed to open side panel:", error);
  }
});

// Auto-open side panel when user navigates to YouTube
// chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
//   if (changeInfo.status === 'complete' && tab.url && tab.url.includes('youtube.com/watch')) {
//     try {
//       // Auto-open side panel when on YouTube video page
//       await chrome.sidePanel.open({ tabId: tabId });
//       console.log("Auto-opened side panel for YouTube video:", tab.url);
//     } catch (error) {
//       console.error("Failed to auto-open side panel:", error);
//     }
//   }
// });