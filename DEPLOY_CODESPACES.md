# 🚀 Deploy Aclarador in GitHub Codespaces

## Overview
Complete guide to deploy and run the Aclarador multi-agent system using GitHub Codespaces - no local setup required!

---

## 📋 Prerequisites
- GitHub account
- GROQ_API_KEY (get from https://console.groq.com/)

---

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub
```bash
# In your local directory
git add .
git commit -m "Add multi-agent aclarador system"
git push origin main
```

### Step 2: Create Codespace
1. Go to your GitHub repository
2. Click the green **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**
5. Wait for the environment to load (2-3 minutes)

### Step 3: Set Environment Variables
In the Codespace terminal:
```bash
# Set your GROQ API key
export GROQ_API_KEY="your_groq_api_key_here"

# Make it persistent for the session
echo 'export GROQ_API_KEY="your_groq_api_key_here"' >> ~/.bashrc
```

### Step 4: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 5: Test the System
```bash
# Test basic functionality first
python3 run_prototype.py

# Should show: "🎊 PROTOTYPE STATUS: WORKING!"
```

### Step 6: Set Up Knowledge Base (Optional)
```bash
# Initialize PDF knowledge base
python setup_knowledge_base.py

# Test knowledge base
python test_knowledge_base.py
```

### Step 7: Run the Application
Choose one of these options:

#### Option A: Enhanced Multi-Agent App
```bash
streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0
```

#### Option B: Original Simple App
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Step 8: Access Your App
1. Codespaces will show a popup: **"Your application running on port 8501 is available"**
2. Click **"Open in Browser"** 
3. Or go to the **"Ports"** tab and click the URL next to port 8501

---

## 🛠 Codespace Configuration (Optional)

### Create `.devcontainer/devcontainer.json`
```json
{
  "name": "Aclarador Python Environment",
  "image": "mcr.microsoft.com/vscode/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8501],
  "portsAttributes": {
    "8501": {
      "label": "Streamlit App",
      "onAutoForward": "openBrowser"
    }
  }
}
```

### Create `.devcontainer/README.md`
```markdown
# Aclarador Development Container

This devcontainer automatically:
- Sets up Python 3.11 environment
- Installs dependencies from requirements.txt
- Forwards port 8501 for Streamlit
- Opens browser automatically when app starts
```

---

## 🚦 Quick Start Commands

After Codespace loads:

```bash
# 1. Set API key
export GROQ_API_KEY="your_key_here"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test system
python3 run_prototype.py

# 4. Run app (choose one)
streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0
# OR
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🔧 Troubleshooting

### Problem: Dependencies fail to install
**Solution:**
```bash
# Try installing individually
pip install streamlit groq
pip install langchain chromadb sentence-transformers pypdf langchain-community
```

### Problem: PDF processing fails
**Solution:**
```bash
# Skip knowledge base setup, use basic mode
streamlit run app_enhanced.py
# Select "Groq original" in the sidebar
```

### Problem: Port not accessible
**Solution:**
```bash
# Check ports tab in Codespace
# Make sure app is running with --server.address 0.0.0.0
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Problem: GROQ API key not working
**Solution:**
```bash
# Verify key is set
echo $GROQ_API_KEY

# Reset if needed
export GROQ_API_KEY="your_new_key"
```

---

## 🌐 Accessing Your App

### URL Format
Your Codespace app will be available at:
```
https://[codespace-name]-8501.app.github.dev
```

### Sharing Your App
1. Go to **Ports** tab in Codespace
2. Right-click port 8501
3. Select **"Port Visibility" → "Public"**
4. Share the generated URL

---

## 🎯 Testing Your Deployment

### Test Cases to Try

1. **Basic Text:**
```
"Este es un texto simple para probar."
```

2. **Grammar Issues:**
```
"Este texto tiene errores que que necesitan corrección."
```

3. **Long Sentences:**
```
"Este es un texto muy largo y complejo que tiene más de treinta palabras en esta oración y utiliza vocabulario técnico que podría ser difícil de entender para los usuarios."
```

4. **Web Content:**
```
"Nuestro sitio web www.ejemplo.com ofrece servicios de SEO y optimización para motores de búsqueda."
```

### Expected Results
- ✅ Grammar corrections applied
- ✅ Style suggestions provided  
- ✅ Text analysis displayed
- ✅ Agent coordination working
- ✅ Quality scores calculated

---

## 📊 Features Available in Codespaces

### Multi-Agent System Features
- **🔍 Analyzer**: Text classification and routing
- **📝 Grammar**: Grammar error detection and correction
- **✨ Style**: Readability and clarity improvements  
- **🔍 SEO**: Search optimization while maintaining clarity
- **✅ Validator**: Quality assurance and scoring

### Interface Features
- **🎛 Method Selection**: Multi-agent vs. Original Groq
- **🤖 Agent Configuration**: Select which agents to use
- **📊 Results Tabs**: Resultado, Detalles, Manual
- **📈 Status Indicators**: System health monitoring
- **🎨 Responsive UI**: Works on different screen sizes

---

## 🔄 Updating Your Deployment

### Push Updates
```bash
# Make changes locally
git add .
git commit -m "Update description"
git push origin main

# In Codespace, pull changes
git pull origin main

# Restart application
# Ctrl+C to stop current app
streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0
```

### Rebuild Environment
If major changes to requirements:
1. Stop current Codespace
2. Create new Codespace
3. Follow setup steps again

---

## 💡 Pro Tips

### Performance Optimization
- **Cache agents**: System automatically caches agent coordinator
- **Minimize dependencies**: Use original app if performance is slow
- **Monitor resources**: Check Codespace CPU/memory usage

### Development Workflow
- **Live reload**: Streamlit automatically reloads on file changes
- **Debug mode**: Add `st.write()` statements for debugging
- **Log outputs**: Check terminal for error messages

### Security Best Practices
- **Environment variables**: Never commit API keys to Git
- **Port visibility**: Keep ports private unless sharing intentionally
- **Regular updates**: Keep dependencies updated

---

## 🎉 Success Checklist

- [ ] Codespace created and running
- [ ] Environment variables set
- [ ] Dependencies installed successfully
- [ ] Prototype test passes
- [ ] Streamlit app accessible via browser
- [ ] Text processing works correctly
- [ ] Multi-agent system functioning
- [ ] Results displaying properly

---

## 📞 Support Resources

### GitHub Codespaces Documentation
- [Codespaces Overview](https://docs.github.com/en/codespaces)
- [Port Forwarding](https://docs.github.com/en/codespaces/developing-in-codespaces/forwarding-ports-in-your-codespace)
- [Environment Variables](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-environment-variables-for-your-codespaces)

### Streamlit Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [Deployment Guide](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

### GROQ API
- [GROQ Console](https://console.groq.com/)
- [API Documentation](https://console.groq.com/docs/quickstart)

---

## 🎯 Next Steps After Deployment

1. **Share your app** with the public URL
2. **Test with real content** from your use cases
3. **Customize agents** for your specific needs
4. **Set up knowledge base** with your own PDF documents
5. **Monitor usage** and gather feedback

---

**🎊 Congratulations! Your Aclarador multi-agent system is now running in GitHub Codespaces and accessible from anywhere!**