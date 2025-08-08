# Environment Setup Guide for StoxAI

This guide will help you set up your StoxAI application on Netlify with Neon database integration.

## Prerequisites

1. **GitHub Repository**: Your code should be pushed to a GitHub repository
2. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)
3. **Neon Database**: Already provisioned (as shown in your dashboard)

## Step 1: Connect Repository to Netlify

1. Go to your Netlify dashboard
2. Click "Add new site" → "Import an existing project"
3. Connect to GitHub and select your repository
4. Configure the build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
   - **Node version**: `18`

## Step 2: Configure Environment Variables

In your Netlify dashboard, go to **Site settings** → **Environment variables** and add the following:

### Required Variables

```
JWT_SECRET_KEY=your-actual-secure-jwt-secret-key
NETLIFY_DATABASE_URL=your-neon-database-url
NETLIFY_DATABASE_URL_UNPOOLED=your-neon-database-url-unpooled
```

### Optional Variables (for development)

```
VITE_USE_MOCK_AUTH=true
```

## Step 3: Claim Your Neon Database

1. Go to your Netlify dashboard
2. Navigate to **Extensions** → **Neon**
3. Click "Claim database" to prevent expiration
4. This will keep your database active beyond the initial 7-day period

## Step 4: Deploy

1. Netlify will automatically deploy when you push changes to your repository
2. You can also trigger manual deployments from the Netlify dashboard
3. Check the deployment logs for any build errors

## Step 5: Verify Deployment

1. **Check API Health**: Visit `https://your-site.netlify.app/.netlify/functions/api/health`
2. **Test Registration**: Try creating a new user account
3. **Test Login**: Verify authentication works
4. **Test Chatbot**: Send a message through the chatbot interface

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Node.js version (should be 18+)
   - Verify all dependencies are installed
   - Check for TypeScript compilation errors

2. **Database Connection Issues**:
   - Verify Neon database URLs are correct
   - Ensure database is claimed and active
   - Check network connectivity

3. **Authentication Issues**:
   - Verify JWT_SECRET_KEY is set
   - Check token expiration settings
   - Ensure CORS is properly configured

4. **API Endpoint Errors**:
   - Verify netlify.toml configuration
   - Check function deployment logs
   - Ensure proper routing setup

### Debugging Steps

1. **Check Function Logs**:
   - Go to Netlify dashboard → **Functions** → **api**
   - View recent invocations and logs

2. **Test Local Development**:

   ```bash
   cd stoxai
   npm install
   npm run dev
   ```

3. **Verify Environment Variables**:
   - Check that all variables are set in Netlify
   - Ensure no typos in variable names

## Security Considerations

1. **JWT Secret**: Use a strong, unique secret key in production
2. **Database Credentials**: Keep database URLs secure
3. **CORS**: Configure CORS properly for your domain
4. **HTTPS**: Netlify provides HTTPS by default

## Performance Optimization

1. **Function Optimization**:
   - Keep functions lightweight
   - Use connection pooling for database
   - Implement proper error handling

2. **Frontend Optimization**:
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading

## Monitoring

1. **Netlify Analytics**: Monitor site performance
2. **Function Logs**: Track API usage and errors
3. **Database Monitoring**: Monitor Neon database usage
4. **Error Tracking**: Consider adding error tracking service

## Next Steps

After successful deployment:

1. **Custom Domain**: Set up a custom domain in Netlify
2. **SSL Certificate**: Configure SSL (automatic with Netlify)
3. **Analytics**: Add analytics tracking
4. **Backup Strategy**: Set up database backups
5. **Monitoring**: Implement comprehensive monitoring

## Support

If you encounter issues:

1. Check the Netlify documentation
2. Review function logs in Netlify dashboard
3. Verify environment variable configuration
4. Test locally before deploying
5. Check GitHub issues for similar problems
