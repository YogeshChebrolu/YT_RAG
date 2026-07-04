import { useVideoContext } from "@/context/VideoContext"
import { useEffect, useState } from "react"
import { Button } from "./ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"

// This should display a card with the status of video at top of chat messages 

export function VideoStatus() {
  const { 
    currentVideoId, 
    videoStatus,
    currentVideoTitle,
    currentVideoChannel,
    currentWatchTime,
    error,
    setError,
    handleInitializeVideo, 
    handleProcessCurrentVideo 
  } = useVideoContext()
  
  const [isProcessing, setIsProcessing] = useState(false)

  // Initialize video when currentVideoId changes
  useEffect(() => {
    if (currentVideoId) {
      handleInitializeVideo(currentVideoId)
    }
  }, [currentVideoId, handleInitializeVideo])

  const handleProcessClick = async () => {
    setIsProcessing(true)
    try {
      await handleProcessCurrentVideo()
    } catch(error) {
      setError("Failed to process video")
      console.error(`Error processing the video: ${currentVideoId}`)
    } finally {
      setIsProcessing(false)
    }
  }

  const getStatusDisplay = () => {
    switch (videoStatus) {
      case 'IDLE':
        return {
          text: 'Checking video...',
          color: 'text-gray-500',
          bgColor: 'bg-gray-50'
        }
      case 'NOT_PROCESSED':
        return {
          text: 'Not Processed',
          color: 'text-orange-600',
          bgColor: 'bg-orange-50'
        }
      case 'PROCESSING':
        return {
          text: 'Processing...',
          color: 'text-blue-600',
          bgColor: 'bg-blue-50'
        }
      case 'READY':
        return {
          text: 'Ready',
          color: 'text-green-600',
          bgColor: 'bg-green-50'
        }
      case 'ERROR':
        return {
          text: 'Error',
          color: 'text-red-600',
          bgColor: 'bg-red-50'
        }
      default:
        return {
          text: 'Unknown',
          color: 'text-gray-500',
          bgColor: 'bg-gray-50'
        }
    }
  }

  const statusDisplay = getStatusDisplay()
  const showProcessButton = videoStatus === 'NOT_PROCESSED' || videoStatus === 'ERROR'
  const isButtonDisabled = isProcessing || videoStatus === 'PROCESSING' || !currentVideoId

  if (!currentVideoId) {
    return (
      <Card className="mb-4">
        <CardContent className="pt-6">
          <div className="text-center text-gray-500">
            Navigate to a YouTube video to get started
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="mb-4">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium">Video Status for <span className="font-bold">{currentVideoTitle}</span> by <span className="font-bold">{currentVideoChannel} | {currentVideoId}</span></CardTitle>
        <CardDescription className="text-xs text-gray-500">Current watch time: {(currentWatchTime.toFixed(0))}</CardDescription>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`px-2 py-1 rounded-full text-xs font-medium ${statusDisplay.color} ${statusDisplay.bgColor}`}>
              {statusDisplay.text}
            </div>
            {videoStatus === 'PROCESSING' && (
              <div className="animate-spin h-4 w-4 border-2 border-blue-600 border-t-transparent rounded-full"></div>
            )}
          </div>
          
          {showProcessButton && (
            <Button 
              onClick={handleProcessClick}
              disabled={isButtonDisabled}
              size="sm"
              className="ml-2"
            >
              {isProcessing ? 'Processing...' : 'Process Video'}
            </Button>
          )}
        </div>
        
        {error && (
          <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-600">
            {error}
          </div>
        )}
        
        {videoStatus === 'READY' && (
          <div className="mt-2 text-xs text-gray-500">
            Video is ready for chat
          </div>
        )}
        
        {videoStatus === 'NOT_PROCESSED' && (
          <div className="mt-2 text-xs text-gray-500">
            Process this video to start chatting
          </div>
        )}
      </CardContent>
    </Card>
  )
}