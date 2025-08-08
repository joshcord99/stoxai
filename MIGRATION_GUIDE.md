# Migration Guide: From Two Repos to Single Netlify Repository

This guide will help you migrate from your current two-repository setup (stoxai + stoxai-backend) to a single consolidated Netlify repository.

## Current Setup

- **stoxai**: Vue.js frontend (currently on Netlify)
- **stoxai-backend**: Flask backend (currently on Render)
- **Neon Database**: Already provisioned on Netlify

## Target Setup

- **stoxai**: Consolidated Vue.js frontend + Netlify serverless functions
- **Neon Database**: Same database, now accessed via serverless functions

## Migration Steps

### Step 1: Backup Current Data

1. **Export User Data** (if any users exist):

   ```bash
   # From your current backend
   curl -X GET "https://your-render-backend.com/api/account/export" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

2. **Backup Database** (if needed):
   - Use Neon's backup feature
   - Export any important data

### Step 2: Update Repository Structure

1. **Keep the stoxai repository** as your main repository
2. **Archive the stoxai-backend repository** (optional)
3. **Update stoxai repository** with the new serverless functions

### Step 3: Update Environment Variables

#### In Netlify Dashboard:

**Remove old variables:**

- Any backend-specific variables

**Add new variables:**

```
JWT_SECRET_KEY=your-actual-secure-jwt-secret-key
NETLIFY_DATABASE_URL=your-neon-database-url
NETLIFY_DATABASE_URL_UNPOOLED=your-neon-database-url-unpooled
```

### Step 4: Update Frontend Configuration

The frontend has been updated to:

- Use Netlify functions instead of external backend
- Handle authentication via JWT
- Connect directly to Neon database

### Step 5: Test the Migration

1. **Deploy to Netlify**:

   ```bash
   cd stoxai
   git add .
   git commit -m "Migrate to consolidated Netlify setup"
   git push origin main
   ```

2. **Verify API Endpoints**:
   - Health check: `https://your-site.netlify.app/.netlify/functions/api/health`
   - Registration: Test user registration
   - Login: Test authentication
   - Chatbot: Test AI chatbot

3. **Check Database**:
   - Verify users table is created
   - Test data persistence

### Step 6: Update DNS and Domains

1. **Update any custom domains** to point to Netlify
2. **Remove Render backend** from your domain configuration
3. **Update any external references** to the old backend

### Step 7: Clean Up

1. **Archive Render backend** (optional)
2. **Remove old environment variables** from Render
3. **Update documentation** to reflect new setup
4. **Notify users** of any downtime (if applicable)

## API Endpoint Mapping

| Old Flask Endpoint    | New Netlify Function  | Notes         |
| --------------------- | --------------------- | ------------- |
| `/api/auth/login`     | `/api/auth/login`     | Same endpoint |
| `/api/auth/register`  | `/api/auth/register`  | Same endpoint |
| `/api/auth/profile`   | `/api/user/profile`   | Updated path  |
| `/api/auth/watchlist` | `/api/user/watchlist` | Updated path  |
| `/api/user-chatbot`   | `/api/ai_chatbot`     | Updated path  |
| `/api/health`         | `/api/health`         | Same endpoint |

## Database Schema Changes

The new setup uses the same database schema but with automatic table creation:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  watchlist TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Benefits of Migration

1. **Simplified Architecture**: Single repository, single deployment
2. **Cost Reduction**: No separate backend hosting costs
3. **Easier Maintenance**: All code in one place
4. **Better Performance**: Serverless functions scale automatically
5. **Integrated Database**: Direct Neon integration

## Rollback Plan

If issues occur during migration:

1. **Keep Render backend running** during transition
2. **Maintain both deployments** temporarily
3. **Update frontend environment** to point back to Render if needed
4. **Gradually migrate users** to new system

## Post-Migration Checklist

- [ ] All API endpoints working
- [ ] User authentication functional
- [ ] Database connections stable
- [ ] Chatbot responding correctly
- [ ] Watchlist functionality working
- [ ] Account management working
- [ ] Performance acceptable
- [ ] Error monitoring in place
- [ ] Documentation updated
- [ ] Old backend archived

## Support During Migration

If you encounter issues:

1. **Check Netlify function logs** for errors
2. **Verify environment variables** are set correctly
3. **Test locally** before deploying
4. **Monitor database connections**
5. **Check CORS configuration**

## Timeline

- **Day 1**: Deploy new setup alongside existing
- **Day 2**: Test all functionality
- **Day 3**: Switch traffic to new setup
- **Day 4**: Monitor and optimize
- **Day 5**: Clean up old deployment

This migration consolidates your application into a single, maintainable codebase while leveraging Netlify's serverless architecture for better scalability and cost efficiency.
