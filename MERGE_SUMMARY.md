# Stable-New Branch Creation Summary

## ✅ Task Completed Successfully

The **`stable-new`** branch has been successfully created with the latest changes from RVC-Boss/GPT-SoVITS:main merged in.

## Branch: stable-new

### Purpose
The `stable-new` branch merges the latest changes from RVC-Boss/GPT-SoVITS:main (upstream) while maintaining the stable branch's library-focused approach.

### What Was Done

1. ✅ **Created new branch** `stable-new` based on the `stable` branch
2. ✅ **Added upstream remote** pointing to `https://github.com/RVC-Boss/GPT-SoVITS.git`
3. ✅ **Fetched latest changes** from RVC-Boss/GPT-SoVITS:main (commit c767f0b)
4. ✅ **Merged upstream/main** into stable-new using `--allow-unrelated-histories`
5. ✅ **Resolved conflicts** strategically:
   - Kept stable branch's README.md (library-focused documentation)
   - Kept stable branch's configuration files (.dockerignore, .gitignore, Dockerfile, docker-compose.yaml, install.sh, requirements.txt)
   - Kept stable branch's documentation files (docs/*/README.md, docs/*/Changelog*.md)
   - Accepted all new files and code from upstream (294+ files added)

### Merge Details
- **Branch**: `stable-new`
- **Merge commit hash**: `07ff104`
- **Commit message**: "Merge latest changes from RVC-Boss/GPT-SoVITS:main into stable-new"
- **Parent commits**: 
  - `e68dcf2` (stable branch)
  - `c767f0b` (upstream/main)

### Current Status
- ✅ Branch `stable-new` exists locally and is ready
- ✅ Contains all latest upstream changes (c767f0b: 修复bug #2704)
- ✅ Maintains stable branch's library-focused approach
- ⚠️ **Branch needs to be pushed to origin manually**

### Next Step: Push the Branch

Due to authentication limitations in the automated environment, you need to push the branch manually. Run either:

**Option 1: Use the provided script**
```bash
./push-stable-new.sh
```

**Option 2: Push directly**
```bash
git push origin stable-new
```

After pushing, the branch will be available at:
`https://github.com/rsxdalv/GPT-SoVITS/tree/stable-new`

### What's New in stable-new
The merge brought in 294+ files from upstream including:
- Complete GPT_SoVITS module updates (AR models, BigVGAN, TTS components)
- New tools (ASR, audio processing, UVR5 integration)
- Enhanced training scripts (s1_train.py, s2_train.py, s2_train_v3.py, etc.)
- Updated API endpoints (api.py, api_v2.py)
- Additional i18n locale files
- New WebUI components
- GitHub Actions workflows
- And many more updates from the upstream repository

All while retaining the stable branch's library-oriented setup and documentation.
