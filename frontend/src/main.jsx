import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import 'antd/dist/reset.css' // 確保 antd 樣式正常

// 🎯 移除 React.StrictMode，避免開發階段元件雙重渲染引發後端死鎖
ReactDOM.createRoot(document.getElementById('root')).render(
  <App />
)
