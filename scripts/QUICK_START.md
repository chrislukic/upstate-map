# Quick Start Guide - Place ID Assignment

## 🚀 Quick Setup (5 minutes)

### 1. Get Google Places API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select project → Enable "Places API" → Create API Key
3. Copy your API key

### 2. Set Environment Variable
```bash
export GOOGLE_PLACES_API_KEY="your_api_key_here"
```

### 3. Test Connection
```bash
cd scripts
python test_api_connection.py
```

### 4. Run Assignment
```bash
python run_place_id_assignment.py
```

## 📋 What It Does

- **Finds accurate place IDs** for all locations in your JSON files
- **Adds Google Maps URLs** for easy navigation
- **Handles rate limiting** to respect API quotas
- **Provides detailed logging** of the process
- **Updates files in place** with the new data

## 📊 Expected Results

- **children.json**: ~25 place IDs assigned
- **trail-heads.json**: ~60 place IDs assigned  
- **our-airbnbs.json**: ~15 place IDs assigned
- **points_of_interest.json**: ~32 place IDs assigned
- **Total cost**: ~$0.02 (within free tier)

## 🔧 Advanced Usage

```bash
# Process specific files only
python assign_place_ids.py --api-key YOUR_KEY --files children.json

# Dry run (preview changes)
python assign_place_ids.py --api-key YOUR_KEY --dry-run

# Custom data directory
python assign_place_ids.py --api-key YOUR_KEY --data-dir /path/to/data
```

## ⚠️ Important Notes

- **Backup your data** before running (the script modifies files in place)
- **API costs**: First 1,000 requests/day are free, then $0.017 per request
- **Rate limiting**: Built-in delays prevent quota exhaustion
- **Logging**: Check `place_id_assignment.log` for detailed information

## 🆘 Troubleshooting

**API Key Issues:**
```bash
# Test your API key
python test_api_connection.py
```

**Permission Errors:**
```bash
# Make sure you have write access
ls -la public/data/
```

**Quota Exceeded:**
- Wait 24 hours for reset
- Check Google Cloud Console for usage
- Consider upgrading to paid tier

## 📁 Files Created

- `assign_place_ids.py` - Main assignment script
- `run_place_id_assignment.py` - Simple wrapper script
- `test_api_connection.py` - API connection tester
- `requirements_place_ids.txt` - Python dependencies
- `README_place_ids.md` - Detailed documentation
- `place_id_assignment.log` - Process log (created when run)

## 🎯 Success Indicators

You'll know it worked when you see:
- ✅ "API connection successful!" in test
- ✅ "Overall: X/X successful" in summary
- ✅ JSON files now have `place_id` and `google_maps_url` fields
- ✅ No more `null` place_id values
