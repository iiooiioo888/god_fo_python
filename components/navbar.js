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
          background: linear-gradient(90deg, #8b5cf6, #a855f7);
          transform: translateY(-2px);
        }

        /* User profile styles */
        .user-menu {
          position: relative;
        }

        .user-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          cursor: pointer;
          transition: all 0.2s;
        }

        .user-avatar:hover {
          transform: scale(1.1);
        }

        .user-dropdown {
          position: absolute;
          top: 100%;
          right: 0;
          margin-top: 8px;
          background: rgba(15, 23, 42, 0.95);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(148, 163, 184, 0.1);
          border-radius: 8px;
          width: 200px;
          z-index: 1000;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
          opacity: 0;
          visibility: hidden;
          transform: translateY(-10px);
          transition: all 0.2s;
        }

        .user-dropdown.show {
          opacity: 1;
          visibility: visible;
          transform: translateY(0);
        }

        .user-dropdown-item {
          display: block;
          padding: 12px 16px;
          color: #cbd5e1;
          text-decoration: none;
          transition: background-color 0.2s;
        }

        .user-dropdown-item:hover {
          background-color: rgba(59, 130, 246, 0.1);
          color: #3b82f6;
        }

        .user-dropdown-divider {
          border-bottom: 1px solid rgba(148, 163, 184, 0.1);
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
          <li><a href="/workflow.html"><i data-feather="zap"></i> 镜流</a></li>
          <li><a href="/prediction.html"><i data-feather="eye"></i> 预言</a></li>
          <li><a href="/cluster.html"><i data-feather="network"></i> 镜阵</a></li>
          <li><a href="/sdk.html"><i data-feather="code"></i> SDK</a></li>
          <li><a href="/chat.html"><i data-feather="bot"></i> 镜灵</a></li>
          <li><a href="/status.html"><i data-feather="activity"></i> 监控</a></li>
          <li><a href="/community.html"><i data-feather="message-square"></i> 镜厅</a></li>
          <li><a href="/security.html"><i data-feather="shield"></i> 镜盾</a></li>
          <li><a href="/extension.html"><i data-feather="file-text"></i> 扩展规划</a></li>
        </ul>
        
        <div class="auth-buttons" id="auth-buttons">
          <button class="btn btn-login" onclick="openAuthModal('login')">登录</button>
          <button class="btn btn-signup" onclick="openAuthModal('register')">注册</button>
        </div>

        <div class="user-menu" id="user-menu" style="display: none;">
          <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%233b82f6'><circle cx='12' cy='8' r='4'/><path d='M12 14c-6.1 0-8 4-8 4v2h16v-2s-1.9-4-8-4z'/></svg>"
               alt="用户头像" class="user-avatar" onclick="toggleUserMenu()">
          <div class="user-dropdown" id="user-dropdown">
            <div class="user-dropdown-item" onclick="navigateTo('/profile.html')">
              <i data-feather="user"></i> 个人中心
            </div>
            <div class="user-dropdown-item" onclick="navigateTo('/mirrors.html')">
              <i data-feather="bookmark"></i> 我的收藏
            </div>
            <div class="user-dropdown-item" onclick="navigateTo('/notifications')">
              <i data-feather="bell"></i> 消息中心
            </div>
            <div class="user-dropdown-item">
              <i data-feather="message-square"></i> 我的帖子
            </div>
            <div class="user-dropdown-item">
              <i data-feather="download"></i> 下载历史
            </div>
            <div class="user-dropdown-divider"></div>
            <div class="user-dropdown-item">
              <i data-feather="settings"></i> 设置
            </div>
            <div class="user-dropdown-item" onclick="logout()">
              <i data-feather="log-out"></i> 退出登录
            </div>
          </div>
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
