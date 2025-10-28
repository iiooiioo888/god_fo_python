class CustomFooter extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        footer {
          background: rgba(15, 23, 42, 0.9);
          color: #cbd5e1;
          padding: 4rem 2rem 2rem;
          border-top: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 2rem;
        }
        
        .footer-column h3 {
          color: white;
          margin-bottom: 1.5rem;
          font-size: 1.25rem;
        }
        
        .footer-column ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        
        .footer-column ul li {
          margin-bottom: 0.75rem;
        }
        
        .footer-column ul li a {
          color: #94a3b8;
          text-decoration: none;
          transition: color 0.2s;
        }
        
        .footer-column ul li a:hover {
          color: #3b82f6;
        }
        
        .social-links {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
        }
        
        .social-links a {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: rgba(148, 163, 184, 0.1);
          color: #cbd5e1;
          transition: all 0.2s;
        }
        
        .social-links a:hover {
          background: #3b82f6;
          color: white;
          transform: translateY(-3px);
        }
        
        .copyright {
          max-width: 1200px;
          margin: 3rem auto 0;
          padding-top: 2rem;
          border-top: 1px solid rgba(148, 163, 184, 0.1);
          text-align: center;
          color: #64748b;
          font-size: 0.875rem;
        }
        
        @media (max-width: 768px) {
          footer {
            padding: 3rem 1rem 1rem;
          }
        }
      </style>
      <footer>
        <div class="footer-content">
          <div class="footer-column">
            <h3>镜界平台</h3>
            <p style="color: #94a3b8; line-height: 1.6; margin-bottom: 1rem;">
              让每一张图片、每一段视频，都有迹可循。
              专业的数据源镜像平台，助力开发者高效获取网络资源。
            </p>
            <div class="social-links">
              <a href="#"><i data-feather="github"></i></a>
              <a href="#"><i data-feather="twitter"></i></a>
              <a href="#"><i data-feather="linkedin"></i></a>
            </div>
          </div>
          
          <div class="footer-column">
            <h3>核心功能</h3>
            <ul>
              <li><a href="/mirrors.html">镜库 - 数据源仓库</a></li>
              <li><a href="/tools.html">照妖镜分析工具</a></li>
              <li><a href="/#status-monitoring">镜像状态监控</a></li>
              <li><a href="/tools.html">镜像工坊 - 工具集成</a></li>
              <li><a href="/community.html">镜厅 - 社区交流</a></li>
              <li><a href="/extension.html">扩展规划文档</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h3>用户服务</h3>
            <ul>
              <li><a href="#">帮助中心</a></li>
              <li><a href="#">使用教程</a></li>
              <li><a href="#">API文档</a></li>
              <li><a href="#">开发者工具</a></li>
              <li><a href="#">高级会员</a></li>
              <li><a href="#">企业服务</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h3>关于我们</h3>
            <ul>
              <li><a href="#">平台介绍</a></li>
              <li><a href="#">团队成员</a></li>
              <li><a href="#">发展历程</a></li>
              <li><a href="#">合作伙伴</a></li>
              <li><a href="#">联系我们</a></li>
              <li><a href="#">法律声明</a></li>
            </ul>
          </div>
        </div>
        
        <div class="copyright">
          &copy; 2023 镜界 - 数据源镜像平台. 保留所有权利。
          <br>
          遵循合法合规原则，尊重网站服务条款和版权法规。
        </div>
      </footer>
    `;
    
    // Initialize Feather icons
    import('https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js').then(() => {
      feather.replace();
    });
  }
}

customElements.define('custom-footer', CustomFooter);
