// Removed unused imports - Clock and ExternalLink are commented out in the JSX
import ReactMarkdown from "react-markdown";
import type { Components } from "react-markdown";
interface Message {
  id: string;
  role: "USER" | "ASSISTANT";
  content: string;
  timestamp: Date
}

interface ChatMessageProps {
  message: Message
}

export function ChatMessage( { message } : ChatMessageProps){
  const isUser = message.role === "USER";

  // Custom components for ReactMarkdown
  const markdownComponents: Components = {
    // Paragraphs with proper spacing
    p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
    
    // Line breaks
    br: () => <br />,
    
    // Ordered lists
    ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1 ml-4">{children}</ol>,
    
    // Unordered lists
    ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1 ml-4">{children}</ul>,
    
    // List items
    li: ({ children }) => <li className="leading-relaxed">{children}</li>,
    
    // Headings
    h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
    h2: ({ children }) => <h2 className="text-base font-bold mb-2">{children}</h2>,
    h3: ({ children }) => <h3 className="text-sm font-bold mb-1">{children}</h3>,
    
    // Code blocks
    code: ({ children, className }) => {
      const isInline = !className;
      if (isInline) {
        return <code className="bg-muted px-1 py-0.5 rounded text-xs font-mono">{children}</code>;
      }
      return <pre className="bg-muted p-2 rounded text-xs font-mono overflow-x-auto mb-2"><code>{children}</code></pre>;
    },
    
    // Blockquotes
    blockquote: ({ children }) => <blockquote className="border-l-4 border-muted-foreground/30 pl-3 mb-2 italic">{children}</blockquote>,
    
    // Strong/bold text
    strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
    
    // Emphasis/italic text
    em: ({ children }) => <em className="italic">{children}</em>,
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[85%] ${isUser ? "order-2" : "order-1"}`}>
        {/* Message Bubble */}
        <div
          className={`
            rounded-2xl px-4 py-3 shadow-sm transition-all duration-200 hover:shadown-md
            ${
              isUser
              ? "bg-user-message text-user-message-foreground rounded-br-md"
              : "bg-ai-message text-ai-message-foreground rounded-bl-md"
            }
          `}
        >
          <div className="text-sm leading-relaxed">
            <ReactMarkdown components={markdownComponents}>
              {message.content}
            </ReactMarkdown>
          </div>

          {/* Image if present */}
          {/* {message.image && (
            <div className="mt-3">
              <img
                src={message.image}
                alt="Relevant frames"
                className="rounded-lg max-w-full h-auto shadow-sm"
              />
            </div>
          )} */}

          {/* Links if present */}
          {/* {message.links && message.links.length > 0 && (
            <div className="mt-3 space-y-2">
              {message.links.map((link, index) => (
                <a
                  key={index}
                  href={link.url}
                  className={`
                    flex items-center space-x-2 text-xs rounded-lg px-3 py-2 transition-colors hover:opacity-80
                    ${
                      isUser
                      ? "bg-white/20 text-user-message-foreground"
                      : "bg-primary/10 text-primary hover:bg-primary/20"
                    }
                  `}
                >
                  {link.timestamp ? (
                    <Clock className="w-3 h-3" />
                  ) : (
                    <ExternalLink className="w-3 h-3" />
                  )}
                  <span>{link.text}</span>
                  {link.timestamp && (
                    <span className="ml-auto font-mono text-xs opacity-75">
                      {link.timestamp}
                    </span>
                  )}
                </a>
              ))}
            </div>
          )} */}
        </div>
        {/* Timestamp */}
        <div className={`mt-1 px-2 ${isUser ? "text-right" : "text-left"}`}>
          <span className="text-xs text-muted-foreground">
            {message.timestamp.toLocaleTimeString([], {
              day: "2-digit",
              month: "2-digit",
              year: "2-digit",
              hour: "2-digit",
              minute: "2-digit", 
            })}
          </span>
        </div>
      </div>
    </div>
  );
};