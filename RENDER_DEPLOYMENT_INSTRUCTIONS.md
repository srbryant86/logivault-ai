# LogiVault AI - Render Deployment Instructions

## Quick Fix Steps:

1. **Commit these changes:**
   ```bash
   git add .
   git commit -m "Fix Render deployment configuration v2"
   git push origin main
   ```

2. **In Render Dashboard:**
   - Go to your logivault-ai service
   - Click "Settings" → "Build & Deploy"
   - Update Build Command to: `pip install --upgrade pip && pip install -r requirements.txt`
   - Update Start Command to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Click "Save Changes"

3. **Set Environment Variables:**
   - Go to "Environment" tab
   - Add: `CLAUDE_API_KEY` = your_actual_claude_key
   - Add: `PYTHON_VERSION` = 3.11
   - Add: `PIP_NO_CACHE_DIR` = 1

4. **Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

## If Still Failing:

Try these alternative approaches:

### Option A: Use Dockerfile
- Render will automatically detect the Dockerfile
- This provides more control over the build environment

### Option B: Minimal Requirements
- The new requirements.txt has only essential packages
- Reduces chance of dependency conflicts

### Option C: Check Logs
- Look for specific error messages
- Common issues: missing system dependencies, Python version mismatch

## Testing:
After deployment, test the endpoint:
```bash
curl https://your-render-url.onrender.com/health
```

## Support:
If issues persist, check:
1. Python version compatibility
2. System dependencies
3. Environment variable configuration
4. CORS settings in backend/main.py
