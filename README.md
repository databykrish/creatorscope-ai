# CreatorScope AI Dashboard

A production-ready full-stack influencer intelligence and campaign audit platform built with Next.js, FastAPI, and YouTube Data API integration.

## 🚀 Features

- **Creator Search & Discovery**: Search creators across YouTube, Instagram, TikTok with real-time filtering
- **Campaign Readiness Scoring**: AI-driven assessment of creator campaign suitability
- **Analytics Dashboard**: Real-time stats on tracked creators, engagement metrics, and campaign performance
- **Creator Audits**: Deep analysis of upload consistency, engagement trends, and risk flags
- **Data Export**: Download creator analytics in CSV, JSON, or PDF formats
- **Live Console**: Real-time processing logs via WebSocket streaming
- **Fallback Integration**: Automatic yt-dlp scraping when YouTube API quota exceeded
- **Type-Safe**: Full TypeScript implementation with Pydantic validation

## 📋 Tech Stack

### Frontend
- Next.js 16.2.6 with React 19
- TypeScript 5.7.3
- Tailwind CSS v4
- Framer Motion for animations
- Radix UI components (shadcn/ui)
- Custom React hooks for API integration

### Backend
- FastAPI 0.104.1
- Python 3.12
- YouTube Data API v3
- yt-dlp (fallback scraper)
- Uvicorn ASGI server
- Pydantic v2 validation

### Deployment
- Docker containerization
- Render.com for backend
- Vercel for frontend
- Environment-based configuration

## 🏗️ Project Structure

### Backend
```
backend/
├── core/                 # Configuration, exceptions, logging
├── api/routes/          # API endpoints
├── services/            # Business logic
├── models/              # Pydantic schemas
├── utils/               # Rate limiter, cache, formatters
├── main.py              # FastAPI app
└── requirements.txt
```

### Frontend
```
components/dashboard/   # Dashboard components
hooks/                  # Custom React hooks
lib/
├── api.ts              # API client
└── types.ts            # TypeScript types
```

## 🔧 Prerequisites

- Node.js 18+ / pnpm
- Python 3.12 / pip
- YouTube Data API key (get from [Google Cloud Console](https://console.cloud.google.com/))
- Git

## 🛠️ Local Development Setup

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
```
Edit `.env` with your YouTube API key:
```env
YOUTUBE_API_KEY=your_api_key_here
ENVIRONMENT=development
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000
```

4. **Start backend server**
```bash
uvicorn main:app --reload --port 8000
```

Backend API: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies**
```bash
pnpm install
```

2. **Configure environment**
```bash
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

3. **Start development server**
```bash
pnpm dev
```

Frontend: `http://localhost:3000`

## 🌍 Deployment

### Deploy Backend to Render

1. Create Render account and new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add environment variables:
   - `YOUTUBE_API_KEY`: Your API key
   - `ENVIRONMENT`: production
   - `DEBUG`: false
6. Deploy - auto-deploys on git push

### Deploy Frontend to Vercel

1. Create Vercel account
2. Import GitHub repository
3. Set `NEXT_PUBLIC_API_URL` environment variable to your Render backend URL
4. Deploy - auto-deploys on git push

### Docker Deployment

```bash
docker build -t creatorscope-api .
docker run -p 8000:8000 \
  -e YOUTUBE_API_KEY=your_key \
  -e ENVIRONMENT=production \
  creatorscope-api
```

## 📡 API Endpoints

### Health Check
- `GET /api/health` - Service status

### Creators
- `GET /api/creators/search` - Search creators
- `GET /api/creators/{id}` - Get creator details
- `GET /api/creators/{id}/audit` - Run audit

### Analytics
- `GET /api/analytics/stats` - Dashboard stats

### Export
- `POST /api/export/{format}` - Create export (csv|json|pdf)
- `GET /api/export/{export_id}/download` - Download file

### WebSocket
- `WS /ws/console` - Real-time logs

## 🔐 Environment Variables

### Backend (.env)
```
YOUTUBE_API_KEY=your_api_key_here
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
RATE_LIMIT_DELAY_SECONDS=2
CACHE_TTL_SECONDS=3600
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ⚠️ Important: Render Free Tier Cold Start

The backend is hosted on Render's free tier. **Free instances spin down after 15 minutes of inactivity.**

When the evaluator or first user hits the API after a period of inactivity, the backend will take **30–60 seconds to wake up**. This is expected behaviour — not a bug.

**What you'll see**: The frontend may show a loading spinner or "connecting…" for up to a minute on first load. Subsequent requests are fast.

To pre-warm the backend before a demo, visit:
```
https://creatorscope-ai.onrender.com/api/health
```
Wait for `{"status": "ok"}` before opening the frontend.


## 🔐 Authentication & Age-Gated Content

### Option A: YouTube Data API Key (recommended)

Set `YOUTUBE_API_KEY` in your backend `.env`. All standard public channel data is accessible without additional authentication.

### Option B: Cookie-based session (for age-gated or restricted content)

The yt-dlp fallback supports browser cookie injection for restricted videos:

1. Export your YouTube cookies from your browser using the [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) extension.
2. Save the file as `backend/cookies.txt`.
3. Set the env var:
   ```
   YT_DLP_COOKIES_PATH=cookies.txt
   ```
4. The yt-dlp service will automatically pass `--cookies cookies.txt` when this env var is present.

> **Note**: Never commit `cookies.txt` to the repository — it is already in `.gitignore`.


## 📊 Output Format

Results are returned as a list of dictionaries and are exportable to CSV or JSON via the `/api/export/{format}` endpoint.

### Field reference

| Field | Description | Fallback value |
|---|---|---|
| `channel_id` | Unique YT channel identifier | — |
| `channel_name` | Display name | — |
| `subscribers` | Total subscriber count | `"Metric restricted"` |
| `total_views` | Lifetime view count | `"Metric restricted"` |
| `recent_post_1..5` | Upload dates (YYYY-MM-DD) of 5 most recent videos | `"Date not found"` |
| `engagement_rate` | Calculated engagement % | `"Metric restricted"` |
| `campaign_ready` | Boolean audit flag | `false` |

A pre-generated sample output (5 creators) is in [`sample_output.csv`](./sample_output.csv).


## 🧪 Testing

### Test Backend
```bash
# Health check
curl http://localhost:8000/api/health

# Search creators
curl "http://localhost:8000/api/creators/search?q=mkbhd&platform=youtube&limit=10"

# Get stats
curl http://localhost:8000/api/analytics/stats
```

### Test Frontend
1. Open http://localhost:3000
2. Search for creators
3. Check WebSocket console logs
4. Test export functionality
5. Verify stats auto-refresh

## 📊 Features Details

### Rate Limiting
- 2-second mandatory delay between YouTube API calls
- Prevents API abuse and quota exhaustion

### Caching
- 1-hour TTL on creator search results
- Reduces API calls and improves response times

### Fallback System
- Automatically switches to yt-dlp when YouTube API quota exceeded
- Maintains service availability during quota limits

## 🐛 Troubleshooting

### YouTube API Quota Exceeded
System automatically falls back to yt-dlp scraping. Check UI for fallback indicator.

### CORS Errors
Verify `ALLOWED_ORIGINS` in backend `.env` includes your frontend URL.

### Connection Refused
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

### WebSocket Connection Failed
- Backend must be running
- Check network tab in browser DevTools

## 📝 Development Workflow

1. **Backend changes**: Edit in `backend/`, server auto-reloads with `--reload`
2. **Frontend changes**: Edit components, Next.js auto-refreshes
3. **API contract changes**: Update both `backend/models/schemas.py` and `lib/types.ts`
4. **Hook changes**: Test hook with component to verify integration

## 🚀 Production Checklist

- [ ] YouTube API key configured
- [ ] Backend running on production server
- [ ] Frontend deployed to Vercel
- [ ] NEXT_PUBLIC_API_URL set to production backend URL
- [ ] ALLOWED_ORIGINS updated with production domain
- [ ] DEBUG=false in production backend
- [ ] Monitor backend logs for errors
- [ ] Set up alerts for API failures
- [ ] Test all features on production

## 🔒 Security

- TypeScript strict mode enabled
- Security headers configured
- No browser source maps in production
- Content Security Policy ready
- XSS protection enabled

## 📊 Performance Optimizations

- Image optimization with AVIF/WebP format support
- Package import optimization
- Experimental optimizePackageImports enabled
- Response compression enabled
- Minified output

## 📄 License

MIT
