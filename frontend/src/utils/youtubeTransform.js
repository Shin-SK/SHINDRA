export function convertYoutubeLinksToIframe(content) {
	if (!content) return ''
  
	// 1) 短縮URL (youtu.be/VIDEO_ID) を変換
	content = content.replace(
	  /https?:\/\/youtu\.be\/([\w-]+)/g,
	  (match, videoId) => {
		return `<iframe
				  src="https://www.youtube.com/embed/${videoId}"
				  frameborder="0"
				  allowfullscreen>
				</iframe>`
	  }
	)
  
	// 2) 通常URL (youtube.com/watch?v=VIDEO_ID) を変換
	content = content.replace(
	  /https?:\/\/(www\.)?youtube\.com\/watch\?v=([\w-]+)/g,
	  (match, _, videoId) => {
		return `<iframe
				  src="https://www.youtube.com/embed/${videoId}"
				  frameborder="0"
				  allowfullscreen>
				</iframe>`
	  }
	)
  
	return content
  }
  