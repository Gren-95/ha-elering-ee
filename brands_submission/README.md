# Brands Repository Submission

To make the HACS brands validation check pass, you need to submit your integration to the official Home Assistant brands repository.

## Repository

https://github.com/home-assistant/brands

## What You Need

1. **icon.png** - 256x256px PNG with transparency
2. **logo.png** - 512x256px PNG with transparency (optional but recommended)
3. **dark_icon.png** - 256x256px for dark mode (optional)
4. **dark_logo.png** - 512x256px for dark mode (optional)

## File Structure for Submission

```
brands/
└── custom_integrations/
    └── elering_ee/
        ├── icon.png
        ├── logo.png
        ├── dark_icon.png (optional)
        └── dark_logo.png (optional)
```

## Submission Steps

### 1. Fork the Repository
```bash
# Go to https://github.com/home-assistant/brands
# Click "Fork" button
```

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
mkdir -p custom_integrations/elering_ee
cp /path/to/your/icon.png custom_integrations/elering_ee/
cp /path/to/your/logo.png custom_integrations/elering_ee/
```

### 5. Commit and Push
```bash
git add custom_integrations/elering_ee/
git commit -m "Add Elering Estonia integration branding"
git push origin add-elering-ee
```

### 6. Create Pull Request
1. Go to https://github.com/home-assistant/brands
2. Click "Pull requests" → "New pull request"
3. Click "compare across forks"
4. Select your fork and branch
5. Create PR with title: "Add Elering Estonia (elering_ee)"
6. Wait for review and approval

## After Approval

Once your PR is merged:
- HACS brands validation will pass ✅
- Your integration will have a custom icon in Home Assistant
- It may take a few days for the changes to propagate

## Need Icons?

Place your icon files in the `icons/` folder of this repository first, then copy them for the brands submission.

## Questions?

See: https://github.com/home-assistant/brands/blob/master/CONTRIBUTING.md
