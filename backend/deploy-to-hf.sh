#!/bin/bash
# Deployment script for Hugging Face Spaces

echo "🚀 Preparing files for Hugging Face deployment..."

# Copy and rename files
cp Dockerfile.hf Dockerfile
cp requirements-hf.txt requirements.txt
cp .env.production .env

echo "✅ Files prepared!"
echo ""
echo "Next steps:"
echo "1. Initialize git: git init"
echo "2. Add Hugging Face remote: git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/SPACE-NAME"
echo "3. Add files: git add ."
echo "4. Commit: git commit -m 'Initial deployment'"
echo "5. Push: git push hf main"
