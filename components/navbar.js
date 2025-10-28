class CustomNavbar extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          transition: all 0.3s ease;
        }
        
        nav {
          background: rgba(15, 23, 42, 0.8);
          backdrop-filter: blur(10px);
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        :host(.scrolled) nav {
          background: rgba(15, 23, 42, 0.95);
          padding: 0.75rem 2rem;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .logo {
          display: flex;
          align-items: center;
          color: white;
          font-weight: bold;
          font-size: 1.5rem;
          text-decoration: none;
        }
        
        .logo i {
          margin-right: 10px;
          color: #3b82f6;
        }
        
        .nav-links {
          display: flex;
          gap: 2rem;
          list-style: none;
          margin: 0;
          padding: 0;
        }
        
        .nav-links a {
          color: #cbd5e1;
          text-decoration: none;
          font-weight: 500;
          transition: color 0.2s;
          display: flex;
          align-items: center;
        }
        
        .nav-links a:hover {
          color: #3b82f6;
        }
        
        .nav-links a i {
          margin-right: 5px;
        }
        
        .auth-buttons {
          display: flex;
          gap: 1rem;
        }
        
        .btn {
          padding: 0.5rem 1.25rem;
          border-radius: 0.5rem;
          font-weight: 500;
          transition: all 0.2s;
          cursor: pointer;
        }
        
        .btn-login {
          background: transparent;
          color: #cbd5e1;
          border: 1px solid #475569;
        }
        
        .btn-login:hover {
          background: rgba(59, 130, 246, 0.1);
          color: #3b82f6;
          border-color: #3b82f6;
        }
        
        .btn-signup {
          background: linear-gradient(90deg, #3b82f6, #8b5cf6);
          color: white;
          border: none;
        }
        
        .btn-signup:hover {
          opacity: 0.9;
          transform: translateY(-2px);
        }
        
        .mobile-menu-btn {
          display: none;
          background: none;
          border: none;
          color: white;
          font-size: 1.5rem;
          cursor: pointer;
        }
        
        @media (max-width: 768px) {
          .nav-links, .auth-buttons {
            display: none;
          }
          
          .mobile-menu-btn {
            display: block;
          }
        }
      </style>
      <nav>
        <a href="/" class="logo">
          <i data-feather="disc"></i>
          <span>镜界</span>
        </a>
        
        <ul class="nav-links">
          <li><a href="/"><i data-feather="home"></i> 首页</a></li>
          <li><a href="/mirrors.html"><i data-feather="database"></i> 镜库</a></li>
          <li><a href="/tools.html"><i data-feather="tool"></i> 工坊</a></li>
          <li><a href="/collection.html"><i data-feather="hexagon"></i> 万花筒</a></li>
          <li><a href="/pipeline.html"><i data-feather="git-branch"></i> 镜链</a></li>
          <li><a href="/prediction.html"><i data-feather="eye"></i> 预言</a></li>
          <li><a href="/cluster.html"><i data-feather="network"></i> 镜阵</a></li>
          <li><a href="/sdk.html"><i data-feather="code"></i> SDK</a></li>
          <li><a href="/chat.html"><i data-feather="bot"></i> 镜灵</a></li>
          <li><a href="/status.html"><i data-feather="activity"></i> 监控</a></li>
          <li><a href="/community.html"><i data-feather="message-square"></i> 镜厅</a></li>
          <li><a href="/extension.html"><i data-feather="file-text"></i> 扩展规划</a></li>
        </ul>
        
        <div class="auth-buttons">
          <button class="btn btn-login">登录</button>
          <button class="btn btn-signup">注册</button>
        </div>
        
        <button class="mobile-menu-btn">
          <i data-feather="menu"></i>
        </button>
      </nav>
    `;
    
    // Initialize Feather icons
    import('https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js').then(() => {
      feather.replace();
    });
  }
}

customElements.define('custom-navbar', CustomNavbar);
