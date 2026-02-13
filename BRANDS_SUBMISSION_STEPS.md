# Quick Guide: Submit Icons to Home Assistant Brands

## Why This Is Needed
Home Assistant **only** shows icons from the official brands repository. Local icons in custom integrations are **not supported** by design.

## Quick Steps (5 minutes)

### 1. Fork the Brands Repo
Go to: https://github.com/home-assistant/brands
Click: **Fork** (top right)

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/brands.git
cd brands
```

### 3. Create Branch
```bash
git checkout -b add-elering-ee
```

### 4. Add Your Icons
```bash
# Create folder
mkdir -p custom_integrations/elering_ee

# Copy icons from your integration repo
cp path/to/ha-elering-ee/brands_submission/elering_ee/* custom_integrations/elering_ee/

# Or manually copy these 3 files to custom_integrations/elering_ee/:
# - icon.png (256x256)
# - logo.png (512x256)
# - dark_icon.png (256x256)
```

### 5. Commit and Push
```bash
git add custom_integrations/elering_ee/
git commit -m "Add Elering Estonia (elering_ee)"
git push origin add-elering-ee
```

### 6. Create Pull Request
1. Go to: https://github.com/home-assistant/brands
2. Click: **Pull requests** → **New pull request**
3. Click: **compare across forks**
4. Select: your fork → add-elering-ee branch
5. Create PR with title: **Add Elering Estonia (elering_ee)**

### 7. Wait for Approval
- Usually takes 1-3 days
- Automated checks will run
- Once merged, icons appear in Home Assistant!

## Files You Need

Your icons are ready in: `brands_submission/elering_ee/`
- ✅ icon.png (256x256)
- ✅ logo.png (512x256)
- ✅ dark_icon.png (256x256)

## After Approval

Once the PR is merged:
- ✅ Icons show in Home Assistant
- ✅ HACS brands check passes (8/8)
- ✅ Integration looks professional

## Need Help?

See full guide: `brands_submission/README.md`

Or I can walk you through it step by step!
