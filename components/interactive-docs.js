/**
 * Interactive Documentation JavaScript Module
 * Reusable functions for animations and interactions in documentation pages
 */

class InteractiveDocs {
  constructor(options = {}) {
    this.defaults = {
      animationDelay: 300,
      animationDuration: 500,
      scrollOffset: 100,
      autoStart: false
    };

    this.config = { ...this.defaults, ...options };
    this.observers = new Map();
    this.animationTimeouts = [];
  }

  /**
   * Initialize the interactive documentation
   */
  init() {
    this.setupScrollObserver();
    this.setupIntersectionObserver();

    if (this.config.autoStart) {
      this.startAllAnimations();
    }

    // Add global click handlers
    document.addEventListener('click', this.handleGlobalClick.bind(this));

    console.log('InteractiveDocs initialized');
  }

  /**
   * Setup scroll-based animations
   */
  setupScrollObserver() {
    const scrollHandler = this.handleScroll.bind(this);
    window.addEventListener('scroll', scrollHandler);
    this.observers.set('scroll', scrollHandler);
  }

  /**
   * Setup intersection observer for element visibility
   */
  setupIntersectionObserver() {
    const options = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          const animationType = element.dataset.animation || 'animate-in';

          this.animateElement(element, animationType);

          // Unobserve after animation
          observer.unobserve(element);
        }
      });
    }, options);

    this.observers.set('intersection', observer);
  }

  /**
   * Handle global click events
   */
  handleGlobalClick(event) {
    const target = event.target;

    // Handle service card clicks
    if (target.closest('.service-card')) {
      this.handleServiceCardClick(target.closest('.service-card'), event);
    }

    // Handle CRUD button clicks
    if (target.matches('.crud-button')) {
      this.handleCrudButtonClick(target, event);
    }

    // Handle tree node clicks
    if (target.closest('.tree-node-content')) {
      this.handleTreeNodeClick(target.closest('.tree-node-content'), event);
    }

    // Handle API demo clicks
    if (target.matches('.api-demo-btn')) {
      this.handleApiDemoClick(target, event);
    }
  }

  /**
   * Handle scroll events for progress updates
   */
  handleScroll(event) {
    // Update progress bars based on scroll position
    const progressElements = document.querySelectorAll('.progress-fill');
    progressElements.forEach(element => {
      const container = element.closest('[data-progress-container]');
      if (container) {
        const rect = container.getBoundingClientRect();
        const progress = Math.min(100, Math.max(0, ((window.innerHeight - rect.top) / (rect.height + window.innerHeight)) * 100));
        element.style.width = `${progress}%`;
      }
    });
  }

  /**
   * Animate a single element
   */
  animateElement(element, animationType = 'animate-in', delay = 0) {
    const timeoutId = setTimeout(() => {
      element.style.opacity = '0';

      // Apply animation classes
      switch (animationType) {
        case 'slide-in':
          element.classList.add('animate-slide-in');
          break;
        case 'fade-in':
          element.classList.add('animate-fade-in-up');
          break;
        case 'animate-in':
        default:
          element.style.opacity = '1';
          element.classList.add('animate-in');
          break;
      }

      // Force reflow for animation to trigger
      element.offsetHeight;

      element.style.opacity = '1';
    }, delay);

    this.animationTimeouts.push(timeoutId);
  }

  /**
   * Animate a sequence of elements
   */
  animateSequence(elements, interval = 200) {
    elements.forEach((element, index) => {
      this.animateElement(element, 'animate-in', index * interval);
    });
  }

  /**
   * Animate code execution flow
   */
  animateCodeFlow(containerSelector, steps = []) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const stepElements = container.querySelectorAll('.code-step');
    let currentStep = 0;

    const animateNext = () => {
      if (currentStep < stepElements.length) {
        const step = stepElements[currentStep];
        const isLast = currentStep === stepElements.length - 1;

        // Mark previous step as completed
        if (currentStep > 0) {
          stepElements[currentStep - 1].classList.add('completed');
          stepElements[currentStep - 1].classList.remove('active');
        }

        // Animate current step
        step.classList.add('active');

        // Trigger custom event
        if (steps[currentStep] && steps[currentStep].callback) {
          steps[currentStep].callback(step, currentStep);
        }

        currentStep++;

        // Continue to next step after delay
        if (!isLast) {
          setTimeout(animateNext, steps[currentStep - 1]?.duration || 1000);
        }
      }
    };

    animateNext();
  }

  /**
   * Animate data flow between elements
   */
  animateDataFlow(fromSelector, toSelector, data = {}) {
    const fromElement = document.querySelector(fromSelector);
    const toElement = document.querySelector(toSelector);

    if (!fromElement || !toElement) return;

    // Create connection line
    const connection = this.createConnectionLine(fromElement, toElement);
    connection.classList.add('active');

    // Animate data packet
    const packet = document.createElement('div');
    packet.className = 'data-packet';
    packet.textContent = data.label || '📦';
    packet.style.position = 'absolute';
    packet.style.fontSize = '1.2rem';
    packet.style.zIndex = '1000';

    const fromRect = fromElement.getBoundingClientRect();
    const toRect = toElement.getBoundingClientRect();

    packet.style.left = `${fromRect.left + fromRect.width / 2}px`;
    packet.style.top = `${fromRect.top + fromRect.height / 2}px`;

    document.body.appendChild(packet);

    // Animate packet movement
    setTimeout(() => {
      packet.style.transition = 'all 1s ease-in-out';
      packet.style.left = `${toRect.left + toRect.width / 2}px`;
      packet.style.top = `${toRect.top + toRect.height / 2}px`;
    }, 100);

    // Clean up
    setTimeout(() => {
      document.body.removeChild(packet);
      connection.classList.remove('active');
    }, 1500);
  }

  /**
   * Create animated connection line between two elements
   */
  createConnectionLine(fromElement, toElement) {
    const fromRect = fromElement.getBoundingClientRect();
    const toRect = toElement.getBoundingClientRect();

    const connection = document.createElement('div');
    connection.className = 'data-connection';

    // Calculate line properties
    const length = Math.sqrt(Math.pow(toRect.left - fromRect.left, 2) + Math.pow(toRect.top - fromRect.top, 2));
    const angle = Math.atan2(toRect.top - fromRect.top, toRect.left - fromRect.left) * 180 / Math.PI;

    connection.style.width = `${length}px`;
    connection.style.left = `${fromRect.left + fromRect.width / 2}px`;
    connection.style.top = `${fromRect.top + fromRect.height / 2}px`;
    connection.style.transformOrigin = '0 50%';
    connection.style.transform = `rotate(${angle}deg)`;

    document.body.appendChild(connection);

    // Auto-remove after animation
    setTimeout(() => {
      if (connection.parentNode) {
        connection.parentNode.removeChild(connection);
      }
    }, 3000);

    return connection;
  }

  /**
   * Handle service card interactions
   */
  handleServiceCardClick(card, event) {
    const cardId = card.dataset.serviceId;
    card.classList.add('active');

    // Trigger service-specific animation
    switch (cardId) {
      case 'datasource':
        this.animateDataSourceService();
        break;
      case 'search':
        this.animateSearchService();
        break;
      case 'category':
        this.animateCategoryService();
        break;
    }

    // Remove active state after animation
    setTimeout(() => {
      card.classList.remove('active');
    }, 3000);
  }

  /**
   * Handle CRUD operations animation
   */
  handleCrudButtonClick(button, event) {
    const action = button.dataset.action;
    const table = button.closest('.crud-interface').querySelector('.data-table');

    if (!table) return;

    const tbody = table.querySelector('tbody');
    let newRow;

    switch (action) {
      case 'create':
        newRow = this.createMockDataRow(table);
        tbody.appendChild(newRow);
        this.animateElement(newRow, 'animate-in');
        break;

      case 'update':
        const firstRow = tbody.querySelector('.data-row');
        if (firstRow) {
          firstRow.classList.add('update-animation');
          setTimeout(() => firstRow.classList.remove('update-animation'), 1000);
        }
        break;

      case 'delete':
        const lastRow = tbody.querySelector('.data-row:last-child');
        if (lastRow) {
          lastRow.style.transition = 'all 0.5s ease-out';
          lastRow.style.opacity = '0';
          lastRow.style.transform = 'translateX(100%)';
          setTimeout(() => lastRow.remove(), 500);
        }
        break;
    }
  }

  /**
   * Handle tree node toggle
   */
  handleTreeNodeClick(nodeContent, event) {
    const node = nodeContent.closest('.tree-node');
    const children = node.querySelector('.tree-children');
    const toggle = nodeContent.querySelector('.tree-toggle');

    if (children && toggle) {
      const isExpanded = children.style.maxHeight !== '0px' && children.style.maxHeight !== '';

      if (isExpanded) {
        // Collapse
        children.style.maxHeight = children.scrollHeight + 'px';
        children.offsetHeight; // Trigger reflow
        children.style.maxHeight = '0px';
        toggle.classList.remove('rotate');
      } else {
        // Expand
        children.style.maxHeight = children.scrollHeight + 'px';
        toggle.classList.add('rotate');

        // Animate children
        const childNodes = children.querySelectorAll('.tree-node');
        this.animateSequence(childNodes, 100);

        // Reset height after animation
        setTimeout(() => {
          children.style.maxHeight = 'none';
        }, 500);
      }
    }
  }

  /**
   * Handle API demo interactions
   */
  handleApiDemoClick(button, event) {
    const demoType = button.dataset.demo;
    this.runApiDemo(demoType);
  }

  /**
   * Create mock data row for CRUD demonstration
   */
  createMockDataRow(table) {
    const row = document.createElement('tr');
    row.className = 'data-row';

    const mockData = {
      id: 'ds-' + Math.random().toString(36).substr(2, 8),
      name: 'New Data Source',
      type: 'api',
      status: 'active'
    };

    row.innerHTML = `
      <td>${mockData.id}</td>
      <td>${mockData.name}</td>
      <td>${mockData.type}</td>
      <td><span class="status-badge ${mockData.status}">${mockData.status}</span></td>
    `;

    return row;
  }

  /**
   * Animate DataSource service workflow
   */
  animateDataSourceService() {
    // Find service container
    const container = document.querySelector('[data-service="datasource"]');
    if (!container) return;

    const steps = [
      { duration: 500, callback: (step) => {
        // Validate step
        const validationElements = container.querySelectorAll('.validation-step');
        validationElements.forEach(el => el.classList.add('active'));
      }},
      { duration: 800, callback: (step) => {
        // Save step
        const saveIndicator = container.querySelector('.save-indicator');
        if (saveIndicator) saveIndicator.classList.add('animate-pulse');
      }},
      { duration: 600, callback: (step) => {
        // Index step
        const indexIndicator = container.querySelector('.index-indicator');
        if (indexIndicator) indexIndicator.classList.add('animate-pulse');
      }}
    ];

    this.animateCodeFlow('[data-service="datasource"] .code-flow', steps);
  }

  /**
   * Animate Search service workflow
   */
  animateSearchService() {
    const container = document.querySelector('[data-service="search"]');
    if (!container) return;

    const queryInput = container.querySelector('.search-input');
    const resultsContainer = container.querySelector('.search-results');

    // Simulate search process
    if (queryInput && resultsContainer) {
      queryInput.classList.add('animate-pulse');

      setTimeout(() => {
        queryInput.classList.remove('animate-pulse');
        queryInput.classList.add('searching');

        // Animate results appearing
        const resultItems = resultsContainer.querySelectorAll('.result-item');
        this.animateSequence(resultItems, 150);

        setTimeout(() => {
          queryInput.classList.remove('searching');
        }, 1000);
      }, 500);
    }
  }

  /**
   * Animate Category service workflow
   */
  animateCategoryService() {
    const container = document.querySelector('[data-service="category"]');
    if (!container) return;

    // Animate tree building
    const treeNodes = container.querySelectorAll('.tree-node');
    this.animateSequence(treeNodes, 200);
  }

  /**
   * Run API demonstration
   */
  runApiDemo(type) {
    const requestElement = document.querySelector(`.api-request[data-type="${type}"]`);
    const responseElement = document.querySelector(`.api-response[data-type="${type}"]`);

    if (requestElement && responseElement) {
      // Animate request
      requestElement.classList.add('animate-in', 'active');

      setTimeout(() => {
        requestElement.classList.remove('active');

        // Animate response
        responseElement.classList.add('animate-in');

        // Add loading dots animation
        const responseContent = responseElement.querySelector('.response-content');
        if (responseContent) {
          responseContent.textContent = '...';
          setTimeout(() => {
            responseContent.textContent = '{"success": true, "data": {...}}';
          }, 800);
        }

      }, 1000);
    }
  }

  /**
   * Start all animations on the page
   */
  startAllAnimations() {
    // Animate service cards
    const serviceCards = document.querySelectorAll('.service-card');
    this.animateSequence(serviceCards, 150);

    // Setup intersection observer for other elements
    const observer = this.observers.get('intersection');
    if (observer) {
      const animatedElements = document.querySelectorAll('[data-animation]');
      animatedElements.forEach(element => {
        observer.observe(element);
      });
    }
  }

  /**
   * Stop all animations and clean up
   */
  stopAllAnimations() {
    // Clear all timeouts
    this.animationTimeouts.forEach(timeoutId => clearTimeout(timeoutId));
    this.animationTimeouts = [];

    // Clear all observers
    this.observers.forEach((observer, type) => {
      if (type === 'intersection') {
        observer.disconnect();
      } else if (type === 'scroll') {
        window.removeEventListener('scroll', observer);
      }
    });
    this.observers.clear();
  }

  /**
   * Utility function to get element position
   */
  getElementPosition(element) {
    const rect = element.getBoundingClientRect();
    return {
      top: rect.top + window.pageYOffset,
      left: rect.left + window.pageXOffset,
      width: rect.width,
      height: rect.height
    };
  }

  /**
   * Create a reusable component instance
   */
  static createComponent(type, config = {}) {
    switch (type) {
      case 'codeFlow':
        return new CodeFlowComponent(config);
      case 'dataFlow':
        return new DataFlowComponent(config);
      case 'apiDemo':
        return new ApiDemoComponent(config);
      default:
        return new InteractiveDocs(config);
    }
  }
}

/**
 * Code Flow Component
 */
class CodeFlowComponent {
  constructor(config) {
    this.config = config;
    this.steps = [];
    this.currentStep = 0;
  }

  addStep(element, callback, duration = 1000) {
    this.steps.push({ element, callback, duration });
  }

  start() {
    this.animateNext();
  }

  animateNext() {
    if (this.currentStep < this.steps.length) {
      const step = this.steps[this.currentStep];
      step.element.classList.add('active');

      if (step.callback) {
        step.callback(step.element, this.currentStep);
      }

      setTimeout(() => {
        step.element.classList.add('completed');
        step.element.classList.remove('active');
        this.currentStep++;
        this.animateNext();
      }, step.duration);
    }
  }
}

/**
 * Data Flow Component
 */
class DataFlowComponent {
  constructor(config) {
    this.config = config;
  }

  animate(fromElement, toElement, data = {}) {
    // Implementation for data flow animation
    const docs = new InteractiveDocs();
    docs.animateDataFlow(`#${fromElement}`, `#${toElement}`, data);
  }
}

/**
 * API Demo Component
 */
class ApiDemoComponent {
  constructor(config) {
    this.config = config;
  }

  demonstrate(type) {
    const docs = new InteractiveDocs();
    docs.runApiDemo(type);
  }
}

// Export for use in HTML or other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = InteractiveDocs;
}

// Auto-initialize if loaded directly in browser
if (typeof window !== 'undefined') {
  window.InteractiveDocs = InteractiveDocs;

  // Auto-initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.interactive-docs')) {
      const docs = new InteractiveDocs({ autoStart: true });
      docs.init();
    }
  });
}
