#!/bin/bash

echo "🚀 Setting up my.local domain..."

# Check if my.local already exists in /etc/hosts
if grep -q "my.local" /etc/hosts; then
    echo "✅ my.local already exists in /etc/hosts"
else
    echo "➕ Adding my.local to /etc/hosts..."
    echo "127.0.0.1    my.local" | sudo tee -a /etc/hosts
    echo "✅ my.local added to /etc/hosts"
fi

# Display current hosts file content for my.local
echo ""
echo "📋 Current hosts file entries for my.local:"
grep "my.local" /etc/hosts || echo "No entries found"

echo ""
echo "🎉 Domain setup complete! You can now access your site at:"
echo "   http://my.local"
echo ""
echo "📌 To remove my.local later, run:"
echo "   sudo sed -i '' '/my.local/d' /etc/hosts"