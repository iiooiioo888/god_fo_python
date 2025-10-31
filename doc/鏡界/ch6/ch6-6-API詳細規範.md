# 第6章：AI輔助開发系統 (AI-Assisted Development System)

## 6.6 API詳細規範

**[← 返回第6章首頁](ch6-index.md)**

---

#### 6.6.1 代码生成API

**生成爬蟲代码 (POST /api/v1/code:generate)**

*请求示例:*
```http
POST /api/v1/code:generate HTTP/1.1
Host: aids.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "request": "请生成一個爬取https://example.com/products的Python爬蟲，需要處理分頁和User-Agent轮换",
  "context": {
    "language": "python",
    "preferred_style": "functional",
    "avoid_selenium": true
  }
}
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": "import requests\nfrom fake_useragent import UserAgent\n\nua = UserAgent()\n\nfor page in range(1, 11):\n    url = f'https://example.com/products?page={page}'\n    headers = {'User-Agent': ua.random}\n    response = requests.get(url, headers=headers)\n    # 處理響應...\n    print(f'Page {page} status: {response.status_code}')",
  "scene_type": "pagination",
  "templates_used": ["pagination-python", "user-agent-rotation"],
  "validation": {
    "is_valid": true,
    "errors": []
  },
  "confidence": 0.92,
  "processing_time": 1.45
}
```

#### 6.6.2 问题诊断API

**诊断错误问题 (POST /api/v1/diagnose)**

*请求示例:*
```http
POST /api/v1/diagnose HTTP/1.1
Host: aids.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "error_log": "requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://example.com/api/data?page=5",
  "context": {
    "url": "https://example.com/api/data",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
}
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "error_log": "requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://example.com/api/data?page=5",
  "analysis": {
    "error_message": "requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://example.com/api/data?page=5",
    "error_type": "client_error",
    "status_code": 403,
    "anti_crawling_indicators": ["user-agent-check"],
    "technology": "cloudflare",
    "url": "https://example.com/api/data?page=5"
  },
  "diagnosis": {
    "root_cause": "網站通過User-Agent檢測识别出爬蟲请求",
    "impact": "请求被服務器拒绝，无法獲取資料",
    "suggested_solutions": [
      "使用更真實的User-Agent轮换策略",
      "添加必要的请求头模拟浏览器行為",
      "考慮使用代理IP轮换"
    ]
  },
  "solutions": [
    {
      "id": "sol-1",
      "description": "使用更真實的User-Agent轮换策略",
      "confidence": 0.85,
      "implementation": "from fake_useragent import UserAgent\nua = UserAgent()\nheaders = {'User-Agent': ua.random}"
    },
    {
      "id": "sol-2",
      "description": "添加必要的请求头模拟浏览器行為",
      "confidence": 0.78,
      "implementation": "headers = {\n    'User-Agent': 'Mozilla/5.0...',\n    'Accept-Language': 'en-US,en;q=0.9',\n    'Sec-Ch-Ua': '\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not_A Brand\";v=\"24\"'\n}"
    }
  ],
  "confidence": 0.82,
  "processing_time": 0.87
}
```

#### 6.6.3 学习推薦API

**獲取学习推薦 (GET /api/v1/learning/recommendations)**

*请求示例:*
```http
GET /api/v1/learning/recommendations HTTP/1.1
Host: aids.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功響應示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "user_id": "user-123",
  "profile_snapshot": {
    "user_id": "user-123",
    "experience_level": "intermediate",
    "preferred_language": "en",
    "content_preferences": ["video", "interactive"],
    "learning_goals": ["web_scraping", "data_processing"],
    "areas_of_interest": ["python", "automation"],
    "skill_levels": {
      "static_html": 3.5,
      "dynamic_rendering": 2.0,
      "api_integration": 2.5
    },
    "last_updated": "2023-06-15T10:30:45Z"
  },
  "skill_assessment": {
    "user_id": "user-123",
    "domain_assessments": {
      "web_scraping": {
        "overall_level": 2.8,
        "skills": {
          "static_html": 3.5,
          "dynamic_rendering": 2.0,
          "pagination": 3.0,
          "anti_crawling": 2.5
        },
        "strengths": ["static_html", "pagination"],
        "weaknesses": ["dynamic_rendering", "anti_crawling"]
      },
      "data_processing": {
        "overall_level": 3.2,
        "skills": {
          "data_cleaning": 3.5,
          "data_transformation": 3.0,
          "data_storage": 3.0
        },
        "strengths": ["data_cleaning"],
        "weaknesses": []
      }
    },
    "behavioral_analysis": {
      "activity_level": "medium",
      "learning_style": "visual",
      "problem_solving_pattern": "step_by_step",
      "coding_style": "concise",
      "common_challenges": ["access_denied", "rate_limiting"]
    },
    "assessment_date": "2023-06-15T10:30:45Z",
    "detailed": true
  },
  "skill_gaps": [
    {
      "domain": "web_scraping",
      "skill": "dynamic_rendering",
      "current_level": 2.0,
      "target_level": 3.5,
      "gap_size": 1.5
    },
    {
      "domain": "web_scraping",
      "skill": "anti_crawling",
      "current_level": 2.5,
      "target_level": 4.0,
      "gap_size": 1.5
    }
  ],
  "recommended_content": {
    "title": "個性化爬蟲技能提升路径",
    "description": "根據您的技能評估生成的個性化学习路径",
    "domains": [
      {
        "domain": "web_scraping",
        "paths": [
          {
            "skill": "dynamic_rendering",
            "description": "dynamic_rendering技能提升路径",
            "contents": [
              {
                "id": "content-1",
                "title": "使用Selenium處理JavaScript渲染頁面",
                "description": "学习如何使用Selenium處理動态渲染的網頁內容",
                "domain": "web_scraping",
                "skill": "dynamic_rendering",
                "format": "video",
                "difficulty": 3,
                "estimated_duration": 30,
                "content_url": "https://learning.example.com/selenium-basics",
                "language": "en",
                "prerequisites": ["static_html"],
                "tags": ["selenium", "javascript"],
                "relevance_score": 0.92,
                "created_at": "2023-06-10T08:15:30Z"
              },
              {
                "id": "content-2",
                "title": "Playwright高级应用：處理单頁应用",
                "description": "深入学习Playwright處理複杂的单頁应用",
                "domain": "web_scraping",
                "skill": "dynamic_rendering",
                "format": "tutorial",
                "difficulty": 4,
                "estimated_duration": 45,
                "content_url": "https://learning.example.com/playwright-spa",
                "language": "en",
                "prerequisites": ["dynamic_rendering"],
                "tags": ["playwright", "spa"],
                "relevance_score": 0.88,
                "created_at": "2023-06-12T14:20:15Z"
              }
            ],
            "estimated_time": "PT1H15M"
          },
          {
            "skill": "anti_crawling",
            "description": "anti_crawling技能提升路径",
            "contents": [
              {
                "id": "content-3",
                "title": "绕過常见反爬機制：理论與實践",
                "description": "全面了解並学习绕過各種反爬機制的方法",
                "domain": "web_scraping",
                "skill": "anti_crawling",
                "format": "article",
                "difficulty": 3,
                "estimated_duration": 25,
                "content_url": "https://learning.example.com/anti-crawling-basics",
                "language": "en",
                "prerequisites": ["web_scraping"],
                "tags": ["anti-crawling", "bypass"],
                "relevance_score": 0.95,
                "created_at": "2023-06-08T09:30:45Z"
              }
            ],
            "estimated_time": "PT25M"
          }
        ],
        "estimated_time": "PT1H40M"
      }
    ],
    "estimated_duration": "PT1H40M",
    "difficulty_level": "intermediate"
  },
  "confidence": 0.85,
  "generated_at": "2023-06-15T10:35:20Z",
  "processing_time": 0.65
}
```

---

## 📑 相關章節

| 前序 | 當前 | 後續 |
|-----|------|------|
| [6.5 資料模型詳細定義](ch6-5-資料模型詳細定義.md) | **6.6 API詳細規範** | [6.7 效能優化策略](ch6-7-效能優化策略.md) |

**快速鏈接：**
- [6.5 資料模型詳細定義](ch6-5-資料模型詳細定義.md)
- [6.7 效能優化策略](ch6-7-效能優化策略.md)
- [← 返回第6章首頁](ch6-index.md)
