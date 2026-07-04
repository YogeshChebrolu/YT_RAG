# YouTube RAG Chrome Extension

A Chrome extension that enables intelligent chat with YouTube videos using RAG (Retrieval-Augmented Generation). Process YouTube videos and ask questions about their content with AI-powered responses.

## Features

- 🎥 YouTube video processing and analysis
- 💬 AI-powered chat interface for video content
- 🔐 Secure authentication with Supabase
- 📱 Modern React UI with Tailwind CSS
- 🌓 Theme support
- 📝 Markdown rendering for rich responses
- 🔄 Real-time video processing status

## Tech Stack

- **Frontend**: React 19 + TypeScript + Vite
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI primitives
- **Authentication**: Supabase Auth
- **Markdown**: React Markdown
- **Build Tool**: Vite with Chrome Extension support

## Prerequisites

- Node.js (v18 or higher)
- npm
- Chrome browser for testing

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd yt-rag-frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

> **Note**: Use the `.env.example` file as a template

### 4. Run development server

```bash
npm run dev
```

This will start the development server at `http://localhost:5173`

### 5. Development with Chrome Extension

For Chrome extension development, you can load the `dist` folder directly:

1. Build the project: `npm run build`
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the `dist` folder

## Building for Production

### Build the extension

```bash
npm run build
```

This creates a `dist` folder with:
- Optimized React app
- Chrome extension manifest
- Background and content scripts
- All necessary assets

### Load as Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked extension"
4. Select the `dist` folder from your project
5. The extension will be loaded and ready to use

## Project Structure

```
src/
├── api/           # API services and utilities
├── components/    # React components
│   ├── ui/        # Reusable UI components
│   └── ...        # Feature components
├── context/       # React context providers
├── lib/           # Utilities and configurations
└── assets/        # Static assets

public/
├── manifest.json  # Chrome extension manifest
├── background.js  # Extension background script
├── content.js     # Extension content script
└── icons/         # Extension icons
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Chrome Extension Features

- **Manifest V3** compatible
- **Background script** for extension lifecycle
- **Content script** for YouTube page integration
- **Popup interface** for quick access
- **Secure authentication** flow

## Environment Variables

The app uses Vite's environment variable system. All variables must be prefixed with `VITE_`:

- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anonymous key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the extension
5. Submit a pull request
