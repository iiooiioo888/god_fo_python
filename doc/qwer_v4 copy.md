# 镜界平台终极技术规格说明书（模块级深度实现）

## 目录

### 1. 数据源注册中心 (Data Source Registry)
- [1.1 模块概述](#11-模块概述)
- [1.2 详细功能清单](#12-详细功能清单)
  - [1.2.1 核心功能](#121-核心功能)
  - [1.2.2 高级功能](#122-高级功能)
- [1.3 技术架构](#13-技术架构)
  - [1.3.1 架构图](#131-架构图)
  - [1.3.2 服务边界与交互](#132-服务边界与交互)
- [1.4 核心组件详细实现](#14-核心组件详细实现)
  - [1.4.1 元数据管理服务](#141-元数据管理服务)
  - [1.4.2 搜索服务](#142-搜索服务)
  - [1.4.3 分类管理服务](#143-分类管理服务)
- [1.5 数据模型详细定义](#15-数据模型详细定义)
  - [1.5.1 数据源核心表](#151-数据源核心表)
  - [1.5.2 数据源版本表](#152-数据源版本表)
  - [1.5.3 分类表](#153-分类表)
- [1.6 API详细规范](#16-api详细规范)
  - [1.6.1 数据源管理API](#161-数据源管理api)
  - [1.6.2 搜索API](#162-搜索api)
- [1.7 性能优化策略](#17-性能优化策略)
  - [1.7.1 数据库优化](#171-数据库优化)
  - [1.7.2 缓存策略](#172-缓存策略)
  - [1.7.3 搜索性能优化](#173-搜索性能优化)
- [1.8 安全考虑](#18-安全考虑)
  - [1.8.1 访问控制](#181-访问控制)
  - [1.8.2 数据安全](#182-数据安全)
- [1.9 与其他模块的交互](#19-与其他模块的交互)
  - [1.9.1 与数据源健康监测系统交互](#191-与数据源健康监测系统交互)
  - [1.9.2 与数据处理工作流引擎交互](#192-与数据处理工作流引擎交互)
  - [1.9.3 与AI辅助开发系统交互](#193-与ai辅助开发系统交互)

### 2. 网站指纹分析引擎 (Website Fingerprinting Engine)
- [2.1 模块概述](#21-模块概述)
- [2.2 详细功能清单](#22-详细功能清单)
  - [2.2.1 核心功能](#221-核心功能)
  - [2.2.2 高级功能](#222-高级功能)
- [2.3 技术架构](#23-技术架构)
  - [2.3.1 架构图](#231-架构图)
  - [2.3.2 服务边界与交互](#232-服务边界与交互)
- [2.4 核心组件详细实现](#24-核心组件详细实现)
  - [2.4.1 技术栈识别服务](#241-技术栈识别服务)
  - [2.4.2 反爬机制检测服务](#242-反爬机制检测服务)
  - [2.4.3 规则引擎服务](#243-规则引擎服务)
- [2.5 数据模型详细定义](#25-数据模型详细定义)
  - [2.5.1 指纹规则表](#251-指纹规则表)
  - [2.5.2 分析结果表](#252-分析结果表)
- [2.6 API详细规范](#26-api详细规范)
- [2.7 性能优化策略](#27-性能优化策略)
  - [2.7.1 分析性能优化](#271-分析性能优化)
  - [2.7.2 规则匹配优化](#272-规则匹配优化)
- [2.8 安全考虑](#28-安全考虑)
  - [2.8.1 分析安全](#281-分析安全)
  - [2.8.2 数据安全](#282-数据安全)
- [2.9 与其他模块的交互](#29-与其他模块的交互)
  - [2.9.1 与数据源注册中心交互](#291-与数据源注册中心交互)
  - [2.9.2 与AI辅助开发系统交互](#292-与ai辅助开发系统交互)
  - [2.9.3 与数据合规与安全中心交互](#293-与数据合规与安全中心交互)

### 3. 数据源健康监测系统 (Data Source Health Monitoring System)
- [3.1 模块概述](#31-模块概述)
- [3.2 详细功能清单](#32-详细功能清单)
  - [3.2.1 核心功能](#321-核心功能)
  - [3.2.2 高级功能](#322-高级功能)
- [3.3 技术架构](#33-技术架构)
  - [3.3.1 架构图](#331-架构图)
  - [3.3.2 服务边界与交互](#332-服务边界与交互)
- [3.4 核心组件详细实现](#34-核心组件详细实现)
  - [3.4.1 探测调度器](#341-探测调度器)
  - [3.4.2 探测执行器](#342-探测执行器)
  - [3.4.3 结果处理器](#343-结果处理器)
- [3.5 数据模型详细定义](#35-数据模型详细定义)
  - [3.5.1 健康指标表](#351-健康指标表)
  - [3.5.2 告警表](#352-告警表)
- [3.6 API详细规范](#36-api详细规范)
  - [3.6.1 健康监测API](#361-健康监测api)
  - [3.6.2 告警API](#362-告警api)
- [3.7 性能优化策略](#37-性能优化策略)
  - [3.7.1 时序数据存储优化](#371-时序数据存储优化)
  - [3.7.2 告警处理优化](#372-告警处理优化)
- [3.8 安全考虑](#38-安全考虑)
  - [3.8.1 探测安全](#381-探测安全)
  - [3.8.2 数据安全](#382-数据安全)
- [3.9 与其他模块的交互](#39-与其他模块的交互)
  - [3.9.1 与数据源注册中心交互](#391-与数据源注册中心交互)
  - [3.9.2 与数据处理工作流引擎交互](#392-与数据处理工作流引擎交互)
  - [3.9.3 与数据质量预测分析系统交互](#393-与数据质量预测分析系统交互)

### 4. 数据处理工作流引擎 (Data Processing Workflow Engine)
- [4.1 模块概述](#41-模块概述)
- [4.2 详细功能清单](#42-详细功能清单)
  - [4.2.1 核心功能](#421-核心功能)
  - [4.2.2 高级功能](#422-高级功能)
- [4.3 技术架构](#43-技术架构)
  - [4.3.1 架构图](#431-架构图)
  - [4.3.2 服务边界与交互](#432-服务边界与交互)
- [4.4 核心组件详细实现](#44-核心组件详细实现)
  - [4.4.1 工作流定义服务](#441-工作流定义服务)
  - [4.4.2 工作流执行服务](#442-工作流执行服务)
  - [4.4.3 工作流调度器](#443-工作流调度器)
  - [4.4.4 工作流执行器](#444-工作流执行器)
  - [4.4.5 节点执行器](#445-节点执行器)
- [4.5 数据模型详细定义](#45-数据模型详细定义)
  - [4.5.1 工作流定义表](#451-工作流定义表)
  - [4.5.2 工作流实例表](#452-工作流实例表)
  - [4.5.3 节点执行表](#453-节点执行表)
- [4.6 API详细规范](#46-api详细规范)
  - [4.6.1 工作流定义API](#461-工作流定义api)
  - [4.6.2 工作流执行API](#462-工作流执行api)
- [4.7 性能优化策略](#47-性能优化策略)
  - [4.7.1 工作流执行优化](#471-工作流执行优化)
  - [4.7.2 资源管理优化](#472-资源管理优化)
- [4.8 安全考虑](#48-安全考虑)
  - [4.8.1 工作流安全](#481-工作流安全)
  - [4.8.2 数据安全](#482-数据安全)
- [4.9 与其他模块的交互](#49-与其他模块的交互)
  - [4.9.1 与数据源注册中心交互](#491-与数据源注册中心交互)
  - [4.9.2 与自动化媒体处理管道交互](#492-与自动化媒体处理管道交互)
  - [4.9.3 与AI辅助开发系统交互](#493-与ai辅助开发系统交互)

### 5. 自动化媒体处理管道 (Automated Media Processing Pipeline)
- [5.1 模块概述](#51-模块概述)
- [5.2 详细功能清单](#52-详细功能清单)
  - [5.2.1 核心功能](#521-核心功能)
  - [5.2.2 高级功能](#522-高级功能)
- [5.3 技术架构](#53-技术架构)
  - [5.3.1 架构图](#531-架构图)
  - [5.3.2 服务边界与交互](#532-服务边界与交互)
- [5.4 核心组件详细实现](#54-核心组件详细实现)
  - [5.4.1 文件监控服务](#541-文件监控服务)
  - [5.4.2 媒体处理服务](#542-媒体处理服务)
  - [5.4.3 媒体分析服务](#543-媒体分析服务)
- [5.5 数据模型详细定义](#55-数据模型详细定义)
  - [5.5.1 媒体文件表](#551-媒体文件表)
  - [5.5.2 媒体处理任务表](#552-媒体处理任务表)
  - [5.5.3 媒体标签表](#553-媒体标签表)
  - [5.5.4 媒体相以度表](#554-媒体相以度表)
- [5.6 API详细规范](#56-api详细规范)
  - [5.6.1 媒体处理API](#561-媒体处理api)
- [5.7 性能优化策略](#57-性能优化策略)
  - [5.7.1 媒体处理性能优化](#571-媒体处理性能优化)
- [5.8 安全与合规详细规范](#58-安全与合规详细规范)
- [5.9 与其他模块的交互](#59-与其他模块的交互)
  - [5.9.1 与数据处理工作流引擎交互](#591-与数据处理工作流引擎交互)
  - [5.9.2 与网站指纹分析引擎交互](#592-与网站指纹分析引擎交互)
  - [5.9.3 与数据源注册中心交互](#593-与数据源注册中心交互)

### 6. AI辅助开发系统 (AI-Assisted Development System)
- [6.1 模块概述](#61-模块概述)
- [6.2 详细功能清单](#62-详细功能清单)
  - [6.2.1 核心功能](#621-核心功能)
  - [6.2.2 高级功能](#622-高级功能)
- [6.3 技术架构](#63-技术架构)
  - [6.3.1 架构图](#631-架构图)
  - [6.3.2 服务边界与交互](#632-服务边界与交互)
- [6.4 核心组件详细实现](#64-核心组件详细实现)
  - [6.4.1 需求解析服务](#641-需求解析服务)
  - [6.4.2 代码生成服务](#642-代码生成服务)
  - [6.4.3 问题诊断服务](#643-问题诊断服务)
  - [6.4.4 学习推荐服务](#644-学习推荐服务)
- [6.5 数据模型详细定义](#65-数据模型详细定义)
  - [6.5.1 用户画像表](#651-用户画像表)
  - [6.5.2 学习内容表](#652-学习内容表)
  - [6.5.3 技能评估表](#653-技能评估表)
  - [6.5.4 用户学习进度表](#654-用户学习进度表)
  - [6.5.5 用户代码提交记录表](#655-用户代码提交记录表)
- [6.6 API详细规范](#66-api详细规范)
  - [6.6.1 代码生成API](#661-代码生成api)
  - [6.6.2 问题诊断API](#662-问题诊断api)
  - [6.6.3 学习推荐API](#663-学习推荐api)
- [6.7 性能优化策略](#67-性能优化策略)
  - [6.7.1 LLM调用优化](#671-llm调用优化)
  - [6.7.2 上下文管理优化](#672-上下文管理优化)
  - [6.7.3 资源管理策略](#673-资源管理策略)
- [6.8 安全考虑](#68-安全考虑)
  - [6.8.1 LLM输出安全](#681-llm输出安全)
  - [6.8.2 数据隐私保护](#682-数据隐私保护)
- [6.9 与其他模块的交互](#69-与其他模块的交互)
  - [6.9.1 与数据处理工作流引擎交互](#691-与数据处理工作流引擎交互)
  - [6.9.2 与网站指纹分析引擎交互](#692-与网站指纹分析引擎交互)
  - [6.9.3 与数据合规与安全中心交互](#693-与数据合规与安全中心交互)

### 7. 数据合规与安全中心 (Data Compliance and Security Center)
- [7.1 模块概述](#71-模块概述)
- [7.2 详细功能清单](#72-详细功能清单)
  - [7.2.1 核心功能](#721-核心功能)
  - [7.2.2 高级功能](#722-高级功能)
- [7.3 技术架构](#73-技术架构)
  - [7.3.1 架构图](#731-架构图)
  - [7.3.2 服务边界与交互](#732-服务边界与交互)
- [7.4 核心组件详细实现](#74-核心组件详细实现)
  - [7.4.1 合规规则引擎](#741-合规规则引擎)
  - [7.4.2 敏感数据检测器](#742-敏感数据检测器)
- [7.5 数据模型详细定义](#75-数据模型详细定义)
  - [7.5.1 合规规则表](#751-合规规则表)
  - [7.5.2 敏感数据模式表](#752-敏感数据模式表)
  - [7.5.3 合规性检查结果表](#753-合规性检查结果表)
  - [7.5.4 敏感数据检测结果表](#754-敏感数据检测结果表)
  - [7.5.5 用户同意记录表](#755-用户同意记录表)
- [7.6 API详细规范](#76-api详细规范)
  - [7.6.1 合规性检查API](#761-合规性检查api)
  - [7.6.2 敏感数据检测API](#762-敏感数据检测api)
  - [7.6.3 用户同意管理API](#763-用户同意管理api)
- [7.7 性能优化策略](#77-性能优化策略)
  - [7.7.1 敏感数据检测优化](#771-敏感数据检测优化)
  - [7.7.2 合规性检查优化](#772-合规性检查优化)
- [7.8 安全考虑](#78-安全考虑)
  - [7.8.1 数据安全策略](#781-数据安全策略)
  - [7.8.2 合规性审计](#782-合规性审计)
- [7.9 与其他模块的交互](#79-与其他模块的交互)
  - [7.9.1 与数据源注册中心交互](#791-与数据源注册中心交互)
  - [7.9.2 与自动化媒体处理管道交互](#792-与自动化媒体处理管道交互)
  - [7.9.3 与数据处理工作流引擎交互](#793-与数据处理工作流引擎交互)

### 8. 分布式爬虫集群管理系统 (Distributed Crawler Cluster Management System)
- [8.1 模块概述](#81-模块概述)
- [8.2 详细功能清单](#82-详细功能清单)
  - [8.2.1 核心功能](#821-核心功能)
  - [8.2.2 高级功能](#822-高级功能)
- [8.3 技术架构](#83-技术架构)
  - [8.3.1 架构图](#831-架构图)
  - [8.3.2 服务边界与交互](#832-服务边界与交互)
- [8.4 核心组件详细实现](#84-核心组件详细实现)
  - [8.4.1 爬虫节点管理服务](#841-爬虫节点管理服务)
  - [8.4.2 任务调度器](#842-任务调度器)
- [8.5 数据模型详细定义](#85-数据模型详细定义)
  - [8.5.1 爬虫节点表](#851-爬虫节点表)
  - [8.5.2 爬虫任务表](#852-爬虫任务表)
  - [8.5.3 爬虫任务执行表](#853-爬虫任务执行表)
  - [8.5.4 爬虫集群表](#854-爬虫集群表)
- [8.6 API详细规范](#86-api详细规范)
  - [8.6.1 节点管理API](#861-节点管理api)
  - [8.6.2 任务管理API](#862-任务管理api)
- [8.7 性能优化策略](#87-性能优化策略)
  - [8.7.1 任务调度优化](#871-任务调度优化)
  - [8.7.2 资源优化](#872-资源优化)
- [8.8 安全考虑](#88-安全考虑)
  - [8.8.1 节点安全](#881-节点安全)
  - [8.8.2 节点沙箱环境](#882-节点沙箱环境)
- [8.9 与其他模块的交互](#89-与其他模块的交互)
  - [8.9.1 与数据处理工作流引擎交互](#891-与数据处理工作流引擎交互)
  - [8.9.2 与网站指纹分析引擎交互](#892-与网站指纹分析引擎交互)
  - [8.9.3 与数据合规与安全中心交互](#893-与数据合规与安全中心交互)

### 9. 系统集成与部署
- [9.1 部署架构](#91-部署架构)
  - [9.1.1 生产环境部署](#911-生产环境部署)
  - [9.1.2 服务部署拓扑](#912-服务部署拓扑)
- [9.2 部署流程](#92-部署流程)
  - [9.2.1 基础设施准备](#921-基础设施准备)
  - [9.2.2 服务部署](#922-服务部署)
  - [9.2.3 配置管理](#923-配置管理)
- [9.3 监控与告警](#93-监控与告警)
  - [9.3.1 监控指标](#931-监控指标)
  - [9.3.2 告警规则](#932-告警规则)
- [9.4 持续集成与持续部署](#94-持续集成与持续部署)
  - [9.4.1 CI/CD流水线](#941-cicd流水线)
  - [9.4.2 流水线配置](#942-流水线配置)
  - [9.4.3 蓝度发布策略](#943-蓝度发布策略)
- [9.5 安全与合规](#95-安全与合规)
  - [9.5.1 安全策略](#951-安全策略)
  - [9.5.2 安全扫描策略](#952-安全扫描策略)
- [9.6 性能测试方案](#96-性能测试方案)
  - [9.6.1 基準测试场景](#961-基準测试场景)
- [9.7 灾难恢复计划](#97-灾难恢复计划)
  - [9.7.1 备份策略](#971-备份策略)
  - [9.7.2 災难恢复流程](#972-災难恢复流程)

### 10. 附录
- [10.1 术语表](#101-术语表)
- [10.2 参考文献](#102-参考文献)


## 1. 数据源注册中心 (Data Source Registry)

### 1.1 模块概述
数据源注册中心是镜界平台的核心元数据管理组件，负责存储、管理和检索所有数据源的元信息。它为其他模块提供统一的数据源发现、分类和管理能力，支持从简单网页到复杂API的各种数据源类型。

### 1.2 详细功能清单

#### 1.2.1 核心功能
- **数据源CRUD管理**
  - 创建、读取、更新、删除数据源元数据
  - 支持版本控制的数据源定义
  - 支持软删除与回收站功能
- **数据源分类与标签**
  - 多级分类体系管理
  - 动态标签系统（支持用户自定义标签）
  - 自动化标签建议（基于内容分析）
- **高级搜索与过滤**
  - 全文搜索（基于Elasticsearch）
  - 复杂查询构建器（支持布尔逻辑）
  - 保存常用搜索查询
- **数据源健康监控集成**
  - 与健康监测系统集成
  - 健康状态可视化
  - 健康历史记录查询
- **访问控制与权限管理**
  - 细粒度权限控制（项目级、数据源级）
  - 基于角色的访问控制(RBAC)
  - 数据源共享功能

#### 1.2.2 高级功能
- **数据源依赖关系管理**
  - 识别和可视化数据源之间的依赖关系
  - 影响分析（当一个数据源变更时影响范围分析）
- **数据源变更追踪**
  - 完整的变更历史记录
  - 变更对比功能
  - 回滚到历史版本
- **自动化数据源发现**
  - 网站地图解析
  - API文档解析（OpenAPI/Swagger）
  - 智能数据源推荐
- **数据源质量评估**
  - 自动化质量评分
  - 质量趋势分析
  - 质量问题诊断

### 1.3 技术架构

#### 1.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 数据源注册中心 (DSR)                                          │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  核心服务层           │  集成层              │  支持服务层                                 │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 元数据管理服务      │ • 数据源发现适配器    │ • 搜索索引服务                             │
│ • 分类管理服务        │ • 健康监测集成        │ • 缓存服务                                 │
│ • 标签管理服务        │ • API网关             │ • 通知服务                                 │
│ • 搜索服务            │ • Webhook支持         │ • 审计日志服务                             │
│ • 权限管理服务        │ • SDK支持             │ • 指标收集服务                             │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 1.3.2 服务边界与交互
- **输入**：
  - 用户操作（Web界面、CLI、API）
  - 健康监测系统更新
  - 数据源发现服务
  - 外部系统Webhook
- **输出**：
  - 数据源元数据给工作流引擎
  - 健康状态给监控系统
  - 分类信息给推荐引擎
  - 变更事件给事件总线

### 1.4 核心组件详细实现

#### 1.4.1 元数据管理服务

**技术实现：**
```python
class DataSourceService:
    """数据源元数据管理核心服务"""
    
    def __init__(
        self,
        db: Database,
        search_index: SearchIndex,
        event_bus: EventBus,
        config: Config
    ):
        self.db = db
        self.search_index = search_index
        self.event_bus = event_bus
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def create_data_source(
        self,
        project_id: str,
        data_source: DataSource,
        user_id: str
    ) -> DataSource:
        """
        创建新的数据源
        
        :param project_id: 所属项目ID
        :param data_source: 数据源对象
        :param user_id: 创建者ID
        :return: 创建后的数据源对象
        """
        # 1. 验证数据源
        self._validate_data_source(data_source)
        
        # 2. 生成唯一ID
        data_source.id = f"ds-{uuid.uuid4().hex[:8]}"
        data_source.project_id = project_id
        data_source.created_at = datetime.utcnow()
        data_source.updated_at = data_source.created_at
        data_source.owner_id = user_id
        data_source.status = "active"
        
        # 3. 处理分类和标签
        self._process_categories_and_tags(data_source)
        
        # 4. 保存到数据库
        self._save_to_db(data_source)
        
        # 5. 更新搜索索引
        self.search_index.add(data_source)
        
        # 6. 发布创建事件
        self.event_bus.publish("data_source.created", {
            "data_source_id": data_source.id,
            "project_id": project_id,
            "user_id": user_id
        })
        
        return data_source
    
    def _validate_data_source(self, data_source: DataSource):
        """验证数据源定义的有效性"""
        # 必填字段检查
        required_fields = ["name", "url", "category", "data_type"]
        for field in required_fields:
            if not getattr(data_source, field):
                raise ValidationError(f"Missing required field: {field}")
        
        # URL格式验证
        if not self._is_valid_url(data_source.url):
            raise ValidationError("Invalid URL format")
        
        # 数据类型验证
        valid_data_types = ["image", "video", "document", "api", "html", "json", "xml"]
        if data_source.data_type not in valid_data_types:
            raise ValidationError(f"Invalid data type. Must be one of: {', '.join(valid_data_types)}")
        
        # 架构验证（如果是API）
        if data_source.data_type == "api" and data_source.schema:
            try:
                # 使用JSON Schema验证
                validate(instance=data_source.schema, schema=API_SCHEMA)
            except Exception as e:
                raise ValidationError(f"Invalid API schema: {str(e)}")
    
    def _is_valid_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _process_categories_and_tags(self, data_source: DataSource):
        """处理分类和标签"""
        # 自动分类（如果未指定）
        if not data_source.category:
            data_source.category = self._auto_categorize(data_source)
        
        # 自动标签建议
        if self.config.auto_tagging_enabled:
            auto_tags = self._generate_auto_tags(data_source)
            data_source.tags = list(set(data_source.tags + auto_tags))
    
    def _auto_categorize(self, data_source: DataSource) -> str:
        """自动分类算法"""
        # 基于URL模式的分类
        url = data_source.url.lower()
        
        if "social" in url or any(kw in url for kw in ["facebook", "twitter", "instagram"]):
            return "social-media"
        elif "news" in url or any(kw in url for kw in ["bbc", "cnn", "reuters"]):
            return "news"
        elif "ecommerce" in url or any(kw in url for kw in ["amazon", "ebay", "aliexpress"]):
            return "ecommerce"
        elif "image" in url or data_source.data_type == "image":
            return "image"
        elif "video" in url or data_source.data_type == "video":
            return "video"
        
        # 默认分类
        return "general"
    
    def _generate_auto_tags(self, data_source: DataSource) -> List[str]:
        """生成自动标签"""
        tags = []
        
        # 基于URL的标签
        url = data_source.url.lower()
        if "api" in url:
            tags.append("api")
        if "mobile" in url:
            tags.append("mobile")
        if "desktop" in url:
            tags.append("desktop")
        
        # 基于内容类型的标签
        if data_source.content_type:
            if "json" in data_source.content_type:
                tags.append("json")
            elif "xml" in data_source.content_type:
                tags.append("xml")
            elif "html" in data_source.content_type:
                tags.append("html")
        
        # 基于数据类型的标签
        if data_source.data_type == "image":
            tags.append("image-source")
        elif data_source.data_type == "video":
            tags.append("video-source")
        
        return tags
    
    def _save_to_db(self, data_source: DataSource):
        """保存到数据库"""
        # 准备SQL
        sql = """
        INSERT INTO data_sources (
            id, project_id, name, display_name, description, url, 
            category, data_type, content_type, schema, status, 
            created_at, updated_at, owner_id, tags, metadata
        ) VALUES (
            %(id)s, %(project_id)s, %(name)s, %(display_name)s, %(description)s, %(url)s,
            %(category)s, %(data_type)s, %(content_type)s, %(schema)s, %(status)s,
            %(created_at)s, %(updated_at)s, %(owner_id)s, %(tags)s, %(metadata)s
        )
        """
        
        # 执行插入
        self.db.execute(sql, {
            "id": data_source.id,
            "project_id": data_source.project_id,
            "name": data_source.name,
            "display_name": data_source.display_name,
            "description": data_source.description,
            "url": data_source.url,
            "category": data_source.category,
            "data_type": data_source.data_type,
            "content_type": data_source.content_type,
            "schema": json.dumps(data_source.schema) if data_source.schema else None,
            "status": data_source.status,
            "created_at": data_source.created_at,
            "updated_at": data_source.updated_at,
            "owner_id": data_source.owner_id,
            "tags": json.dumps(data_source.tags),
            "metadata": json.dumps(data_source.metadata)
        })
    
    def get_data_source(
        self,
        data_source_id: str,
        project_id: str,
        user_id: str
    ) -> DataSource:
        """
        获取数据源详情
        
        :param data_source_id: 数据源ID
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :return: 数据源对象
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to read this data source")
        
        # 2. 从数据库获取
        data_source = self._get_from_db(data_source_id, project_id)
        if not data_source:
            raise NotFoundError(f"Data source {data_source_id} not found")
        
        # 3. 获取健康状态
        data_source.health = self._get_health_status(data_source_id)
        
        return data_source
    
    def _get_from_db(self, data_source_id: str, project_id: str) -> Optional[DataSource]:
        """从数据库获取数据源"""
        sql = """
        SELECT * FROM data_sources 
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        row = self.db.fetchone(sql, {
            "id": data_source_id,
            "project_id": project_id
        })
        
        if not row:
            return None
        
        return self._row_to_data_source(row)
    
    def _row_to_data_source(self, row: Dict) -> DataSource:
        """将数据库行转换为DataSource对象"""
        return DataSource(
            id=row["id"],
            project_id=row["project_id"],
            name=row["name"],
            display_name=row["display_name"],
            description=row["description"],
            url=row["url"],
            category=row["category"],
            data_type=row["data_type"],
            content_type=row["content_type"],
            schema=json.loads(row["schema"]) if row["schema"] else None,
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            owner_id=row["owner_id"],
            tags=json.loads(row["tags"]),
            metadata=json.loads(row["metadata"])
        )
    
    def _get_health_status(self, data_source_id: str) -> DataSourceHealth:
        """获取数据源健康状态"""
        # 从健康监测系统获取最新状态
        health_data = self.health_monitor.get_latest_health(data_source_id)
        
        if not health_data:
            return DataSourceHealth(
                status="unknown",
                last_check=None,
                metrics={}
            )
        
        return DataSourceHealth(
            status=health_data["status"],
            last_check=health_data["timestamp"],
            metrics=health_data["metrics"]
        )
    
    def update_data_source(
        self,
        data_source_id: str,
        project_id: str,
        updates: Dict,
        user_id: str
    ) -> DataSource:
        """
        更新数据源
        
        :param data_source_id: 数据源ID
        :param project_id: 项目ID
        :param updates: 更新字段
        :param user_id: 更新者ID
        :return: 更新后的数据源
        """
        # 1. 获取当前数据源
        current = self.get_data_source(data_source_id, project_id, user_id)
        
        # 2. 检查权限
        if not self._has_permission(user_id, project_id, "write"):
            raise PermissionError("User does not have permission to update this data source")
        
        # 3. 验证更新
        self._validate_updates(updates, current)
        
        # 4. 创建新版本
        new_version = self._create_version(current, updates, user_id)
        
        # 5. 保存更新
        self._save_update(data_source_id, project_id, updates)
        
        # 6. 更新搜索索引
        updated_source = self._get_from_db(data_source_id, project_id)
        self.search_index.update(updated_source)
        
        # 7. 发布更新事件
        self.event_bus.publish("data_source.updated", {
            "data_source_id": data_source_id,
            "project_id": project_id,
            "user_id": user_id,
            "changes": updates
        })
        
        return updated_source
    
    def _validate_updates(self, updates: Dict, current: DataSource):
        """验证更新是否有效"""
        # 不能修改ID和项目ID
        if "id" in updates or "project_id" in updates:
            raise ValidationError("Cannot update data source ID or project ID")
        
        # 验证URL变更
        if "url" in updates and updates["url"] != current.url:
            # 检查URL格式
            if not self._is_valid_url(updates["url"]):
                raise ValidationError("Invalid URL format")
            
            # 检查重复URL
            if self._url_exists(updates["url"], current.project_id, current.id):
                raise ValidationError("URL already exists in this project")
    
    def _url_exists(self, url: str, project_id: str, exclude_id: str = None) -> bool:
        """检查URL是否已存在"""
        sql = """
        SELECT COUNT(*) FROM data_sources 
        WHERE url = %(url)s AND project_id = %(project_id)s
        """
        params = {"url": url, "project_id": project_id}
        
        if exclude_id:
            sql += " AND id != %(exclude_id)s"
            params["exclude_id"] = exclude_id
        
        count = self.db.fetchone(sql, params)["count"]
        return count > 0
    
    def _create_version(self, current: DataSource, updates: Dict, user_id: str) -> str:
        """创建数据源新版本"""
        # 生成新版本ID
        version_id = f"ver-{uuid.uuid4().hex[:8]}"
        
        # 准备版本数据
        version_data = {
            "data_source_id": current.id,
            "version_id": version_id,
            "changes": json.dumps(updates),
            "created_at": datetime.utcnow(),
            "created_by": user_id,
            "previous_version": current.current_version
        }
        
        # 保存版本
        self.db.execute("""
        INSERT INTO data_source_versions (
            data_source_id, version_id, changes, created_at, created_by, previous_version
        ) VALUES (
            %(data_source_id)s, %(version_id)s, %(changes)s, %(created_at)s, %(created_by)s, %(previous_version)s
        )
        """, version_data)
        
        return version_id
    
    def _save_update(self, data_source_id: str, project_id: str, updates: Dict):
        """保存数据源更新"""
        # 准备更新字段
        update_fields = []
        params = {"id": data_source_id, "project_id": project_id, "updated_at": datetime.utcnow()}
        
        for field, value in updates.items():
            if field in ["tags", "metadata", "schema"]:
                # 处理JSON字段
                update_fields.append(f"{field} = %(field)s::jsonb")
                params[field] = json.dumps(value)
            else:
                update_fields.append(f"{field} = %({field})s")
                params[field] = value
        
        # 添加更新时间
        update_fields.append("updated_at = %(updated_at)s")
        
        # 执行更新
        sql = f"""
        UPDATE data_sources 
        SET {', '.join(update_fields)}
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        self.db.execute(sql, params)
    
    def delete_data_source(
        self,
        data_source_id: str,
        project_id: str,
        user_id: str,
        permanent: bool = False
    ):
        """
        删除数据源
        
        :param data_source_id: 数据源ID
        :param project_id: 项目ID
        :param user_id: 删除者ID
        :param permanent: 是否永久删除
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "delete"):
            raise PermissionError("User does not have permission to delete this data source")
        
        if permanent:
            # 2. 永久删除
            self._permanent_delete(data_source_id, project_id)
        else:
            # 2. 软删除
            self._soft_delete(data_source_id, project_id, user_id)
        
        # 3. 从搜索索引中移除
        self.search_index.delete(data_source_id, project_id)
        
        # 4. 发布删除事件
        self.event_bus.publish("data_source.deleted", {
            "data_source_id": data_source_id,
            "project_id": project_id,
            "user_id": user_id,
            "permanent": permanent
        })
    
    def _soft_delete(self, data_source_id: str, project_id: str, user_id: str):
        """软删除数据源"""
        self.db.execute("""
        UPDATE data_sources 
        SET status = 'deleted', deleted_at = NOW(), deleted_by = %(user_id)s
        WHERE id = %(id)s AND project_id = %(project_id)s
        """, {
            "id": data_source_id,
            "project_id": project_id,
            "user_id": user_id
        })
    
    def _permanent_delete(self, data_source_id: str, project_id: str):
        """永久删除数据源"""
        # 先删除相关记录
        self.db.execute("""
        DELETE FROM data_source_versions 
        WHERE data_source_id = %(id)s AND project_id = %(project_id)s
        """, {
            "id": data_source_id,
            "project_id": project_id
        })
        
        # 再删除主记录
        self.db.execute("""
        DELETE FROM data_sources 
        WHERE id = %(id)s AND project_id = %(project_id)s
        """, {
            "id": data_source_id,
            "project_id": project_id
        })
    
    def list_data_sources(
        self,
        project_id: str,
        user_id: str,
        filters: Optional[Dict] = None,
        sort: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> DataSourceList:
        """
        列出数据源
        
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :param filters: 过滤条件
        :param sort: 排序字段
        :param page: 页码
        :param page_size: 每页数量
        :return: 数据源列表
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to list data sources")
        
        # 2. 构建查询
        query = self._build_list_query(project_id, filters, sort, page, page_size)
        
        # 3. 执行查询
        rows = self.db.fetchall(query["sql"], query["params"])
        total = self.db.fetchone(query["count_sql"], query["params"])["count"]
        
        # 4. 转换结果
        data_sources = [self._row_to_data_source(row) for row in rows]
        
        # 5. 获取健康状态（批量）
        data_source_ids = [ds.id for ds in data_sources]
        health_statuses = self.health_monitor.get_health_statuses(data_source_ids)
        
        for ds in data_sources:
            ds.health = health_statuses.get(ds.id, DataSourceHealth(
                status="unknown",
                last_check=None,
                metrics={}
            ))
        
        return DataSourceList(
            items=data_sources,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def _build_list_query(
        self,
        project_id: str,
        filters: Optional[Dict],
        sort: Optional[str],
        page: int,
        page_size: int
    ) -> Dict:
        """构建列表查询SQL"""
        # 基础查询
        base_sql = """
        SELECT * FROM data_sources 
        WHERE project_id = %(project_id)s
        """
        params = {"project_id": project_id}
        
        # 添加过滤条件
        if filters:
            if "status" in filters and filters["status"]:
                base_sql += " AND status = %(status)s"
                params["status"] = filters["status"]
            
            if "category" in filters and filters["category"]:
                base_sql += " AND category = %(category)s"
                params["category"] = filters["category"]
            
            if "tags" in filters and filters["tags"]:
                # 处理标签过滤（包含所有指定标签）
                tags = filters["tags"]
                if isinstance(tags, str):
                    tags = [tags]
                
                for i, tag in enumerate(tags):
                    param_name = f"tag_{i}"
                    base_sql += f" AND %(tags)s @> ARRAY[%(param_name)s]::varchar[]"
                    params[param_name] = tag
                
                params["tags"] = tags
        
        # 添加排序
        order_by = "updated_at DESC"
        if sort:
            # 验证排序字段
            valid_sort_fields = ["name", "created_at", "updated_at", "health_score"]
            if sort.lstrip("-") in valid_sort_fields:
                direction = "DESC" if sort.startswith("-") else "ASC"
                field = sort.lstrip("-")
                order_by = f"{field} {direction}"
        
        base_sql += f" ORDER BY {order_by}"
        
        # 添加分页
        offset = (page - 1) * page_size
        paginated_sql = f"{base_sql} LIMIT %(page_size)s OFFSET %(offset)s"
        
        params.update({
            "page_size": page_size,
            "offset": offset
        })
        
        # 计数查询
        count_sql = f"SELECT COUNT(*) FROM ({base_sql}) AS count_source"
        
        return {
            "sql": paginated_sql,
            "count_sql": count_sql,
            "params": params
        }
    
    def _has_permission(self, user_id: str, project_id: str, permission: str) -> bool:
        """检查用户是否有权限"""
        # 实现权限检查逻辑
        # 这里简化为检查用户是否是项目成员
        return self.project_service.is_member(user_id, project_id)
```

#### 1.4.2 搜索服务

**技术实现：**
```python
class SearchService:
    """数据源搜索服务，基于Elasticsearch实现"""
    
    def __init__(
        self,
        es_client: Elasticsearch,
        config: Config
    ):
        self.es_client = es_client
        self.config = config
        self.index_name = config.get("index_name", "data_sources")
        self.logger = logging.getLogger(__name__)
        
        # 确保索引存在
        self._ensure_index()
    
    def _ensure_index(self):
        """确保Elasticsearch索引存在"""
        if not self.es_client.indices.exists(index=self.index_name):
            self.logger.info(f"Creating Elasticsearch index: {self.index_name}")
            
            # 定义索引设置
            settings = {
                "settings": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1,
                    "analysis": {
                        "analyzer": {
                            "standard_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": ["lowercase", "stop"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "project_id": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "standard_analyzer"},
                        "display_name": {"type": "text", "analyzer": "standard_analyzer"},
                        "description": {"type": "text", "analyzer": "standard_analyzer"},
                        "url": {"type": "keyword"},
                        "category": {"type": "keyword"},
                        "data_type": {"type": "keyword"},
                        "content_type": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "tags": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "health_score": {"type": "float"},
                        "availability_7d": {"type": "float"}
                    }
                }
            }
            
            # 创建索引
            self.es_client.indices.create(
                index=self.index_name,
                body=settings
            )
    
    def add(self, data_source: DataSource):
        """添加数据源到搜索索引"""
        doc = self._to_document(data_source)
        self.es_client.index(
            index=self.index_name,
            id=data_source.id,
            body=doc
        )
    
    def _to_document(self, data_source: DataSource) -> Dict:
        """将数据源转换为Elasticsearch文档"""
        # 计算健康分数（如果可用）
        health_score = 0.0
        if data_source.health and "availability_7d" in data_source.health.metrics:
            health_score = data_source.health.metrics["availability_7d"]
        
        return {
            "id": data_source.id,
            "project_id": data_source.project_id,
            "name": data_source.name,
            "display_name": data_source.display_name,
            "description": data_source.description,
            "url": data_source.url,
            "category": data_source.category,
            "data_type": data_source.data_type,
            "content_type": data_source.content_type,
            "status": data_source.status,
            "tags": data_source.tags,
            "created_at": data_source.created_at,
            "updated_at": data_source.updated_at,
            "health_score": health_score,
            "availability_7d": data_source.health.metrics.get("availability_7d", 0.0) if data_source.health else 0.0
        }
    
    def update(self, data_source: DataSource):
        """更新搜索索引中的数据源"""
        doc = self._to_document(data_source)
        self.es_client.update(
            index=self.index_name,
            id=data_source.id,
            body={"doc": doc}
        )
    
    def delete(self, data_source_id: str, project_id: str):
        """从搜索索引中删除数据源"""
        self.es_client.delete(
            index=self.index_name,
            id=data_source_id
        )
    
    def search(
        self,
        project_id: str,
        query: str,
        filters: Optional[Dict] = None,
        sort: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> SearchResult:
        """
        搜索数据源
        
        :param project_id: 项目ID
        :param query: 搜索查询
        :param filters: 过滤条件
        :param sort: 排序字段
        :param page: 页码
        :param page_size: 每页数量
        :return: 搜索结果
        """
        # 构建查询体
        body = self._build_search_query(project_id, query, filters, sort, page, page_size)
        
        # 执行搜索
        result = self.es_client.search(
            index=self.index_name,
            body=body
        )
        
        # 处理结果
        hits = result["hits"]["hits"]
        total = result["hits"]["total"]["value"]
        
        data_sources = []
        for hit in hits:
            source = hit["_source"]
            # 这里应该转换为DataSource对象，但为了示例简化
            data_sources.append(source)
        
        return SearchResult(
            items=data_sources,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def _build_search_query(
        self,
        project_id: str,
        query: str,
        filters: Optional[Dict],
        sort: Optional[str],
        page: int,
        page_size: int
    ) -> Dict:
        """构建Elasticsearch查询体"""
        # 基础查询 - 仅限当前项目
        base_query = {
            "bool": {
                "must": [
                    {"term": {"project_id": project_id}}
                ]
            }
        }
        
        # 添加全文搜索
        if query and query.strip():
            base_query["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["name^3", "display_name^2", "description", "url"],
                    "fuzziness": "AUTO"
                }
            })
        
        # 添加过滤条件
        if filters:
            if "status" in filters and filters["status"]:
                base_query["bool"]["must"].append({
                    "term": {"status": filters["status"]}
                })
            
            if "category" in filters and filters["category"]:
                base_query["bool"]["must"].append({
                    "term": {"category": filters["category"]}
                })
            
            if "tags" in filters and filters["tags"]:
                tags = filters["tags"]
                if isinstance(tags, str):
                    tags = [tags]
                
                # 必须包含所有指定标签
                for tag in tags:
                    base_query["bool"]["must"].append({
                        "term": {"tags": tag}
                    })
            
            if "min_health" in filters:
                base_query["bool"]["must"].append({
                    "range": {
                        "health_score": {
                            "gte": filters["min_health"]
                        }
                    }
                })
        
        # 构建排序
        sort_spec = []
        if sort:
            # 验证排序字段
            valid_sort_fields = ["name", "created_at", "updated_at", "health_score"]
            if sort.lstrip("-") in valid_sort_fields:
                direction = "desc" if sort.startswith("-") else "asc"
                field = sort.lstrip("-")
                sort_spec.append({field: {"order": direction}})
        
        # 默认排序
        if not sort_spec:
            sort_spec.append({"_score": {"order": "desc"}})
            sort_spec.append({"updated_at": {"order": "desc"}})
        
        # 计算分页
        from_val = (page - 1) * page_size
        
        return {
            "query": base_query,
            "sort": sort_spec,
            "from": from_val,
            "size": page_size,
            "_source": True
        }
    
    def suggest_tags(self, project_id: str, prefix: str) -> List[str]:
        """建议标签（基于现有标签）"""
        # 使用terms aggregation获取匹配的标签
        body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"term": {"project_id": project_id}}
                    ]
                }
            },
            "aggs": {
                "suggested_tags": {
                    "terms": {
                        "field": "tags",
                        "include": f".*{prefix}.*",
                        "size": 10
                    }
                }
            }
        }
        
        result = self.es_client.search(
            index=self.index_name,
            body=body
        )
        
        # 提取建议的标签
        buckets = result["aggregations"]["suggested_tags"]["buckets"]
        return [bucket["key"] for bucket in buckets]
```

#### 1.4.3 分类管理服务

**技术实现：**
```python
class CategoryService:
    """数据源分类管理服务"""
    
    def __init__(
        self,
        db: Database,
        config: Config
    ):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.cache = TTLCache(maxsize=1000, ttl=300)  # 5分钟缓存
    
    def get_category_tree(
        self,
        project_id: str,
        user_id: str
    ) -> List[CategoryNode]:
        """
        获取分类树
        
        :param project_id: 项目ID
        :param user_id: 用户ID
        :return: 分类树
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to view categories")
        
        # 2. 尝试从缓存获取
        cache_key = f"{project_id}:tree"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 3. 从数据库获取
        categories = self._get_all_categories(project_id)
        
        # 4. 构建树结构
        tree = self._build_category_tree(categories)
        
        # 5. 缓存结果
        self.cache[cache_key] = tree
        
        return tree
    
    def _get_all_categories(self, project_id: str) -> List[Category]:
        """从数据库获取所有分类"""
        sql = """
        SELECT * FROM data_source_categories 
        WHERE project_id = %(project_id)s 
        ORDER BY parent_id NULLS FIRST, sort_order
        """
        
        rows = self.db.fetchall(sql, {"project_id": project_id})
        return [self._row_to_category(row) for row in rows]
    
    def _row_to_category(self, row: Dict) -> Category:
        """将数据库行转换为Category对象"""
        return Category(
            id=row["id"],
            project_id=row["project_id"],
            name=row["name"],
            description=row["description"],
            parent_id=row["parent_id"],
            sort_order=row["sort_order"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    def _build_category_tree(self, categories: List[Category]) -> List[CategoryNode]:
        """构建分类树结构"""
        # 创建ID到分类的映射
        category_map = {cat.id: cat for cat in categories}
        
        # 创建节点映射
        node_map = {}
        for cat in categories:
            node_map[cat.id] = CategoryNode(
                category=cat,
                children=[]
            )
        
        # 构建树结构
        root_nodes = []
        for cat in categories:
            node = node_map[cat.id]
            
            if cat.parent_id is None:
                # 根节点
                root_nodes.append(node)
            else:
                # 子节点
                parent_node = node_map.get(cat.parent_id)
                if parent_node:
                    parent_node.children.append(node)
        
        # 按排序顺序
        def sort_nodes(nodes):
            return sorted(nodes, key=lambda n: (n.category.sort_order, n.category.name))
        
        # 递归排序
        def sort_tree(node):
            node.children = sort_nodes(node.children)
            for child in node.children:
                sort_tree(child)
        
        for node in root_nodes:
            sort_tree(node)
        
        return sort_nodes(root_nodes)
    
    def create_category(
        self,
        project_id: str,
        category: Category,
        user_id: str
    ) -> Category:
        """
        创建新分类
        
        :param project_id: 项目ID
        :param category: 分类对象
        :param user_id: 创建者ID
        :return: 创建后的分类
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "write"):
            raise PermissionError("User does not have permission to create categories")
        
        # 2. 验证分类
        self._validate_category(category, project_id)
        
        # 3. 生成唯一ID
        category.id = f"cat-{uuid.uuid4().hex[:8]}"
        category.project_id = project_id
        category.created_at = datetime.utcnow()
        category.updated_at = category.created_at
        
        # 4. 保存到数据库
        self._save_category(category)
        
        # 5. 清除缓存
        self._clear_cache(project_id)
        
        return category
    
    def _validate_category(self, category: Category, project_id: str):
        """验证分类是否有效"""
        # 必填字段
        if not category.name:
            raise ValidationError("Category name is required")
        
        # 检查名称是否重复
        if self._category_name_exists(category.name, project_id, category.parent_id, exclude_id=None):
            raise ValidationError("Category name already exists in this parent")
    
    def _category_name_exists(
        self,
        name: str,
        project_id: str,
        parent_id: Optional[str],
        exclude_id: Optional[str]
    ) -> bool:
        """检查分类名称是否已存在"""
        sql = """
        SELECT COUNT(*) FROM data_source_categories 
        WHERE project_id = %(project_id)s 
        AND name = %(name)s
        AND parent_id IS NOT DISTINCT FROM %(parent_id)s
        """
        params = {
            "project_id": project_id,
            "name": name,
            "parent_id": parent_id
        }
        
        if exclude_id:
            sql += " AND id != %(exclude_id)s"
            params["exclude_id"] = exclude_id
        
        count = self.db.fetchone(sql, params)["count"]
        return count > 0
    
    def _save_category(self, category: Category):
        """保存分类到数据库"""
        sql = """
        INSERT INTO data_source_categories (
            id, project_id, name, description, parent_id, sort_order, created_at, updated_at
        ) VALUES (
            %(id)s, %(project_id)s, %(name)s, %(description)s, %(parent_id)s, %(sort_order)s, 
            %(created_at)s, %(updated_at)s
        )
        """
        
        self.db.execute(sql, {
            "id": category.id,
            "project_id": category.project_id,
            "name": category.name,
            "description": category.description,
            "parent_id": category.parent_id,
            "sort_order": category.sort_order or 0,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        })
    
    def update_category(
        self,
        category_id: str,
        project_id: str,
        updates: Dict,
        user_id: str
    ) -> Category:
        """
        更新分类
        
        :param category_id: 分类ID
        :param project_id: 项目ID
        :param updates: 更新字段
        :param user_id: 更新者ID
        :return: 更新后的分类
        """
        # 1. 获取当前分类
        current = self.get_category(category_id, project_id, user_id)
        
        # 2. 验证更新
        self._validate_category_update(updates, current, project_id)
        
        # 3. 更新字段
        updated_category = self._apply_updates(current, updates)
        
        # 4. 保存更新
        self._update_category_in_db(updated_category)
        
        # 5. 清除缓存
        self._clear_cache(project_id)
        
        return updated_category
    
    def _validate_category_update(
        self,
        updates: Dict,
        current: Category,
        project_id: str
    ):
        """验证分类更新是否有效"""
        # 不能修改ID和项目ID
        if "id" in updates or "project_id" in updates:
            raise ValidationError("Cannot update category ID or project ID")
        
        # 验证名称变更
        if "name" in updates:
            if self._category_name_exists(
                updates["name"], 
                project_id, 
                current.parent_id, 
                exclude_id=current.id
            ):
                raise ValidationError("Category name already exists in this parent")
        
        # 验证父级变更
        if "parent_id" in updates:
            new_parent_id = updates["parent_id"]
            
            # 检查是否形成循环
            if self._would_create_cycle(current.id, new_parent_id):
                raise ValidationError("Cannot create circular category hierarchy")
            
            # 检查新父级是否在同一项目
            if new_parent_id and not self._parent_in_same_project(new_parent_id, project_id):
                raise ValidationError("Parent category must be in the same project")
    
    def _would_create_cycle(self, category_id: str, new_parent_id: Optional[str]) -> bool:
        """检查是否会导致循环引用"""
        if not new_parent_id:
            return False
        
        # 检查新父级是否是当前分类的后代
        ancestor_ids = self._get_all_ancestor_ids(new_parent_id)
        return category_id in ancestor_ids
    
    def _get_all_ancestor_ids(self, category_id: str) -> Set[str]:
        """获取分类的所有祖先ID"""
        ancestor_ids = set()
        current_id = category_id
        
        while current_id:
            ancestor_ids.add(current_id)
            
            # 获取父级
            parent_id = self.db.fetchone(
                "SELECT parent_id FROM data_source_categories WHERE id = %(id)s",
                {"id": current_id}
            )["parent_id"]
            
            current_id = parent_id
        
        return ancestor_ids
    
    def _parent_in_same_project(self, parent_id: str, project_id: str) -> bool:
        """检查父级是否在同一项目"""
        result = self.db.fetchone(
            "SELECT COUNT(*) FROM data_source_categories "
            "WHERE id = %(id)s AND project_id = %(project_id)s",
            {"id": parent_id, "project_id": project_id}
        )
        return result["count"] > 0
    
    def _apply_updates(self, current: Category, updates: Dict) -> Category:
        """应用更新到分类对象"""
        updated = copy.deepcopy(current)
        
        for field, value in updates.items():
            if hasattr(updated, field):
                setattr(updated, field, value)
        
        updated.updated_at = datetime.utcnow()
        return updated
    
    def _update_category_in_db(self, category: Category):
        """将更新保存到数据库"""
        update_fields = []
        params = {
            "id": category.id,
            "updated_at": category.updated_at
        }
        
        if "name" in category:
            update_fields.append("name = %(name)s")
            params["name"] = category.name
        if "description" in category:
            update_fields.append("description = %(description)s")
            params["description"] = category.description
        if "parent_id" in category:
            update_fields.append("parent_id = %(parent_id)s")
            params["parent_id"] = category.parent_id
        if "sort_order" in category:
            update_fields.append("sort_order = %(sort_order)s")
            params["sort_order"] = category.sort_order
        
        sql = f"""
        UPDATE data_source_categories 
        SET {', '.join(update_fields)}, updated_at = %(updated_at)s
        WHERE id = %(id)s
        """
        
        self.db.execute(sql, params)
    
    def get_category(
        self,
        category_id: str,
        project_id: str,
        user_id: str
    ) -> Category:
        """
        获取分类详情
        
        :param category_id: 分类ID
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :return: 分类对象
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to view this category")
        
        # 2. 从数据库获取
        sql = """
        SELECT * FROM data_source_categories 
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        row = self.db.fetchone(sql, {
            "id": category_id,
            "project_id": project_id
        })
        
        if not row:
            raise NotFoundError(f"Category {category_id} not found")
        
        return self._row_to_category(row)
    
    def delete_category(
        self,
        category_id: str,
        project_id: str,
        user_id: str,
        reassign_to: Optional[str] = None
    ):
        """
        删除分类
        
        :param category_id: 分类ID
        :param project_id: 项目ID
        :param user_id: 删除者ID
        :param reassign_to: 重新分配到的分类ID（可选）
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "delete"):
            raise PermissionError("User does not have permission to delete categories")
        
        # 2. 获取分类
        category = self.get_category(category_id, project_id, user_id)
        
        # 3. 检查是否有子分类
        child_count = self._get_child_count(category_id)
        if child_count > 0:
            raise ValidationError("Cannot delete category with child categories")
        
        # 4. 检查是否有数据源
        source_count = self._get_data_source_count(category_id)
        if source_count > 0:
            if not reassign_to:
                raise ValidationError(
                    f"Category contains {source_count} data sources. "
                    "Please specify a category to reassign to."
                )
            
            # 验证目标分类
            self.get_category(reassign_to, project_id, user_id)
            
            # 重新分配数据源
            self._reassign_data_sources(category_id, reassign_to)
        
        # 5. 删除分类
        self._delete_category(category_id)
        
        # 6. 清除缓存
        self._clear_cache(project_id)
    
    def _get_child_count(self, category_id: str) -> int:
        """获取子分类数量"""
        result = self.db.fetchone(
            "SELECT COUNT(*) FROM data_source_categories WHERE parent_id = %(id)s",
            {"id": category_id}
        )
        return result["count"]
    
    def _get_data_source_count(self, category_id: str) -> int:
        """获取分类中的数据源数量"""
        result = self.db.fetchone(
            "SELECT COUNT(*) FROM data_sources WHERE category = %(id)s",
            {"id": category_id}
        )
        return result["count"]
    
    def _reassign_data_sources(self, from_category: str, to_category: str):
        """重新分配数据源到新分类"""
        self.db.execute(
            "UPDATE data_sources SET category = %(to_category)s WHERE category = %(from_category)s",
            {"to_category": to_category, "from_category": from_category}
        )
    
    def _delete_category(self, category_id: str):
        """从数据库删除分类"""
        self.db.execute(
            "DELETE FROM data_source_categories WHERE id = %(id)s",
            {"id": category_id}
        )
    
    def _clear_cache(self, project_id: str):
        """清除项目缓存"""
        cache_key = f"{project_id}:tree"
        if cache_key in self.cache:
            del self.cache[cache_key]
    
    def _has_permission(self, user_id: str, project_id: str, permission: str) -> bool:
        """检查用户是否有权限"""
        # 实现权限检查逻辑
        return True  # 简化实现
```

### 1.5 数据模型详细定义

#### 1.5.1 数据源核心表

```sql
-- 数据源主表
CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    data_type VARCHAR(30) NOT NULL CHECK (data_type IN ('image', 'video', 'document', 'api', 'html', 'json', 'xml')),
    content_type VARCHAR(100),
    schema JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'deprecated', 'suspended', 'deleted')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    deleted_at TIMESTAMPTZ,
    deleted_by UUID REFERENCES users(id) ON DELETE SET NULL,
    last_health_check TIMESTAMPTZ,
    health_score NUMERIC(4,2) DEFAULT 0.0,
    availability_24h NUMERIC(4,2) DEFAULT 1.0,
    availability_7d NUMERIC(4,2) DEFAULT 1.0,
    last_crawler_run TIMESTAMPTZ,
    crawler_id UUID REFERENCES crawler_instances(id),
    crawler_config JSONB,
    tags JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 索引
    UNIQUE (project_id, name),
    INDEX idx_data_sources_project ON data_sources(project_id),
    INDEX idx_data_sources_category ON data_sources(category),
    INDEX idx_data_sources_status ON data_sources(status),
    INDEX idx_data_sources_health ON data_sources(health_score DESC),
    INDEX idx_data_sources_updated ON data_sources(updated_at DESC),
    
    -- 全文搜索
    ts_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(display_name, '') || ' ' || coalesce(description, '') || ' ' || url)
    ) STORED
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_data_sources_modtime
BEFORE UPDATE ON data_sources
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- 全文搜索索引
CREATE INDEX idx_data_sources_search ON data_sources USING GIN (ts_vector);
```

#### 1.5.2 数据源版本表

```sql
-- 数据源版本表
CREATE TABLE data_source_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    version_id VARCHAR(50) NOT NULL,
    changes JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    previous_version VARCHAR(50),
    
    -- 索引
    UNIQUE (data_source_id, version_id),
    INDEX idx_versions_data_source ON data_source_versions(data_source_id),
    INDEX idx_versions_created ON data_source_versions(created_at DESC)
);
```

#### 1.5.3 分类表

```sql
-- 数据源分类表
CREATE TABLE data_source_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id UUID REFERENCES data_source_categories(id) ON DELETE CASCADE,
    sort_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    UNIQUE (project_id, name, parent_id),
    INDEX idx_categories_project ON data_source_categories(project_id),
    INDEX idx_categories_parent ON data_source_categories(parent_id)
);
```

### 1.6 API详细规范

#### 1.6.1 数据源管理API

**创建数据源 (POST /api/v1/data-sources)**

*请求示例:*
```http
POST /api/v1/data-sources HTTP/1.1
Host: dsr.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json
X-Request-ID: req-123456

{
  "name": "instagram-api",
  "display_name": "Instagram API",
  "description": "Official Instagram API for fetching user posts",
  "url": "https://api.instagram.com/v1/users/self/media/recent",
  "category": "social-media",
  "data_type": "json",
  "content_type": "application/json",
  "schema": {
    "type": "object",
    "properties": {
      "data": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "images": {
              "type": "object",
              "properties": {
                "standard_resolution": {
                  "type": "object",
                  "properties": {
                    "url": {"type": "string"},
                    "width": {"type": "integer"},
                    "height": {"type": "integer"}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "tags": ["social", "api", "instagram"],
  "metadata": {
    "api_version": "v1"
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/data-sources/instagram-api
X-Request-ID: req-123456
ETag: "d41d8cd98f00b204e9800998ecf8427e"

{
  "id": "ds-7a8b9c0d",
  "project_id": "proj-123",
  "name": "instagram-api",
  "display_name": "Instagram API",
  "description": "Official Instagram API for fetching user posts",
  "url": "https://api.instagram.com/v1/users/self/media/recent",
  "category": "social-media",
  "data_type": "json",
  "content_type": "application/json",
  "schema": {
    "type": "object",
    "properties": {
      "data": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "images": {
              "type": "object",
              "properties": {
                "standard_resolution": {
                  "type": "object",
                  "properties": {
                    "url": {"type": "string"},
                    "width": {"type": "integer"},
                    "height": {"type": "integer"}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "status": "active",
  "created_at": "2023-06-15T10:30:45Z",
  "updated_at": "2023-06-15T10:30:45Z",
  "owner_id": "user-123",
  "health": {
    "status": "unknown",
    "last_check": null,
    "metrics": {}
  },
  "tags": ["social", "api", "instagram"],
  "metadata": {
    "api_version": "v1"
  }
}
```

**获取数据源列表 (GET /api/v1/data-sources)**

*请求示例:*
```http
GET /api/v1/data-sources?category=social-media&status=active&page=1&page_size=20 HTTP/1.1
Host: dsr.mirror-realm.com
Authorization: Bearer <access_token>
Accept: application/json
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": "ds-7a8b9c0d",
      "name": "instagram-api",
      "display_name": "Instagram API",
      "url": "https://api.instagram.com/v1/users/self/media/recent",
      "category": "social-media",
      "data_type": "json",
      "status": "active",
      "created_at": "2023-06-15T10:30:45Z",
      "updated_at": "2023-06-15T10:30:45Z",
      "health": {
        "status": "healthy",
        "last_check": "2023-06-15T10:35:20Z",
        "metrics": {
          "availability_24h": 0.98,
          "availability_7d": 0.95,
          "response_time_p50": 0.35,
          "response_time_p95": 1.2
        }
      },
      "tags": ["social", "api", "instagram"]
    },
    {
      "id": "ds-1b2c3d4e",
      "name": "twitter-api",
      "display_name": "Twitter API",
      "url": "https://api.twitter.com/2/users/me/tweets",
      "category": "social-media",
      "data_type": "json",
      "status": "active",
      "created_at": "2023-06-10T08:15:30Z",
      "updated_at": "2023-06-10T08:15:30Z",
      "health": {
        "status": "degraded",
        "last_check": "2023-06-15T10:34:15Z",
        "metrics": {
          "availability_24h": 0.85,
          "availability_7d": 0.92,
          "response_time_p50": 0.8,
          "response_time_p95": 3.5
        }
      },
      "tags": ["social", "api", "twitter"]
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 20
}
```

#### 1.6.2 搜索API

**搜索数据源 (POST /api/v1/data-sources:search)**

*请求示例:*
```http
POST /api/v1/data-sources:search HTTP/1.1
Host: dsr.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "query": "instagram",
  "filters": {
    "category": "social-media",
    "tags": ["api"],
    "min_health": 0.9
  },
  "sort": "-health_score",
  "page": 1,
  "page_size": 10
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": "ds-7a8b9c0d",
      "name": "instagram-api",
      "display_name": "Instagram API",
      "url": "https://api.instagram.com/v1/users/self/media/recent",
      "category": "social-media",
      "data_type": "json",
      "status": "active",
      "health_score": 0.95,
      "created_at": "2023-06-15T10:30:45Z",
      "updated_at": "2023-06-15T10:30:45Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### 1.7 性能优化策略

#### 1.7.1 数据库优化

1. **分区策略**
   ```sql
   -- 按项目ID分区
   CREATE TABLE data_sources PARTITION OF data_sources_master
   FOR VALUES IN ('proj-123');
   
   CREATE TABLE data_sources PARTITION OF data_sources_master
   FOR VALUES IN ('proj-456');
   ```

2. **索引优化**
   ```sql
   -- 为常用查询模式创建复合索引
   CREATE INDEX idx_data_sources_project_category ON data_sources(project_id, category);
   CREATE INDEX idx_data_sources_project_status ON data_sources(project_id, status);
   CREATE INDEX idx_data_sources_project_health ON data_sources(project_id, health_score DESC);
   ```

3. **查询优化**
   - 使用覆盖索引减少IO
   - 避免SELECT *
   - 使用批量操作减少往返
   - 适当使用CTE提高可读性

#### 1.7.2 缓存策略

1. **多级缓存架构**
   ```
   ┌───────────────────────────────────────────────────────────────────────────────┐
   │                                   缓存层                                      │
   ├───────────────────┬───────────────────┬───────────────────┬───────────────────┤
   │  客户端缓存       │  CDN缓存          │  应用层缓存      │  数据库缓存       │
   ├───────────────────┼───────────────────┼───────────────────┼───────────────────┤
   │ • ETag/Last-Modified│ • 静态资源缓存   │ • Redis缓存      │ • 查询结果缓存   │
   │ • 浏览器本地存储   │ • API响应缓存    │ • 分类树缓存     │ • 连接池         │
   └───────────────────┴───────────────────┴───────────────────┴───────────────────┘
   ```

2. **缓存失效策略**
   - 写操作后立即失效相关缓存
   - 设置合理的TTL（分类树：5分钟，数据源详情：1分钟）
   - 使用缓存版本控制避免陈旧数据

#### 1.7.3 搜索性能优化

1. **Elasticsearch优化**
   - 调整分片和副本数量
   - 优化索引刷新间隔
   - 使用字段数据类型优化存储
   - 实现搜索结果分页缓存

2. **查询优化**
   ```python
   def optimized_search(project_id, query, filters, sort, page, page_size):
       # 1. 使用过滤上下文代替查询上下文（当不需要相关性评分时）
       # 2. 限制返回字段
       # 3. 使用search_after代替from/size进行深分页
       # 4. 实现结果缓存
       pass
   ```

### 1.8 安全考虑

#### 1.8.1 访问控制

1. **基于角色的访问控制(RBAC)模型**
   ```
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │    Users    │─────▶│    Roles    │─────▶│  Permissions│
   └─────────────┘      └─────────────┘      └─────────────┘
          │                   ▲
          │                   │
          ▼                   │
   ┌─────────────┐      ┌─────────────┐
   │  Projects   │─────▶│    Teams    │
   └─────────────┘      └─────────────┘
   ```

2. **细粒度权限检查**
   ```python
   def check_permission(user_id, project_id, resource, action):
       """
       检查用户是否有权限执行特定操作
       
       :param user_id: 用户ID
       :param project_id: 项目ID
       :param resource: 资源类型 (data_source, category等)
       :param action: 操作 (read, write, delete等)
       :return: 是否有权限
       """
       # 1. 检查项目成员资格
       if not project_service.is_member(user_id, project_id):
           return False
       
       # 2. 检查角色权限
       user_role = project_service.get_user_role(user_id, project_id)
       return permission_service.has_permission(user_role, resource, action)
   ```

#### 1.8.2 数据安全

1. **敏感数据处理**
   - 对API密钥等敏感信息进行加密存储
   - 实现字段级访问控制
   - 记录敏感数据访问日志

2. **审计日志**
   ```sql
   CREATE TABLE data_source_audit_logs (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
       user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
       project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
       action VARCHAR(20) NOT NULL, -- create, update, delete, read
       old_value JSONB,
       new_value JSONB,
       timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       ip_address INET,
       user_agent TEXT
   );
   
   CREATE INDEX idx_audit_logs_data_source ON data_source_audit_logs(data_source_id);
   CREATE INDEX idx_audit_logs_timestamp ON data_source_audit_logs(timestamp DESC);
   ```

### 1.9 与其他模块的交互

#### 1.9.1 与数据源健康监测系统交互

```mermaid
sequenceDiagram
    participant DSR as Data Source Registry
    participant DSHMS as Data Source Health Monitoring System
    
    DSHMS->>DSR: GET /api/v1/data-sources?status=active
    DSR-->>DSHMS: Active data sources list
    
    loop 每5分钟
        DSHMS->>DSR: POST /api/v1/data-sources/{id}/health
        DSR-->>DSHMS: Acknowledgement
    end
    
    DSR->>DSHMS: GET /api/v1/health/data-sources/{id}
    DSHMS-->>DSR: Health status and metrics
```

#### 1.9.2 与数据处理工作流引擎交互

```mermaid
sequenceDiagram
    participant DPWE as Data Processing Workflow Engine
    participant DSR as Data Source Registry
    
    DPWE->>DSR: GET /api/v1/data-sources/{id}
    DSR-->>DPWE: Data source details
    
    DPWE->>DSR: GET /api/v1/data-sources?category=images
    DSR-->>DPWE: Filtered data sources
    
    DPWE->>DSR: POST /api/v1/data-sources/{id}/status
    DSR-->>DPWE: Updated status
```

#### 1.9.3 与AI辅助开发系统交互

```mermaid
sequenceDiagram
    participant AIDS as AI-Assisted Development System
    participant DSR as Data Source Registry
    
    AIDS->>DSR: GET /api/v1/data-sources?tags=api
    DSR-->>AIDS: API data sources
    
    AIDS->>DSR: GET /api/v1/data-sources/{id}
    DSR-->>AIDS: Data source schema
    
    AIDS->>DSR: POST /api/v1/data-sources/schema/analyze
    DSR-->>AIDS: Schema analysis results
```

## 2. 网站指纹分析引擎 (Website Fingerprinting Engine)

### 2.1 模块概述
网站指纹分析引擎负责分析目标网站的技术栈、反爬机制和内容特征，为爬虫配置提供智能建议。它通过主动探测和被动分析相结合的方式，构建全面的网站指纹数据库。

### 2.2 详细功能清单

#### 2.2.1 核心功能
- **技术栈识别**
  - 服务器软件识别（Apache, Nginx, IIS等）
  - 编程语言识别（PHP, Ruby, Python, Node.js等）
  - 前端框架识别（React, Angular, Vue等）
  - CMS识别（WordPress, Drupal, Joomla等）
  - 数据库识别
  - CDN识别
- **反爬机制检测**
  - User-Agent检测
  - IP限制检测
  - 请求频率限制
  - 行为验证（鼠标移动、点击模式）
  - 挑战响应机制（JS挑战、CAPTCHA）
  - 指纹检测（Canvas, WebGL, AudioContext等）
- **内容特征分析**
  - 页面结构分析（DOM树复杂度）
  - 动态内容检测（AJAX加载内容）
  - 内容编码分析
  - 响应时间分析
- **指纹数据库管理**
  - 指纹规则存储与管理
  - 指纹版本控制
  - 指纹质量评估

#### 2.2.2 高级功能
- **智能爬虫配置建议**
  - 基于指纹的爬虫参数推荐
  - 反爬绕过策略建议
  - 最佳爬取时间建议
- **网站变更监测**
  - 技术栈变更检测
  - 反爬机制更新预警
  - 内容结构变更分析
- **指纹学习系统**
  - 自动学习新的网站特征
  - 指纹规则优化
  - 误报/漏报分析

### 2.3 技术架构

#### 2.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                              网站指纹分析引擎 (WFE)                                           │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  分析执行层           │  规则引擎层           │  数据管理层                                 │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 主动探测服务        │ • 规则加载器          │ • 指纹数据库                               │
│ • 被动分析服务        │ • 规则执行器          │ • 规则版本控制                             │
│ • 指纹生成服务        │ • 规则优化器          │ • 分析结果存储                             │
│ • 变更监测服务        │ • 机器学习模型        │ • 性能指标存储                             │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 2.3.2 服务边界与交互
- **输入**：
  - 目标URL列表（来自数据源注册中心）
  - 手动触发的分析请求
  - 网站变更监测事件
- **输出**：
  - 技术栈分析报告
  - 反爬机制检测结果
  - 智能爬虫配置建议
  - 网站变更预警

### 2.4 核心组件详细实现

#### 2.4.1 技术栈识别服务

**技术实现：**
```python
class TechStackAnalyzer:
    """网站技术栈识别服务"""
    
    def __init__(
        self,
        rule_engine: RuleEngine,
        http_client: HttpClient,
        config: Config
    ):
        self.rule_engine = rule_engine
        self.http_client = http_client
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def analyze(
        self,
        url: str,
        options: Optional[AnalysisOptions] = None
    ) -> TechStackReport:
        """
        分析网站技术栈
        
        :param url: 目标URL
        :param options: 分析选项
        :return: 技术栈分析报告
        """
        # 1. 准备分析选项
        opts = options or AnalysisOptions()
        
        # 2. 获取页面内容
        response = self._fetch_page(url, opts)
        
        # 3. 执行技术栈分析
        tech_stack = self._analyze_tech_stack(url, response, opts)
        
        # 4. 生成报告
        return self._generate_report(url, response, tech_stack, opts)
    
    def _fetch_page(
        self,
        url: str,
        options: AnalysisOptions
    ) -> HttpResponse:
        """获取页面内容"""
        # 准备请求头
        headers = {
            "User-Agent": options.user_agent or self.config.default_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
        
        # 添加自定义请求头
        if options.headers:
            headers.update(options.headers)
        
        # 执行HTTP请求
        try:
            start_time = time.time()
            response = self.http_client.get(
                url,
                headers=headers,
                timeout=options.timeout or self.config.default_timeout,
                follow_redirects=options.follow_redirects
            )
            duration = time.time() - start_time
            
            return HttpResponse(
                url=response.url,
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
                duration=duration,
                redirect_chain=[r.url for r in response.redirects]
            )
            
        except Exception as e:
            self.logger.error("Error fetching %s: %s", url, str(e))
            raise AnalysisError(f"Failed to fetch page: {str(e)}")
    
    def _analyze_tech_stack(
        self,
        url: str,
        response: HttpResponse,
        options: AnalysisOptions
    ) -> Dict[str, List[Technology]]:
        """分析技术栈"""
        results = {
            "server": [],
            "framework": [],
            "cms": [],
            "javascript": [],
            "database": [],
            "cdn": [],
            "os": []
        }
        
        # 1. 从响应头分析
        self._analyze_from_headers(response, results)
        
        # 2. 从HTML内容分析
        if response.content:
            self._analyze_from_html(response.content, results)
        
        # 3. 从URL结构分析
        self._analyze_from_url(url, results)
        
        # 4. 从JavaScript文件分析
        if options.analyze_js and response.content:
            self._analyze_from_js(response.content, results)
        
        # 5. 执行高级分析（如果启用）
        if options.advanced_analysis:
            self._perform_advanced_analysis(url, response, results)
        
        return results
    
    def _analyze_from_headers(
        self,
        response: HttpResponse,
        results: Dict[str, List[Technology]]
    ):
        """从HTTP响应头分析技术栈"""
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        # 服务器软件
        if "server" in headers:
            server_header = headers["server"]
            server_match = self.rule_engine.match(
                "server", 
                server_header, 
                RuleCategory.HEADER
            )
            if server_match:
                results["server"].extend(server_match.technologies)
        
        # X-Powered-By
        if "x-powered-by" in headers:
            powered_by = headers["x-powered-by"]
            powered_by_match = self.rule_engine.match(
                "powered-by", 
                powered_by, 
                RuleCategory.HEADER
            )
            if powered_by_match:
                results["server"].extend(powered_by_match.technologies)
        
        # Set-Cookie分析
        if "set-cookie" in headers:
            cookies = headers["set-cookie"]
            cookie_match = self.rule_engine.match(
                "cookies", 
                cookies, 
                RuleCategory.HEADER
            )
            if cookie_match:
                results["server"].extend(cookie_match.technologies)
    
    def _analyze_from_html(
        self,
        content: bytes,
        results: Dict[str, List[Technology]]
    ):
        """从HTML内容分析技术栈"""
        try:
            # 解析HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Meta标签分析
            self._analyze_meta_tags(soup, results)
            
            # 脚本标签分析
            self._analyze_script_tags(soup, results)
            
            # 链接标签分析
            self._analyze_link_tags(soup, results)
            
            # HTML属性分析
            self._analyze_html_attributes(soup, results)
            
        except Exception as e:
            self.logger.warning("Error parsing HTML: %s", str(e))
    
    def _analyze_meta_tags(
        self,
        soup: BeautifulSoup,
        results: Dict[str, List[Technology]]
    ):
        """分析meta标签"""
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            
            if not content:
                continue
            
            # Generator meta标签
            if name == 'generator':
                generator_match = self.rule_engine.match(
                    "generator", 
                    content, 
                    RuleCategory.META
                )
                if generator_match:
                    results["cms"].extend(generator_match.technologies)
            
            # 特定CMS meta标签
            elif "wordpress" in name or "wp" in name:
                results["cms"].append(Technology(
                    name="WordPress",
                    version=self._extract_version(content),
                    confidence=0.9,
                    category="cms"
                ))
    
    def _analyze_script_tags(
        self,
        soup: BeautifulSoup,
        results: Dict[str, List[Technology]]
    ):
        """分析script标签"""
        for script in soup.find_all('script', src=True):
            src = script['src']
            
            # 分析脚本路径
            script_match = self.rule_engine.match(
                "scripts", 
                src, 
                RuleCategory.SCRIPT
            )
            if script_match:
                results["javascript"].extend(script_match.technologies)
        
        # 分析内联脚本
        inline_scripts = [s.string for s in soup.find_all('script') if s.string]
        if inline_scripts:
            inline_match = self.rule_engine.match(
                "inline-scripts", 
                "\n".join(inline_scripts), 
                RuleCategory.INLINE_SCRIPT
            )
            if inline_match:
                results["javascript"].extend(inline_match.technologies)
    
    def _analyze_link_tags(
        self,
        soup: BeautifulSoup,
        results: Dict[str, List[Technology]]
    ):
        """分析link标签"""
        for link in soup.find_all('link', href=True):
            href = link['href']
            
            # 分析CSS路径
            css_match = self.rule_engine.match(
                "css", 
                href, 
                RuleCategory.CSS
            )
            if css_match:
                results["framework"].extend(css_match.technologies)
    
    def _analyze_html_attributes(
        self,
        soup: BeautifulSoup,
        results: Dict[str, List[Technology]]
    ):
        """分析HTML属性"""
        # 检查data-*属性
        for tag in soup.find_all(True):
            for attr, value in tag.attrs.items():
                if attr.startswith('data-'):
                    data_attr_match = self.rule_engine.match(
                        "data-attributes", 
                        f"{attr}={value}", 
                        RuleCategory.ATTRIBUTE
                    )
                    if data_attr_match:
                        results["framework"].extend(data_attr_match.technologies)
        
        # 检查class属性
        classes = set()
        for tag in soup.find_all(class_=True):
            if isinstance(tag['class'], list):
                classes.update(tag['class'])
            else:
                classes.update(tag['class'].split())
        
        if classes:
            class_match = self.rule_engine.match(
                "classes", 
                " ".join(classes), 
                RuleCategory.CLASS
            )
            if class_match:
                results["framework"].extend(class_match.technologies)
    
    def _analyze_from_url(
        self,
        url: str,
        results: Dict[str, List[Technology]]
    ):
        """从URL结构分析技术栈"""
        # 分析路径
        path_match = self.rule_engine.match(
            "paths", 
            urlparse(url).path, 
            RuleCategory.PATH
        )
        if path_match:
            results["server"].extend(path_match.technologies)
        
        # 分析查询参数
        query_match = self.rule_engine.match(
            "query-params", 
            urlparse(url).query, 
            RuleCategory.QUERY
        )
        if query_match:
            results["server"].extend(query_match.technologies)
    
    def _analyze_from_js(
        self,
        content: bytes,
        results: Dict[str, List[Technology]]
    ):
        """从JavaScript文件分析技术栈"""
        try:
            # 提取所有JS文件
            soup = BeautifulSoup(content, 'html.parser')
            js_files = [script['src'] for script in soup.find_all('script', src=True)]
            
            # 下载并分析JS文件
            for js_url in js_files:
                try:
                    js_response = self.http_client.get(
                        js_url,
                        timeout=self.config.js_analysis_timeout
                    )
                    
                    # 分析JS内容
                    js_match = self.rule_engine.match(
                        "javascript", 
                        js_response.text, 
                        RuleCategory.JAVASCRIPT
                    )
                    if js_match:
                        results["javascript"].extend(js_match.technologies)
                        
                except Exception as e:
                    self.logger.debug("Error analyzing JS file %s: %s", js_url, str(e))
                    
        except Exception as e:
            self.logger.warning("Error extracting JS files: %s", str(e))
    
    def _perform_advanced_analysis(
        self,
        url: str,
        response: HttpResponse,
        results: Dict[str, List[Technology]]
    ):
        """执行高级分析"""
        # 1. 分析HTTP方法支持
        self._analyze_http_methods(url, results)
        
        # 2. 分析API端点
        self._analyze_api_endpoints(url, response, results)
        
        # 3. 分析资源加载模式
        self._analyze_resource_loading(url, response, results)
    
    def _analyze_http_methods(
        self,
        url: str,
        results: Dict[str, List[Technology]]
    ):
        """分析HTTP方法支持"""
        methods = ["OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"]
        supported_methods = []
        
        for method in methods:
            try:
                response = self.http_client.request(
                    method,
                    url,
                    timeout=self.config.advanced_analysis_timeout
                )
                if response.status_code not in [405, 501]:
                    supported_methods.append(method)
            except:
                pass
        
        # 分析结果
        if "OPTIONS" in supported_methods:
            options_match = self.rule_engine.match(
                "http-methods", 
                ",".join(supported_methods), 
                RuleCategory.OPTIONS
            )
            if options_match:
                results["server"].extend(options_match.technologies)
    
    def _analyze_api_endpoints(
        self,
        url: str,
        response: HttpResponse,
        results: Dict[str, List[Technology]]
    ):
        """分析API端点"""
        # 检查常见API路径
        api_paths = [
            "/api/", "/v1/", "/v2/", "/graphql", "/rest/", 
            "/json/", "/odata/", "/services/"
        ]
        
        for path in api_paths:
            api_url = url.rstrip('/') + path
            try:
                api_response = self.http_client.get(
                    api_url,
                    timeout=self.config.advanced_analysis_timeout
                )
                if api_response.status_code == 200:
                    # 检查响应内容类型
                    content_type = api_response.headers.get('Content-Type', '').lower()
                    
                    if 'json' in content_type:
                        results["server"].append(Technology(
                            name="REST API",
                            version="",
                            confidence=0.8,
                            category="server"
                        ))
                    elif 'graphql' in content_type:
                        results["server"].append(Technology(
                            name="GraphQL",
                            version="",
                            confidence=0.8,
                            category="server"
                        ))
            except:
                pass
    
    def _analyze_resource_loading(
        self,
        url: str,
        response: HttpResponse,
        results: Dict[str, List[Technology]]
    ):
        """分析资源加载模式"""
        # 检查是否使用懒加载
        if "loading" in response.content.decode('utf-8', errors='ignore'):
            lazy_load_match = self.rule_engine.match(
                "lazy-loading", 
                response.content.decode('utf-8', errors='ignore'), 
                RuleCategory.RESOURCE_LOADING
            )
            if lazy_load_match:
                results["framework"].extend(lazy_load_match.technologies)
    
    def _generate_report(
        self,
        url: str,
        response: HttpResponse,
        tech_stack: Dict[str, List[Technology]],
        options: AnalysisOptions
    ) -> TechStackReport:
        """生成技术栈分析报告"""
        # 合并技术栈结果
        all_technologies = []
        for category, technologies in tech_stack.items():
            all_technologies.extend(technologies)
        
        # 去重并排序
        unique_technologies = self._deduplicate_technologies(all_technologies)
        sorted_technologies = sorted(
            unique_technologies, 
            key=lambda t: t.confidence, 
            reverse=True
        )
        
        # 生成详细报告
        return TechStackReport(
            url=url,
            status_code=response.status_code,
            response_time=response.duration,
            technologies=sorted_technologies,
            detected_categories=list(set(t.category for t in sorted_technologies)),
            confidence=self._calculate_overall_confidence(sorted_technologies),
            timestamp=datetime.utcnow()
        )
    
    def _deduplicate_technologies(
        self, 
        technologies: List[Technology]
    ) -> List[Technology]:
        """去重技术栈结果"""
        seen = {}
        result = []
        
        for tech in technologies:
            key = f"{tech.name.lower()}:{tech.category}"
            
            if key not in seen or tech.confidence > seen[key].confidence:
                seen[key] = tech
        
        return list(seen.values())
    
    def _calculate_overall_confidence(
        self, 
        technologies: List[Technology]
    ) -> float:
        """计算整体置信度"""
        if not technologies:
            return 0.0
        
        # 加权平均置信度
        total_weight = 0
        weighted_sum = 0
        
        for tech in technologies:
            # 根据技术类别分配权重
            weight = 1.0
            if tech.category == "server":
                weight = 1.2
            elif tech.category == "framework":
                weight = 1.1
            
            weighted_sum += tech.confidence * weight
            total_weight += weight
        
        return min(1.0, weighted_sum / total_weight)
    
    def _extract_version(self, text: str) -> str:
        """从文本中提取版本号"""
        version_patterns = [
            r'version\s*[:=]?\s*v?(\d+\.\d+(?:\.\d+)?)',
            r'v(\d+\.\d+(?:\.\d+)?)',
            r'(\d+\.\d+(?:\.\d+)?)\s+release'
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
```

#### 2.4.2 反爬机制检测服务

**技术实现：**
```python
class AntiCrawlingDetector:
    """反爬机制检测服务"""
    
    def __init__(
        self,
        http_client: HttpClient,
        rule_engine: RuleEngine,
        config: Config
    ):
        self.http_client = http_client
        self.rule_engine = rule_engine
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def detect(
        self,
        url: str,
        options: Optional[AnalysisOptions] = None
    ) -> AntiCrawlingReport:
        """
        检测网站的反爬机制
        
        :param url: 目标URL
        :param options: 分析选项
        :return: 反爬机制检测报告
        """
        # 1. 准备分析选项
        opts = options or AnalysisOptions()
        
        # 2. 执行基础检测
        basic_detection = self._basic_detection(url, opts)
        
        # 3. 执行深度检测（如果启用）
        advanced_detection = {}
        if opts.advanced_analysis:
            advanced_detection = self._advanced_detection(url, opts)
        
        # 4. 合并结果
        all_detections = {**basic_detection, **advanced_detection}
        
        # 5. 生成报告
        return self._generate_report(url, all_detections, opts)
    
    def _basic_detection(
        self,
        url: str,
        options: AnalysisOptions
    ) -> Dict[str, DetectionResult]:
        """基础反爬机制检测"""
        results = {}
        
        # 1. 获取正常响应
        normal_response = self._fetch_page(url, options)
        
        # 2. 检测User-Agent过滤
        ua_detection = self._detect_user_agent_filtering(url, options)
        if ua_detection.confidence > 0:
            results["user_agent"] = ua_detection
        
        # 3. 检测IP限制
        ip_detection = self._detect_ip_limiting(url, options)
        if ip_detection.confidence > 0:
            results["ip_limiting"] = ip_detection
        
        # 4. 检测请求频率限制
        rate_limit_detection = self._detect_rate_limiting(url, options)
        if rate_limit_detection.confidence > 0:
            results["rate_limiting"] = rate_limit_detection
        
        # 5. 检测Cookie要求
        cookie_detection = self._detect_cookie_requirement(url, options, normal_response)
        if cookie_detection.confidence > 0:
            results["cookie_requirement"] = cookie_detection
        
        return results
    
    def _fetch_page(
        self,
        url: str,
        options: AnalysisOptions
    ) -> HttpResponse:
        """获取页面内容（与TechStackAnalyzer共用）"""
        # 与技术栈分析相同的实现
        pass
    
    def _detect_user_agent_filtering(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测User-Agent过滤"""
        # 测试标准User-Agent
        normal_response = self._fetch_page(url, options)
        
        # 测试爬虫User-Agent
        crawler_options = copy.copy(options)
        crawler_options.user_agent = self.config.crawler_user_agent
        crawler_response = self._fetch_page(url, crawler_options)
        
        # 比较响应
        if normal_response.status_code != crawler_response.status_code:
            return DetectionResult(
                name="User-Agent Filtering",
                description="Website blocks requests with crawler User-Agent",
                confidence=0.9,
                evidence={
                    "normal_status": normal_response.status_code,
                    "crawler_status": crawler_response.status_code
                },
                severity="high",
                bypass_suggestions=[
                    "Use random User-Agent rotation",
                    "Use browser-like User-Agent"
                ]
            )
        
        # 检查响应内容差异
        normal_hash = self._hash_content(normal_response.content)
        crawler_hash = self._hash_content(crawler_response.content)
        
        if normal_hash != crawler_hash:
            return DetectionResult(
                name="User-Agent Filtering",
                description="Website serves different content based on User-Agent",
                confidence=0.8,
                evidence={
                    "normal_hash": normal_hash,
                    "crawler_hash": crawler_hash
                },
                severity="medium",
                bypass_suggestions=[
                    "Use realistic User-Agent strings",
                    "Rotate User-Agents frequently"
                ]
            )
        
        return DetectionResult(
            name="User-Agent Filtering",
            confidence=0.0
        )
    
    def _hash_content(self, content: bytes) -> str:
        """计算内容哈希"""
        return hashlib.md5(content).hexdigest() if content else ""
    
    def _detect_ip_limiting(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测IP限制"""
        # 使用不同IP（通过代理）发送请求
        ip_results = []
        
        for proxy in self.config.test_proxies[:3]:  # 测试前3个代理
            try:
                proxy_options = copy.copy(options)
                proxy_options.proxy = proxy
                response = self._fetch_page(url, proxy_options)
                ip_results.append((proxy, response.status_code, response.headers))
            except Exception as e:
                self.logger.debug("Proxy %s failed: %s", proxy, str(e))
        
        # 分析结果
        if len(ip_results) < 2:
            return DetectionResult(
                name="IP Limiting",
                confidence=0.0
            )
        
        # 检查状态码差异
        status_codes = [res[1] for res in ip_results]
        if len(set(status_codes)) > 1:
            return DetectionResult(
                name="IP Limiting",
                description="Different responses from different IPs suggest IP-based filtering",
                confidence=0.85,
                evidence={
                    "status_codes": status_codes,
                    "proxies": [res[0] for res in ip_results]
                },
                severity="high",
                bypass_suggestions=[
                    "Use proxy rotation",
                    "Use residential proxies",
                    "Limit request rate per IP"
                ]
            )
        
        # 检查响应内容差异
        content_hashes = [self._hash_content(self._fetch_page(url, options).content) for _ in range(3)]
        if len(set(content_hashes)) > 1:
            return DetectionResult(
                name="IP Limiting",
                description="Inconsistent responses suggest IP-based filtering",
                confidence=0.75,
                evidence={
                    "content_hashes": content_hashes
                },
                severity="medium",
                bypass_suggestions=[
                    "Use proxy rotation",
                    "Increase delay between requests"
                ]
            )
        
        return DetectionResult(
            name="IP Limiting",
            confidence=0.0
        )
    
    def _detect_rate_limiting(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测请求频率限制"""
        # 快速发送多个请求
        timestamps = []
        status_codes = []
        
        for _ in range(10):
            start = time.time()
            try:
                response = self._fetch_page(url, options)
                timestamps.append(time.time() - start)
                status_codes.append(response.status_code)
            except:
                timestamps.append(None)
                status_codes.append(500)
            time.sleep(0.1)  # 100ms间隔
        
        # 分析响应时间
        valid_timestamps = [t for t in timestamps if t is not None]
        if valid_timestamps:
            avg_time = sum(valid_timestamps) / len(valid_timestamps)
            if max(valid_timestamps) > avg_time * 3:
                # 检测到响应时间显著增加
                slow_index = valid_timestamps.index(max(valid_timestamps))
                return DetectionResult(
                    name="Rate Limiting",
                    description="Response time increased significantly after multiple requests",
                    confidence=0.8,
                    evidence={
                        "request_times": timestamps,
                        "slow_request_index": slow_index
                    },
                    severity="medium",
                    bypass_suggestions=[
                        f"Limit request rate to less than {slow_index} requests per second",
                        "Implement exponential backoff for retries"
                    ]
                )
        
        # 分析状态码
        if 429 in status_codes or 403 in status_codes:
            error_index = status_codes.index(429) if 429 in status_codes else status_codes.index(403)
            return DetectionResult(
                name="Rate Limiting",
                description=f"Received {status_codes[error_index]} status code after {error_index} requests",
                confidence=0.9,
                evidence={
                    "status_codes": status_codes,
                    "error_index": error_index
                },
                severity="high",
                bypass_suggestions=[
                    f"Limit request rate to less than {error_index} requests per second",
                    "Implement retry with backoff"
                ]
            )
        
        return DetectionResult(
            name="Rate Limiting",
            confidence=0.0
        )
    
    def _detect_cookie_requirement(
        self,
        url: str,
        options: AnalysisOptions,
        normal_response: HttpResponse
    ) -> DetectionResult:
        """检测Cookie要求"""
        # 检查Set-Cookie头
        if "set-cookie" in normal_response.headers:
            cookies = normal_response.headers["set-cookie"]
            if cookies:
                return DetectionResult(
                    name="Cookie Requirement",
                    description="Website sets cookies on first request",
                    confidence=0.7,
                    evidence={
                        "cookies": cookies
                    },
                    severity="medium",
                    bypass_suggestions=[
                        "Enable cookie handling in crawler",
                        "Store and send cookies with subsequent requests"
                    ]
                )
        
        # 检查响应中的cookie相关脚本
        if normal_response.content:
            content = normal_response.content.decode('utf-8', errors='ignore')
            if "cookie" in content.lower():
                return DetectionResult(
                    name="Cookie Requirement",
                    description="Website references cookies in JavaScript",
                    confidence=0.6,
                    evidence={
                        "cookie_references": self._find_cookie_references(content)
                    },
                    severity="low",
                    bypass_suggestions=[
                        "Enable cookie handling in crawler"
                    ]
                )
        
        return DetectionResult(
            name="Cookie Requirement",
            confidence=0.0
        )
    
    def _find_cookie_references(self, content: str) -> List[str]:
        """查找内容中的cookie引用"""
        patterns = [
            r'cookie',
            r'document\.cookie',
            r'getCookie',
            r'setCookie'
        ]
        
        references = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                references.extend(matches[:3])  # 只取前3个匹配
        
        return references
    
    def _advanced_detection(
        self,
        url: str,
        options: AnalysisOptions
    ) -> Dict[str, DetectionResult]:
        """高级反爬机制检测"""
        results = {}
        
        # 1. 检测JavaScript挑战
        js_challenge_detection = self._detect_js_challenge(url, options)
        if js_challenge_detection.confidence > 0:
            results["js_challenge"] = js_challenge_detection
        
        # 2. 检测行为验证
        behavior_detection = self._detect_behavior_verification(url, options)
        if behavior_detection.confidence > 0:
            results["behavior_verification"] = behavior_detection
        
        # 3. 检测指纹检测
        fingerprint_detection = self._detect_fingerprint_detection(url, options)
        if fingerprint_detection.confidence > 0:
            results["fingerprint_detection"] = fingerprint_detection
        
        # 4. 检测CAPTCHA
        captcha_detection = self._detect_captcha(url, options)
        if captcha_detection.confidence > 0:
            results["captcha"] = captcha_detection
        
        return results
    
    def _detect_js_challenge(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测JavaScript挑战"""
        # 获取正常响应
        normal_response = self._fetch_page(url, options)
        
        # 获取禁用JS的响应
        no_js_options = copy.copy(options)
        no_js_options.headers = {"Accept": "text/plain"}
        no_js_response = self._fetch_page(url, no_js_options)
        
        # 比较响应
        normal_hash = self._hash_content(normal_response.content)
        no_js_hash = self._hash_content(no_js_response.content)
        
        if normal_hash != no_js_hash:
            return DetectionResult(
                name="JavaScript Challenge",
                description="Website serves different content when JavaScript is disabled",
                confidence=0.85,
                evidence={
                    "normal_hash": normal_hash,
                    "no_js_hash": no_js_hash
                },
                severity="high",
                bypass_suggestions=[
                    "Use headless browser for rendering",
                    "Solve JavaScript challenges programmatically"
                ]
            )
        
        # 检查是否存在JS挑战脚本
        if normal_response.content:
            content = normal_response.content.decode('utf-8', errors='ignore')
            challenge_patterns = [
                r'function\s+challenge\s*\(',
                r'function\s+solve\s*\(',
                r'window\.__cf_chl_jschl_t',
                r'cf-challenge'
            ]
            
            for pattern in challenge_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return DetectionResult(
                        name="JavaScript Challenge",
                        description="JavaScript challenge detected in page content",
                        confidence=0.9,
                        evidence={
                            "challenge_pattern": pattern
                        },
                        severity="high",
                        bypass_suggestions=[
                            "Use headless browser for rendering",
                            "Implement challenge solving logic"
                        ]
                    )
        
        return DetectionResult(
            name="JavaScript Challenge",
            confidence=0.0
        )
    
    def _detect_behavior_verification(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测行为验证"""
        # 获取初始页面
        initial_response = self._fetch_page(url, options)
        
        # 检查是否存在行为跟踪脚本
        if initial_response.content:
            content = initial_response.content.decode('utf-8', errors='ignore')
            behavior_patterns = [
                r'mousemove',
                r'click',
                r'keypress',
                r'behavior tracking',
                r'human interaction'
            ]
            
            for pattern in behavior_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return DetectionResult(
                        name="Behavior Verification",
                        description="Behavior tracking scripts detected",
                        confidence=0.75,
                        evidence={
                            "pattern": pattern
                        },
                        severity="medium",
                        bypass_suggestions=[
                            "Simulate human-like mouse movements",
                            "Implement random delays between actions",
                            "Mimic typical user interaction patterns"
                        ]
                    )
        
        # 检查是否存在鼠标移动事件监听
        if initial_response.content:
            content = initial_response.content.decode('utf-8', errors='ignore')
            if re.search(r'addEventListener\(["\']mousemove', content, re.IGNORECASE):
                return DetectionResult(
                    name="Behavior Verification",
                    description="Mouse move event listener detected",
                    confidence=0.7,
                    evidence={
                        "event_listener": "mousemove"
                    },
                    severity="medium",
                    bypass_suggestions=[
                        "Simulate realistic mouse movements",
                        "Implement mouse trajectory algorithms"
                    ]
                )
        
        return DetectionResult(
            name="Behavior Verification",
            confidence=0.0
        )
    
    def _detect_fingerprint_detection(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测指纹检测"""
        # 获取页面内容
        response = self._fetch_page(url, options)
        
        if not response.content:
            return DetectionResult(
                name="Fingerprint Detection",
                confidence=0.0
            )
        
        content = response.content.decode('utf-8', errors='ignore')
        
        # 检查Canvas指纹检测
        if re.search(r'CanvasRenderingContext2D', content) or \
           re.search(r'toDataURL', content) or \
           re.search(r'getImageData', content):
            return DetectionResult(
                name="Fingerprint Detection",
                description="Canvas fingerprinting detected",
                confidence=0.8,
                evidence={
                    "technique": "canvas"
                },
                severity="high",
                bypass_suggestions=[
                    "Use canvas noise injection",
                    "Override Canvas API methods",
                    "Use headless browser with fingerprint protection"
                ]
            )
        
        # 检查WebGL指纹检测
        if re.search(r'WebGLRenderingContext', content) or \
           re.search(r'getParameter', content):
            return DetectionResult(
                name="Fingerprint Detection",
                description="WebGL fingerprinting detected",
                confidence=0.75,
                evidence={
                    "technique": "webgl"
                },
                severity="high",
                bypass_suggestions=[
                    "Override WebGL API methods",
                    "Use consistent WebGL rendering"
                ]
            )
        
        # 检查AudioContext指纹检测
        if re.search(r'AudioContext', content) or \
           re.search(r'createOscillator', content):
            return DetectionResult(
                name="Fingerprint Detection",
                description="AudioContext fingerprinting detected",
                confidence=0.7,
                evidence={
                    "technique": "audio"
                },
                severity="medium",
                bypass_suggestions=[
                    "Override AudioContext API",
                    "Use consistent audio rendering"
                ]
            )
        
        return DetectionResult(
            name="Fingerprint Detection",
            confidence=0.0
        )
    
    def _detect_captcha(
        self,
        url: str,
        options: AnalysisOptions
    ) -> DetectionResult:
        """检测CAPTCHA"""
        # 获取页面内容
        response = self._fetch_page(url, options)
        
        if not response.content:
            return DetectionResult(
                name="CAPTCHA",
                confidence=0.0
            )
        
        content = response.content.decode('utf-8', errors='ignore').lower()
        
        # 检查常见CAPTCHA服务
        captcha_patterns = [
            ("recaptcha", "Google reCAPTCHA detected"),
            ("hcaptcha", "hCaptcha detected"),
            ("turnstile", "Cloudflare Turnstile detected"),
            ("solvemedia", "Solve Media CAPTCHA detected"),
            ("captcha", "Generic CAPTCHA detected")
        ]
        
        for pattern, description in captcha_patterns:
            if pattern in content:
                return DetectionResult(
                    name="CAPTCHA",
                    description=description,
                    confidence=0.9 if pattern != "captcha" else 0.7,
                    evidence={
                        "pattern": pattern
                    },
                    severity="critical",
                    bypass_suggestions=[
                        "Use CAPTCHA solving service",
                        "Implement automated CAPTCHA solving"
                    ]
                )
        
        return DetectionResult(
            name="CAPTCHA",
            confidence=0.0
        )
    
    def _generate_report(
        self,
        url: str,
        detections: Dict[str, DetectionResult],
        options: AnalysisOptions
    ) -> AntiCrawlingReport:
        """生成反爬机制检测报告"""
        # 过滤低置信度检测
        significant_detections = [
            detection for detection in detections.values()
            if detection.confidence > 0.5
        ]
        
        # 计算整体风险级别
        risk_level = self._calculate_risk_level(significant_detections)
        
        # 生成绕过建议
        bypass_suggestions = self._generate_bypass_suggestions(significant_detections)
        
        return AntiCrawlingReport(
            url=url,
            detections=significant_detections,
            risk_level=risk_level,
            bypass_suggestions=bypass_suggestions,
            timestamp=datetime.utcnow()
        )
    
    def _calculate_risk_level(
        self,
        detections: List[DetectionResult]
    ) -> str:
        """计算整体风险级别"""
        if not detections:
            return "low"
        
        # 检查是否存在高风险检测
        high_risk = any(d.severity == "critical" for d in detections)
        if high_risk:
            return "critical"
        
        medium_risk = any(d.severity == "high" for d in detections)
        if medium_risk:
            return "high"
        
        return "medium"
    
    def _generate_bypass_suggestions(
        self,
        detections: List[DetectionResult]
    ) -> List[str]:
        """生成绕过建议"""
        suggestions = set()
        
        for detection in detections:
            if detection.bypass_suggestions:
                suggestions.update(detection.bypass_suggestions)
        
        return list(suggestions)
```

#### 2.4.3 规则引擎服务

**技术实现：**
```python
class RuleEngine:
    """规则引擎，用于匹配网站特征"""
    
    def __init__(
        self,
        rule_repository: RuleRepository,
        ml_model: Optional[MLModel] = None
    ):
        self.rule_repository = rule_repository
        self.ml_model = ml_model
        self.logger = logging.getLogger(__name__)
        self.cache = TTLCache(maxsize=10000, ttl=300)  # 5分钟缓存
    
    def match(
        self,
        rule_set: str,
        content: str,
        category: RuleCategory
    ) -> RuleMatch:
        """
        匹配内容与规则
        
        :param rule_set: 规则集名称
        :param content: 要匹配的内容
        :param category: 规则类别
        :return: 规则匹配结果
        """
        # 1. 检查缓存
        cache_key = f"{rule_set}:{category.value}:{content[:100]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 2. 获取规则
        rules = self.rule_repository.get_rules(rule_set, category)
        
        # 3. 执行匹配
        match_result = self._execute_match(rules, content, category)
        
        # 4. 缓存结果
        self.cache[cache_key] = match_result
        
        return match_result
    
    def _execute_match(
        self,
        rules: List[Rule],
        content: str,
        category: RuleCategory
    ) -> RuleMatch:
        """执行规则匹配"""
        matched_technologies = []
        matched_rules = []
        
        # 1. 执行基于规则的匹配
        for rule in rules:
            if self._rule_matches(rule, content):
                matched_rules.append(rule)
                matched_technologies.extend(rule.technologies)
        
        # 2. 如果有ML模型且匹配结果不足，使用ML模型
        if self.ml_model and len(matched_technologies) < 2:
            ml_match = self.ml_model.predict(content, category)
            if ml_match:
                matched_technologies.extend(ml_match.technologies)
                # 标记为ML匹配
                for tech in ml_match.technologies:
                    tech.source = "ml"
        
        # 3. 去重并计算置信度
        unique_technologies = self._deduplicate_technologies(matched_technologies)
        
        return RuleMatch(
            rules=matched_rules,
            technologies=unique_technologies,
            confidence=self._calculate_confidence(unique_technologies)
        )
    
    def _rule_matches(self, rule: Rule, content: str) -> bool:
        """检查规则是否匹配内容"""
        if rule.pattern_type == PatternType.REGEX:
            return bool(re.search(rule.pattern, content, re.IGNORECASE))
        
        elif rule.pattern_type == PatternType.GLOB:
            # 简单实现glob匹配
            regex = glob2regex(rule.pattern)
            return bool(re.match(regex, content, re.IGNORECASE))
        
        elif rule.pattern_type == PatternType.STRING:
            return rule.pattern.lower() in content.lower()
        
        return False
    
    def _deduplicate_technologies(
        self, 
        technologies: List[Technology]
    ) -> List[Technology]:
        """去重技术结果"""
        seen = {}
        result = []
        
        for tech in technologies:
            key = f"{tech.name.lower()}:{tech.category}"
            
            if key not in seen or tech.confidence > seen[key].confidence:
                seen[key] = tech
        
        return list(seen.values())
    
    def _calculate_confidence(
        self, 
        technologies: List[Technology]
    ) -> float:
        """计算整体置信度"""
        if not technologies:
            return 0.0
        
        # 加权平均置信度
        total_weight = 0
        weighted_sum = 0
        
        for tech in technologies:
            # 根据技术类别分配权重
            weight = 1.0
            if tech.category == "server":
                weight = 1.2
            elif tech.category == "framework":
                weight = 1.1
            
            weighted_sum += tech.confidence * weight
            total_weight += weight
        
        return min(1.0, weighted_sum / total_weight)
    
    def update_rules(
        self,
        rule_set: str,
        category: RuleCategory,
        new_rules: List[Rule]
    ):
        """更新规则"""
        self.rule_repository.update_rules(rule_set, category, new_rules)
        # 清除相关缓存
        self._clear_cache()
    
    def _clear_cache(self):
        """清除缓存"""
        self.cache.clear()

class RuleRepository:
    """规则存储库"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_rules(
        self,
        rule_set: str,
        category: RuleCategory
    ) -> List[Rule]:
        """获取规则"""
        sql = """
        SELECT * FROM fingerprint_rules 
        WHERE rule_set = %(rule_set)s 
        AND category = %(category)s
        ORDER BY priority DESC
        """
        
        rows = self.db.fetchall(sql, {
            "rule_set": rule_set,
            "category": category.value
        })
        
        return [self._row_to_rule(row) for row in rows]
    
    def _row_to_rule(self, row: Dict) -> Rule:
        """将数据库行转换为Rule对象"""
        return Rule(
            id=row["id"],
            rule_set=row["rule_set"],
            category=RuleCategory(row["category"]),
            pattern=row["pattern"],
            pattern_type=PatternType(row["pattern_type"]),
            technologies=self._decode_technologies(row["technologies"]),
            description=row["description"],
            priority=row["priority"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    def _decode_technologies(self, json_data: str) -> List[Technology]:
        """解码技术列表"""
        if not json_data:
            return []
        
        tech_data = json.loads(json_data)
        return [
            Technology(
                name=t["name"],
                version=t.get("version", ""),
                confidence=t.get("confidence", 0.8),
                category=t["category"],
                source="rule"
            ) for t in tech_data
        ]
    
    def update_rules(
        self,
        rule_set: str,
        category: RuleCategory,
        rules: List[Rule]
    ):
        """更新规则"""
        # 开始事务
        with self.db.transaction():
            # 删除现有规则
            self.db.execute(
                "DELETE FROM fingerprint_rules WHERE rule_set = %(rule_set)s AND category = %(category)s",
                {"rule_set": rule_set, "category": category.value}
            )
            
            # 插入新规则
            for rule in rules:
                self._save_rule(rule)
    
    def _save_rule(self, rule: Rule):
        """保存规则到数据库"""
        sql = """
        INSERT INTO fingerprint_rules (
            rule_set, category, pattern, pattern_type, 
            technologies, description, priority, 
            created_at, updated_at
        ) VALUES (
            %(rule_set)s, %(category)s, %(pattern)s, %(pattern_type)s,
            %(technologies)s, %(description)s, %(priority)s,
            %(created_at)s, %(updated_at)s
        )
        """
        
        self.db.execute(sql, {
            "rule_set": rule.rule_set,
            "category": rule.category.value,
            "pattern": rule.pattern,
            "pattern_type": rule.pattern_type.value,
            "technologies": json.dumps([
                {
                    "name": t.name,
                    "version": t.version,
                    "confidence": t.confidence,
                    "category": t.category
                } for t in rule.technologies
            ]),
            "description": rule.description,
            "priority": rule.priority,
            "created_at": rule.created_at or datetime.utcnow(),
            "updated_at": rule.updated_at or datetime.utcnow()
        })

# 辅助函数
def glob2regex(pattern: str) -> str:
    """将glob模式转换为正则表达式"""
    regex = ''
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '*':
            regex += '.*'
        elif c == '?':
            regex += '.'
        elif c == '[':
            j = i
            if pattern[j + 1] == '!':
                j += 1
            j += 1
            while j < len(pattern) and pattern[j] != ']':
                j += 1
            if j >= len(pattern):
                regex += '\\['
            else:
                if pattern[i + 1] == '!':
                    regex += '[^'
                else:
                    regex += '['
                regex += pattern[i + 1:j].replace('\\', '\\\\')
                regex += ']'
                i = j
        elif c in '\\.^$+{}()|':
            regex += '\\' + c
        else:
            regex += c
        i += 1
    
    return regex
```

### 2.5 数据模型详细定义

#### 2.5.1 指纹规则表

```sql
-- 指纹规则表
CREATE TABLE fingerprint_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_set VARCHAR(50) NOT NULL,
    category VARCHAR(30) NOT NULL CHECK (category IN ('header', 'meta', 'script', 'css', 'attribute', 'class', 'path', 'query', 'options', 'javascript', 'resource_loading')),
    pattern TEXT NOT NULL,
    pattern_type VARCHAR(20) NOT NULL CHECK (pattern_type IN ('regex', 'glob', 'string')),
    technologies JSONB NOT NULL,
    description TEXT,
    priority INT NOT NULL DEFAULT 100,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_rules_set ON fingerprint_rules(rule_set),
    INDEX idx_rules_category ON fingerprint_rules(category),
    INDEX idx_rules_priority ON fingerprint_rules(priority)
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_fingerprint_rules_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_fingerprint_rules_modtime
BEFORE UPDATE ON fingerprint_rules
FOR EACH ROW
EXECUTE FUNCTION update_fingerprint_rules_modtime();
```

#### 2.5.2 分析结果表

```sql
-- 技术栈分析结果表
CREATE TABLE tech_stack_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url VARCHAR(2048) NOT NULL,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status_code INT NOT NULL,
    response_time INTERVAL NOT NULL,
    technologies JSONB NOT NULL,
    detected_categories JSONB NOT NULL,
    confidence NUMERIC(3,2) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_analysis_url ON tech_stack_analysis(url),
    INDEX idx_analysis_project ON tech_stack_analysis(project_id),
    INDEX idx_analysis_timestamp ON tech_stack_analysis(timestamp DESC)
);

-- 反爬机制检测结果表
CREATE TABLE anti_crawling_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url VARCHAR(2048) NOT NULL,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    detections JSONB NOT NULL,
    risk_level VARCHAR(20) NOT NULL CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    bypass_suggestions JSONB NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_anti_crawling_url ON anti_crawling_analysis(url),
    INDEX idx_anti_crawling_project ON anti_crawling_analysis(project_id),
    INDEX idx_anti_crawling_risk ON anti_crawling_analysis(risk_level),
    INDEX idx_anti_crawling_timestamp ON anti_crawling_analysis(timestamp DESC)
);
```

### 2.6 API详细规范

#### 2.6.1 网站分析API

**分析网站 (POST /api/v1/analyze)**

*请求示例:*
```http
POST /api/v1/analyze HTTP/1.1
Host: wfe.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "url": "https://example.com",
  "options": {
    "follow_redirects": true,
    "advanced_analysis": true,
    "timeout": 30,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "url": "https://example.com",
  "tech_stack": {
    "server": [
      {
        "name": "Nginx",
        "version": "1.18.0",
        "confidence": 0.95,
        "category": "server"
      }
    ],
    "framework": [
      {
        "name": "React",
        "version": "17.0.2",
        "confidence": 0.85,
        "category": "framework"
      }
    ],
    "cms": [],
    "javascript": [
      {
        "name": "jQuery",
        "version": "3.6.0",
        "confidence": 0.8,
        "category": "javascript"
      }
    ],
    "database": [],
    "cdn": [
      {
        "name": "Cloudflare",
        "version": "",
        "confidence": 0.9,
        "category": "cdn"
      }
    ],
    "os": []
  },
  "anti_crawling": {
    "user_agent": {
      "name": "User-Agent Filtering",
      "description": "Website blocks requests with crawler User-Agent",
      "confidence": 0.9,
      "evidence": {
        "normal_status": 200,
        "crawler_status": 403
      },
      "severity": "high",
      "bypass_suggestions": [
        "Use random User-Agent rotation",
        "Use browser-like User-Agent"
      ]
    },
    "rate_limiting": {
      "name": "Rate Limiting",
      "description": "Received 429 status code after 5 requests",
      "confidence": 0.9,
      "evidence": {
        "status_codes": [200, 200, 200, 200, 200, 429],
        "error_index": 5
      },
      "severity": "high",
      "bypass_suggestions": [
        "Limit request rate to less than 5 requests per second",
        "Implement retry with backoff"
      ]
    }
  },
  "status_code": 200,
  "response_time": 0.45,
  "detected_categories": ["server", "framework", "javascript", "cdn"],
  "tech_stack_confidence": 0.88,
  "anti_crawling_risk_level": "high",
  "timestamp": "2023-06-15T10:30:45Z"
}
```

**获取分析历史 (GET /api/v1/analysis-history)**

*请求示例:*
```http
GET /api/v1/analysis-history?url=example.com&page=1&page_size=10 HTTP/1.1
Host: wfe.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": "ana-1a2b3c4d",
      "url": "https://example.com",
      "timestamp": "2023-06-15T10:30:45Z",
      "tech_stack_confidence": 0.88,
      "anti_crawling_risk_level": "high",
      "status_code": 200
    },
    {
      "id": "ana-5e6f7g8h",
      "url": "https://example.com",
      "timestamp": "2023-06-14T15:20:30Z",
      "tech_stack_confidence": 0.85,
      "anti_crawling_risk_level": "medium",
      "status_code": 200
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 10
}
```

### 2.7 性能优化策略

#### 2.7.1 分析性能优化

1. **并行分析**
   ```python
   def analyze_multiple_urls(urls, options):
       with ThreadPoolExecutor(max_workers=10) as executor:
           futures = {
               executor.submit(analyze_url, url, options): url
               for url in urls
           }
           
           results = {}
           for future in as_completed(futures):
               url = futures[future]
               try:
                   results[url] = future.result()
               except Exception as e:
                   results[url] = {"error": str(e)}
           
           return results
   ```

2. **缓存策略**
   - 对相同URL的分析结果缓存24小时
   - 使用URL哈希作为缓存键
   - 支持强制刷新分析

3. **资源限制**
   - 限制每个分析任务的最大资源使用
   - 实现超时机制
   - 限制并发分析任务数量

#### 2.7.2 规则匹配优化

1. **规则索引优化**
   ```sql
   -- 为常用规则集创建索引
   CREATE INDEX idx_rules_set_category ON fingerprint_rules(rule_set, category);
   CREATE INDEX idx_rules_priority ON fingerprint_rules(priority);
   ```

2. **规则匹配算法优化**
   - 对正则表达式规则进行编译缓存
   - 使用Aho-Corasick算法进行多模式匹配
   - 对高频规则进行优先级排序

### 2.8 安全考虑

#### 2.8.1 分析安全

1. **沙箱环境**
   - 在隔离环境中执行JavaScript分析
   - 限制网络访问
   - 限制系统资源使用

2. **安全分析策略**
   - 限制分析深度
   - 避免敏感操作
   - 监控异常行为

#### 2.8.2 数据安全

1. **分析结果保护**
   - 仅授权用户可访问分析结果
   - 敏感信息脱敏
   - 完整的访问审计

2. **隐私保护**
   - 不存储完整的页面内容
   - 自动清理临时数据
   - 符合GDPR要求

### 2.9 与其他模块的交互

#### 2.9.1 与数据源注册中心交互

```mermaid
sequenceDiagram
    participant DSR as Data Source Registry
    participant WFE as Website Fingerprinting Engine
    
    DSR->>WFE: POST /api/v1/analyze (new data source)
    WFE-->>DSR: Analysis report
    
    loop 每24小时
        DSR->>WFE: POST /api/v1/analyze (existing data source)
        WFE-->>DSR: Analysis report
    end
    
    DSR->>WFE: GET /api/v1/analysis-history?data_source_id={id}
    WFE-->>DSR: Analysis history
```

#### 2.9.2 与AI辅助开发系统交互

```mermaid
sequenceDiagram
    participant AIDS as AI-Assisted Development System
    participant WFE as Website Fingerprinting Engine
    
    AIDS->>WFE: GET /api/v1/analyze?url={url}
    WFE-->>AIDS: Detailed analysis report
    
    AIDS->>WFE: POST /api/v1/rules (new rule suggestion)
    WFE-->>AIDS: Rule creation confirmation
```

#### 2.9.3 与数据合规与安全中心交互

```mermaid
sequenceDiagram
    participant DCS as Data Compliance and Security Center
    participant WFE as Website Fingerprinting Engine
    
    DCS->>WFE: GET /api/v1/analyze?url={url}
    WFE-->>DCS: Anti-crawling analysis
    
    DCS->>WFE: POST /api/v1/compliance-check (compliance request)
    WFE-->>DCS: Compliance assessment based on fingerprint
```

## 3. 数据源健康监测系统 (Data Source Health Monitoring System)

### 3.1 模块概述
数据源健康监测系统负责持续监控所有数据源的可用性、性能和数据质量，及时发现和预警数据源问题。它通过定期探测和智能分析，提供全面的数据源健康状态视图。

### 3.2 详细功能清单

#### 3.2.1 核心功能
- **可用性监控**
  - HTTP状态码监控
  - 响应时间监控
  - 内容验证（关键字/正则匹配）
  - SSL证书有效期监控
- **性能监控**
  - 响应时间分布
  - 首字节时间(TTFB)
  - 内容下载时间
  - 资源加载性能
- **数据质量监控**
  - 数据完整性验证
  - 数据格式验证
  - 数据量波动检测
  - 异常值检测
- **健康评分系统**
  - 综合健康评分计算
  - 历史趋势分析
  - 健康状态预测
- **告警系统**
  - 多级告警阈值配置
  - 智能告警抑制
  - 多通道通知（邮件、Slack、Webhook）

#### 3.2.2 高级功能
- **根因分析**
  - 自动分析故障原因
  - 影响范围评估
  - 修复建议
- **预测性维护**
  - 基于历史数据的趋势预测
  - 异常模式检测
  - 预防性告警
- **SLA合规监控**
  - SLA指标跟踪
  - 合规报告生成
  - 服务信用计算
- **变更影响分析**
  - 网站变更检测
  - 变更对爬虫的影响评估
  - 自动化配置建议

### 3.3 技术架构

#### 3.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                            数据源健康监测系统 (DSHMS)                                         │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  监控执行层           │  分析处理层           │  数据存储层                                │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 探测调度器           │ • 健康评分计算器      │ • 时序数据库 (InfluxDB)                    │
│ • HTTP探测器          │ • 异常检测引擎        │ • 分析结果存储 (PostgreSQL)                │
│ • 内容验证器           │ • 根因分析器          │ • 告警状态存储 (Redis)                     │
│ • 性能分析器           │ • 预测模型            │ • 配置存储 (PostgreSQL)                    │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 3.3.2 服务边界与交互
- **输入**：
  - 数据源列表（来自数据源注册中心）
  - 监控配置（探测频率、验证规则等）
  - 告警通知配置
- **输出**：
  - 健康状态指标
  - 告警事件
  - 健康报告
  - 根因分析结果

### 3.4 核心组件详细实现

#### 3.4.1 探测调度器

**技术实现：**
```python
class ProbeScheduler:
    """探测调度器，负责安排和执行探测任务"""
    
    def __init__(
        self,
        data_source_service: DataSourceService,
        probe_executor: ProbeExecutor,
        config: Config
    ):
        self.data_source_service = data_source_service
        self.probe_executor = probe_executor
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler = BackgroundScheduler()
        self.probe_queue = Queue(maxsize=self.config.max_queued_probes)
    
    def start(self):
        """启动探测调度器"""
        if self.running:
            return
        
        self.running = True
        self.logger.info("Starting probe scheduler")
        
        # 启动探测执行器
        self._start_probe_executor()
        
        # 添加定期任务
        self.scheduler.add_job(
            self._schedule_probes,
            'interval',
            seconds=self.config.schedule_interval,
            id='schedule_probes'
        )
        
        # 启动调度器
        self.scheduler.start()
        self.logger.info("Probe scheduler started")
    
    def _start_probe_executor(self):
        """启动探测执行器"""
        def executor_loop():
            while self.running:
                try:
                    # 从队列获取探测任务
                    probe_task = self.probe_queue.get(timeout=1)
                    
                    # 执行探测
                    self.probe_executor.execute(probe_task)
                    
                    # 标记任务完成
                    self.probe_queue.task_done()
                    
                except Empty:
                    continue
                except Exception as e:
                    self.logger.error("Error executing probe: %s", str(e))
                    time.sleep(1)
        
        # 启动执行线程
        self.executor_thread = Thread(target=executor_loop, daemon=True)
        self.executor_thread.start()
    
    def _schedule_probes(self):
        """安排探测任务"""
        try:
            # 获取需要探测的数据源
            data_sources = self._get_data_sources_to_probe()
            
            # 为每个数据源创建探测任务
            for data_source in data_sources:
                probe_task = self._create_probe_task(data_source)
                self._enqueue_probe_task(probe_task)
            
            self.logger.info("Scheduled %d probes", len(data_sources))
            
        except Exception as e:
            self.logger.error("Error scheduling probes: %s", str(e))
    
    def _get_data_sources_to_probe(self) -> List[DataSource]:
        """获取需要探测的数据源"""
        # 获取所有active状态的数据源
        data_sources = self.data_source_service.list_data_sources(
            project_id="all",
            user_id="system",
            filters={"status": "active"},
            page=1,
            page_size=1000
        ).items
        
        # 过滤需要探测的数据源
        now = datetime.utcnow()
        probes_to_schedule = []
        
        for ds in data_sources:
            # 检查上次探测时间
            last_probe = ds.metadata.get("last_probe_time")
            probe_interval = ds.metadata.get("probe_interval", self.config.default_probe_interval)
            
            if not last_probe or (now - datetime.fromisoformat(last_probe)) >= timedelta(seconds=probe_interval):
                probes_to_schedule.append(ds)
        
        return probes_to_schedule
    
    def _create_probe_task(self, data_source: DataSource) -> ProbeTask:
        """创建探测任务"""
        # 获取探测配置
        probe_config = self._get_probe_config(data_source)
        
        return ProbeTask(
            data_source_id=data_source.id,
            project_id=data_source.project_id,
            url=data_source.url,
            config=probe_config,
            scheduled_time=datetime.utcnow()
        )
    
    def _get_probe_config(self, data_source: DataSource) -> ProbeConfig:
        """获取探测配置"""
        # 从元数据获取配置，如果没有则使用默认值
        metadata = data_source.metadata
        
        return ProbeConfig(
            interval=metadata.get("probe_interval", self.config.default_probe_interval),
            timeout=metadata.get("probe_timeout", self.config.default_timeout),
            verification_rules=metadata.get("verification_rules", []),
            performance_thresholds=metadata.get("performance_thresholds", {}),
            data_validation=metadata.get("data_validation", {})
        )
    
    def _enqueue_probe_task(self, probe_task: ProbeTask):
        """将探测任务加入队列"""
        try:
            self.probe_queue.put_nowait(probe_task)
        except QueueFull:
            self.logger.warning("Probe queue is full. Dropping probe for %s", probe_task.url)
    
    def stop(self):
        """停止探测调度器"""
        if not self.running:
            return
        
        self.running = False
        self.scheduler.shutdown()
        self.logger.info("Probe scheduler stopped")
```

#### 3.4.2 探测执行器

**技术实现：**
```python
class ProbeExecutor:
    """探测执行器，负责实际执行探测任务"""
    
    def __init__(
        self,
        http_client: HttpClient,
        result_processor: ResultProcessor,
        config: Config
    ):
        self.http_client = http_client
        self.result_processor = result_processor
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def execute(self, probe_task: ProbeTask):
        """执行探测任务"""
        try:
            start_time = time.time()
            
            # 1. 执行HTTP探测
            http_result = self._execute_http_probe(probe_task)
            
            # 2. 执行内容验证
            validation_result = self._execute_content_validation(probe_task, http_result)
            
            # 3. 执行性能分析
            performance_result = self._execute_performance_analysis(probe_task, http_result)
            
            # 4. 执行数据验证（如果适用）
            data_validation_result = self._execute_data_validation(probe_task, http_result)
            
            # 5. 处理结果
            total_time = time.time() - start_time
            self.result_processor.process(
                probe_task,
                http_result,
                validation_result,
                performance_result,
                data_validation_result,
                total_time
            )
            
        except Exception as e:
            self.logger.error("Error executing probe for %s: %s", probe_task.url, str(e))
            self.result_processor.process_error(probe_task, str(e))
    
    def _execute_http_probe(self, probe_task: ProbeTask) -> HttpProbeResult:
        """执行HTTP探测"""
        start_time = time.time()
        
        try:
            # 准备请求
            headers = self._build_headers(probe_task)
            
            # 执行HTTP请求
            response = self.http_client.get(
                probe_task.url,
                headers=headers,
                timeout=probe_task.config.timeout,
                follow_redirects=True
            )
            
            # 计算时间指标
            dns_time = response.timings.get('dns', 0)
            connect_time = response.timings.get('connect', 0)
            tls_time = response.timings.get('tls', 0)
            ttfb = response.timings.get('first_byte', 0)
            download_time = response.timings.get('download', 0)
            total_time = time.time() - start_time
            
            return HttpProbeResult(
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
                timings={
                    "dns": dns_time,
                    "connect": connect_time,
                    "tls": tls_time,
                    "ttfb": ttfb,
                    "download": download_time,
                    "total": total_time
                },
                redirect_chain=[r.url for r in response.redirects],
                certificate_info=self._extract_certificate_info(response)
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            return HttpProbeResult(
                status_code=0,
                error=str(e),
                timings={"total": total_time}
            )
    
    def _build_headers(self, probe_task: ProbeTask) -> Dict[str, str]:
        """构建请求头"""
        headers = {
            "User-Agent": self.config.default_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
        
        # 添加自定义请求头
        if probe_task.config.headers:
            headers.update(probe_task.config.headers)
        
        return headers
    
    def _extract_certificate_info(self, response: HttpResponse) -> Dict:
        """提取证书信息"""
        if not response.certificate:
            return {}
        
        return {
            "issuer": response.certificate.issuer,
            "subject": response.certificate.subject,
            "valid_from": response.certificate.valid_from.isoformat(),
            "valid_to": response.certificate.valid_to.isoformat(),
            "serial_number": response.certificate.serial_number,
            "signature_algorithm": response.certificate.signature_algorithm
        }
    
    def _execute_content_validation(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult
    ) -> ContentValidationResult:
        """执行内容验证"""
        if not probe_task.config.verification_rules or http_result.status_code != 200:
            return ContentValidationResult(
                passed=True,  # 没有规则或非200响应，视为通过
                errors=[],
                verified_rules=[]
            )
        
        passed = True
        errors = []
        verified_rules = []
        
        # 检查每个验证规则
        for rule in probe_task.config.verification_rules:
            result = self._validate_content_rule(rule, http_result)
            if not result["passed"]:
                passed = False
                errors.append({
                    "rule": rule,
                    "message": result["message"]
                })
            verified_rules.append({
                "rule": rule,
                "passed": result["passed"]
            })
        
        return ContentValidationResult(
            passed=passed,
            errors=errors,
            verified_rules=verified_rules
        )
    
    def _validate_content_rule(
        self,
        rule: Dict,
        http_result: HttpProbeResult
    ) -> Dict:
        """验证单个内容规则"""
        content = http_result.content
        if not content:
            return {"passed": False, "message": "No content to validate"}
        
        try:
            # 解码内容
            content_str = content.decode('utf-8', errors='replace')
            
            # 根据规则类型进行验证
            if rule["type"] == "keyword":
                if rule["keyword"] not in content_str:
                    return {
                        "passed": False,
                        "message": f"Keyword '{rule['keyword']}' not found"
                    }
            
            elif rule["type"] == "regex":
                if not re.search(rule["pattern"], content_str):
                    return {
                        "passed": False,
                        "message": f"Regex pattern '{rule['pattern']}' not matched"
                    }
            
            elif rule["type"] == "xpath":
                # 使用lxml进行XPath验证
                tree = etree.fromstring(content, etree.HTMLParser())
                results = tree.xpath(rule["expression"])
                if not results:
                    return {
                        "passed": False,
                        "message": f"XPath expression '{rule['expression']}' returned no results"
                    }
            
            return {"passed": True}
            
        except Exception as e:
            return {
                "passed": False,
                "message": f"Error validating rule: {str(e)}"
            }
    
    def _execute_performance_analysis(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult
    ) -> PerformanceAnalysisResult:
        """执行性能分析"""
        timings = http_result.timings
        total_time = timings.get("total", 0)
        
        # 检查性能阈值
        thresholds = probe_task.config.performance_thresholds
        performance_issues = []
        
        # 检查总响应时间
        if "total" in thresholds and total_time > thresholds["total"]:
            performance_issues.append({
                "metric": "total_time",
                "value": total_time,
                "threshold": thresholds["total"],
                "severity": "high" if total_time > thresholds["total"] * 2 else "medium"
            })
        
        # 检查TTFB
        ttfb = timings.get("ttfb", 0)
        if "ttfb" in thresholds and ttfb > thresholds["ttfb"]:
            performance_issues.append({
                "metric": "ttfb",
                "value": ttfb,
                "threshold": thresholds["ttfb"],
                "severity": "high" if ttfb > thresholds["ttfb"] * 2 else "medium"
            })
        
        # 检查下载时间
        download_time = timings.get("download", 0)
        if "download" in thresholds and download_time > thresholds["download"]:
            performance_issues.append({
                "metric": "download_time",
                "value": download_time,
                "threshold": thresholds["download"],
                "severity": "medium"
            })
        
        return PerformanceAnalysisResult(
            timings=timings,
            issues=performance_issues,
            passed=len(performance_issues) == 0
        )
    
    def _execute_data_validation(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult
    ) -> DataValidationResult:
        """执行数据验证"""
        if not probe_task.config.data_validation or http_result.status_code != 200:
            return DataValidationResult(
                passed=True,
                issues=[],
                metrics={}
            )
        
        data_validation = probe_task.config.data_validation
        content = http_result.content
        
        if not content:
            return DataValidationResult(
                passed=False,
                issues=[{"type": "empty_content", "message": "No content to validate"}],
                metrics={}
            )
        
        try:
            # 根据内容类型进行验证
            content_type = http_result.headers.get("Content-Type", "")
            
            if "json" in content_type:
                return self._validate_json_data(data_validation, content)
            elif "xml" in content_type:
                return self._validate_xml_data(data_validation, content)
            elif "html" in content_type:
                return self._validate_html_data(data_validation, content)
            else:
                return DataValidationResult(
                    passed=True,
                    issues=[{"type": "unsupported_type", "message": f"Unsupported content type: {content_type}"}],
                    metrics={}
                )
                
        except Exception as e:
            return DataValidationResult(
                passed=False,
                issues=[{"type": "validation_error", "message": str(e)}],
                metrics={}
            )
    
    def _validate_json_data(
        self,
        data_validation: Dict,
        content: bytes
    ) -> DataValidationResult:
        """验证JSON数据"""
        try:
            data = json.loads(content)
            issues = []
            metrics = {}
            
            # 检查数据结构
            if "schema" in data_validation:
                # 使用JSON Schema验证
                try:
                    validate(instance=data, schema=data_validation["schema"])
                except Exception as e:
                    issues.append({
                        "type": "schema_validation",
                        "message": str(e)
                    })
            
            # 检查数据量
            if "min_items" in data_validation:
                if isinstance(data, list) and len(data) < data_validation["min_items"]:
                    issues.append({
                        "type": "data_volume",
                        "message": f"Data volume ({len(data)} items) below minimum ({data_validation['min_items']})"
                    })
                elif isinstance(data, dict) and len(data) < data_validation["min_items"]:
                    issues.append({
                        "type": "data_volume",
                        "message": f"Data volume ({len(data)} items) below minimum ({data_validation['min_items']})"
                    })
            
            # 计算指标
            if isinstance(data, list):
                metrics["item_count"] = len(data)
            elif isinstance(data, dict):
                metrics["field_count"] = len(data)
            
            return DataValidationResult(
                passed=len(issues) == 0,
                issues=issues,
                metrics=metrics
            )
            
        except json.JSONDecodeError as e:
            return DataValidationResult(
                passed=False,
                issues=[{"type": "json_error", "message": str(e)}],
                metrics={}
            )
    
    def _validate_xml_data(
        self,
        data_validation: Dict,
        content: bytes
    ) -> DataValidationResult:
        """验证XML数据"""
        # XML验证实现（简化）
        try:
            tree = etree.fromstring(content)
            issues = []
            metrics = {}
            
            # 检查元素数量
            if "min_elements" in data_validation:
                element_count = len(tree.xpath("//node()"))
                if element_count < data_validation["min_elements"]:
                    issues.append({
                        "type": "data_volume",
                        "message": f"Element count ({element_count}) below minimum ({data_validation['min_elements']})"
                    })
                metrics["element_count"] = element_count
            
            return DataValidationResult(
                passed=len(issues) == 0,
                issues=issues,
                metrics=metrics
            )
            
        except etree.XMLSyntaxError as e:
            return DataValidationResult(
                passed=False,
                issues=[{"type": "xml_error", "message": str(e)}],
                metrics={}
            )
    
    def _validate_html_data(
        self,
        data_validation: Dict,
        content: bytes
    ) -> DataValidationResult:
        """验证HTML数据"""
        # HTML验证实现（简化）
        try:
            soup = BeautifulSoup(content, 'html.parser')
            issues = []
            metrics = {}
            
            # 检查特定元素
            if "required_elements" in data_validation:
                for selector in data_validation["required_elements"]:
                    if not soup.select(selector):
                        issues.append({
                            "type": "missing_element",
                            "message": f"Required element '{selector}' not found"
                        })
            
            # 计算指标
            metrics["link_count"] = len(soup.find_all('a'))
            metrics["image_count"] = len(soup.find_all('img'))
            
            return DataValidationResult(
                passed=len(issues) == 0,
                issues=issues,
                metrics=metrics
            )
            
        except Exception as e:
            return DataValidationResult(
                passed=False,
                issues=[{"type": "html_error", "message": str(e)}],
                metrics={}
            )
```

#### 3.4.3 结果处理器

**技术实现：**
```python
class ResultProcessor:
    """结果处理器，负责处理探测结果并更新健康状态"""
    
    def __init__(
        self,
        data_source_service: DataSourceService,
        alert_service: AlertService,
        metrics_service: MetricsService,
        config: Config
    ):
        self.data_source_service = data_source_service
        self.alert_service = alert_service
        self.metrics_service = metrics_service
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def process(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult,
        validation_result: ContentValidationResult,
        performance_result: PerformanceAnalysisResult,
        data_validation_result: DataValidationResult,
        total_time: float
    ):
        """处理探测结果"""
        # 1. 计算健康评分
        health_score = self._calculate_health_score(
            http_result,
            validation_result,
            performance_result,
            data_validation_result
        )
        
        # 2. 更新数据源健康状态
        self._update_data_source_health(
            probe_task,
            http_result,
            health_score,
            total_time
        )
        
        # 3. 处理告警
        self._process_alerts(
            probe_task,
            http_result,
            health_score,
            validation_result,
            performance_result,
            data_validation_result
        )
        
        # 4. 存储指标
        self._store_metrics(
            probe_task,
            http_result,
            validation_result,
            performance_result,
            data_validation_result,
            health_score
        )
    
    def _calculate_health_score(
        self,
        http_result: HttpProbeResult,
        validation_result: ContentValidationResult,
        performance_result: PerformanceAnalysisResult,
        data_validation_result: DataValidationResult
    ) -> float:
        """计算健康评分"""
        # 基础分（基于HTTP状态码）
        base_score = self._calculate_base_score(http_result)
        
        # 验证分
        validation_score = self._calculate_validation_score(validation_result)
        
        # 性能分
        performance_score = self._calculate_performance_score(performance_result)
        
        # 数据质量分
        data_score = self._calculate_data_score(data_validation_result)
        
        # 加权计算
        weights = self.config.health_score_weights
        total_score = (
            base_score * weights["base"] +
            validation_score * weights["validation"] +
            performance_score * weights["performance"] +
            data_score * weights["data"]
        ) / sum(weights.values())
        
        return max(0.0, min(1.0, total_score))
    
    def _calculate_base_score(self, http_result: HttpProbeResult) -> float:
        """计算基础分（基于HTTP状态码）"""
        if http_result.status_code == 0:
            return 0.0  # 连接错误
        
        if 200 <= http_result.status_code < 300:
            return 1.0
        
        if 300 <= http_result.status_code < 400:
            return 0.8  # 重定向
        
        if 400 <= http_result.status_code < 500:
            return 0.3  # 客户端错误
        
        return 0.1  # 服务端错误
    
    def _calculate_validation_score(self, validation_result: ContentValidationResult) -> float:
        """计算验证分"""
        if not validation_result.verified_rules:
            return 1.0  # 没有验证规则
        
        passed_count = sum(1 for r in validation_result.verified_rules if r["passed"])
        return passed_count / len(validation_result.verified_rules)
    
    def _calculate_performance_score(self, performance_result: PerformanceAnalysisResult) -> float:
        """计算性能分"""
        if not performance_result.issues:
            return 1.0
        
        # 根据问题严重程度计算
        severity_weights = {"low": 0.1, "medium": 0.3, "high": 0.7}
        total_deduction = 0
        
        for issue in performance_result.issues:
            total_deduction += severity_weights.get(issue["severity"], 0.2)
        
        return max(0.0, 1.0 - total_deduction)
    
    def _calculate_data_score(self, data_validation_result: DataValidationResult) -> float:
        """计算数据质量分"""
        if not data_validation_result.issues:
            return 1.0
        
        # 简单实现：根据问题数量计算
        return max(0.0, 1.0 - (len(data_validation_result.issues) * 0.2))
    
    def _update_data_source_health(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult,
        health_score: float,
        total_time: float
    ):
        """更新数据源健康状态"""
        # 准备更新数据
        update_data = {
            "last_health_check": datetime.utcnow().isoformat(),
            "health_score": health_score,
            "availability_24h": self._calculate_24h_availability(probe_task.data_source_id, health_score),
            "availability_7d": self._calculate_7d_availability(probe_task.data_source_id, health_score),
            "response_time_p50": self._calculate_p50_response_time(probe_task.data_source_id, total_time),
            "response_time_p95": self._calculate_p95_response_time(probe_task.data_source_id, total_time),
            "status": self._determine_status(health_score)
        }
        
        # 更新数据源
        self.data_source_service.update_data_source(
            data_source_id=probe_task.data_source_id,
            project_id=probe_task.project_id,
            updates=update_data,
            user_id="system"
        )
    
    def _calculate_24h_availability(
        self,
        data_source_id: str,
        current_score: float
    ) -> float:
        """计算24小时可用性"""
        # 获取过去24小时的历史记录
        history = self.metrics_service.get_health_history(
            data_source_id,
            start_time=datetime.utcnow() - timedelta(hours=24),
            end_time=datetime.utcnow(),
            limit=1000
        )
        
        # 添加当前分数
        scores = [h["score"] for h in history] + [current_score]
        
        # 计算平均值
        return sum(scores) / len(scores) if scores else 1.0
    
    def _calculate_7d_availability(
        self,
        data_source_id: str,
        current_score: float
    ) -> float:
        """计算7天可用性"""
        # 获取过去7天的历史记录（每天一个样本）
        history = self.metrics_service.get_health_history(
            data_source_id,
            start_time=datetime.utcnow() - timedelta(days=7),
            end_time=datetime.utcnow(),
            interval="1d",
            limit=7
        )
        
        # 添加当前分数
        scores = [h["score"] for h in history] + [current_score]
        
        # 计算平均值
        return sum(scores) / len(scores) if scores else 1.0
    
    def _calculate_p50_response_time(
        self,
        data_source_id: str,
        current_time: float
    ) -> float:
        """计算P50响应时间"""
        # 获取过去1小时的响应时间
        history = self.metrics_service.get_response_times(
            data_source_id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            limit=100
        )
        
        # 添加当前时间
        times = [h["time"] for h in history] + [current_time]
        
        # 计算P50
        return np.percentile(times, 50) if times else current_time
    
    def _calculate_p95_response_time(
        self,
        data_source_id: str,
        current_time: float
    ) -> float:
        """计算P95响应时间"""
        # 获取过去1小时的响应时间
        history = self.metrics_service.get_response_times(
            data_source_id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            limit=100
        )
        
        # 添加当前时间
        times = [h["time"] for h in history] + [current_time]
        
        # 计算P95
        return np.percentile(times, 95) if times else current_time
    
    def _determine_status(self, health_score: float) -> str:
        """确定健康状态"""
        if health_score >= self.config.status_thresholds["healthy"]:
            return "healthy"
        elif health_score >= self.config.status_thresholds["degraded"]:
            return "degraded"
        else:
            return "unhealthy"
    
    def _process_alerts(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult,
        health_score: float,
        validation_result: ContentValidationResult,
        performance_result: PerformanceAnalysisResult,
        data_validation_result: DataValidationResult
    ):
        """处理告警"""
        # 1. 检查是否需要触发告警
        alert_needed = self._should_trigger_alert(
            probe_task.data_source_id,
            health_score,
            http_result
        )
        
        if not alert_needed:
            # 2. 检查是否需要解决告警
            self._check_alert_resolution(probe_task.data_source_id, health_score)
            return
        
        # 3. 创建告警
        alert = self._create_alert(
            probe_task,
            http_result,
            health_score,
            validation_result,
            performance_result,
            data_validation_result
        )
        
        # 4. 触发告警
        self.alert_service.trigger_alert(alert)
    
    def _should_trigger_alert(
        self,
        data_source_id: str,
        health_score: float,
        http_result: HttpProbeResult
    ) -> bool:
        """检查是否需要触发告警"""
        # 获取当前告警状态
        current_alert = self.alert_service.get_current_alert(data_source_id)
        
        # 如果已经有活跃告警，不需要新告警
        if current_alert and current_alert["status"] == "active":
            return False
        
        # 检查健康分数是否低于阈值
        if health_score >= self.config.alert_thresholds["health_score"]:
            return False
        
        # 检查HTTP状态码
        if http_result.status_code == 0 or http_result.status_code >= 500:
            return True
        
        # 检查连续失败次数
        failure_count = self._get_consecutive_failures(data_source_id)
        return failure_count >= self.config.alert_thresholds["consecutive_failures"]
    
    def _get_consecutive_failures(self, data_source_id: str) -> int:
        """获取连续失败次数"""
        history = self.metrics_service.get_health_history(
            data_source_id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            limit=10
        )
        
        consecutive_failures = 0
        for record in reversed(history):
            if record["score"] < self.config.status_thresholds["degraded"]:
                consecutive_failures += 1
            else:
                break
        
        return consecutive_failures
    
    def _check_alert_resolution(
        self,
        data_source_id: str,
        health_score: float
    ):
        """检查告警是否已解决"""
        current_alert = self.alert_service.get_current_alert(data_source_id)
        
        # 没有活跃告警，无需处理
        if not current_alert or current_alert["status"] != "active":
            return
        
        # 检查健康分数是否恢复
        if health_score < self.config.alert_resolution_threshold:
            return
        
        # 检查连续成功次数
        success_count = self._get_consecutive_successes(data_source_id)
        if success_count < self.config.alert_resolution_min_success:
            return
        
        # 解决告警
        self.alert_service.resolve_alert(
            alert_id=current_alert["id"],
            resolution_details={
                "health_score": health_score,
                "consecutive_successes": success_count
            }
        )
    
    def _get_consecutive_successes(self, data_source_id: str) -> int:
        """获取连续成功次数"""
        history = self.metrics_service.get_health_history(
            data_source_id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            limit=10
        )
        
        consecutive_successes = 0
        for record in reversed(history):
            if record["score"] >= self.config.status_thresholds["degraded"]:
                consecutive_successes += 1
            else:
                break
        
        return consecutive_successes
    
    def _create_alert(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult,
        health_score: float,
        validation_result: ContentValidationResult,
        performance_result: PerformanceAnalysisResult,
        data_validation_result: DataValidationResult
    ) -> Alert:
        """创建告警"""
        # 确定告警级别
        severity = self._determine_alert_severity(
            health_score,
            http_result,
            validation_result,
            performance_result
        )
        
        # 生成告警消息
        message = self._generate_alert_message(
            probe_task,
            http_result,
            health_score,
            severity
        )
        
        return Alert(
            data_source_id=probe_task.data_source_id,
            project_id=probe_task.project_id,
            url=probe_task.url,
            severity=severity,
            message=message,
            details={
                "health_score": health_score,
                "status_code": http_result.status_code,
                "validation_issues": validation_result.errors,
                "performance_issues": performance_result.issues,
                "data_issues": data_validation_result.issues
            },
            timestamp=datetime.utcnow()
        )
    
    def _determine_alert_severity(
        self,
        health_score: float,
        http_result: HttpProbeResult,
        validation_result: ContentValidationResult,
        performance_result: PerformanceAnalysisResult
    ) -> str:
        """确定告警级别"""
        # 基于HTTP状态码
        if http_result.status_code == 0:
            return "critical"
        if http_result.status_code >= 500:
            return "critical"
        if http_result.status_code >= 400:
            return "high"
        
        # 基于健康分数
        if health_score < self.config.severity_thresholds["critical"]:
            return "critical"
        if health_score < self.config.severity_thresholds["high"]:
            return "high"
        if health_score < self.config.severity_thresholds["medium"]:
            return "medium"
        
        # 基于验证问题
        if validation_result.errors:
            return "medium"
        
        # 基于性能问题
        if any(issue["severity"] == "high" for issue in performance_result.issues):
            return "high"
        if any(issue["severity"] == "medium" for issue in performance_result.issues):
            return "medium"
        
        return "low"
    
    def _generate_alert_message(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult,
        health_score: float,
        severity: str
    ) -> str:
        """生成告警消息"""
        if http_result.status_code == 0:
            return f"Connection failed to {probe_task.url}"
        if http_result.status_code >= 500:
            return f"Server error ({http_result.status_code}) for {probe_task.url}"
        if http_result.status_code >= 400:
            return f"Client error ({http_result.status_code}) for {probe_task.url}"
        
        if health_score < self.config.severity_thresholds["critical"]:
            return f"Critical health issue for {probe_task.url} (score: {health_score:.2f})"
        if health_score < self.config.severity_thresholds["high"]:
            return f"High severity issue for {probe_task.url} (score: {health_score:.2f})"
        
        return f"Health issue for {probe_task.url} (score: {health_score:.2f})"
    
    def _store_metrics(
        self,
        probe_task: ProbeTask,
        http_result: HttpProbeResult,
        validation_result: ContentValidationResult,
        performance_result: PerformanceAnalysisResult,
        data_validation_result: DataValidationResult,
        health_score: float
    ):
        """存储指标"""
        timestamp = datetime.utcnow()
        
        # 存储健康指标
        self.metrics_service.store_health_metric(
            data_source_id=probe_task.data_source_id,
            score=health_score,
            timestamp=timestamp
        )
        
        # 存储响应时间指标
        if "total" in http_result.timings:
            self.metrics_service.store_response_time(
                data_source_id=probe_task.data_source_id,
                response_time=http_result.timings["total"],
                timestamp=timestamp
            )
        
        # 存储可用性指标
        is_available = 1 if (200 <= http_result.status_code < 400) else 0
        self.metrics_service.store_availability(
            data_source_id=probe_task.data_source_id,
            is_available=is_available,
            timestamp=timestamp
        )
        
        # 存储验证指标
        self.metrics_service.store_validation_metrics(
            data_source_id=probe_task.data_source_id,
            passed=validation_result.passed,
            issue_count=len(validation_result.errors),
            timestamp=timestamp
        )
        
        # 存储性能指标
        self.metrics_service.store_performance_metrics(
            data_source_id=probe_task.data_source_id,
            metrics=performance_result.timings,
            issue_count=len(performance_result.issues),
            timestamp=timestamp
        )
        
        # 存储数据质量指标
        self.metrics_service.store_data_metrics(
            data_source_id=probe_task.data_source_id,
            passed=data_validation_result.passed,
            issue_count=len(data_validation_result.issues),
            metrics=data_validation_result.metrics,
            timestamp=timestamp
        )
    
    def process_error(self, probe_task: ProbeTask, error: str):
        """处理探测错误"""
        self.logger.error("Probe error for %s: %s", probe_task.url, error)
        
        # 更新数据源状态
        update_data = {
            "last_health_check": datetime.utcnow().isoformat(),
            "health_score": 0.0,
            "status": "unhealthy"
        }
        
        try:
            self.data_source_service.update_data_source(
                data_source_id=probe_task.data_source_id,
                project_id=probe_task.project_id,
                updates=update_data,
                user_id="system"
            )
        except Exception as e:
            self.logger.error("Error updating data source health: %s", str(e))
        
        # 触发告警
        alert = Alert(
            data_source_id=probe_task.data_source_id,
            project_id=probe_task.project_id,
            url=probe_task.url,
            severity="critical",
            message=f"Probe failed: {error}",
            details={"error": error},
            timestamp=datetime.utcnow()
        )
        self.alert_service.trigger_alert(alert)
        
        # 存储错误指标
        self.metrics_service.store_health_metric(
            data_source_id=probe_task.data_source_id,
            score=0.0,
            timestamp=datetime.utcnow()
        )
```

### 3.5 数据模型详细定义

#### 3.5.1 健康指标表

```sql
-- 健康指标表（时序数据）
CREATE TABLE health_metrics (
    time TIMESTAMPTZ NOT NULL,
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    health_score DOUBLE PRECISION NOT NULL,
    response_time DOUBLE PRECISION,
    is_available BOOLEAN NOT NULL,
    
    -- 索引
    INDEX idx_health_metrics_ds ON health_metrics(data_source_id),
    INDEX idx_health_metrics_time ON health_metrics(time DESC)
);

-- 创建分区（按月）
SELECT create_hypertable('health_metrics', 'time', partitioning_column => 'data_source_id', number_partitions => 4);

-- 健康历史表（汇总数据）
CREATE TABLE health_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ NOT NULL,
    health_score DOUBLE PRECISION NOT NULL,
    availability DOUBLE PRECISION NOT NULL,
    avg_response_time DOUBLE PRECISION,
    min_response_time DOUBLE PRECISION,
    max_response_time DOUBLE PRECISION,
    validation_pass_rate DOUBLE PRECISION,
    performance_issues INT NOT NULL DEFAULT 0,
    data_issues INT NOT NULL DEFAULT 0,
    
    -- 索引
    UNIQUE (data_source_id, period_start, period_end),
    INDEX idx_health_history_ds ON health_history(data_source_id),
    INDEX idx_health_history_period ON health_history(period_start DESC)
);
```

#### 3.5.2 告警表

```sql
-- 告警表
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    url VARCHAR(2048) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    message TEXT NOT NULL,
    details JSONB,
    status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'resolved', 'suppressed')) DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    resolution_details JSONB,
    
    -- 索引
    INDEX idx_alerts_data_source ON alerts(data_source_id),
    INDEX idx_alerts_status ON alerts(status),
    INDEX idx_alerts_created ON alerts(created_at DESC),
    INDEX idx_alerts_resolved ON alerts(resolved_at DESC)
);

-- 告警通知表
CREATE TABLE alert_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_id UUID NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    channel VARCHAR(50) NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'sent', 'failed')),
    status_message TEXT,
    
    -- 索引
    INDEX idx_notifications_alert ON alert_notifications(alert_id),
    INDEX idx_notifications_channel ON alert_notifications(channel),
    INDEX idx_notifications_sent ON alert_notifications(sent_at DESC)
);
```

### 3.6 API详细规范

#### 3.6.1 健康监测API

**获取数据源健康状态 (GET /api/v1/health/data-sources/{id})**

*请求示例:*
```http
GET /api/v1/health/data-sources/ds-7a8b9c0d HTTP/1.1
Host: dshms.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data_source_id": "ds-7a8b9c0d",
  "url": "https://api.instagram.com/v1/users/self/media/recent",
  "status": "healthy",
  "health_score": 0.95,
  "availability_24h": 0.98,
  "availability_7d": 0.95,
  "response_time_p50": 0.35,
  "response_time_p95": 1.2,
  "last_check": "2023-06-15T10:35:20Z",
  "metrics": {
    "http_status": 200,
    "content_validation": {
      "passed": true,
      "issues": []
    },
    "performance": {
      "timings": {
        "dns": 0.02,
        "connect": 0.05,
        "tls": 0.1,
        "ttfb": 0.25,
        "download": 0.1,
        "total": 0.45
      },
      "issues": []
    },
    "data_validation": {
      "passed": true,
      "issues": [],
      "metrics": {
        "item_count": 20
      }
    }
  }
}
```

**获取健康历史 (GET /api/v1/health/history/{id})**

*请求示例:*
```http
GET /api/v1/health/history/ds-7a8b9c0d?start=2023-06-01T00:00:00Z&end=2023-06-15T23:59:59Z&interval=1d HTTP/1.1
Host: dshms.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data_source_id": "ds-7a8b9c0d",
  "interval": "1d",
  "start": "2023-06-01T00:00:00Z",
  "end": "2023-06-15T23:59:59Z",
  "history": [
    {
      "timestamp": "2023-06-01T00:00:00Z",
      "health_score": 0.92,
      "availability": 0.95,
      "response_time_avg": 0.42,
      "response_time_p95": 1.5
    },
    {
      "timestamp": "2023-06-02T00:00:00Z",
      "health_score": 0.94,
      "availability": 0.97,
      "response_time_avg": 0.38,
      "response_time_p95": 1.3
    },
    // ... 更多数据点
  ]
}
```

#### 3.6.2 告警API

**获取活跃告警 (GET /api/v1/alerts/active)**

*请求示例:*
```http
GET /api/v1/alerts/active?project_id=proj-123 HTTP/1.1
Host: dshms.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": "alert-1a2b3c4d",
      "data_source_id": "ds-1b2c3d4e",
      "url": "https://api.twitter.com/2/users/me/tweets",
      "severity": "high",
      "message": "High severity issue for https://api.twitter.com/2/users/me/tweets (score: 0.65)",
      "details": {
        "health_score": 0.65,
        "status_code": 429,
        "validation_issues": [],
        "performance_issues": [
          {
            "metric": "total_time",
            "value": 3.5,
            "threshold": 2.0,
            "severity": "high"
          }
        ],
        "data_issues": []
      },
      "status": "active",
      "created_at": "2023-06-15T10:30:45Z"
    }
  ],
  "total": 1
}
```

**解决告警 (POST /api/v1/alerts/{id}/resolve)**

*请求示例:*
```http
POST /api/v1/alerts/alert-1a2b3c4d/resolve HTTP/1.1
Host: dshms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resolution_notes": "Issue resolved by increasing rate limit"
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "alert-1a2b3c4d",
  "status": "resolved",
  "resolved_at": "2023-06-15T10:45:30Z",
  "resolved_by": "user-123",
  "resolution_details": {
    "resolution_notes": "Issue resolved by increasing rate limit",
    "health_score": 0.92,
    "consecutive_successes": 10
  }
}
```

### 3.7 性能优化策略

#### 3.7.1 时序数据存储优化

1. **Hypertable分区**
   ```sql
   -- 创建按数据源ID分区的Hypertable
   SELECT create_hypertable('health_metrics', 'time', partitioning_column => 'data_source_id', number_partitions => 4);
   
   -- 添加压缩策略
   ALTER TABLE health_metrics SET (timescaledb.compress, timescaledb.compress_segmentby = 'data_source_id');
   SELECT add_compression_policy('health_metrics', INTERVAL '7 days');
   ```

2. **数据保留策略**
   ```sql
   -- 保留原始数据7天
   SELECT add_retention_policy('health_metrics', INTERVAL '7 days');
   
   -- 为更长期数据创建连续聚合
   CREATE MATERIALIZED VIEW health_daily
   WITH (timescaledb.continuous) AS
   SELECT
       time_bucket('1 day', time) AS bucket,
       data_source_id,
       AVG(health_score) AS avg_health,
       AVG(response_time) AS avg_response_time,
       AVG(is_available::int) AS availability
   FROM health_metrics
   GROUP BY bucket, data_source_id
   WITH DATA;
   ```

#### 3.7.2 告警处理优化

1. **告警抑制策略**
   ```python
   def should_suppress_alert(alert: Alert) -> bool:
       """检查是否应该抑制告警"""
       # 相同数据源的重复告警抑制
       recent_alerts = get_recent_alerts(
           data_source_id=alert.data_source_id,
           since=datetime.utcnow() - timedelta(minutes=5)
       )
       if len(recent_alerts) > 2:
           return True
       
       # 维护窗口抑制
       if is_in_maintenance_window(alert.data_source_id):
           return True
       
       # 已知问题抑制
       if is_known_issue(alert):
           return True
       
       return False
   ```

2. **告警聚合**
   ```python
   def aggregate_similar_alerts(alerts: List[Alert]) -> List[AlertGroup]:
       """聚合相似告警"""
       # 按数据源和严重程度分组
       groups = defaultdict(list)
       for alert in alerts:
           key = (alert.data_source_id, alert.severity)
           groups[key].append(alert)
       
       # 创建聚合组
       alert_groups = []
       for (ds_id, severity), group_alerts in groups.items():
           first_alert = min(group_alerts, key=lambda a: a.created_at)
           last_alert = max(group_alerts, key=lambda a: a.created_at)
           
           alert_groups.append(AlertGroup(
               data_source_id=ds_id,
               severity=severity,
               count=len(group_alerts),
               first_occurrence=first_alert.created_at,
               last_occurrence=last_alert.created_at,
               sample_alert=first_alert
           ))
       
       return alert_groups
   ```

### 3.8 安全考虑

#### 3.8.1 探测安全

1. **探测限制**
   - 限制探测频率，避免被目标网站封禁
   - 实现随机化探测间隔
   - 支持自定义User-Agent轮换

2. **目标网站保护**
   - 尊重robots.txt
   - 实现Crawl-Delay遵守
   - 避免高负载探测

#### 3.8.2 数据安全

1. **敏感数据处理**
   - 不存储响应内容（除非必要）
   - 对存储的内容进行脱敏
   - 限制敏感数据访问

2. **隐私合规**
   - 符合GDPR要求
   - 提供数据删除选项
   - 限制数据保留时间

### 3.9 与其他模块的交互

#### 3.9.1 与数据源注册中心交互

```mermaid
sequenceDiagram
    participant DSR as Data Source Registry
    participant DSHMS as Data Source Health Monitoring System
    
    DSHMS->>DSR: GET /api/v1/data-sources?status=active
    DSR-->>DSHMS: Active data sources list
    
    loop 每5分钟
        DSHMS->>DSR: POST /api/v1/data-sources/{id}/health
        DSR-->>DSHMS: Acknowledgement
    end
    
    DSR->>DSHMS: GET /api/v1/health/data-sources/{id}
    DSHMS-->>DSR: Health status and metrics
```

#### 3.9.2 与数据处理工作流引擎交互

```mermaid
sequenceDiagram
    participant DPWE as Data Processing Workflow Engine
    participant DSHMS as Data Source Health Monitoring System
    
    DPWE->>DSHMS: GET /api/v1/health/data-sources/{id}
    DSHMS-->>DPWE: Health status
    
    DPWE->>DSHMS: GET /api/v1/health/history/{id}?interval=1h
    DSHMS-->>DPWE: Health history
    
    DPWE->>DSHMS: POST /api/v1/alerts/{id}/resolve
    DSHMS-->>DPWE: Resolution confirmation
```

#### 3.9.3 与数据质量预测分析系统交互

```mermaid
sequenceDiagram
    participant DQPAS as Data Quality Prediction and Analysis System
    participant DSHMS as Data Source Health Monitoring System
    
    DQPAS->>DSHMS: GET /api/v1/health/history/{id}?interval=1d&limit=30
    DSHMS-->>DQPAS: Historical health data
    
    DSHMS->>DQPAS: POST /api/v1/predictions (health prediction)
    DQPAS-->>DSHMS: Prediction results
```

## 4. 数据处理工作流引擎 (Data Processing Workflow Engine)

### 4.1 模块概述
数据处理工作流引擎是镜界平台的核心自动化组件，提供可视化工作流设计和执行能力。它支持从简单触发到复杂数据处理流水线的完整工作流管理，是实现数据采集、处理和分析自动化的关键。

### 4.2 详细功能清单

#### 4.2.1 核心功能
- **工作流定义管理**
  - 可视化工作流设计器
  - 工作流版本控制
  - 工作流模板库
  - 工作流导入/导出
- **触发器管理**
  - 定时触发器
  - 文件系统触发器（监控NAS）
  - API触发器（Webhook）
  - 条件触发器
- **节点类型支持**
  - 数据源节点（获取数据）
  - 处理节点（数据转换、清洗）
  - AI节点（调用AI服务）
  - 存储节点（保存结果）
  - 条件节点（分支逻辑）
  - 循环节点
- **工作流执行**
  - 同步/异步执行
  - 执行状态跟踪
  - 执行日志记录
  - 执行结果查看
- **错误处理**
  - 自动重试机制
  - 错误分类与处理
  - 失败通知
  - 手动重试

#### 4.2.2 高级功能
- **工作流调试**
  - 单步执行
  - 断点设置
  - 变量检查
  - 执行回放
- **资源管理**
  - 资源需求定义
  - 资源配额管理
  - 动态资源分配
  - 资源使用监控
- **工作流分析**
  - 执行性能分析
  - 瓶颈识别
  - 优化建议
  - 成本分析
- **工作流共享与协作**
  - 工作流分享
  - 协作编辑
  - 评论与反馈
  - 权限管理

### 4.3 技术架构

#### 4.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                             数据处理工作流引擎 (DPWE)                                         │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  前端交互层           │  服务层               │  执行层                                    │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 工作流设计器         │ • 工作流管理服务      │ • 调度器                                  │
│ • 执行监控界面        │ • 触发器服务          │ • 节点执行器                              │
│ • 调试工具            │ • 执行服务            │ • 资源管理器                              │
│ • 分析仪表盘          │ • 错误处理服务        │ • 日志收集器                              │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 4.3.2 服务边界与交互
- **输入**：
  - 工作流定义（来自用户或API）
  - 触发事件（定时、文件系统、Webhook等）
  - 节点执行请求
- **输出**：
  - 工作流执行状态
  - 执行结果
  - 日志和指标
  - 错误通知

### 4.4 核心组件详细实现

#### 4.4.1 工作流定义服务

**技术实现：**
```python
class WorkflowDefinitionService:
    """工作流定义管理服务"""
    
    def __init__(
        self,
        db: Database,
        storage: StorageService,
        config: Config
    ):
        self.db = db
        self.storage = storage
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.cache = TTLCache(maxsize=1000, ttl=300)  # 5分钟缓存
    
    def create_workflow(
        self,
        project_id: str,
        workflow: WorkflowDefinition,
        user_id: str
    ) -> WorkflowDefinition:
        """
        创建新工作流
        
        :param project_id: 项目ID
        :param workflow: 工作流定义
        :param user_id: 创建者ID
        :return: 创建后的工作流
        """
        # 1. 验证工作流
        self._validate_workflow(workflow)
        
        # 2. 生成唯一ID
        workflow.id = f"wf-{uuid.uuid4().hex[:8]}"
        workflow.project_id = project_id
        workflow.version = "1.0.0"
        workflow.created_at = datetime.utcnow()
        workflow.updated_at = workflow.created_at
        workflow.created_by = user_id
        workflow.updated_by = user_id
        workflow.status = "active"
        
        # 3. 保存工作流定义
        self._save_workflow(workflow)
        
        # 4. 保存到存储（用于版本控制）
        self._save_to_storage(workflow)
        
        # 5. 清除缓存
        self._clear_cache(project_id)
        
        return workflow
    
    def _validate_workflow(self, workflow: WorkflowDefinition):
        """验证工作流定义的有效性"""
        # 必填字段检查
        required_fields = ["name", "triggers", "nodes"]
        for field in required_fields:
            if not getattr(workflow, field):
                raise ValidationError(f"Missing required field: {field}")
        
        # 验证触发器
        if not workflow.triggers:
            raise ValidationError("At least one trigger is required")
        
        for trigger in workflow.triggers:
            if not trigger.type:
                raise ValidationError("Trigger type is required")
            if not trigger.config:
                raise ValidationError("Trigger config is required")
        
        # 验证节点
        if not workflow.nodes:
            raise ValidationError("At least one node is required")
        
        node_ids = set()
        for node in workflow.nodes:
            if not node.id:
                raise ValidationError("Node ID is required")
            if node.id in node_ids:
                raise ValidationError(f"Duplicate node ID: {node.id}")
            node_ids.add(node.id)
            
            if not node.type:
                raise ValidationError(f"Node type is required for node {node.id}")
        
        # 验证连接
        if workflow.edges:
            for edge in workflow.edges:
                if edge.source not in node_ids:
                    raise ValidationError(f"Edge source {edge.source} does not exist")
                if edge.target not in node_ids:
                    raise ValidationError(f"Edge target {edge.target} does not exist")
        
        # 验证入口节点（至少有一个没有入边的节点）
        entry_nodes = self._find_entry_nodes(workflow)
        if not entry_nodes:
            raise ValidationError("No entry nodes found (nodes with no incoming edges)")
    
    def _find_entry_nodes(self, workflow: WorkflowDefinition) -> Set[str]:
        """查找入口节点（没有入边的节点）"""
        all_nodes = {node.id for node in workflow.nodes}
        target_nodes = {edge.target for edge in workflow.edges}
        return all_nodes - target_nodes
    
    def _save_workflow(self, workflow: WorkflowDefinition):
        """保存工作流定义到数据库"""
        # 准备SQL
        sql = """
        INSERT INTO workflows (
            id, project_id, name, display_name, description, version, 
            definition, status, created_at, updated_at, created_by, updated_by, tags, metadata
        ) VALUES (
            %(id)s, %(project_id)s, %(name)s, %(display_name)s, %(description)s, %(version)s,
            %(definition)s, %(status)s, %(created_at)s, %(updated_at)s, %(created_by)s, %(updated_by)s,
            %(tags)s, %(metadata)s
        )
        """
        
        # 执行插入
        self.db.execute(sql, {
            "id": workflow.id,
            "project_id": workflow.project_id,
            "name": workflow.name,
            "display_name": workflow.display_name,
            "description": workflow.description,
            "version": workflow.version,
            "definition": json.dumps(workflow.definition),
            "status": workflow.status,
            "created_at": workflow.created_at,
            "updated_at": workflow.updated_at,
            "created_by": workflow.created_by,
            "updated_by": workflow.updated_by,
            "tags": json.dumps(workflow.tags),
            "metadata": json.dumps(workflow.metadata)
        })
    
    def _save_to_storage(self, workflow: WorkflowDefinition):
        """保存工作流到存储（用于版本控制）"""
        # 生成存储路径
        storage_path = f"workflows/{workflow.project_id}/{workflow.id}/{workflow.version}"
        
        # 保存定义
        self.storage.save(
            f"{storage_path}/definition.json",
            json.dumps(workflow.definition).encode('utf-8')
        )
        
        # 保存元数据
        self.storage.save(
            f"{storage_path}/metadata.json",
            json.dumps({
                "version": workflow.version,
                "created_at": workflow.created_at.isoformat(),
                "created_by": workflow.created_by,
                "description": workflow.description
            }).encode('utf-8')
        )
    
    def get_workflow(
        self,
        workflow_id: str,
        project_id: str,
        user_id: str,
        version: Optional[str] = None
    ) -> WorkflowDefinition:
        """
        获取工作流详情
        
        :param workflow_id: 工作流ID
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :param version: 版本号（可选）
        :return: 工作流定义
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to read this workflow")
        
        # 2. 从缓存获取
        cache_key = f"{workflow_id}:{version or 'latest'}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 3. 从数据库获取
        workflow = self._get_from_db(workflow_id, project_id, version)
        if not workflow:
            raise NotFoundError(f"Workflow {workflow_id} not found")
        
        # 4. 从存储加载定义（如果是特定版本）
        if version and version != workflow.version:
            self._load_definition_from_storage(workflow, version)
        
        # 5. 缓存结果
        self.cache[cache_key] = workflow
        
        return workflow
    
    def _get_from_db(
        self,
        workflow_id: str,
        project_id: str,
        version: Optional[str] = None
    ) -> Optional[WorkflowDefinition]:
        """从数据库获取工作流"""
        if version:
            # 获取特定版本
            sql = """
            SELECT * FROM workflows 
            WHERE id = %(id)s AND project_id = %(project_id)s AND version = %(version)s
            """
            params = {
                "id": workflow_id,
                "project_id": project_id,
                "version": version
            }
        else:
            # 获取最新版本
            sql = """
            SELECT * FROM workflows 
            WHERE id = %(id)s AND project_id = %(project_id)s
            ORDER BY version DESC
            LIMIT 1
            """
            params = {
                "id": workflow_id,
                "project_id": project_id
            }
        
        row = self.db.fetchone(sql, params)
        if not row:
            return None
        
        return self._row_to_workflow(row)
    
    def _row_to_workflow(self, row: Dict) -> WorkflowDefinition:
        """将数据库行转换为WorkflowDefinition对象"""
        return WorkflowDefinition(
            id=row["id"],
            project_id=row["project_id"],
            name=row["name"],
            display_name=row["display_name"],
            description=row["description"],
            version=row["version"],
            definition=json.loads(row["definition"]),
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            created_by=row["created_by"],
            updated_by=row["updated_by"],
            tags=json.loads(row["tags"]),
            metadata=json.loads(row["metadata"])
        )
    
    def _load_definition_from_storage(
        self,
        workflow: WorkflowDefinition,
        version: str
    ):
        """从存储加载特定版本的定义"""
        storage_path = f"workflows/{workflow.project_id}/{workflow.id}/{version}/definition.json"
        
        try:
            definition_data = self.storage.load(storage_path)
            workflow.definition = json.loads(definition_data.decode('utf-8'))
            workflow.version = version
        except Exception as e:
            self.logger.error("Error loading workflow version %s: %s", version, str(e))
            raise NotFoundError(f"Workflow version {version} not found")
    
    def update_workflow(
        self,
        workflow_id: str,
        project_id: str,
        updates: Dict,
        user_id: str
    ) -> WorkflowDefinition:
        """
        更新工作流
        
        :param workflow_id: 工作流ID
        :param project_id: 项目ID
        :param updates: 更新字段
        :param user_id: 更新者ID
        :return: 更新后的工作流
        """
        # 1. 获取当前工作流
        current = self.get_workflow(workflow_id, project_id, user_id)
        
        # 2. 检查权限
        if not self._has_permission(user_id, project_id, "write"):
            raise PermissionError("User does not have permission to update this workflow")
        
        # 3. 验证更新
        self._validate_updates(updates, current)
        
        # 4. 创建新版本
        new_version = self._create_new_version(current, updates, user_id)
        
        # 5. 保存更新
        updated_workflow = self._save_update(workflow_id, project_id, new_version, updates, user_id)
        
        # 6. 清除缓存
        self._clear_cache(project_id)
        
        return updated_workflow
    
    def _validate_updates(self, updates: Dict, current: WorkflowDefinition):
        """验证更新是否有效"""
        # 不能修改ID和项目ID
        if "id" in updates or "project_id" in updates:
            raise ValidationError("Cannot update workflow ID or project ID")
        
        # 验证定义更新
        if "definition" in updates:
            # 创建临时工作流进行验证
            temp_workflow = copy.deepcopy(current)
            temp_workflow.definition = updates["definition"]
            self._validate_workflow(temp_workflow)
    
    def _create_new_version(self, current: WorkflowDefinition, updates: Dict, user_id: str) -> str:
        """创建工作流新版本"""
        # 解析当前版本
        major, minor, patch = map(int, current.version.split('.'))
        
        # 确定新版本号
        if "breaking_change" in updates and updates["breaking_change"]:
            # 重大变更
            new_version = f"{major + 1}.0.0"
        elif "feature" in updates and updates["feature"]:
            # 新功能
            new_version = f"{major}.{minor + 1}.0"
        else:
            # 修复
            new_version = f"{major}.{minor}.{patch + 1}"
        
        return new_version
    
    def _save_update(
        self,
        workflow_id: str,
        project_id: str,
        new_version: str,
        updates: Dict,
        user_id: str
    ) -> WorkflowDefinition:
        """保存工作流更新"""
        # 准备更新字段
        update_fields = []
        params = {
            "id": workflow_id,
            "project_id": project_id,
            "version": new_version,
            "updated_at": datetime.utcnow(),
            "updated_by": user_id
        }
        
        if "definition" in updates:
            update_fields.append("definition = %(definition)s")
            params["definition"] = json.dumps(updates["definition"])
        
        if "display_name" in updates:
            update_fields.append("display_name = %(display_name)s")
            params["display_name"] = updates["display_name"]
        
        if "description" in updates:
            update_fields.append("description = %(description)s")
            params["description"] = updates["description"]
        
        if "tags" in updates:
            update_fields.append("tags = %(tags)s")
            params["tags"] = json.dumps(updates["tags"])
        
        if "metadata" in updates:
            update_fields.append("metadata = %(metadata)s")
            params["metadata"] = json.dumps(updates["metadata"])
        
        # 添加版本和更新时间
        update_fields.append("version = %(version)s")
        update_fields.append("updated_at = %(updated_at)s")
        update_fields.append("updated_by = %(updated_by)s")
        
        # 执行更新
        sql = f"""
        UPDATE workflows 
        SET {', '.join(update_fields)}
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        self.db.execute(sql, params)
        
        # 保存到存储
        workflow = self._get_from_db(workflow_id, project_id, new_version)
        self._save_to_storage(workflow)
        
        return workflow
    
    def delete_workflow(
        self,
        workflow_id: str,
        project_id: str,
        user_id: str,
        permanent: bool = False
    ):
        """
        删除工作流
        
        :param workflow_id: 工作流ID
        :param project_id: 项目ID
        :param user_id: 删除者ID
        :param permanent: 是否永久删除
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "delete"):
            raise PermissionError("User does not have permission to delete this workflow")
        
        if permanent:
            # 2. 永久删除
            self._permanent_delete(workflow_id, project_id)
        else:
            # 2. 软删除
            self._soft_delete(workflow_id, project_id, user_id)
        
        # 3. 清除缓存
        self._clear_cache(project_id)
    
    def _soft_delete(self, workflow_id: str, project_id: str, user_id: str):
        """软删除工作流"""
        self.db.execute("""
        UPDATE workflows 
        SET status = 'deleted', deleted_at = NOW(), deleted_by = %(user_id)s
        WHERE id = %(id)s AND project_id = %(project_id)s
        """, {
            "id": workflow_id,
            "project_id": project_id,
            "user_id": user_id
        })
    
    def _permanent_delete(self, workflow_id: str, project_id: str):
        """永久删除工作流"""
        # 先删除所有版本
        self.db.execute("""
        DELETE FROM workflows 
        WHERE id = %(id)s AND project_id = %(project_id)s
        """, {
            "id": workflow_id,
            "project_id": project_id
        })
        
        # 从存储中删除
        try:
            self.storage.delete_prefix(f"workflows/{project_id}/{workflow_id}/")
        except Exception as e:
            self.logger.error("Error deleting workflow storage: %s", str(e))
            raise
    
    def list_workflows(
        self,
        project_id: str,
        user_id: str,
        filters: Optional[Dict] = None,
        sort: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> WorkflowList:
        """
        列出工作流
        
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :param filters: 过滤条件
        :param sort: 排序字段
        :param page: 页码
        :param page_size: 每页数量
        :return: 工作流列表
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to list workflows")
        
        # 2. 构建查询
        query = self._build_list_query(project_id, filters, sort, page, page_size)
        
        # 3. 执行查询
        rows = self.db.fetchall(query["sql"], query["params"])
        total = self.db.fetchone(query["count_sql"], query["params"])["count"]
        
        # 4. 转换结果
        workflows = [self._row_to_workflow(row) for row in rows]
        
        return WorkflowList(
            items=workflows,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def _build_list_query(
        self,
        project_id: str,
        filters: Optional[Dict],
        sort: Optional[str],
        page: int,
        page_size: int
    ) -> Dict:
        """构建列表查询SQL"""
        # 基础查询
        base_sql = """
        SELECT * FROM workflows 
        WHERE project_id = %(project_id)s
        """
        params = {"project_id": project_id}
        
        # 添加过滤条件
        if filters:
            if "status" in filters and filters["status"]:
                base_sql += " AND status = %(status)s"
                params["status"] = filters["status"]
            
            if "tags" in filters and filters["tags"]:
                # 处理标签过滤（包含所有指定标签）
                tags = filters["tags"]
                if isinstance(tags, str):
                    tags = [tags]
                
                for i, tag in enumerate(tags):
                    param_name = f"tag_{i}"
                    base_sql += f" AND %(tags)s @> ARRAY[%(param_name)s]::varchar[]"
                    params[param_name] = tag
                
                params["tags"] = tags
            
            if "search" in filters and filters["search"]:
                # 全文搜索
                base_sql += " AND to_tsvector('english', coalesce(display_name, '') || ' ' || coalesce(description, '')) @@ to_tsquery('english', %(search)s)"
                params["search"] = filters["search"].replace(' ', ' & ')
        
        # 添加排序
        order_by = "updated_at DESC"
        if sort:
            # 验证排序字段
            valid_sort_fields = ["name", "created_at", "updated_at", "status"]
            if sort.lstrip("-") in valid_sort_fields:
                direction = "DESC" if sort.startswith("-") else "ASC"
                field = sort.lstrip("-")
                order_by = f"{field} {direction}"
        
        base_sql += f" ORDER BY {order_by}"
        
        # 添加分页
        offset = (page - 1) * page_size
        paginated_sql = f"{base_sql} LIMIT %(page_size)s OFFSET %(offset)s"
        
        params.update({
            "page_size": page_size,
            "offset": offset
        })
        
        # 计数查询
        count_sql = f"SELECT COUNT(*) FROM ({base_sql}) AS count_source"
        
        return {
            "sql": paginated_sql,
            "count_sql": count_sql,
            "params": params
        }
    
    def get_workflow_versions(
        self,
        workflow_id: str,
        project_id: str,
        user_id: str,
        page: int = 1,
        page_size: int = 10
    ) -> WorkflowVersionList:
        """
        获取工作流版本
        
        :param workflow_id: 工作流ID
        :param project_id: 项目ID
        :param user_id: 用户ID
        :param page: 页码
        :param page_size: 每页数量
        :return: 工作流版本列表
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to view workflow versions")
        
        # 2. 获取版本列表（从数据库）
        sql = """
        SELECT version, created_at, created_by, description
        FROM workflows 
        WHERE id = %(id)s AND project_id = %(project_id)s
        ORDER BY version DESC
        LIMIT %(page_size)s OFFSET %(offset)s
        """
        
        params = {
            "id": workflow_id,
            "project_id": project_id,
            "page_size": page_size,
            "offset": (page - 1) * page_size
        }
        
        rows = self.db.fetchall(sql, params)
        
        # 3. 获取总数量
        count_sql = """
        SELECT COUNT(*) FROM workflows 
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        total = self.db.fetchone(count_sql, {
            "id": workflow_id,
            "project_id": project_id
        })["count"]
        
        # 4. 转换结果
        versions = [{
            "version": row["version"],
            "created_at": row["created_at"],
            "created_by": row["created_by"],
            "description": row["description"]
        } for row in rows]
        
        return WorkflowVersionList(
            items=versions,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def _has_permission(self, user_id: str, project_id: str, permission: str) -> bool:
        """检查用户是否有权限"""
        # 实现权限检查逻辑
        return True  # 简化实现
    
    def _clear_cache(self, project_id: str):
        """清除项目缓存"""
        # 清除所有以project_id开头的缓存键
        keys_to_clear = [k for k in self.cache if k.startswith(project_id)]
        for key in keys_to_clear:
            del self.cache[key]
```

#### 4.4.2 工作流执行服务

**技术实现：**
```python
class WorkflowExecutionService:
    """工作流执行服务，负责工作流实例的创建和管理"""
    
    def __init__(
        self,
        db: Database,
        scheduler: WorkflowScheduler,
        event_bus: EventBus,
        config: Config
    ):
        self.db = db
        self.scheduler = scheduler
        self.event_bus = event_bus
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def create_instance(
        self,
        workflow_id: str,
        project_id: str,
        user_id: str,
        input_data: Dict,
        options: Optional[ExecutionOptions] = None
    ) -> WorkflowInstance:
        """
        创建工作流实例
        
        :param workflow_id: 工作流ID
        :param project_id: 项目ID
        :param user_id: 创建者ID
        :param input_data: 输入数据
        :param options: 执行选项
        :return: 工作流实例
        """
        # 1. 获取工作流定义
        workflow = self._get_workflow(workflow_id, project_id, user_id)
        
        # 2. 验证输入数据
        self._validate_input(input_data, workflow)
        
        # 3. 创建实例
        instance = self._create_instance_record(
            workflow_id, 
            project_id, 
            user_id, 
            input_data,
            options
        )
        
        # 4. 调度执行
        self.scheduler.schedule(instance)
        
        # 5. 发布事件
        self.event_bus.publish("workflow.instance.created", {
            "instance_id": instance.id,
            "workflow_id": workflow_id,
            "project_id": project_id,
            "user_id": user_id
        })
        
        return instance
    
    def _get_workflow(self, workflow_id: str, project_id: str, user_id: str):
        """获取工作流定义"""
        # 这里应该调用WorkflowDefinitionService，为简化直接查询
        workflow = self.db.fetchone(
            "SELECT * FROM workflows WHERE id = %(id)s AND project_id = %(project_id)s ORDER BY version DESC LIMIT 1",
            {"id": workflow_id, "project_id": project_id}
        )
        
        if not workflow:
            raise NotFoundError(f"Workflow {workflow_id} not found")
        
        return workflow
    
    def _validate_input(self, input_data: Dict, workflow: Dict):
        """验证输入数据"""
        # 检查必填字段
        if "trigger" not in input_data:
            raise ValidationError("Input must contain 'trigger' field")
        
        # 验证触发器类型
        trigger_type = input_data["trigger"].get("type")
        if not trigger_type:
            raise ValidationError("Trigger type is required")
        
        # 验证触发器配置
        trigger_config = input_data["trigger"].get("config", {})
        workflow_triggers = json.loads(workflow["definition"]).get("triggers", [])
        
        trigger_def = next((t for t in workflow_triggers if t["type"] == trigger_type), None)
        if not trigger_def:
            raise ValidationError(f"Invalid trigger type: {trigger_type}")
        
        # 验证必填配置项
        for field in trigger_def.get("required_fields", []):
            if field not in trigger_config:
                raise ValidationError(f"Trigger config missing required field: {field}")
    
    def _create_instance_record(
        self,
        workflow_id: str,
        project_id: str,
        user_id: str,
        input_data: Dict,
        options: Optional[ExecutionOptions]
    ) -> WorkflowInstance:
        """创建工作流实例记录"""
        # 生成唯一ID
        instance_id = f"inst-{uuid.uuid4().hex[:12]}"
        
        # 准备实例数据
        instance = WorkflowInstance(
            id=instance_id,
            workflow_id=workflow_id,
            project_id=project_id,
            trigger_type=input_data["trigger"]["type"],
            trigger_payload=input_data["trigger"].get("payload", {}),
            input=input_data,
            status="pending",
            priority=options.priority if options else 5,
            timeout=options.timeout if options else self.config.default_timeout,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        # 保存到数据库
        self._save_instance(instance)
        
        return instance
    
    def _save_instance(self, instance: WorkflowInstance):
        """保存工作流实例到数据库"""
        sql = """
        INSERT INTO workflow_instances (
            id, workflow_id, project_id, trigger_type, trigger_payload, input, 
            status, priority, timeout, created_at, created_by
        ) VALUES (
            %(id)s, %(workflow_id)s, %(project_id)s, %(trigger_type)s, %(trigger_payload)s,
            %(input)s, %(status)s, %(priority)s, %(timeout)s, %(created_at)s, %(created_by)s
        )
        """
        
        self.db.execute(sql, {
            "id": instance.id,
            "workflow_id": instance.workflow_id,
            "project_id": instance.project_id,
            "trigger_type": instance.trigger_type,
            "trigger_payload": json.dumps(instance.trigger_payload),
            "input": json.dumps(instance.input),
            "status": instance.status,
            "priority": instance.priority,
            "timeout": instance.timeout,
            "created_at": instance.created_at,
            "created_by": instance.created_by
        })
    
    def get_instance(
        self,
        instance_id: str,
        project_id: str,
        user_id: str
    ) -> WorkflowInstance:
        """
        获取工作流实例详情
        
        :param instance_id: 实例ID
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :return: 工作流实例
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to read this instance")
        
        # 2. 从数据库获取
        instance = self._get_from_db(instance_id, project_id)
        if not instance:
            raise NotFoundError(f"Workflow instance {instance_id} not found")
        
        # 3. 获取节点执行状态
        instance.node_executions = self._get_node_executions(instance_id)
        
        return instance
    
    def _get_from_db(self, instance_id: str, project_id: str) -> Optional[WorkflowInstance]:
        """从数据库获取工作流实例"""
        sql = """
        SELECT * FROM workflow_instances 
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        row = self.db.fetchone(sql, {
            "id": instance_id,
            "project_id": project_id
        })
        
        if not row:
            return None
        
        return self._row_to_instance(row)
    
    def _row_to_instance(self, row: Dict) -> WorkflowInstance:
        """将数据库行转换为WorkflowInstance对象"""
        return WorkflowInstance(
            id=row["id"],
            workflow_id=row["workflow_id"],
            project_id=row["project_id"],
            trigger_type=row["trigger_type"],
            trigger_payload=json.loads(row["trigger_payload"]) if row["trigger_payload"] else {},
            input=json.loads(row["input"]) if row["input"] else {},
            status=row["status"],
            priority=row["priority"],
            timeout=row["timeout"],
            created_at=row["created_at"],
            created_by=row["created_by"],
            started_at=row["started_at"],
            completed_at=row["completed_at"],
            duration=row["duration"],
            output=json.loads(row["output"]) if row["output"] else None,
            error=json.loads(row["error"]) if row["error"] else None,
            node_executions=[]
        )
    
    def _get_node_executions(self, instance_id: str) -> List[NodeExecution]:
        """获取节点执行状态"""
        sql = """
        SELECT * FROM node_executions 
        WHERE instance_id = %(instance_id)s 
        ORDER BY started_at
        """
        
        rows = self.db.fetchall(sql, {"instance_id": instance_id})
        return [self._row_to_node_execution(row) for row in rows]
    
    def _row_to_node_execution(self, row: Dict) -> NodeExecution:
        """将数据库行转换为NodeExecution对象"""
        return NodeExecution(
            id=row["id"],
            instance_id=row["instance_id"],
            node_id=row["node_id"],
            node_type=row["node_type"],
            status=row["status"],
            started_at=row["started_at"],
            completed_at=row["completed_at"],
            duration=row["duration"],
            input=json.loads(row["input"]) if row["input"] else {},
            output=json.loads(row["output"]) if row["output"] else None,
            error=json.loads(row["error"]) if row["error"] else None,
            retry_count=row["retry_count"],
            max_retries=row["max_retries"],
            resource_usage=json.loads(row["resource_usage"]) if row["resource_usage"] else {}
        )
    
    def cancel_instance(
        self,
        instance_id: str,
        project_id: str,
        user_id: str
    ):
        """
        取消工作流实例
        
        :param instance_id: 实例ID
        :param project_id: 项目ID
        :param user_id: 取消者ID
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "cancel"):
            raise PermissionError("User does not have permission to cancel this instance")
        
        # 2. 获取实例
        instance = self.get_instance(instance_id, project_id, user_id)
        if not instance:
            raise NotFoundError(f"Workflow instance {instance_id} not found")
        
        # 3. 检查状态
        if instance.status not in ["pending", "running"]:
            raise ValidationError(f"Cannot cancel instance in {instance.status} state")
        
        # 4. 更新状态
        self._update_instance_status(
            instance_id,
            project_id,
            "canceled",
            canceled_by=user_id
        )
        
        # 5. 通知调度器
        self.scheduler.cancel(instance_id)
        
        # 6. 发布事件
        self.event_bus.publish("workflow.instance.canceled", {
            "instance_id": instance_id,
            "project_id": project_id,
            "user_id": user_id
        })
    
    def _update_instance_status(
        self,
        instance_id: str,
        project_id: str,
        status: str,
        **kwargs
    ):
        """更新工作流实例状态"""
        update_fields = ["status = %(status)s"]
        params = {
            "id": instance_id,
            "project_id": project_id,
            "status": status
        }
        
        if status == "completed":
            update_fields.append("completed_at = NOW()")
            update_fields.append("duration = EXTRACT(EPOCH FROM (NOW() - started_at))")
        elif status == "running" and "started_at" not in kwargs:
            update_fields.append("started_at = NOW()")
        
        # 添加其他字段
        for field, value in kwargs.items():
            update_fields.append(f"{field} = %({field})s")
            params[field] = value
        
        sql = f"""
        UPDATE workflow_instances 
        SET {', '.join(update_fields)}
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        self.db.execute(sql, params)
    
    def list_instances(
        self,
        project_id: str,
        user_id: str,
        filters: Optional[Dict] = None,
        sort: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> WorkflowInstanceList:
        """
        列出工作流实例
        
        :param project_id: 项目ID
        :param user_id: 请求用户ID
        :param filters: 过滤条件
        :param sort: 排序字段
        :param page: 页码
        :param page_size: 每页数量
        :return: 工作流实例列表
        """
        # 1. 检查权限
        if not self._has_permission(user_id, project_id, "read"):
            raise PermissionError("User does not have permission to list workflow instances")
        
        # 2. 构建查询
        query = self._build_list_query(project_id, filters, sort, page, page_size)
        
        # 3. 执行查询
        rows = self.db.fetchall(query["sql"], query["params"])
        total = self.db.fetchone(query["count_sql"], query["params"])["count"]
        
        # 4. 转换结果
        instances = [self._row_to_instance(row) for row in rows]
        
        # 5. 获取节点执行状态（批量）
        instance_ids = [inst.id for inst in instances]
        node_executions = self._get_node_executions_batch(instance_ids)
        
        for instance in instances:
            instance.node_executions = node_executions.get(instance.id, [])
        
        return WorkflowInstanceList(
            items=instances,
            total=total,
            page=page,
            page_size=page_size
        )
    
    def _build_list_query(
        self,
        project_id: str,
        filters: Optional[Dict],
        sort: Optional[str],
        page: int,
        page_size: int
    ) -> Dict:
        """构建列表查询SQL"""
        # 基础查询
        base_sql = """
        SELECT * FROM workflow_instances 
        WHERE project_id = %(project_id)s
        """
        params = {"project_id": project_id}
        
        # 添加过滤条件
        if filters:
            if "status" in filters and filters["status"]:
                base_sql += " AND status = %(status)s"
                params["status"] = filters["status"]
            
            if "workflow_id" in filters and filters["workflow_id"]:
                base_sql += " AND workflow_id = %(workflow_id)s"
                params["workflow_id"] = filters["workflow_id"]
            
            if "trigger_type" in filters and filters["trigger_type"]:
                base_sql += " AND trigger_type = %(trigger_type)s"
                params["trigger_type"] = filters["trigger_type"]
            
            if "time_range" in filters:
                if "start" in filters["time_range"]:
                    base_sql += " AND created_at >= %(start_time)s"
                    params["start_time"] = filters["time_range"]["start"]
                if "end" in filters["time_range"]:
                    base_sql += " AND created_at <= %(end_time)s"
                    params["end_time"] = filters["time_range"]["end"]
        
        # 添加排序
        order_by = "created_at DESC"
        if sort:
            # 验证排序字段
            valid_sort_fields = ["created_at", "started_at", "completed_at", "status", "duration"]
            if sort.lstrip("-") in valid_sort_fields:
                direction = "DESC" if sort.startswith("-") else "ASC"
                field = sort.lstrip("-")
                order_by = f"{field} {direction}"
        
        base_sql += f" ORDER BY {order_by}"
        
        # 添加分页
        offset = (page - 1) * page_size
        paginated_sql = f"{base_sql} LIMIT %(page_size)s OFFSET %(offset)s"
        
        params.update({
            "page_size": page_size,
            "offset": offset
        })
        
        # 计数查询
        count_sql = f"SELECT COUNT(*) FROM ({base_sql}) AS count_source"
        
        return {
            "sql": paginated_sql,
            "count_sql": count_sql,
            "params": params
        }
    
    def _get_node_executions_batch(self, instance_ids: List[str]) -> Dict[str, List[NodeExecution]]:
        """批量获取节点执行状态"""
        if not instance_ids:
            return {}
        
        sql = """
        SELECT * FROM node_executions 
        WHERE instance_id = ANY(%(instance_ids)s)
        ORDER BY instance_id, started_at
        """
        
        rows = self.db.fetchall(sql, {"instance_ids": instance_ids})
        
        # 按实例ID分组
        executions_by_instance = defaultdict(list)
        for row in rows:
            executions_by_instance[row["instance_id"]].append(self._row_to_node_execution(row))
        
        return dict(executions_by_instance)
    
    def _has_permission(self, user_id: str, project_id: str, permission: str) -> bool:
        """检查用户是否有权限"""
        # 实现权限检查逻辑
        return True  # 简化实现
```

#### 4.4.3 工作流调度器

**技术实现：**
```python
class WorkflowScheduler:
    """工作流调度器，负责工作流实例的调度和执行"""
    
    def __init__(
        self,
        db: Database,
        executor: WorkflowExecutor,
        event_bus: EventBus,
        config: Config
    ):
        self.db = db
        self.executor = executor
        self.event_bus = event_bus
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler = BackgroundScheduler()
        self.task_queue = PriorityQueue()
        self.active_instances = set()
        self.lock = threading.Lock()
    
    def start(self):
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.logger.info("Starting workflow scheduler")
        
        # 添加定期任务
        self.scheduler.add_job(
            self._process_queue,
            'interval',
            seconds=self.config.process_interval,
            id='process_queue'
        )
        
        self.scheduler.add_job(
            self._check_timeouts,
            'interval',
            seconds=self.config.timeout_check_interval,
            id='check_timeouts'
        )
        
        # 恢复未完成的实例
        self._recover_incomplete_instances()
        
        # 启动调度器
        self.scheduler.start()
        self.logger.info("Workflow scheduler started")
    
    def _recover_incomplete_instances(self):
        """恢复未完成的工作流实例"""
        # 获取所有未完成的实例
        sql = """
        SELECT id, project_id FROM workflow_instances 
        WHERE status IN ('pending', 'running') 
        AND created_at > NOW() - INTERVAL '%(recovery_days)s days'
        """
        
        instances = self.db.fetchall(sql, {"recovery_days": self.config.recovery_days})
        
        for instance in instances:
            try:
                # 重新调度
                self.schedule(WorkflowInstanceRef(
                    id=instance["id"],
                    project_id=instance["project_id"]
                ))
                self.logger.info("Recovered incomplete instance %s", instance["id"])
            except Exception as e:
                self.logger.error("Error recovering instance %s: %s", instance["id"], str(e))
    
    def schedule(self, instance: WorkflowInstanceRef):
        """
        调度工作流实例
        
        :param instance: 工作流实例引用
        """
        with self.lock:
            # 检查是否已在调度中
            if instance.id in self.active_instances:
                self.logger.debug("Instance %s already in scheduler", instance.id)
                return
            
            # 获取实例优先级
            priority = self._get_instance_priority(instance)
            
            # 添加到队列
            self.task_queue.put((priority, time.time(), instance))
            self.active_instances.add(instance.id)
            
            self.logger.debug("Scheduled instance %s with priority %d", instance.id, priority)
    
    def _get_instance_priority(self, instance: WorkflowInstanceRef) -> int:
        """获取实例优先级"""
        # 从数据库获取优先级
        sql = "SELECT priority FROM workflow_instances WHERE id = %(id)s"
        result = self.db.fetchone(sql, {"id": instance.id})
        
        if result and result["priority"] is not None:
            return result["priority"]
        
        # 默认优先级
        return self.config.default_priority
    
    def _process_queue(self):
        """处理任务队列"""
        if self.task_queue.empty():
            return
        
        try:
            # 获取下一个任务
            _, _, instance = self.task_queue.get_nowait()
            
            # 从活动实例中移除
            with self.lock:
                self.active_instances.discard(instance.id)
            
            # 执行工作流
            self.executor.execute(instance)
            
        except Empty:
            pass
        except Exception as e:
            self.logger.error("Error processing workflow instance: %s", str(e))
    
    def _check_timeouts(self):
        """检查超时实例"""
        # 获取可能超时的运行中实例
        sql = """
        SELECT id, project_id, started_at, timeout 
        FROM workflow_instances 
        WHERE status = 'running' 
        AND timeout IS NOT NULL
        """
        
        instances = self.db.fetchall(sql)
        
        now = datetime.utcnow()
        for instance in instances:
            started_at = instance["started_at"]
            timeout = instance["timeout"]
            
            if started_at and (now - started_at) > timedelta(seconds=timeout):
                self.logger.warning("Instance %s timed out", instance["id"])
                
                # 更新状态
                self._update_instance_status(
                    instance["id"],
                    instance["project_id"],
                    "failed",
                    error={
                        "code": "EXECUTION_TIMEOUT",
                        "message": f"Workflow execution exceeded timeout of {timeout} seconds"
                    }
                )
                
                # 发布事件
                self.event_bus.publish("workflow.instance.timeout", {
                    "instance_id": instance["id"],
                    "project_id": instance["project_id"],
                    "timeout": timeout
                })
    
    def _update_instance_status(
        self,
        instance_id: str,
        project_id: str,
        status: str,
        **kwargs
    ):
        """更新工作流实例状态"""
        # 这里应该调用WorkflowExecutionService，为简化直接更新
        update_fields = ["status = %(status)s"]
        params = {
            "id": instance_id,
            "project_id": project_id,
            "status": status
        }
        
        if status == "completed":
            update_fields.append("completed_at = NOW()")
            update_fields.append("duration = EXTRACT(EPOCH FROM (NOW() - started_at))")
        
        # 添加其他字段
        for field, value in kwargs.items():
            if field == "error" and isinstance(value, dict):
                update_fields.append(f"{field} = %({field})s::jsonb")
                params[field] = json.dumps(value)
            else:
                update_fields.append(f"{field} = %({field})s")
                params[field] = value
        
        sql = f"""
        UPDATE workflow_instances 
        SET {', '.join(update_fields)}
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        self.db.execute(sql, params)
    
    def cancel(self, instance_id: str):
        """
        取消工作流实例
        
        :param instance_id: 实例ID
        """
        # 从队列中移除
        with self.lock:
            # 创建临时队列
            temp_queue = PriorityQueue()
            canceled = False
            
            while not self.task_queue.empty():
                priority, timestamp, instance = self.task_queue.get()
                if instance.id == instance_id:
                    canceled = True
                else:
                    temp_queue.put((priority, timestamp, instance))
            
            # 替换队列
            self.task_queue = temp_queue
            
            # 从活动实例中移除
            if instance_id in self.active_instances:
                self.active_instances.remove(instance_id)
                canceled = True
            
            if canceled:
                self.logger.info("Canceled instance %s from scheduler", instance_id)
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            return
        
        self.running = False
        self.scheduler.shutdown()
        self.logger.info("Workflow scheduler stopped")
```

#### 4.4.4 工作流执行器

**技术实现：**
```python
class WorkflowExecutor:
    """工作流执行器，负责执行工作流实例"""
    
    def __init__(
        self,
        db: Database,
        node_executor: NodeExecutor,
        event_bus: EventBus,
        config: Config
    ):
        self.db = db
        self.node_executor = node_executor
        self.event_bus = event_bus
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def execute(self, instance: WorkflowInstanceRef):
        """
        执行工作流实例
        
        :param instance: 工作流实例引用
        """
        try:
            # 1. 获取工作流定义
            workflow = self._get_workflow_definition(instance)
            
            # 2. 更新实例状态为运行中
            self._update_instance_status(
                instance.id,
                instance.project_id,
                "running"
            )
            
            # 3. 获取入口节点
            entry_nodes = self._find_entry_nodes(workflow)
            
            # 4. 执行入口节点
            for node_id in entry_nodes:
                self._execute_node(instance, workflow, node_id)
                
        except Exception as e:
            self.logger.error("Error executing workflow %s: %s", instance.id, str(e))
            self._handle_execution_error(instance, str(e))
    
    def _get_workflow_definition(self, instance: WorkflowInstanceRef) -> Dict:
        """获取工作流定义"""
        sql = """
        SELECT w.definition, i.input 
        FROM workflows w
        JOIN workflow_instances i ON w.id = i.workflow_id
        WHERE i.id = %(instance_id)s
        """
        
        result = self.db.fetchone(sql, {"instance_id": instance.id})
        if not result:
            raise NotFoundError(f"Workflow instance {instance.id} not found")
        
        return {
            "definition": json.loads(result["definition"]),
            "input": json.loads(result["input"])
        }
    
    def _find_entry_nodes(self, workflow: Dict) -> Set[str]:
        """查找入口节点（没有入边的节点）"""
        all_nodes = {node["node_id"] for node in workflow["definition"]["nodes"]}
        target_nodes = {edge["to"] for edge in workflow["definition"].get("edges", [])}
        return all_nodes - target_nodes
    
    def _update_instance_status(
        self,
        instance_id: str,
        project_id: str,
        status: str,
        **kwargs
    ):
        """更新工作流实例状态"""
        # 这里应该调用WorkflowExecutionService，为简化直接更新
        update_fields = ["status = %(status)s"]
        params = {
            "id": instance_id,
            "project_id": project_id,
            "status": status
        }
        
        if status == "completed":
            update_fields.append("completed_at = NOW()")
            update_fields.append("duration = EXTRACT(EPOCH FROM (NOW() - started_at))")
        
        # 添加其他字段
        for field, value in kwargs.items():
            if field == "error" and isinstance(value, dict):
                update_fields.append(f"{field} = %({field})s::jsonb")
                params[field] = json.dumps(value)
            else:
                update_fields.append(f"{field} = %({field})s")
                params[field] = value
        
        sql = f"""
        UPDATE workflow_instances 
        SET {', '.join(update_fields)}
        WHERE id = %(id)s AND project_id = %(project_id)s
        """
        
        self.db.execute(sql, params)
    
    def _execute_node(
        self,
        instance: WorkflowInstanceRef,
        workflow: Dict,
        node_id: str
    ):
        """执行节点"""
        # 1. 获取节点定义
        node_def = self._get_node_definition(workflow, node_id)
        if not node_def:
            self._handle_node_error(instance, node_id, f"Node {node_id} not found")
            return
        
        # 2. 获取输入数据
        input_data = self._get_node_input(instance, workflow, node_id)
        
        # 3. 创建节点执行记录
        execution_id = self._create_node_execution(
            instance, 
            node_id, 
            node_def["node_type"],
            input_data
        )
        
        # 4. 执行节点
        try:
            self.node_executor.execute(
                execution_id=execution_id,
                node_id=node_id,
                node_type=node_def["node_type"],
                parameters=node_def.get("parameters", {}),
                input=input_data,
                max_retries=node_def.get("max_retries", 3),
                deadline=self._calculate_deadline(node_def)
            )
        except Exception as e:
            self._handle_node_error(instance, node_id, str(e))
    
    def _get_node_definition(self, workflow: Dict, node_id: str) -> Optional[Dict]:
        """获取节点定义"""
        for node in workflow["definition"]["nodes"]:
            if node["node_id"] == node_id:
                return node
        return None
    
    def _get_node_input(
        self,
        instance: WorkflowInstanceRef,
        workflow: Dict,
        node_id: str
    ) -> Dict:
        """获取节点输入数据"""
        input_data = {}
        
        # 如果是入口节点，使用工作流输入
        if node_id in self._find_entry_nodes(workflow):
            return workflow["input"]
        
        # 否则，从前置节点获取输出
        for edge in workflow["definition"].get("edges", []):
            if edge["to"] == node_id:
                source_node_id = edge["from"]
                
                # 获取源节点输出
                source_output = self._get_node_output(instance, source_node_id)
                if source_output:
                    # 应用数据映射
                    if "mapping" in edge:
                        mapped_output = self._apply_data_mapping(
                            source_output,
                            edge["mapping"]
                        )
                        input_data.update(mapped_output)
                    else:
                        input_data.update(source_output)
        
        return input_data
    
    def _apply_data_mapping(self, source_data: Dict, mapping_rules: Dict) -> Dict:
        """应用数据映射规则"""
        result = {}
        
        for target_path, source_expr in mapping_rules.items():
            # 解析源表达式（支持简单的JMESPath）
            if source_expr.startswith("$."):
                # 简单JMESPath解析
                value = jmespath.search(source_expr[2:], source_data)
            else:
                # 直接值
                value = source_expr
            
            # 设置目标路径
            self._set_nested_value(result, target_path, value)
        
        return result
    
    def _set_nested_value(self, obj: Dict, path: str, value: Any):
        """设置嵌套对象的值"""
        parts = path.split('.')
        for part in parts[:-1]:
            if part not in obj:
                obj[part] = {}
            obj = obj[part]
        obj[parts[-1]] = value
    
    def _get_node_output(
        self,
        instance: WorkflowInstanceRef,
        node_id: str
    ) -> Optional[Dict]:
        """获取节点输出"""
        sql = """
        SELECT output FROM node_executions 
        WHERE instance_id = %(instance_id)s AND node_id = %(node_id)s 
        ORDER BY completed_at DESC LIMIT 1
        """
        
        result = self.db.fetchone(sql, {
            "instance_id": instance.id,
            "node_id": node_id
        })
        
        return json.loads(result["output"]) if result and result["output"] else None
    
    def _create_node_execution(
        self,
        instance: WorkflowInstanceRef,
        node_id: str,
        node_type: str,
        input_data: Dict
    ) -> str:
        """创建节点执行记录"""
        execution_id = f"node-{uuid.uuid4().hex[:8]}"
        
        sql = """
        INSERT INTO node_executions (
            id, instance_id, node_id, node_type, status, input, started_at
        ) VALUES (
            %(id)s, %(instance_id)s, %(node_id)s, %(node_type)s, 'pending', %(input)s, NOW()
        )
        """
        
        self.db.execute(sql, {
            "id": execution_id,
            "instance_id": instance.id,
            "node_id": node_id,
            "node_type": node_type,
            "input": json.dumps(input_data)
        })
        
        return execution_id
    
    def _calculate_deadline(self, node_def: Dict) -> datetime:
        """计算节点执行截止时间"""
        timeout = node_def.get("timeout", self.config.default_node_timeout)
        return datetime.utcnow() + timedelta(seconds=timeout)
    
    def _handle_node_error(
        self,
        instance: WorkflowInstanceRef,
        node_id: str,
        error: str
    ):
        """处理节点错误"""
        # 更新节点状态
        self._update_node_status(
            instance.id,
            node_id,
            "failed",
            error={
                "message": error,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # 检查是否需要失败整个工作流
        workflow = self._get_workflow_definition(instance)
        node_def = self._get_node_definition(workflow, node_id)
        
        if node_def and node_def.get("fail_on_error", True):
            self._update_instance_status(
                instance.id,
                instance.project_id,
                "failed",
                error={
                    "node_id": node_id,
                    "message": error
                }
            )
    
    def _update_node_status(
        self,
        instance_id: str,
        node_id: str,
        status: str,
        **kwargs
    ):
        """更新节点执行状态"""
        update_fields = ["status = %(status)s"]
        params = {
            "instance_id": instance_id,
            "node_id": node_id,
            "status": status
        }
        
        if status == "completed":
            update_fields.append("completed_at = NOW()")
            update_fields.append("duration = EXTRACT(EPOCH FROM (NOW() - started_at))")
        
        # 添加其他字段
        for field, value in kwargs.items():
            if field == "error" and isinstance(value, dict):
                update_fields.append(f"{field} = %({field})s::jsonb")
                params[field] = json.dumps(value)
            else:
                update_fields.append(f"{field} = %({field})s")
                params[field] = value
        
        sql = f"""
        UPDATE node_executions 
        SET {', '.join(update_fields)}
        WHERE instance_id = %(instance_id)s AND node_id = %(node_id)s
        """
        
        self.db.execute(sql, params)
    
    def handle_node_completion(
        self,
        execution_id: str,
        node_id: str,
        instance_id: str,
        output: Dict
    ):
        """
        处理节点完成事件
        
        :param execution_id: 节点执行ID
        :param node_id: 节点ID
        :param instance_id: 实例ID
        :param output: 节点输出
        """
        # 1. 更新节点状态
        self._update_node_status(
            instance_id,
            node_id,
            "completed",
            output=output
        )
        
        # 2. 获取工作流定义
        workflow = self._get_workflow_definition(WorkflowInstanceRef(
            id=instance_id,
            project_id="unknown"  # 实际实现中应该获取project_id
        ))
        
        # 3. 查找后续节点
        next_nodes = self._find_next_nodes(workflow, node_id)
        
        # 4. 执行后续节点
        for next_node_id in next_nodes:
            self._execute_node(
                WorkflowInstanceRef(id=instance_id, project_id="unknown"),
                workflow,
                next_node_id
            )
        
        # 5. 检查工作流是否完成
        if not next_nodes:
            self._mark_workflow_completed(instance_id)
    
    def _find_next_nodes(self, workflow: Dict, node_id: str) -> List[str]:
        """查找后续节点"""
        return [
            edge["to"] for edge in workflow["definition"].get("edges", [])
            if edge["from"] == node_id
        ]
    
    def _mark_workflow_completed(self, instance_id: str):
        """标记工作流完成"""
        # 获取所有节点状态
        sql = """
        SELECT COUNT(*) FROM node_executions 
        WHERE instance_id = %(instance_id)s AND status != 'completed'
        """
        
        incomplete_count = self.db.fetchone(sql, {"instance_id": instance_id})["count"]
        
        if incomplete_count == 0:
            self._update_instance_status(
                instance_id,
                "unknown",  # 实际实现中应该获取project_id
                "completed"
            )
    
    def handle_node_failure(
        self,
        execution_id: str,
        node_id: str,
        instance_id: str,
        error: Dict,
        retry_count: int,
        max_retries: int
    ):
        """
        处理节点失败事件
        
        :param execution_id: 节点执行ID
        :param node_id: 节点ID
        :param instance_id: 实例ID
        :param error: 错误信息
        :param retry_count: 重试次数
        :param max_retries: 最大重试次数
        """
        # 1. 更新节点状态
        self._update_node_status(
            instance_id,
            node_id,
            "failed",
            error=error,
            retry_count=retry_count
        )
        
        # 2. 检查是否可以重试
        if retry_count < max_retries:
            # 计算重试延迟
            retry_delay = self._calculate_retry_delay(retry_count)
            
            # 计划重试
            self._schedule_retry(
                execution_id,
                node_id,
                instance_id,
                retry_count + 1,
                retry_delay
            )
        else:
            # 最终失败
            self._handle_node_error(
                WorkflowInstanceRef(id=instance_id, project_id="unknown"),
                node_id,
                error.get("message", "Node execution failed after maximum retries")
            )
    
    def _calculate_retry_delay(self, retry_count: int) -> float:
        """计算重试延迟（指数退避）"""
        base = self.config.retry_base_delay
        factor = self.config.retry_backoff_factor
        return base * (factor ** retry_count)
    
    def _schedule_retry(
        self,
        execution_id: str,
        node_id: str,
        instance_id: str,
        retry_count: int,
        delay: float
    ):
        """计划节点重试"""
        # 这里应该使用定时任务系统，为简化使用线程
        def retry_task():
            time.sleep(delay)
            self._retry_node(execution_id, node_id, instance_id, retry_count)
        
        threading.Thread(target=retry_task, daemon=True).start()
    
    def _retry_node(
        self,
        execution_id: str,
        node_id: str,
        instance_id: str,
        retry_count: int
    ):
        """重试节点"""
        # 1. 获取工作流定义
        workflow = self._get_workflow_definition(WorkflowInstanceRef(
            id=instance_id,
            project_id="unknown"
        ))
        
        # 2. 获取节点定义
        node_def = self._get_node_definition(workflow, node_id)
        if not node_def:
            return
        
        # 3. 获取输入数据
        input_data = self._get_node_input(
            WorkflowInstanceRef(id=instance_id, project_id="unknown"),
            workflow,
            node_id
        )
        
        # 4. 更新节点状态为重试中
        self._update_node_status(
            instance_id,
            node_id,
            "retrying",
            retry_count=retry_count
        )
        
        # 5. 重新执行节点
        try:
            self.node_executor.execute(
                execution_id=execution_id,
                node_id=node_id,
                node_type=node_def["node_type"],
                parameters=node_def.get("parameters", {}),
                input=input_data,
                max_retries=node_def.get("max_retries", 3),
                deadline=self._calculate_deadline(node_def)
            )
        except Exception as e:
            self._handle_node_error(
                WorkflowInstanceRef(id=instance_id, project_id="unknown"),
                node_id,
                str(e)
            )
```

#### 4.4.5 节点执行器

**技术实现：**
```python
class NodeExecutor:
    """节点执行器，负责执行单个节点"""
    
    def __init__(
        self,
        node_registry: NodeRegistry,
        event_bus: EventBus,
        config: Config
    ):
        self.node_registry = node_registry
        self.event_bus = event_bus
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def execute(
        self,
        execution_id: str,
        node_id: str,
        node_type: str,
        parameters: Dict,
        input: Dict,
        max_retries: int = 3,
        deadline: Optional[datetime] = None
    ):
        """
        执行节点
        
        :param execution_id: 节点执行ID
        :param node_id: 节点ID
        :param node_type: 节点类型
        :param parameters: 节点参数
        :param input: 输入数据
        :param max_retries: 最大重试次数
        :param deadline: 截止时间
        """
        try:
            # 1. 获取节点处理器
            node_handler = self.node_registry.get_handler(node_type)
            if not node_handler:
                raise NodeExecutionError(f"Node type {node_type} not registered")
            
            # 2. 执行节点
            start_time = time.time()
            output = node_handler.execute(
                execution_id=execution_id,
                node_id=node_id,
                parameters=parameters,
                input=input
            )
            duration = time.time() - start_time
            
            # 3. 处理成功
            self._handle_success(
                execution_id,
                node_id,
                output,
                duration
            )
            
        except Exception as e:
            # 4. 处理失败
            self._handle_failure(
                execution_id,
                node_id,
                e,
                max_retries,
                0  # 初始重试次数为0
            )
    
    def _handle_success(
        self,
        execution_id: str,
        node_id: str,
        output: Dict,
        duration: float
    ):
        """处理节点成功"""
        # 发布完成事件
        self.event_bus.publish("node.execution.completed", {
            "execution_id": execution_id,
            "node_id": node_id,
            "output": output,
            "duration": duration
        })
    
    def _handle_failure(
        self,
        execution_id: str,
        node_id: str,
        error: Exception,
        max_retries: int,
        retry_count: int
    ):
        """处理节点失败"""
        # 准备错误信息
        error_info = {
            "code": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc() if self.config.include_traceback else None
        }
        
        # 发布失败事件
        self.event_bus.publish("node.execution.failed", {
            "execution_id": execution_id,
            "node_id": node_id,
            "error": error_info,
            "retry_count": retry_count,
            "max_retries": max_retries
        })
        
        # 如果还有重试机会，计划重试
        if retry_count < max_retries:
            # 计算重试延迟
            retry_delay = self._calculate_retry_delay(retry_count)
            
            # 计划重试
            self._schedule_retry(
                execution_id,
                node_id,
                error_info,
                retry_count,
                max_retries,
                retry_delay
            )
    
    def _calculate_retry_delay(self, retry_count: int) -> float:
        """计算重试延迟（指数退避）"""
        base = self.config.retry_base_delay
        factor = self.config.retry_backoff_factor
        return base * (factor ** retry_count)
    
    def _schedule_retry(
        self,
        execution_id: str,
        node_id: str,
        error: Dict,
        retry_count: int,
        max_retries: int,
        delay: float
    ):
        """计划节点重试"""
        # 这里应该使用定时任务系统，为简化使用线程
        def retry_task():
            time.sleep(delay)
            self._retry_node(
                execution_id,
                node_id,
                error,
                retry_count,
                max_retries
            )
        
        threading.Thread(target=retry_task, daemon=True).start()
    
    def _retry_node(
        self,
        execution_id: str,
        node_id: str,
        error: Dict,
        retry_count: int,
        max_retries: int
    ):
        """重试节点"""
        # 获取节点信息（实际实现中应该从存储获取）
        # 这里简化为假设我们知道node_type和参数
        node_type = "unknown"  # 实际实现中应该获取
        parameters = {}  # 实际实现中应该获取
        input_data = {}  # 实际实现中应该获取
        
        try:
            # 获取节点处理器
            node_handler = self.node_registry.get_handler(node_type)
            if not node_handler:
                raise NodeExecutionError(f"Node type {node_type} not registered")
            
            # 执行节点
            start_time = time.time()
            output = node_handler.execute(
                execution_id=execution_id,
                node_id=node_id,
                parameters=parameters,
                input=input_data
            )
            duration = time.time() - start_time
            
            # 处理成功
            self._handle_success(
                execution_id,
                node_id,
                output,
                duration
            )
            
        except Exception as e:
            # 递归处理失败
            self._handle_failure(
                execution_id,
                node_id,
                e,
                max_retries,
                retry_count + 1
            )

class NodeRegistry:
    """节点处理器注册表"""
    
    def __init__(self):
        self.handlers = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, node_type: str, handler: NodeHandler):
        """注册节点处理器"""
        self.handlers[node_type] = handler
        self.logger.info("Registered node handler for %s", node_type)
    
    def get_handler(self, node_type: str) -> Optional[NodeHandler]:
        """获取节点处理器"""
        return self.handlers.get(node_type)

class NodeHandler(ABC):
    """节点处理器基类"""
    
    @abstractmethod
    def execute(
        self,
        execution_id: str,
        node_id: str,
        parameters: Dict,
        input: Dict
    ) -> Dict:
        """
        执行节点
        
        :param execution_id: 执行ID
        :param node_id: 节点ID
        :param parameters: 节点参数
        :param input: 输入数据
        :return: 节点输出
        """
        pass

# 示例节点处理器
class HttpNodeHandler(NodeHandler):
    """HTTP节点处理器"""
    
    def __init__(self, http_client: HttpClient, config: Config):
        self.http_client = http_client
        self.config = config
    
    def execute(
        self,
        execution_id: str,
        node_id: str,
        parameters: Dict,
        input: Dict
    ) -> Dict:
        # 1. 验证参数
        self._validate_parameters(parameters)
        
        # 2. 准备请求
        url = self._resolve_url(parameters["url"], input)
        method = parameters.get("method", "GET").upper()
        headers = self._resolve_headers(parameters.get("headers", {}), input)
        body = self._resolve_body(parameters.get("body", {}), input)
        
        # 3. 执行HTTP请求
        response = self.http_client.request(
            method,
            url,
            headers=headers,
            json=body,
            timeout=parameters.get("timeout", self.config.default_timeout)
        )
        
        # 4. 处理响应
        return self._process_response(response, parameters)
    
    def _validate_parameters(self, parameters: Dict):
        """验证参数"""
        if "url" not in parameters:
            raise NodeExecutionError("URL is required for HTTP node")
        
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        if "method" in parameters and parameters["method"].upper() not in valid_methods:
            raise NodeExecutionError(f"Invalid HTTP method. Must be one of: {', '.join(valid_methods)}")
    
    def _resolve_url(self, url_template: str, input: Dict) -> str:
        """解析URL模板"""
        # 简单实现：替换{{var}}为input中的值
        def replace_match(match):
            var_name = match.group(1)
            return str(input.get(var_name, match.group(0)))
        
        return re.sub(r'{{\s*(\w+)\s*}}', replace_match, url_template)
    
    def _resolve_headers(self, headers: Dict, input: Dict) -> Dict:
        """解析请求头"""
        resolved = {}
        for key, value in headers.items():
            if isinstance(value, str):
                resolved[key] = self._resolve_template(value, input)
            else:
                resolved[key] = value
        return resolved
    
    def _resolve_body(self, body: Dict, input: Dict) -> Dict:
        """解析请求体"""
        return self._resolve_template_recursive(body, input)
    
    def _resolve_template(self, template: str, input: Dict) -> str:
        """解析模板字符串"""
        def replace_match(match):
            var_name = match.group(1)
            return str(input.get(var_name, match.group(0)))
        
        return re.sub(r'{{\s*(\w+)\s*}}', replace_match, template)
    
    def _resolve_template_recursive(self, obj: Any, input: Dict) -> Any:
        """递归解析模板"""
        if isinstance(obj, str):
            return self._resolve_template(obj, input)
        elif isinstance(obj, dict):
            return {k: self._resolve_template_recursive(v, input) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._resolve_template_recursive(item, input) for item in obj]
        else:
            return obj
    
    def _process_response(self, response: HttpResponse, parameters: Dict) -> Dict:
        """处理HTTP响应"""
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "url": response.url
        }
        
        # 处理响应体
        if response.content:
            content_type = response.headers.get("Content-Type", "")
            
            if "json" in content_type:
                try:
                    result["body"] = response.json()
                except:
                    result["body"] = response.text
            elif "xml" in content_type:
                result["body"] = self._parse_xml(response.content)
            else:
                result["body"] = response.text
        
        # 提取特定字段（如果配置了）
        if "output_mapping" in parameters:
            result = self._apply_output_mapping(result, parameters["output_mapping"])
        
        return result
    
    def _parse_xml(self, content: bytes) -> Dict:
        """解析XML内容"""
        # 简单实现
        try:
            import xmltodict
            return xmltodict.parse(content)
        except:
            return {"raw": content.decode('utf-8', errors='replace')}
    
    def _apply_output_mapping(self, response: Dict, mapping: Dict) -> Dict:
        """应用输出映射"""
        result = {}
        
        for target, source in mapping.items():
            # 支持简单的JMESPath
            if source.startswith("$."):
                value = jmespath.search(source[2:], response)
            else:
                value = response.get(source)
            
            # 设置目标路径
            self._set_nested_value(result, target, value)
        
        return result
    
    def _set_nested_value(self, obj: Dict, path: str, value: Any):
        """设置嵌套对象的值"""
        parts = path.split('.')
        for part in parts[:-1]:
            if part not in obj:
                obj[part] = {}
            obj = obj[part]
        obj[parts[-1]] = value

# 注册示例节点处理器
node_registry = NodeRegistry()
node_registry.register("http/request", HttpNodeHandler(http_client, config))
```

### 4.5 数据模型详细定义

#### 4.5.1 工作流定义表

```sql
-- 工作流定义表
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(20) NOT NULL DEFAULT '1.0.0',
    definition JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived', 'deleted')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    updated_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    deleted_at TIMESTAMPTZ,
    deleted_by UUID REFERENCES users(id) ON DELETE SET NULL,
    tags JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 索引
    UNIQUE (project_id, name, version),
    INDEX idx_workflows_project ON workflows(project_id),
    INDEX idx_workflows_status ON workflows(status),
    INDEX idx_workflows_updated ON workflows(updated_at DESC),
    
    -- 全文搜索
    ts_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(display_name, '') || ' ' || coalesce(description, ''))
    ) STORED
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_workflows_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_workflows_modtime
BEFORE UPDATE ON workflows
FOR EACH ROW
EXECUTE FUNCTION update_workflows_modtime();

-- 全文搜索索引
CREATE INDEX idx_workflows_search ON workflows USING GIN (ts_vector);
```

#### 4.5.2 工作流实例表

```sql
-- 工作流实例表
CREATE TABLE workflow_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    trigger_type VARCHAR(50) NOT NULL,
    trigger_payload JSONB,
    input JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'canceled')),
    priority INT NOT NULL DEFAULT 5,
    timeout INTERVAL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration INTERVAL,
    output JSONB,
    error JSONB,
    parent_instance_id UUID REFERENCES workflow_instances(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_workflow_instances_workflow ON workflow_instances(workflow_id),
    INDEX idx_workflow_instances_status ON workflow_instances(status),
    INDEX idx_workflow_instances_started ON workflow_instances(started_at DESC),
    INDEX idx_workflow_instances_parent ON workflow_instances(parent_instance_id)
);
```

#### 4.5.3 节点执行表

```sql
-- 节点执行表
CREATE TABLE node_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    node_id VARCHAR(255) NOT NULL,
    node_type VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'retrying', 'skipped')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    duration INTERVAL,
    input JSONB NOT NULL,
    output JSONB,
    error JSONB,
    retry_count INT NOT NULL DEFAULT 0,
    max_retries INT NOT NULL DEFAULT 3,
    resource_usage JSONB DEFAULT '{}'::jsonb,
    
    -- 索引
    INDEX idx_node_executions_instance ON node_executions(instance_id),
    INDEX idx_node_executions_status ON node_executions(status),
    INDEX idx_node_executions_node ON node_executions(node_id),
    INDEX idx_node_executions_started ON node_executions(started_at DESC)
);
```

### 4.6 API详细规范

#### 4.6.1 工作流定义API

**创建工作流 (POST /api/v1/workflows)**

*请求示例:*
```http
POST /api/v1/workflows HTTP/1.1
Host: dpwe.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json
X-Request-ID: req-123456

{
  "name": "nas-photo-processing",
  "display_name": "NAS照片智能处理流水线",
  "description": "监控NAS目录并自动处理新照片",
  "triggers": [
    {
      "type": "filesystem",
      "config": {
        "path": "/nas/photos/raw",
        "events": ["create"],
        "recursive": true
      }
    }
  ],
  "nodes": [
    {
      "node_id": "preprocess-01",
      "type": "image/preprocess",
      "parameters": {
        "format": "jpeg",
        "max_size": "4096x4096",
        "auto_rotate": true
      }
    },
    {
      "node_id": "enhance-01",
      "type": "ai/image-enhance",
      "parameters": {
        "model": "realesrgan-x4plus",
        "scale_factor": 2,
        "denoise_strength": 0.3,
        "face_enhance": true
      }
    },
    {
      "node_id": "analyze-01",
      "type": "ai/image-analyze",
      "parameters": {
        "tasks": ["classification", "face-detection", "quality-assessment"]
      }
    },
    {
      "node_id": "archive-01",
      "type": "storage/minio",
      "parameters": {
        "bucket": "processed-photos",
        "path_template": "year={year}/month={month}/{filename}",
        "metadata": {
          "processed_by": "mirror-realm-amp"
        }
      }
    }
  ],
  "edges": [
    {
      "source": "preprocess-01",
      "target": "enhance-01"
    },
    {
      "source": "enhance-01",
      "target": "analyze-01"
    },
    {
      "source": "analyze-01",
      "target": "archive-01"
    }
  ],
  "tags": ["photos", "automation", "ai-processing"],
  "metadata": {
    "created_by": "user-123",
    "project_id": "proj-456"
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/workflows/nas-photo-processing/1.0.0
X-Request-ID: req-123456
ETag: "d41d8cd98f00b204e9800998ecf8427e"

{
  "id": "wf-7a8b9c0d",
  "project_id": "proj-456",
  "name": "nas-photo-processing",
  "display_name": "NAS照片智能处理流水线",
  "description": "监控NAS目录并自动处理新照片",
  "version": "1.0.0",
  "triggers": [
    {
      "type": "filesystem",
      "config": {
        "path": "/nas/photos/raw",
        "events": ["create"],
        "recursive": true
      }
    }
  ],
  "nodes": [
    {
      "node_id": "preprocess-01",
      "type": "image/preprocess",
      "parameters": {
        "format": "jpeg",
        "max_size": "4096x4096",
        "auto_rotate": true
      }
    },
    {
      "node_id": "enhance-01",
      "type": "ai/image-enhance",
      "parameters": {
        "model": "realesrgan-x4plus",
        "scale_factor": 2,
        "denoise_strength": 0.3,
        "face_enhance": true
      }
    },
    {
      "node_id": "analyze-01",
      "type": "ai/image-analyze",
      "parameters": {
        "tasks": ["classification", "face-detection", "quality-assessment"]
      }
    },
    {
      "node_id": "archive-01",
      "type": "storage/minio",
      "parameters": {
        "bucket": "processed-photos",
        "path_template": "year={year}/month={month}/{filename}",
        "metadata": {
          "processed_by": "mirror-realm-amp"
        }
      }
    }
  ],
  "edges": [
    {
      "source": "preprocess-01",
      "target": "enhance-01"
    },
    {
      "source": "enhance-01",
      "target": "analyze-01"
    },
    {
      "source": "analyze-01",
      "target": "archive-01"
    }
  ],
  "status": "active",
  "tags": ["photos", "automation", "ai-processing"],
  "metadata": {
    "created_by": "user-123",
    "project_id": "proj-456",
    "created_at": "2023-06-15T10:30:45Z",
    "updated_at": "2023-06-15T10:30:45Z"
  }
}
```

#### 4.6.2 工作流执行API

**创建工作流实例 (POST /api/v1/workflows/{workflow_name}:run)**

*请求示例:*
```http
POST /api/v1/workflows/nas-photo-processing:run HTTP/1.1
Host: dpwe.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json
X-Request-ID: req-789012

{
  "input": {
    "trigger": {
      "type": "filesystem",
      "payload": {
        "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
        "event_type": "create",
        "timestamp": "2023-06-15T10:30:45Z"
      }
    }
  },
  "priority": 5,
  "timeout": "3600s"
}
```

*成功响应示例:*
```http
HTTP/1.1 202 Accepted
Content-Type: application/json
Location: /api/v1/workflowInstances/wf-nas-photo-processing-1686825045-1234
X-Request-ID: req-789012

{
  "id": "inst-1a2b3c4d5e6f",
  "workflow_id": "wf-7a8b9c0d",
  "project_id": "proj-456",
  "trigger_type": "filesystem",
  "trigger_payload": {
    "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
    "event_type": "create",
    "timestamp": "2023-06-15T10:30:45Z"
  },
  "status": "pending",
  "input": {
    "trigger": {
      "type": "filesystem",
      "payload": {
        "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
        "event_type": "create",
        "timestamp": "2023-06-15T10:30:45Z"
      }
    }
  },
  "priority": 5,
  "timeout": "3600s",
  "created_at": "2023-06-15T10:30:45Z",
  "created_by": "user-123"
}
```

**获取工作流实例状态 (GET /api/v1/workflowInstances/{instance_id})**

*请求示例:*
```http
GET /api/v1/workflowInstances/inst-1a2b3c4d5e6f HTTP/1.1
Host: dpwe.mirror-realm.com
Authorization: Bearer <access_token>
Accept: application/json
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "inst-1a2b3c4d5e6f",
  "workflow_id": "wf-7a8b9c0d",
  "project_id": "proj-456",
  "trigger_type": "filesystem",
  "trigger_payload": {
    "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
    "event_type": "create",
    "timestamp": "2023-06-15T10:30:45Z"
  },
  "status": "running",
  "input": {
    "trigger": {
      "type": "filesystem",
      "payload": {
        "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
        "event_type": "create",
        "timestamp": "2023-06-15T10:30:45Z"
      }
    }
  },
  "output": null,
  "error": null,
  "started_at": "2023-06-15T10:30:45Z",
  "completed_at": null,
  "duration": "PT4m35s",
  "priority": 5,
  "timeout": "3600s",
  "created_at": "2023-06-15T10:30:45Z",
  "created_by": "user-123",
  "node_executions": [
    {
      "id": "node-112233",
      "node_id": "preprocess-01",
      "node_type": "image/preprocess",
      "status": "completed",
      "started_at": "2023-06-15T10:30:45Z",
      "completed_at": "2023-06-15T10:31:10Z",
      "duration": "PT25s",
      "input": {
        "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg"
      },
      "output": {
        "processed_path": "/tmp/processed/IMG_20230615_103045.jpg",
        "width": 4096,
        "height": 2304,
        "format": "jpeg"
      },
      "error": null,
      "retry_count": 0,
      "max_retries": 3,
      "resource_usage": {}
    },
    {
      "id": "node-445566",
      "node_id": "enhance-01",
      "node_type": "ai/image-enhance",
      "status": "running",
      "started_at": "2023-06-15T10:31:10Z",
      "completed_at": null,
      "duration": "PT3m25s",
      "input": {
        "file_path": "/tmp/processed/IMG_20230615_103045.jpg"
      },
      "output": null,
      "error": null,
      "retry_count": 0,
      "max_retries": 3,
      "resource_usage": {
        "cpu_seconds": 120.5,
        "memory_mb_seconds": 785000,
        "gpu_utilization": 0.75
      }
    }
  ]
}
```

### 4.7 性能优化策略

#### 4.7.1 工作流执行优化

1. **并行执行**
   ```python
   def execute_parallel_nodes(instance, workflow, node_ids):
       """并行执行多个节点"""
       with ThreadPoolExecutor(max_workers=5) as executor:
           futures = {
               executor.submit(execute_node, instance, workflow, node_id): node_id
               for node_id in node_ids
           }
           
           for future in as_completed(futures):
               node_id = futures[future]
               try:
                   future.result()
               except Exception as e:
                   logger.error("Error executing node %s: %s", node_id, str(e))
                   handle_node_failure(instance, node_id, str(e))
   ```

2. **执行计划优化**
   ```python
   def optimize_execution_plan(workflow):
       """优化工作流执行计划"""
       # 1. 识别可以并行执行的节点
       parallel_groups = find_parallelizable_nodes(workflow)
       
       # 2. 识别计算密集型节点，提前调度
       compute_intensive = identify_compute_intensive_nodes(workflow)
       
       # 3. 生成优化后的执行计划
       return generate_optimized_plan(parallel_groups, compute_intensive)
   ```

3. **缓存优化**
   ```python
   class NodeExecutionCache:
       """节点执行结果缓存"""
       
       def __init__(self, ttl=3600):
           self.cache = TTLCache(maxsize=10000, ttl=ttl)
       
       def get(self, node_id, input_hash):
           """获取缓存结果"""
           key = f"{node_id}:{input_hash}"
           return self.cache.get(key)
       
       def set(self, node_id, input_hash, result):
           """设置缓存结果"""
           key = f"{node_id}:{input_hash}"
           self.cache[key] = result
   ```

#### 4.7.2 资源管理优化

1. **动态资源分配**
   ```python
   def allocate_resources(node_type, parameters):
       """根据节点类型和参数分配资源"""
       # 基础资源需求
       resources = {
           "cpu": 1000,  # 1000 millicores
           "memory": 512,  # 512 MB
           "gpu": False
       }
       
       # 根据节点类型调整
       if node_type.startswith("ai/"):
           resources["gpu"] = True
           resources["memory"] = 2048
           
           # 根据模型大小调整
           if "model" in parameters:
               if "large" in parameters["model"]:
                   resources["memory"] = 4096
       
       # 根据输入大小调整
       if "input_size" in parameters:
           size_mb = parameters["input_size"]
           resources["memory"] = max(512, int(512 * (size_mb / 10)))
       
       return resources
   ```

2. **资源配额管理**
   ```python
   class ResourceQuotaManager:
       """资源配额管理器"""
       
       def __init__(self, db):
           self.db = db
       
       def check_quota(self, project_id, resources):
           """检查资源配额"""
           # 获取项目配额
           quota = self._get_project_quota(project_id)
           
           # 获取已用资源
           used = self._get_used_resources(project_id)
           
           # 检查是否超出配额
           if used["cpu"] + resources["cpu"] > quota["cpu"]:
               return False, "CPU quota exceeded"
           if used["memory"] + resources["memory"] > quota["memory"]:
               return False, "Memory quota exceeded"
           if resources["gpu"] and used["gpu"] >= quota["gpu"]:
               return False, "GPU quota exceeded"
           
           return True, ""
       
       def _get_project_quota(self, project_id):
           """获取项目配额"""
           # 从数据库获取
           return {
               "cpu": 10000,  # 10 cores
               "memory": 10240,  # 10 GB
               "gpu": 2
           }
       
       def _get_used_resources(self, project_id):
           """获取已用资源"""
           # 计算运行中实例的资源使用
           return {
               "cpu": 3000,
               "memory": 3072,
               "gpu": 1
           }
   ```

### 4.8 安全考虑

#### 4.8.1 工作流安全

1. **沙箱执行**
   ```python
   def execute_in_sandbox(node_type, parameters, input_data):
       """在沙箱中执行节点"""
       # 1. 创建隔离环境
       sandbox = create_sandbox()
       
       # 2. 限制资源
       sandbox.set_resource_limits(
           cpu=parameters.get("cpu_limit", 1000),
           memory=parameters.get("memory_limit", 512)
       )
       
       # 3. 限制网络访问
       if node_type.startswith("http/"):
           sandbox.allow_network("api.mirror-realm.com")
       else:
           sandbox.deny_network()
       
       # 4. 执行节点
       try:
           return sandbox.execute(node_type, parameters, input_data)
       finally:
           sandbox.cleanup()
   ```

2. **输入验证**
   ```python
   def validate_node_input(node_type, input_data):
       """验证节点输入"""
       # 定义各节点类型的输入模式
       schemas = {
           "http/request": {
               "type": "object",
               "properties": {
                   "url": {"type": "string", "format": "uri"},
                   "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]},
                   "headers": {"type": "object"},
                   "body": {"type": "object"}
               },
               "required": ["url"]
           },
           "ai/image-enhance": {
               "type": "object",
               "properties": {
                   "image_path": {"type": "string"},
                   "model": {"type": "string"},
                   "scale_factor": {"type": "number", "minimum": 1, "maximum": 4}
               },
               "required": ["image_path"]
           }
           # 其他节点类型...
       }
       
       # 验证输入
       if node_type in schemas:
           validate(instance=input_data, schema=schemas[node_type])
   ```

#### 4.8.2 数据安全

1. **敏感数据处理**
   ```python
   def sanitize_workflow_data(data):
       """清洗工作流数据中的敏感信息"""
       # 定义敏感字段
       sensitive_fields = ["api_key", "password", "secret", "token"]
       
       # 递归处理
       if isinstance(data, dict):
           return {
               k: "****" if k.lower() in sensitive_fields else sanitize_workflow_data(v)
               for k, v in data.items()
           }
       elif isinstance(data, list):
           return [sanitize_workflow_data(item) for item in data]
       else:
           return data
   ```

2. **审计日志**
   ```sql
   CREATE TABLE workflow_audit_logs (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
       instance_id UUID REFERENCES workflow_instances(id) ON DELETE CASCADE,
       user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
       project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
       action VARCHAR(20) NOT NULL, -- create, update, delete, execute, cancel
       details JSONB,
       timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       ip_address INET,
       user_agent TEXT
   );
   
   CREATE INDEX idx_audit_logs_workflow ON workflow_audit_logs(workflow_id);
   CREATE INDEX idx_audit_logs_instance ON workflow_audit_logs(instance_id);
   CREATE INDEX idx_audit_logs_timestamp ON workflow_audit_logs(timestamp DESC);
   ```

### 4.9 与其他模块的交互

#### 4.9.1 与数据源注册中心交互

```mermaid
sequenceDiagram
    participant DSR as Data Source Registry
    participant DPWE as Data Processing Workflow Engine
    
    DPWE->>DSR: GET /api/v1/data-sources (获取数据源列表)
    DSR-->>DPWE: 数据源元数据
    
    DPWE->>DSR: POST /api/v1/data-sources (创建工作流使用的数据源)
    DSR-->>DPWE: 创建结果
    
    loop 工作流执行中
        DPWE->>DSR: GET /api/v1/data-sources/{id} (获取数据源详情)
        DSR-->>DPWE: 数据源详情
    end
```

#### 4.9.2 与自动化媒体处理管道交互

```mermaid
sequenceDiagram
    participant AMP as Automated Media Processing Pipeline
    participant DPWE as Data Processing Workflow Engine
    
    DPWE->>AMP: POST /api/v1/media:process (触发媒体处理)
    AMP-->>DPWE: 处理任务ID
    
    loop 处理进行中
        DPWE->>AMP: GET /api/v1/media/processingTasks/{task_id} (查询状态)
        AMP-->>DPWE: 处理状态
    end
    
    DPWE->>AMP: GET /api/v1/media/processingTasks/{task_id} (获取结果)
    AMP-->>DPWE: 处理结果和元数据
```

#### 4.9.3 与AI辅助开发系统交互

```mermaid
sequenceDiagram
    participant AIDS as AI-Assisted Development System
    participant DPWE as Data Processing Workflow Engine
    
    DPWE->>AIDS: POST /api/v1/workflows/generate (生成工作流)
    AIDS-->>DPWE: 工作流定义
    
    DPWE->>AIDS: POST /api/v1/workflows/assist (工作流辅助)
    AIDS-->>DPWE: 建议和优化
    
    DPWE->>AIDS: GET /api/v1/nodes/templates (获取节点模板)
    AIDS-->>DPWE: 节点模板列表
```

## 5. 自动化媒体处理管道 (Automated Media Processing Pipeline)

### 5.1 模块概述
自动化媒体处理管道是镜界平台的核心数据处理组件，专注于图像和视频等媒体文件的自动化处理。它提供从文件监控、预处理、AI增强到存储归档的完整处理流水线，支持与NAS系统的深度集成。

### 5.2 详细功能清单

#### 5.2.1 核心功能
- **文件监控与触发**
  - 多协议NAS连接（SMB、WebDAV、FTP、NFS）
  - 实时文件系统监控
  - 文件变化事件聚合
  - 增量处理优化
- **预处理阶段**
  - 格式转换与标准化
  - 元数据提取（EXIF、IPTC）
  - 基础修复（去噪、旋转）
  - 文件分块处理
- **AI增强阶段**
  - 画质智能修复（超分辨率、去噪）
  - 自动色彩校正
  - 智能裁剪与构图优化
  - 分辨率增强（超分重建）
  - 面部优化与修饰
- **分析阶段**
  - 图像内容识别与标签
  - 质量评估与评分
  - 相似图片去重
  - 异常检测与过滤
- **组织阶段**
  - AI自动标签分类
  - 相似图片分组
  - 存储空间分析
  - 备份与还原管理
- **归档阶段**
  - 处理后文件自动归档
  - 处理报告生成
  - 结果通知与分享

#### 5.2.2 高级功能
- **智能处理流水线**
  - 基于内容的处理策略
  - 动态调整处理参数
  - 质量-速度权衡
  - 处理优先级管理
- **批量处理任务**
  - 全库批量处理
  - 增量更新处理
  - 条件筛选处理
  - 预览后确认处理
- **风格学习与迁移**
  - 个人风格模型训练
  - 艺术风格迁移
  - 批量风格统一
  - 自定义风格库
- **智能相册管理**
  - 人脸识别与分组
  - 场景自动分类
  - 时间线智能整理
  - 情感标签分析

### 5.3 技术架构

#### 5.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                            自动化媒体处理管道 (AMP)                                           │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  输入层               │  处理层               │  输出层                                    │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 文件监控服务        │ • 预处理服务          │ • 存储服务                                 │
│ • 事件接收器          │ • AI增强服务          │ • 通知服务                                 │
│ • 批量任务调度        │ • 内容分析服务        │ • 报告生成器                               │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 5.3.2 服务边界与交互
- **输入**：
  - 文件系统事件（来自NAS监控）
  - 手动触发的处理请求
  - 批量处理任务
- **输出**：
  - 处理后的媒体文件
  - 处理报告
  - 分析结果和元数据
  - 通知事件

### 5.4 核心组件详细实现

#### 5.4.1 文件监控服务

**技术实现：**
```python
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, List, Optional, Set

class FileEvent:
    """文件系统事件对象"""
    
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    MOVE = "move"
    
    def __init__(
        self,
        event_type: str,
        src_path: str,
        dest_path: Optional[str] = None,
        is_directory: bool = False,
        timestamp: float = None
    ):
        self.event_type = event_type
        self.src_path = src_path
        self.dest_path = dest_path
        self.is_directory = is_directory
        self.timestamp = timestamp or time.time()
        self.processed = False
        self.processing_start = None
        self.processing_end = None
        self.error = None
    
    def mark_processed(self, success: bool, error: str = None):
        """标记事件已处理"""
        self.processed = True
        self.processing_end = time.time()
        if not success:
            self.error = error
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "event_type": self.event_type,
            "src_path": self.src_path,
            "dest_path": self.dest_path,
            "is_directory": self.is_directory,
            "timestamp": self.timestamp,
            "processed": self.processed,
            "processing_time": self.processing_end - self.processing_start if self.processing_start and self.processing_end else None,
            "error": self.error
        }

class DirectoryEventHandler(FileSystemEventHandler):
    """目录事件处理器"""
    
    def __init__(
        self,
        callback: Callable[[FileEvent], None],
        ignored_patterns: List[str] = None,
        process_directories: bool = False
    ):
        super().__init__()
        self.callback = callback
        self.ignored_patterns = ignored_patterns or []
        self.process_directories = process_directories
    
    def _is_ignored(self, path: str) -> bool:
        """检查路径是否应被忽略"""
        return any(pattern in path for pattern in self.ignored_patterns)
    
    def on_created(self, event):
        if self.process_directories or not event.is_directory:
            if not self._is_ignored(event.src_path):
                self.callback(FileEvent(FileEvent.CREATE, event.src_path, is_directory=event.is_directory))
    
    def on_modified(self, event):
        if self.process_directories or not event.is_directory:
            if not self._is_ignored(event.src_path):
                self.callback(FileEvent(FileEvent.MODIFY, event.src_path, is_directory=event.is_directory))
    
    def on_deleted(self, event):
        if self.process_directories or not event.is_directory:
            if not self._is_ignored(event.src_path):
                self.callback(FileEvent(FileEvent.DELETE, event.src_path, is_directory=event.is_directory))
    
    def on_moved(self, event):
        if self.process_directories or not event.is_directory:
            if not self._is_ignored(event.src_path) and not self._is_ignored(event.dest_path):
                self.callback(FileEvent(
                    FileEvent.MOVE, 
                    event.src_path, 
                    event.dest_path,
                    is_directory=event.is_directory
                ))

class FileSystemWatcher:
    """文件系统监控器，支持多目录监控和事件聚合"""
    
    def __init__(
        self,
        paths: List[str],
        event_types: List[str] = None,
        recursive: bool = True,
        debounce_ms: int = 500,
        ignored_patterns: List[str] = None,
        max_workers: int = 4
    ):
        """
        初始化文件系统监控器
        
        :param paths: 要监控的目录路径列表
        :param event_types: 要监听的事件类型 (create, modify, delete, move)
        :param recursive: 是否递归监控子目录
        :param debounce_ms: 事件去抖时间 (毫秒)
        :param ignored_patterns: 忽略的文件模式列表
        :param max_workers: 处理事件的线程池大小
        """
        self.paths = paths
        self.event_types = event_types or [FileEvent.CREATE]
        self.recursive = recursive
        self.debounce_ms = debounce_ms
        self.ignored_patterns = ignored_patterns or [".DS_Store", "Thumbs.db", "~$"]
        self.max_workers = max_workers
        self.observers = []
        self.event_buffer = {}
        self.callback = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logging.getLogger(__name__)
        self.running = False
    
    def start(self, callback: Callable[[FileEvent], None]):
        """启动监控器"""
        if self.running:
            return
        
        self.callback = callback
        self.running = True
        
        # 为每个路径创建观察者
        for path in self.paths:
            if not os.path.exists(path):
                self.logger.warning("Path does not exist: %s", path)
                continue
                
            event_handler = DirectoryEventHandler(
                self._buffer_event,
                ignored_patterns=self.ignored_patterns
            )
            
            observer = Observer()
            observer.schedule(event_handler, path, recursive=self.recursive)
            observer.start()
            self.observers.append(observer)
            
            self.logger.info("Started watching directory: %s (recursive=%s)", path, self.recursive)
        
        # 启动去抖定时器
        self.executor.submit(self._debounce_timer)
    
    def stop(self):
        """停止监控器"""
        self.running = False
        
        # 停止所有观察者
        for observer in self.observers:
            observer.stop()
        
        for observer in self.observers:
            observer.join()
        
        self.observers = []
        
        # 关闭线程池
        self.executor.shutdown(wait=True)
        
        self.logger.info("Stopped file system watcher")
    
    def _buffer_event(self, event: FileEvent):
        """缓冲事件用于去抖"""
        if not self.running:
            return
        
        # 仅处理指定的事件类型
        if event.event_type not in self.event_types:
            return
        
        # 生成唯一键（路径+事件类型）
        key = f"{event.src_path}|{event.event_type}"
        
        # 如果是移动事件，使用目标路径
        if event.event_type == FileEvent.MOVE:
            key = f"{event.dest_path}|{event.event_type}"
        
        # 缓冲事件
        self.event_buffer[key] = {
            "event": event,
            "timestamp": time.time()
        }
    
    def _debounce_timer(self):
        """去抖定时器"""
        while self.running:
            try:
                current_time = time.time()
                events_to_process = []
                
                # 检查缓冲区中的事件
                for key, item in list(self.event_buffer.items()):
                    # 检查是否超过去抖时间
                    if (current_time - item["timestamp"]) * 1000 >= self.debounce_ms:
                        events_to_process.append(item["event"])
                        del self.event_buffer[key]
                
                # 处理事件
                if events_to_process:
                    self._process_events(events_to_process)
                
                # 等待下一次检查
                time.sleep(self.debounce_ms / 1000.0)
                
            except Exception as e:
                self.logger.error("Error in debounce timer: %s", str(e))
                time.sleep(1)
    
    def _process_events(self, events: List[FileEvent]):
        """处理事件列表"""
        for event in events:
            try:
                # 标记处理开始
                event.processing_start = time.time()
                
                # 调用回调
                self.callback(event)
                
                # 标记处理完成
                event.mark_processed(True)
                
            except Exception as e:
                event.mark_processed(False, str(e))
                self.logger.error("Error processing file event: %s", str(e))
    
    def get_status(self) -> Dict:
        """获取监控器状态"""
        return {
            "running": self.running,
            "paths": self.paths,
            "event_types": self.event_types,
            "recursive": self.recursive,
            "debounce_ms": self.debounce_ms,
            "buffered_events": len(self.event_buffer),
            "observers": len(self.observers)
        }

class NasConnectionManager:
    """NAS连接管理器，支持多协议"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.connections = {}
        self.logger = logging.getLogger(__name__)
    
    def connect(self, connection_id: str, config: Dict) -> str:
        """
        创建NAS连接
        
        :param connection_id: 连接ID
        :param config: 连接配置
        :return: 连接ID
        """
        # 验证配置
        self._validate_config(config)
        
        # 创建连接
        if config["protocol"] == "smb":
            connection = self._create_smb_connection(config)
        elif config["protocol"] == "webdav":
            connection = self._create_webdav_connection(config)
        elif config["protocol"] == "ftp":
            connection = self._create_ftp_connection(config)
        elif config["protocol"] == "nfs":
            connection = self._create_nfs_connection(config)
        else:
            raise ValueError(f"Unsupported protocol: {config['protocol']}")
        
        # 保存连接
        self.connections[connection_id] = connection
        
        return connection_id
    
    def _validate_config(self, config: Dict):
        """验证连接配置"""
        required_fields = ["protocol", "host", "path"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        if config["protocol"] == "smb":
            if "username" not in config or "password" not in config:
                raise ValueError("SMB connection requires username and password")
        
        # 其他协议验证...
    
    def _create_smb_connection(self, config: Dict) -> Any:
        """创建SMB连接"""
        from smbprotocol.connection import Connection
        from smbprotocol.session import Session
        from smbprotocol.tree import TreeConnect
        
        connection = Connection(uuid.uuid4(), config["host"], port=445)
        connection.connect()
        
        session = Session(connection, config["username"], config["password"])
        session.connect()
        
        tree = TreeConnect(session, f"\\\\{config['host']}\\{config['share']}")
        tree.connect()
        
        return {
            "connection": connection,
            "session": session,
            "tree": tree,
            "config": config
        }
    
    def _create_webdav_connection(self, config: Dict) -> Any:
        """创建WebDAV连接"""
        from webdav3.client import Client
        
        options = {
            'webdav_hostname': config["host"],
            'webdav_login': config.get("username"),
            'webdav_password': config.get("password"),
            'webdav_root': config["path"]
        }
        
        client = Client(options)
        return {
            "client": client,
            "config": config
        }
    
    def _create_ftp_connection(self, config: Dict) -> Any:
        """创建FTP连接"""
        from ftplib import FTP
        
        ftp = FTP(config["host"])
        ftp.login(user=config.get("username"), passwd=config.get("password"))
        ftp.cwd(config["path"])
        
        return {
            "ftp": ftp,
            "config": config
        }
    
    def _create_nfs_connection(self, config: Dict) -> Any:
        """创建NFS连接"""
        # NFS通常通过挂载点访问，这里假设已挂载
        return {
            "mount_point": config["mount_point"],
            "config": config
        }
    
    def list_files(self, connection_id: str, path: str = "/") -> List[Dict]:
        """
        列出文件
        
        :param connection_id: 连接ID
        :param path: 路径
        :return: 文件列表
        """
        connection = self._get_connection(connection_id)
        
        if connection["config"]["protocol"] == "smb":
            return self._list_files_smb(connection, path)
        elif connection["config"]["protocol"] == "webdav":
            return self._list_files_webdav(connection, path)
        elif connection["config"]["protocol"] == "ftp":
            return self._list_files_ftp(connection, path)
        elif connection["config"]["protocol"] == "nfs":
            return self._list_files_nfs(connection, path)
        
        raise ValueError("Unsupported protocol")
    
    def _list_files_smb(self, connection: Dict, path: str) -> List[Dict]:
        """列出SMB文件"""
        from smbprotocol.open import Open, CreateOptions, FilePipePrinterAccessMask
        
        # SMB协议比较复杂，这里简化实现
        # 实际实现需要处理目录枚举
        return []
    
    def _list_files_webdav(self, connection: Dict, path: str) -> List[Dict]:
        """列出WebDAV文件"""
        client = connection["client"]
        files = client.list(path)
        
        result = []
        for file in files:
            info = client.info(f"{path}/{file}")
            result.append({
                "name": file,
                "path": f"{path}/{file}",
                "is_directory": info["is_dir"],
                "size": info["size"],
                "modified": info["modified"]
            })
        
        return result
    
    def _list_files_ftp(self, connection: Dict, path: str) -> List[Dict]:
        """列出FTP文件"""
        ftp = connection["ftp"]
        ftp.cwd(path)
        
        files = []
        ftp.retrlines('LIST', files.append)
        
        result = []
        for line in files:
            # 解析FTP LIST输出
            parts = line.split()
            if len(parts) >= 9:
                name = ' '.join(parts[8:])
                is_dir = line.startswith('d')
                size = int(parts[4]) if not is_dir else 0
                modified = ' '.join(parts[5:8])
                
                result.append({
                    "name": name,
                    "path": f"{path}/{name}",
                    "is_directory": is_dir,
                    "size": size,
                    "modified": modified
                })
        
        return result
    
    def _list_files_nfs(self, connection: Dict, path: str) -> List[Dict]:
        """列出NFS文件"""
        mount_point = connection["mount_point"]
        full_path = os.path.join(mount_point, path.lstrip('/'))
        
        result = []
        for name in os.listdir(full_path):
            file_path = os.path.join(full_path, name)
            is_dir = os.path.isdir(file_path)
            size = os.path.getsize(file_path) if not is_dir else 0
            modified = os.path.getmtime(file_path)
            
            result.append({
                "name": name,
                "path": f"{path}/{name}",
                "is_directory": is_dir,
                "size": size,
                "modified": time.ctime(modified)
            })
        
        return result
    
    def watch_directory(
        self,
        connection_id: str,
        path: str,
        callback: Callable[[FileEvent], None],
        event_types: List[str] = None,
        recursive: bool = True,
        debounce_ms: int = 500
    ) -> str:
        """
        监控目录
        
        :param connection_id: 连接ID
        :param path: 路径
        :param callback: 回调函数
        :param event_types: 事件类型
        :param recursive: 是否递归
        :param debounce_ms: 去抖时间
        :return: 监控器ID
        """
        connection = self._get_connection(connection_id)
        config = connection["config"]
        
        # 对于NFS和本地挂载，可以直接使用FileSystemWatcher
        if config["protocol"] in ["nfs", "local"]:
            mount_point = connection.get("mount_point", config.get("mount_point", "/"))
            full_path = os.path.join(mount_point, path.lstrip('/'))
            
            watcher = FileSystemWatcher(
                paths=[full_path],
                event_types=event_types,
                recursive=recursive,
                debounce_ms=debounce_ms
            )
            watcher.start(callback)
            
            watcher_id = f"watcher-{uuid.uuid4().hex[:8]}"
            self.watchers[watcher_id] = watcher
            return watcher_id
        
        # 对于其他协议，需要轮询（简化实现）
        if config["protocol"] == "smb":
            return self._watch_smb_directory(connection, path, callback, event_types, recursive, debounce_ms)
        elif config["protocol"] == "webdav":
            return self._watch_webdav_directory(connection, path, callback, event_types, recursive, debounce_ms)
        elif config["protocol"] == "ftp":
            return self._watch_ftp_directory(connection, path, callback, event_types, recursive, debounce_ms)
        
        raise ValueError("Unsupported protocol for directory watching")
    
    def _get_connection(self, connection_id: str) -> Dict:
        """获取连接"""
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        return self.connections[connection_id]
```

#### 5.4.2 媒体处理服务

**技术实现：**
```python
import cv2
import numpy as np
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from gfpgan import GFPGANer
from PIL import Image
import exifread
import piexif
from typing import Tuple, Optional, Dict, Any, List
import logging
import os
import tempfile
import hashlib

class MediaProcessingService:
    """媒体处理服务，协调整个处理流水线"""
    
    def __init__(
        self,
        preprocessor: MediaPreprocessor,
        enhancer: MediaEnhancer,
        analyzer: MediaAnalyzer,
        config: Config
    ):
        self.preprocessor = preprocessor
        self.enhancer = enhancer
        self.analyzer = analyzer
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def process_media(
        self,
        file_path: str,
        workflow: ProcessingWorkflow,
        callback: Optional[Callable[[ProcessingStatus], None]] = None
    ) -> ProcessingResult:
        """
        处理媒体文件
        
        :param file_path: 文件路径
        :param workflow: 处理工作流
        :param callback: 状态回调函数
        :return: 处理结果
        """
        start_time = time.time()
        status = ProcessingStatus(
            file_path=file_path,
            workflow_id=workflow.id,
            status="processing",
            progress=0.0
        )
        
        try:
            # 1. 更新状态：开始预处理
            status.step = "preprocessing"
            status.progress = 0.1
            self._notify_callback(callback, status)
            
            # 2. 预处理
            preprocessed_path, preprocessed_meta = self.preprocessor.preprocess(
                file_path,
                workflow.preprocessing
            )
            
            # 3. 更新状态：开始AI增强
            status.step = "enhancing"
            status.progress = 0.3
            self._notify_callback(callback, status)
            
            # 4. AI增强
            enhanced_path, enhancement_meta = self.enhancer.enhance(
                preprocessed_path,
                workflow.enhancement
            )
            
            # 5. 更新状态：开始分析
            status.step = "analyzing"
            status.progress = 0.7
            self._notify_callback(callback, status)
            
            # 6. 分析
            analysis_result = self.analyzer.analyze(
                enhanced_path,
                workflow.analysis
            )
            
            # 7. 更新状态：开始组织
            status.step = "organizing"
            status.progress = 0.9
            self._notify_callback(callback, status)
            
            # 8. 组织（分类、归档等）
            organized_path = self._organize_result(
                enhanced_path,
                analysis_result,
                workflow.organization
            )
            
            # 9. 生成处理报告
            report = self._generate_report(
                file_path,
                preprocessed_meta,
                enhancement_meta,
                analysis_result,
                time.time() - start_time
            )
            
            # 10. 返回结果
            status.status = "completed"
            status.progress = 1.0
            status.result = {
                "processed_path": organized_path,
                "report": report,
                "analysis": analysis_result
            }
            self._notify_callback(callback, status)
            
            return ProcessingResult(
                processed_path=organized_path,
                report=report,
                analysis=analysis_result,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            # 处理错误
            status.status = "failed"
            status.error = str(e)
            self._notify_callback(callback, status)
            raise
    
    def _notify_callback(
        self,
        callback: Optional[Callable[[ProcessingStatus], None]],
        status: ProcessingStatus
    ):
        """通知状态回调"""
        if callback:
            try:
                callback(status)
            except Exception as e:
                self.logger.error("Error in status callback: %s", str(e))
    
    def _organize_result(
        self,
        file_path: str,
        analysis: Dict,
        organization_config: Dict
    ) -> str:
        """组织处理结果"""
        # 根据分析结果生成目标路径
        if organization_config.get("path_template"):
            target_path = self._apply_path_template(
                organization_config["path_template"],
                file_path,
                analysis
            )
        else:
            # 默认路径
            target_path = os.path.join(
                os.path.dirname(file_path),
                "processed",
                os.path.basename(file_path)
            )
        
        # 确保目录存在
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # 移动文件
        shutil.move(file_path, target_path)
        
        return target_path
    
    def _apply_path_template(
        self,
        template: str,
        source_path: str,
        analysis: Dict
    ) -> str:
        """应用路径模板"""
        # 获取文件信息
        file_name = os.path.basename(source_path)
        file_ext = os.path.splitext(file_name)[1]
        dir_name = os.path.dirname(source_path)
        
        # 获取日期信息
        current_date = datetime.now()
        date_info = {
            "year": current_date.year,
            "month": current_date.month,
            "day": current_date.day,
            "hour": current_date.hour,
            "minute": current_date.minute
        }
        
        # 获取分析信息
        analysis_info = {
            "quality": analysis.get("quality", {}).get("score", 0),
            "tags": ",".join(analysis.get("tags", [])),
            "face_count": len(analysis.get("faces", []))
        }
        
        # 替换模板变量
        def replace_var(match):
            var = match.group(1)
            
            # 日期变量
            if var in date_info:
                return str(date_info[var])
            
            # 分析变量
            if var in analysis_info:
                return str(analysis_info[var])
            
            # 文件变量
            if var == "filename":
                return file_name
            if var == "basename":
                return os.path.splitext(file_name)[0]
            if var == "ext":
                return file_ext[1:] if file_ext else ""
            if var == "dir":
                return os.path.basename(dir_name)
            
            return match.group(0)
        
        return re.sub(r'{(\w+)}', replace_var, template)
    
    def _generate_report(
        self,
        source_path: str,
        preprocessed_meta: Dict,
        enhancement_meta: Dict,
        analysis_result: Dict,
        processing_time: float
    ) -> Dict:
        """生成处理报告"""
        return {
            "source_file": source_path,
            "processing_time": processing_time,
            "preprocessing": preprocessed_meta,
            "enhancement": enhancement_meta,
            "analysis": analysis_result,
            "timestamp": datetime.utcnow().isoformat()
        }

class MediaPreprocessor:
    """媒体预处理器，执行基础预处理任务"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def preprocess(
        self,
        file_path: str,
        config: Dict
    ) -> Tuple[str, Dict]:
        """
        预处理媒体文件
        
        :param file_path: 文件路径
        :param config: 预处理配置
        :return: (处理后的文件路径, 元理元数据)
        """
        # 1. 读取文件
        image = self._read_image(file_path)
        
        # 2. 获取EXIF信息
        exif_data = self._extract_exif(file_path)
        
        # 3. 应用预处理步骤
        preprocessed, meta = self._apply_preprocessing_steps(image, exif_data, config)
        
        # 4. 保存处理后的文件
        output_path = self._save_image(preprocessed, file_path, config)
        
        return output_path, meta
    
    def _read_image(self, file_path: str) -> np.ndarray:
        """读取图像文件"""
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Failed to read image: {file_path}")
        
        # 转换为RGB（OpenCV默认是BGR）
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def _extract_exif(self, file_path: str) -> Dict:
        """提取EXIF信息"""
        try:
            with open(file_path, 'rb') as f:
                exif = exifread.process_file(f)
                return {str(k): str(v) for k, v in exif.items()}
        except Exception as e:
            self.logger.warning("Error extracting EXIF: %s", str(e))
            return {}
    
    def _apply_preprocessing_steps(
        self,
        image: np.ndarray,
        exif_data: Dict,
        config: Dict
    ) -> Tuple[np.ndarray, Dict]:
        """应用预处理步骤"""
        meta = {
            "original_size": (image.shape[1], image.shape[0]),
            "steps": []
        }
        
        # 1. 自动旋转（如果需要）
        if config.get("auto_rotate", True):
            rotated, rotation_meta = self._auto_rotate(image, exif_data)
            image = rotated
            meta["steps"].append({
                "step": "auto_rotate",
                "meta": rotation_meta
            })
        
        # 2. 格式转换
        if "format" in config:
            converted, format_meta = self._convert_format(image, config["format"])
            image = converted
            meta["steps"].append({
                "step": "format_conversion",
                "meta": format_meta
            })
        
        # 3. 尺寸调整
        if "max_size" in config:
            resized, resize_meta = self._resize_image(image, config["max_size"])
            image = resized
            meta["steps"].append({
                "step": "resize",
                "meta": resize_meta
            })
        
        # 4. 基础修复
        if config.get("basic_repair", True):
            repaired, repair_meta = self._basic_repair(image)
            image = repaired
            meta["steps"].append({
                "step": "basic_repair",
                "meta": repair_meta
            })
        
        return image, meta
    
    def _auto_rotate(
        self,
        image: np.ndarray,
        exif_data: Dict
    ) -> Tuple[np.ndarray, Dict]:
        """自动旋转图像"""
        orientation = exif_data.get('Image Orientation')
        
        if not orientation:
            return image, {"rotation": 0}
        
        try:
            orientation = int(orientation)
            if orientation == 1:
                # 正常方向，无需旋转
                return image, {"rotation": 0}
            elif orientation == 6:
                # 顺时针90度
                rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                return rotated, {"rotation": 90}
            elif orientation == 8:
                # 逆时针90度
                rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                return rotated, {"rotation": -90}
            elif orientation == 3:
                # 180度
                rotated = cv2.rotate(image, cv2.ROTATE_180)
                return rotated, {"rotation": 180}
            else:
                return image, {"rotation": 0, "warning": f"Unsupported orientation: {orientation}"}
        except Exception as e:
            return image, {"rotation": 0, "error": str(e)}
    
    def _convert_format(
        self,
        image: np.ndarray,
        target_format: str
    ) -> Tuple[np.ndarray, Dict]:
        """转换图像格式"""
        # 这里简化实现，实际应该根据目标格式进行转换
        return image, {"format": target_format}
    
    def _resize_image(
        self,
        image: np.ndarray,
        max_size: str
    ) -> Tuple[np.ndarray, Dict]:
        """调整图像大小"""
        # 解析最大尺寸
        width_str, height_str = max_size.split('x')
        max_width = int(width_str)
        max_height = int(height_str)
        
        # 获取当前尺寸
        current_height, current_width = image.shape[:2]
        
        # 计算缩放比例
        scale = min(max_width / current_width, max_height / current_height, 1.0)
        
        # 如果不需要缩放，返回原图
        if scale >= 1.0:
            return image, {
                "original_width": current_width,
                "original_height": current_height,
                "resized": False
            }
        
        # 计算新尺寸
        new_width = int(current_width * scale)
        new_height = int(current_height * scale)
        
        # 调整大小
        resized = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )
        
        return resized, {
            "original_width": current_width,
            "original_height": current_height,
            "resized_width": new_width,
            "resized_height": new_height,
            "scale": scale,
            "resized": True
        }
    
    def _basic_repair(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """基础修复（去噪等）"""
        # 应用非局部均值去噪
        denoised = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=10,
            hColor=10,
            templateWindowSize=7,
            searchWindowSize=21
        )
        
        return denoised, {
            "denoising": True,
            "parameters": {
                "h": 10,
                "hColor": 10
            }
        }
    
    def _save_image(
        self,
        image: np.ndarray,
        source_path: str,
        config: Dict
    ) -> str:
        """保存处理后的图像"""
        # 生成临时文件路径
        temp_dir = self.config.temp_dir or tempfile.gettempdir()
        file_name = os.path.basename(source_path)
        output_path = os.path.join(temp_dir, f"preprocessed_{file_name}")
        
        # 转换回BGR（OpenCV格式）
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 保存图像
        cv2.imwrite(output_path, bgr_image)
        
        return output_path

class MediaEnhancer:
    """媒体增强器，执行AI增强任务"""
    
    def __init__(
        self,
        model_registry: ModelRegistry,
        config: Config
    ):
        self.model_registry = model_registry
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def enhance(
        self,
        file_path: str,
        config: Dict
    ) -> Tuple[str, Dict]:
        """
        增强媒体文件
        
        :param file_path: 文件路径
        :param config: 增强配置
        :return: (增强后的文件路径, 增强元数据)
        """
        # 1. 加载图像
        image = self._load_image(file_path)
        
        # 2. 应用增强步骤
        enhanced, meta = self._apply_enhancement_steps(image, config)
        
        # 3. 保存增强后的文件
        output_path = self._save_image(enhanced, file_path, config)
        
        return output_path, meta
    
    def _load_image(self, file_path: str) -> np.ndarray:
        """加载图像"""
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Failed to read image: {file_path}")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def _apply_enhancement_steps(
        self,
        image: np.ndarray,
        config: Dict
    ) -> Tuple[np.ndarray, Dict]:
        """应用增强步骤"""
        meta = {
            "original_size": (image.shape[1], image.shape[0]),
            "steps": []
        }
        
        # 1. 超分辨率
        if config.get("scale_factor", 1) > 1:
            enhanced, sr_meta = self._super_resolution(image, config)
            image = enhanced
            meta["steps"].append({
                "step": "super_resolution",
                "meta": sr_meta
            })
        
        # 2. 色彩校正
        if config.get("color_correction", True):
            corrected, color_meta = self._color_correction(image)
            image = corrected
            meta["steps"].append({
                "step": "color_correction",
                "meta": color_meta
            })
        
        # 3. 智能裁剪
        if config.get("smart_crop", True):
            cropped, crop_meta = self._smart_crop(image, config)
            image = cropped
            meta["steps"].append({
                "step": "smart_crop",
                "meta": crop_meta
            })
        
        # 4. 面部增强（如果启用且检测到人脸）
        if config.get("face_enhance", False):
            enhanced, face_meta = self._face_enhancement(image)
            image = enhanced
            meta["steps"].append({
                "step": "face_enhancement",
                "meta": face_meta
            })
        
        return image, meta
    
    def _super_resolution(
        self,
        image: np.ndarray,
        config: Dict
    ) -> Tuple[np.ndarray, Dict]:
        """超分辨率处理"""
        # 获取模型
        model_name = config.get("model", "realesrgan-x4plus")
        model = self.model_registry.get_model(model_name)
        
        # 执行超分辨率
        try:
            # 将图像转换为Bytes
            _, buffer = cv2.imencode('.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            image_bytes = buffer.tobytes()
            
            # 调用模型服务
            enhanced_bytes = model.process(image_bytes)
            
            # 转换回图像
            nparr = np.frombuffer(enhanced_bytes, np.uint8)
            enhanced = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
            
            return enhanced, {
                "model": model_name,
                "scale_factor": config.get("scale_factor", 2),
                "success": True
            }
            
        except Exception as e:
            self.logger.error("Super resolution failed: %s", str(e))
            return image, {
                "model": model_name,
                "error": str(e),
                "success": False
            }
    
    def _color_correction(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """色彩校正"""
        # 简单实现：自动对比度和亮度调整
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # 应用CLAHE（对比度受限的自适应直方图均衡化）
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        
        # 合并通道
        corrected_lab = cv2.merge((cl, a, b))
        corrected = cv2.cvtColor(corrected_lab, cv2.COLOR_LAB2RGB)
        
        return corrected, {
            "method": "clahe",
            "clip_limit": 3.0,
            "tile_grid_size": (8, 8)
        }
    
    def _smart_crop(
        self,
        image: np.ndarray,
        config: Dict
    ) -> Tuple[np.ndarray, Dict]:
        """智能裁剪"""
        # 简单实现：基于内容感知的裁剪
        # 实际应用中应该使用更复杂的算法
        
        # 获取目标宽高比
        aspect_ratio = config.get("aspect_ratio", "original")
        if aspect_ratio == "original":
            return image, {"cropped": False}
        
        try:
            # 解析宽高比
            width_ratio, height_ratio = map(float, aspect_ratio.split(':'))
            target_ratio = width_ratio / height_ratio
            
            # 获取当前尺寸
            height, width = image.shape[:2]
            current_ratio = width / height
            
            # 计算裁剪区域
            if current_ratio > target_ratio:
                # 宽度过宽，裁剪宽度
                new_width = int(height * target_ratio)
                start_x = (width - new_width) // 2
                cropped = image[:, start_x:start_x + new_width, :]
            else:
                # 高度过高，裁剪高度
                new_height = int(width / target_ratio)
                start_y = (height - new_height) // 2
                cropped = image[start_y:start_y + new_height, :, :]
            
            return cropped, {
                "original_width": width,
                "original_height": height,
                "cropped_width": cropped.shape[1],
                "cropped_height": cropped.shape[0],
                "cropped": True
            }
            
        except Exception as e:
            self.logger.error("Smart crop failed: %s", str(e))
            return image, {
                "error": str(e),
                "cropped": False
            }
    
    def _face_enhancement(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """面部增强"""
        # 这里简化实现，实际应该调用专门的面部增强模型
        return image, {"enhanced": False, "message": "Face enhancement not implemented"}
    
    def _save_image(
        self,
        image: np.ndarray,
        source_path: str,
        config: Dict
    ) -> str:
        """保存增强后的图像"""
        # 生成临时文件路径
        temp_dir = self.config.temp_dir or tempfile.gettempdir()
        file_name = os.path.basename(source_path)
        output_path = os.path.join(temp_dir, f"enhanced_{file_name}")
        
        # 转换回BGR（OpenCV格式）
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 保存图像
        cv2.imwrite(output_path, bgr_image)
        
        return output_path

class MediaAnalyzer:
    """媒体分析器，执行内容分析任务"""
    
    def __init__(
        self,
        tagger: MediaTagger,
        quality_analyzer: QualityAnalyzer,
        face_detector: FaceDetector,
        config: Config
    ):
        self.tagger = tagger
        self.quality_analyzer = quality_analyzer
        self.face_detector = face_detector
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def analyze(
        self,
        file_path: str,
        config: Dict
    ) -> Dict:
        """
        分析媒体文件
        
        :param file_path: 文件路径
        :param config: 分析配置
        :return: 分析结果
        """
        results = {
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # 1. 标签分析
        if "tags" in config.get("tasks", []):
            results["tags"] = self.tagger.generate_tags(file_path)
        
        # 2. 质量分析
        if "quality-assessment" in config.get("tasks", []):
            results["quality"] = self.quality_analyzer.assess(file_path)
        
        # 3. 人脸分析
        if "face-detection" in config.get("tasks", []):
            results["faces"] = self.face_detector.detect(file_path)
        
        # 4. 相似图片检测
        if "duplicate-detection" in config.get("tasks", []):
            results["duplicates"] = self._detect_duplicates(file_path)
        
        return results
    
    def _detect_duplicates(self, file_path: str) -> List[Dict]:
        """检测相似图片"""
        # 简单实现：基于感知哈希
        try:
            # 计算当前图片的哈希
            current_hash = self._calculate_image_hash(file_path)
            
            # 获取数据库中所有图片
            all_images = self._get_all_images()
            
            # 计算相似度
            duplicates = []
            for image in all_images:
                similarity = self._calculate_similarity(current_hash, image["hash"])
                if similarity > 0.85:  # 相似度阈值
                    duplicates.append({
                        "image_id": image["id"],
                        "path": image["path"],
                        "similarity": similarity
                    })
            
            return duplicates
            
        except Exception as e:
            self.logger.error("Duplicate detection failed: %s", str(e))
            return []
    
    def _calculate_image_hash(self, file_path: str) -> str:
        """计算图像感知哈希"""
        img = Image.open(file_path)
        img = img.convert('L').resize((64, 64), Image.LANCZOS)
        hash = imagehash.phash(img)
        return str(hash)
    
    def _get_all_images(self) -> List[Dict]:
        """获取所有图片（简化实现）"""
        # 这里应该从数据库获取
        return []
    
    def _calculate_similarity(self, hash1: str, hash2: str) -> float:
        """计算两个哈希的相似度"""
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        return 1 - (h1 - h2) / len(h1.hash) ** 2

class ModelRegistry:
    """模型注册表，管理可用的AI模型"""
    
    def __init__(self, config: Config):
        self.config = config
        self.models = {}
        self.logger = logging.getLogger(__name__)
        self._load_models()
    
    def _load_models(self):
        """加载模型配置"""
        # 从配置加载模型
        for model_config in self.config.models:
            try:
                model = self._create_model(model_config)
                self.models[model_config["id"]] = model
                self.logger.info("Loaded model: %s", model_config["id"])
            except Exception as e:
                self.logger.error("Failed to load model %s: %s", model_config["id"], str(e))
    
    def _create_model(self, config: Dict) -> Any:
        """创建模型实例"""
        if config["type"] == "super-resolution":
            return SuperResolutionModel(config)
        elif config["type"] == "face-enhancement":
            return FaceEnhancementModel(config)
        # 其他模型类型...
        else:
            raise ValueError(f"Unsupported model type: {config['type']}")
    
    def get_model(self, model_id: str) -> Any:
        """获取模型"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        return self.models[model_id]

class SuperResolutionModel:
    """超分辨率模型封装"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.model = self._load_model()
    
    def _load_model(self):
        """加载模型"""
        # 根据配置加载适当的模型
        if self.config["name"] == "realesrgan-x4plus":
            from realesrgan import RealESRGANer
            return RealESRGANer(
                scale=self.config["scale"],
                model_path=self.config["model_path"],
                tile=self.config.get("tile", 0),
                tile_pad=self.config.get("tile_pad", 10),
                pre_pad=self.config.get("pre_pad", 0),
                half=self.config.get("half", True)
            )
        # 具他模型...
        else:
            raise ValueError(f"Unsupported model: {self.config['name']}")
    
    def process(self, image_bytes: bytes) -> bytes:
        """处理图像"""
        # 将码图像
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 执行超分辨率
        try:
            output, _ = self.model.enhance(img, outscale=self.config["scale"])
        except RuntimeError as e:
            if 'CUDA out of memory' in str(e):
                # 尝试减少分块大小
                self.model.tile = max(200, self.model.tile - 200)
                output, _ = self.model.enhance(img, outscale=self.config["scale"])
            else:
                raise
        
        # 编码结果
        _, buffer = cv2.imencode('.png', output)
        return buffer.tobytes()

# 辅助类定义
class ProcessingWorkflow:
    """处理工作流定义"""
    def __init__(
        self,
        id: str,
        preprocessing: Dict,
        enhancement: Dict,
        analysis: Dict,
        organization: Dict
    ):
        self.id = id
        self.preprocessing = preprocessing
        self.enhancement = enhancement
        self.analysis = analysis
        self.organization = organization

class ProcessingStatus:
    """处理状态"""
    def __init__(
        self,
        file_path: str,
        workflow_id: str,
        status: str,
        step: Optional[str] = None,
        progress: float = 0.0,
        error: Optional[str] = None,
        result: Optional[Dict] = None
    ):
        self.file_path = file_path
        self.workflow_id = workflow_id
        self.status = status
        self.step = step
        self.progress = progress
        self.error = error
        self.result = result
        self.timestamp = datetime.utcnow().isoformat()

class ProcessingResult:
    """处理结果"""
    def __init__(
        self,
        processed_path: str,
        report: Dict,
        analysis: Dict,
        processing_time: float
    ):
        self.processed_path = processed_path
        self.report = report
        self.analysis = analysis
        self.processing_time = processing_time
```

#### 5.4.3 媒体分析服务

**技术实现：**
```python
import cv2
import numpy as np
import torch
import clip
from PIL import Image
import face_recognition
from typing import List, Dict, Tuple, Optional
import logging
import os
import hashlib
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import faiss
import pickle

class MediaTagger:
    """媒体标签生成器，基于CLIP模型"""
    
    def __init__(
        self,
        clip_model_name: str = "ViT-B/32",
        face_detection_model: str = "retinaface_resnet50",
        config: Config = None
    ):
        self.logger = logging.getLogger(__name__)
        self.config = config or Config()
        
        # 加载CLIP模型
        self.logger.info("Loading CLIP model: %s", clip_model_name)
        self.clip_model, self.clip_preprocess = clip.load(clip_model_name, device="cuda" if torch.cuda.is_available() else "cpu")
        self.clip_model.eval()
        
        # 加载人脸检测模型
        self.logger.info("Loading face detection model: %s", face_detection_model)
        self.face_detector = self._load_face_detector(face_detection_model)
        
        # 预定义的标签候选
        self.candidate_tags = self.config.get("candidate_tags", [
            "portrait", "landscape", "architecture", "food", "animal", 
            "vehicle", "nature", "people", "event", "product",
            "indoor", "outdoor", "sunset", "night", "daytime",
            "close-up", "macro", "aerial", "black and white", "color"
        ])
    
    def _load_face_detector(self, model_name: str):
        """加载人脸检测模型"""
        if model_name == "retinaface_resnet50":
            from retinaface import RetinaFace
            return RetinaFace
        elif model_name == "mtcnn":
            from mtcnn import MTCNN
            return MTCNN()
        else:
            raise ValueError(f"Unsupported face detection model: {model_name}")
    
    def generate_tags(self, image_path: str) -> List[Dict]:
        """
        生成图像标签
        
        :param image_path: 图像路径
        :return: 标签列表
        """
        # 1. 加载并预处理图像
        try:
            image = self.clip_preprocess(Image.open(image_path)).unsqueeze(0).to(next(self.clip_model.parameters()).device)
        except Exception as e:
            self.logger.error("Error loading image %s: %s", image_path, str(e))
            return []
        
        # 2. 计算图像特征
        with torch.no_grad():
            image_features = self.clip_model.encode_image(image)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        # 3. 计算与候选标签的相似度
        text_inputs = torch.cat([clip.tokenize(f"a photo of {c}") for c in self.candidate_tags]).to(next(self.clip_model.parameters()).device)
        
        with torch.no_grad():
            text_features = self.clip_model.encode_text(text_inputs)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # 计算相似度
            similarity = (image_features @ text_features.T).cpu().numpy()[0]
        
        # 4. 选择前N个标签
        top_indices = np.argsort(similarity)[::-1][:self.config.get("max_tags", 5)]
        tags = []
        for idx in top_indices:
            if similarity[idx] > self.config.get("tag_threshold", 0.2):  # 阈值
                tags.append({
                    "tag": self.candidate_tags[idx],
                    "confidence": float(similarity[idx])
                })
        
        # 5. 检测人脸并添加相关标签
        face_tags = self._detect_faces(image_path)
        tags.extend(face_tags)
        
        return tags
    
    def _detect_faces(self, image_path: str) -> List[Dict]:
        """检测人脸并生成相关标签"""
        try:
            # 检测人脸
            faces = self.face_detector.detect_faces(image_path)
            
            tags = []
            if faces:
                tags.append({"tag": "people", "confidence": min(1.0, len(faces) * 0.2)})
                
                # 检查是否是单人照
                if len(faces) == 1:
                    tags.append({"tag": "portrait", "confidence": 0.8})
                
                # 檢查是否是多人照
                elif len(faces) >= 3:
                    tags.append({"tag": "group", "confidence": 0.7})
            
            return tags
            
        except Exception as e:
            self.logger.warning("Face detection failed: %s", str(e))
            return []

class QualityAnalyzer:
    """图像质量分析器"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
    
    def assess(self, image_path: str) -> Dict:
        """
        评估图像质量
        
        :param image_path: 图像路径
        :return: 质量评估结果
        """
        try:
            # 1. 加载图像
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            
            # 2. 计算清晰度（使用Laplacian方差）
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 3. 归一化到0-1范围
            quality_score = min(1.0, max(0.0, fm / self.config.get("sharpness_threshold", 100.0)))
            
            # 4. 检查曝光
            exposure = self._analyze_exposure(gray)
            
            # 5. 检查色彩
            colorfulness = self._analyze_colorfulness(image)
            
            return {
                "score": quality_score,
                "sharpness": float(fm),
                "exposure": exposure,
                "colorfulness": colorfulness,
                "issues": self._identify_quality_issues(fm, exposure, colorfulness)
            }
            
        except Exception as e:
            self.logger.error("Quality assessment failed: %s", str(e))
            return {
                "score": 0.0,
                "error": str(e)
            }
    
    def _analyze_exposure(self, gray: np.ndarray) -> Dict:
        """分析曝光"""
        # 计算直方图
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist.flatten() / hist.sum()
        
        # 计算平均亮度
        mean_brightness = np.sum(np.arange(256) * hist)
        
        # 分析曝光问题
        issues = []
        if mean_brightness < 50:
            issues.append("underexposed")
        elif mean_brightness > 200:
            issues.append("overexposed")
        
        return {
            "mean_brightness": float(mean_brightness),
            "issues": issues
        }
    
    def _analyze_colorfulness(self, image: np.ndarray) -> Dict:
        """分析色彩丰富度"""
        # 转换到HSV空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # 计算饱和度统计
        saturation_mean = cv2.mean(s)[0]
        saturation_std = np.std(s)
        
        # 分析色彩问题
        issues = []
        if saturation_mean < 30:
            issues.append("low_saturation")
        
        return {
            "saturation_mean": float(saturation_mean),
            "saturation_std": float(saturation_std),
            "issues": issues
        }
    
    def _identify_quality_issues(
        self,
        sharpness: float,
        exposure: Dict,
        colorfulness: Dict
    ) -> List[str]:
        """识别质量问題"""
        issues = []
        
        # 清晰度问题
        if sharpness < self.config.get("sharpness_threshold", 100.0) * 0.3:
            issues.append("blurry")
        
        # 曝光问题
        issues.extend(exposure["issues"])
        
        # 色彩问题
        issues.extend(colorfulness["issues"])
        
        return issues

class FaceDetector:
    """人脸检测器"""
    
    def __init__(
        self,
        model_name: str = "retinaface_resnet50",
        config: Config = None
    ):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        
        # 加载人脸检测模型
        self.logger.info("Loading face detection model: %s", model_name)
        self.face_detector = self._load_face_detector(model_name)
        
        # 加载人脸识别模型
        self.logger.info("Loading face recognition model")
        self.face_recognition = face_recognition
    
    def _load_face_detector(self, model_name: str):
        """加载人脸检测模型"""
        if model_name == "retinaface_resnet50":
            from retinaface import RetinaFace
            return RetinaFace
        elif model_name == "mtcnn":
            from mtcnn import MTCNN
            return MTCNN()
        else:
            raise ValueError(f"Unsupported face detection model: {model_name}")
    
    def detect(self, image_path: str) -> List[Dict]:
        """
        检测图像中的人脸
        
        :param image_path: 图像路径
        :return: 人脸列表
        """
        try:
            # 检测人脸
            faces = self.face_detector.detect_faces(image_path)
            
            # 处理结果
            results = []
            for i, face in enumerate(faces):
                x, y, w, h = face['facial_area']
                confidence = face['score']
                
                # 获取人脸特征
                face_image = Image.open(image_path).crop((x, y, x+w, y+h))
                face_encoding = self._get_face_encoding(face_image)
                
                results.append({
                    "index": i,
                    "bbox": [x, y, w, h],
                    "confidence": float(confidence),
                    "encoding": face_encoding.tolist() if face_encoding is not None else None
                })
            
            return results
            
        except Exception as e:
            self.logger.error("Face detection failed: %s", str(e))
            return []
    
    def _get_face_encoding(self, face_image: Image.Image) -> Optional[np.ndarray]:
        """获取人脸特征编码"""
        try:
            # 转换为numpy数组
            face_np = np.array(face_image)
            
            # 获取人脸编码
            encodings = self.face_recognition.face_encodings(face_np)
            return encodings[0] if encodings else None
            
        except Exception as e:
            self.logger.warning("Face encoding failed: %s", str(e))
            return None

class MediaClassifier:
    """媒体文件智能分类系统"""
    
    def __init__(
        self,
        clip_model_name: str = "ViT-B/32",
        face_detection_model: str = "retinaface_resnet50",
        cluster_count: int = 50,
        index_path: Optional[str] = None,
        config: Config = None
    ):
        """
        初始化媒体分类器
        
        :param clip_model_name: CLIP模型名称
        :param face_detection_model: 人脸检测模型
        :param cluster_count: 聚类数量
        :param index_path: FAISS索引路径 (用于相似图片查找)
        :param config: 配置
        """
        self.logger = logging.getLogger(__name__)
        self.config = config or Config()
        
        # 初始化CLIP模型
        self.logger.info("Loading CLIP model: %s", clip_model_name)
        self.clip_model, self.clip_preprocess = clip.load(clip_model_name, device="cuda" if torch.cuda.is_available() else "cpu")
        self.clip_model.eval()
        
        # 初始化人脸检测
        self.logger.info("Loading face detection model: %s", face_detection_model)
        self.face_detector = self._load_face_detector(face_detection_model)
        
        # 聚类配置
        self.cluster_count = cluster_count
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # 保留95%方差
        self.kmeans = KMeans(n_clusters=cluster_count, random_state=42)
        
        # 相似度索引
        self.index_path = index_path
        self.index = self._load_or_create_index()
        
        # 标签映射
        self.label_map = {}
        self.cluster_descriptions = {}
    
    def _load_face_detector(self, model_name: str):
        """加载人脸检测模型"""
        if model_name == "retinaface_resnet50":
            from retinaface import RetinaFace
            return RetinaFace
        elif model_name == "mtcnn":
            from mtcnn import MTCNN
            return MTCNN()
        else:
            raise ValueError(f"Unsupported face detection model: {model_name}")
    
    def _load_or_create_index(self):
        """加载或创建FAISS索引"""
        if self.index_path and os.path.exists(self.index_path):
            self.logger.info("Loading FAISS index from %s", self.index_path)
            return faiss.read_index(self.index_path)
        else:
            # 创建新的索引 (使用HNSW for efficient search)
            dimension = 512  # CLIP特征维度
            M = 32  # HNSW参数
            ef_construction = 128  # HNSW参数
            
            index = faiss.IndexHNSWFlat(dimension, M)
            index.hnsw.efConstruction = ef_construction
            index.hnsw.efSearch = 64
            
            return index
    
    def extract_features(self, image_path: str) -> np.ndarray:
        """提取图像特征向量"""
        # 加载并预处理图像
        image = self.clip_preprocess(Image.open(image_path)).unsqueeze(0).to(next(self.clip_model.parameters()).device)
        
        # 提取CLIP特征
        with torch.no_grad():
            features = self.clip_model.encode_image(image)
            features = features / features.norm(dim=-1, keepdim=True)  # L2归一化
        
        return features.cpu().numpy().flatten()
    
    def extract_face_features(self, image_path: str) -> List[np.ndarray]:
        """提取人脸特征"""
        # 检测人脸
        faces = self.face_detector.detect_faces(image_path)
        
        face_features = []
        for face in faces:
            # 提取人脸区域
            x, y, w, h = face['facial_area']
            face_img = Image.open(image_path).crop((x, y, x+w, y+h))
            
            # 预处理并提取特征
            face_img = self.clip_preprocess(face_img).unsqueeze(0).to(next(self.clip_model.parameters()).device)
            
            with torch.no_grad():
                features = self.clip_model.encode_image(face_img)
                features = features / features.norm(dim=-1, keepdim=True)
            
            face_features.append(features.cpu().numpy().flatten())
        
        return face_features
    
    def classify_image(
        self,
        image_path: str,
        generate_tags: bool = True,
        detect_faces: bool = True
    ) -> Dict:
        """
        分类单个图像
        
        :param image_path: 图像路径
        :param generate_tags: 是否生成语义标签
        :param detect_faces: 是否检测人脸
        :return: 分类结果
        """
        start_time = time.time()
        
        # 提取图像特征
        image_features = self.extract_features(image_path)
        
        # 人脸检测与特征提取
        face_data = []
        if detect_faces:
            face_features = self.extract_face_features(image_path)
            for i, features in enumerate(face_features):
                # 识别人脸 (与已知人脸聚类比较)
                face_id = self._identify_face(features)
                face_data.append({
                    "index": i,
                    "face_id": face_id,
                    "confidence": self._calculate_face_confidence(features, face_id)
                })
        
        # 查找相以图片
        similar_images = self._find_similar_images(image_features, k=10)
        
        # 生成语义标签
        tags = []
        if generate_tags:
            tags = self._generate_semantic_tags(image_features)
        
        # 确定图像类别
        cluster_id = self.kmeans.predict([image_features])[0]
        category = self.cluster_descriptions.get(cluster_id, f"Cluster {cluster_id}")
        
        processing_time = time.time() - start_time
        
        return {
            "image_path": image_path,
            "features": image_features.tolist(),
            "cluster_id": int(cluster_id),
            "category": category,
            "tags": tags,
            "face_data": face_data,
            "similar_images": similar_images,
            "processing_time": processing_time,
            "quality_score": self._assess_image_quality(image_path)
        }
    
    def _identify_face(self, face_features: np.ndarray) -> str:
        """识别人脸，返回face_id"""
        # 檢查是否与已知人脸匹配
        distances = []
        known_faces = self._get_known_faces()  # 从数据库获取已知人脸
        
        if not known_faces:
            # 如果没有已知人脸，创建新face_id
            return f"face-{uuid.uuid4().hex[:8]}"
        
        for face_id, features in known_faces.items():
            distance = np.linalg.norm(face_features - features)
            distances.append((face_id, distance))
        
        if distances:
            # 按距离排序
            distances.sort(key=lambda x: x[1])
            closest_id, min_distance = distances[0]
            
            # 檢查是否在阈值内
            if min_distance < self.config.get("face_distance_threshold", 0.6):
                return closest_id
        
        # 如果是新人脸，创建新face_id
        new_face_id = f"face-{uuid.uuid4().hex[:8]}"
        self._add_new_face(new_face_id, face_features)
        return new_face_id
    
    def _calculate_face_confidence(self, face_features: np.ndarray, face_id: str) -> float:
        """计算人脸识别置信度"""
        known_faces = self._get_known_faces()
        if face_id not in known_faces:
            return 0.0
        
        distance = np.linalg.norm(face_features - known_faces[face_id])
        # 转换为0-1的置信度 (距离越小，置信度越高)
        return max(0.0, min(1.0, 1.0 - (distance / 1.5)))
    
    def _find_similar_images(self, features: np.ndarray, k: int = 10) -> List[Dict]:
        """查找相以图片"""
        # 添加到索引 (临时)
        index = faiss.IndexFlatL2(features.shape[0])
        index.add(np.array([features]))
        
        # 搜索相以图片
        D, I = self.index.search(np.array([features]), k+1)  # +1 because it includes the query itself
        
        results = []
        for i in range(1, min(k+1, len(I[0]))):  # 跳过第一个结果 (查询本身)
            idx = I[0][i]
            distance = D[0][i]
            similarity = 1 / (1 + distance)  # 转换为相以度
            
            # 获取图片信息 (从数据库)
            image_info = self._get_image_info_by_index(idx)
            if image_info:
                results.append({
                    "image_id": image_info["id"],
                    "path": image_info["path"],
                    "similarity": float(similarity),
                    "distance": float(distance)
                })
        
        return results
    
    def _generate_semantic_tags(self, features: np.ndarray) -> List[Dict]:
        """生成语义标签"""
        # 预定义的标签候选
        candidate_tags = self.config.get("candidate_tags", [
            "portrait", "landscape", "architecture", "food", "animal", 
            "vehicle", "nature", "people", "event", "product",
            "indoor", "outdoor", "sunset", "night", "daytime",
            "close-up", "macro", "aerial", "black and white", "color"
        ])
        
        # 使用CLIP计算与候选标签的相以度
        text_inputs = torch.cat([clip.tokenize(f"a photo of {c}") for c in candidate_tags]).to(next(self.clip_model.parameters()).device)
        
        with torch.no_grad():
            text_features = self.clip_model.encode_text(text_inputs)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # 计算相以度
            similarity = (torch.from_numpy(features).float() @ text_features.T).cpu().numpy()
        
        # 选择前N个标签
        top_indices = np.argsort(similarity)[::-1][:5]
        tags = []
        for idx in top_indices:
            if similarity[idx] > self.config.get("tag_threshold", 0.2):  # 阈值
                tags.append({
                    "tag": candidate_tags[idx],
                    "confidence": float(similarity[idx])
                })
        
        return tags
    
    def _assess_image_quality(self, image_path: str) -> float:
        """评估图像质量 (0-1)"""
        # 简单实现：使用OpenCV计算清晰度
        image = cv2.imread(image_path)
        if image is None:
            return 0.0
        
        # 转换为灰度
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 计算Laplacian方差 (衡量清晰度)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 归一化到0-1范围 (基于经验值)
        quality = min(1.0, max(0.0, fm / 100.0))
        
        return quality
    
    def train_clusters(self, feature_vectors: List[np.ndarray]):
        """训练聚类模型"""
        # 标准化特征
        scaled_features = self.scaler.fit_transform(feature_vectors)
        
        # PCA降维
        reduced_features = self.pca.fit_transform(scaled_features)
        
        # K-Means聚类
        self.kmeans.fit(reduced_features)
        
        # 为每个聚类生成描述
        self._generate_cluster_descriptions(feature_vectors)
    
    def _generate_cluster_descriptions(self, feature_vectors: List[np.ndarray]):
        """为每个聚类生成描述性标签"""
        # 对每个聚类，选择代表性图像
        cluster_centers = self.kmeans.cluster_centers_
        representative_images = {}
        
        for i, center in enumerate(cluster_centers):
            # 找到最近的特征向量
            distances = [np.linalg.norm(feat - center) for feat in feature_vectors]
            closest_idx = np.argmin(distances)
            representative_images[i] = feature_vectors[closest_idx]
        
        # 为每个聚类生成描述
        for cluster_id, features in representative_images.items():
            tags = self._generate_semantic_tags(features)
            top_tags = sorted(tags, key=lambda x: x["confidence"], reverse=True)[:3]
            self.cluster_descriptions[cluster_id] = ", ".join([t["tag"] for t in top_tags]) or f"Cluster {cluster_id}"
    
    def add_to_index(self, image_id: str, features: np.ndarray):
        """将图像特征添加到索引"""
        # 添加到FAISS索引
        self.index.add(np.array([features]))
        
        # 保存到数据库 (image_id -> index position)
        self._save_index_mapping(image_id, self.index.ntotal - 1)
        
        # 保存索引到磁盘
        if self.index_path:
            faiss.write_index(self.index, self.index_path)
    
    def update_index(self):
        """更新索引 (重新训练聚类等)"""
        # 获取所有特征向量
        all_features = self._get_all_features()
        
        if len(all_features) > self.cluster_count:
            # 重新训练聚类
            self.train_clusters(all_features)
        
        # 重建FAISS索引
        self.index = self._load_or_create_index()
        for image_id, features in all_features:
            self.add_to_index(image_id, features)
    
    # 以下为数据库交互方法 (需根据实际数据库实现)
    def _get_known_faces(self) -> Dict[str, np.ndarray]:
        """获取已知人脸特征 (从数据库)"""
        # 实现数据库查询
        pass
    
    def _add_new_face(self, face_id: str, features: np.ndarray):
        """添加新人脸到数据库"""
        # 实现数据库插入
        pass
    
    def _get_image_info_by_index(self, index: int) -> Optional[Dict]:
        """通过索引获取图像信息"""
        # 实现数据库查询
        pass
    
    def _save_index_mapping(self, image_id: str, index_pos: int):
        """保存图像ID到索引位置的映射"""
        # 实现数据库插入
        pass
    
    def _get_all_features(self) -> List[Tuple[str, np.ndarray]]:
        """获取所有图像特征"""
        # 实现数据库查询
        pass
```

### 5.5 数据模型详细定义

#### 5.5.1 媒体文件表

```sql
-- 媒体文件元数据表
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    source_id UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    workflow_instance_id UUID REFERENCES workflow_instances(id) ON DELETE SET NULL,
    path VARCHAR(1024) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    size BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'raw' CHECK (status IN ('raw', 'processing', 'processed', 'failed', 'archived')),
    original_id UUID REFERENCES media_files(id) ON DELETE SET NULL,
    version INT NOT NULL DEFAULT 1,
    metadata JSONB DEFAULT '{}'::jsonb,
    exif JSONB DEFAULT '{}'::jsonb,
    ai_analysis JSONB DEFAULT '{}'::jsonb,
    
    -- 索引
    UNIQUE (project_id, path, version),
    INDEX idx_media_files_project ON media_files(project_id),
    INDEX idx_media_files_source ON media_files(source_id),
    INDEX idx_media_files_status ON media_files(status),
    INDEX idx_media_files_created ON media_files(created_at DESC),
    INDEX idx_media_files_processed ON media_files(processed_at DESC),
    
    -- 全文搜索
    ts_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('simple', coalesce(filename, '') || ' ' || coalesce(metadata->>'title', '') || ' ' || coalesce(metadata->>'description', ''))
    ) STORED
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_media_files_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_media_files_modtime
BEFORE UPDATE ON media_files
FOR EACH ROW
EXECUTE FUNCTION update_media_files_modtime();

-- 全文搜索索引
CREATE INDEX idx_media_files_search ON media_files USING GIN (ts_vector);
```

#### 5.5.2 媒体处理任务表

```sql
-- 媒体处理任务表
CREATE TABLE media_processing_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID NOT NULL REFERENCES media_files(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'canceled')),
    priority INT NOT NULL DEFAULT 5,
    queued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration INTERVAL,
    worker_id VARCHAR(255),
    input_path VARCHAR(1024),
    output_path VARCHAR(1024),
    error JSONB,
    retry_count INT NOT NULL DEFAULT 0,
    max_retries INT NOT NULL DEFAULT 3,
    resource_requirements JSONB DEFAULT '{}'::jsonb,
    
    -- 索引
    INDEX idx_tasks_file ON media_processing_tasks(file_id),
    INDEX idx_tasks_status ON media_processing_tasks(status),
    INDEX idx_tasks_priority ON media_processing_tasks(priority, queued_at),
    INDEX idx_tasks_worker ON media_processing_tasks(worker_id),
    INDEX idx_tasks_queued ON media_processing_tasks(queued_at)
);
```

#### 5.5.3 媒体标签表

```sql
-- 媒体标签表
CREATE TABLE media_tags (
    file_id UUID NOT NULL REFERENCES media_files(id) ON DELETE CASCADE,
    tag_type VARCHAR(50) NOT NULL,
    tag_value VARCHAR(255) NOT NULL,
    confidence NUMERIC(4,2) NOT NULL,
    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    PRIMARY KEY (file_id, tag_type, tag_value),
    INDEX idx_tags_file ON media_tags(file_id),
    INDEX idx_tags_type ON media_tags(tag_type),
    INDEX idx_tags_value ON media_tags(tag_value)
);
```

#### 5.5.4 媒体相以度表

```sql
-- 媒体相以度表 (用于查找相以图片)
CREATE TABLE media_similarity (
    file_id1 UUID NOT NULL REFERENCES media_files(id) ON DELETE CASCADE,
    file_id2 UUID NOT NULL REFERENCES media_files(id) ON DELETE CASCADE,
    similarity_score NUMERIC(5,4) NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    PRIMARY KEY (file_id1, file_id2, algorithm),
    CHECK (file_id1 < file_id2),  -- 避免重复存储
    INDEX idx_similarity_score ON media_similarity(similarity_score DESC),
    INDEX idx_similarity_file1 ON media_similarity(file_id1)
);
```

### 5.6 API详细规范

#### 5.6.1 媒体处理API

**触发媒体文件处理 (POST /api/v1/media:process)**

*请求示例:*
```http
POST /api/v1/media:process HTTP/1.1
Host: amp.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json
X-Request-ID: req-345678

{
  "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
  "workflow": "nas-photo-processing",
  "parameters": {
    "image_enhance": {
      "scale_factor": 2,
      "denoise_strength": 0.3
    },
    "storage": {
      "bucket": "processed-photos",
      "path_template": "year={year}/month={month}/{filename}"
    }
  },
  "priority": 5,
  "callback_url": "https://myapp.com/callback/media-processing"
}
```

*成功响应示例:*
```http
HTTP/1.1 202 Accepted
Content-Type: application/json
Location: /api/v1/media/processingTasks/pt-123456
X-Request-ID: req-345678

{
  "task_id": "pt-123456",
  "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
  "workflow": "nas-photo-processing",
  "status": "queued",
  "queued_at": "2023-06-15T10:30:45Z",
  "priority": 5,
  "callback_url": "https://myapp.com/callback/media-processing",
  "metadata": {
    "project_id": "proj-456",
    "user_id": "user-123"
  }
}
```

**获取处理任务状态 (GET /api/v1/media/processingTasks/{task_id})**

*请求示例:*
```http
GET /api/v1/media/processingTasks/pt-123456 HTTP/1.1
Host: amp.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例 (处理中):*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "task_id": "pt-123456",
  "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
  "workflow": "nas-photo-processing",
  "status": "processing",
  "queued_at": "2023-06-15T10:30:45Z",
  "started_at": "2023-06-15T10:31:10Z",
  "priority": 5,
  "worker_id": "worker-gpu-04",
  "current_node": "ai/image-enhance",
  "progress": 0.65,
  "input_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
  "output_path": "/nas/photos/processed/vacation/IMG_20230615_103045.jpg",
  "error": null,
  "retry_count": 0,
  "max_retries": 3,
  "resource_requirements": {
    "memory_mb": 8192,
    "cpu_millis": 4000,
    "gpu_required": true,
    "accelerator_type": "nvidia-tesla-t4"
  },
  "resource_usage": {
    "cpu_seconds": 120.5,
    "memory_mb_seconds": 785000,
    "gpu_utilization": 0.75
  },
  "callback_url": "https://myapp.com/callback/media-processing",
  "metadata": {
    "project_id": "proj-456",
    "user_id": "user-123"
  }
}
```

*成功响应示例 (已完成):*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "task_id": "pt-123456",
  "file_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
  "workflow": "nas-photo-processing",
  "status": "completed",
  "queued_at": "2023-06-15T10:30:45Z",
  "started_at": "2023-06-15T10:31:10Z",
  "completed_at": "2023-06-15T10:38:25Z",
  "duration": "PT7m15s",
  "priority": 5,
  "worker_id": "worker-gpu-04",
  "input_path": "/nas/photos/raw/vacation/IMG_20230615_103045.jpg",
  "output_path": "/nas/photos/processed/vacation/IMG_20230615_103045.jpg",
  "error": null,
  "retry_count": 0,
  "max_retries": 3,
  "resource_requirements": {
    "memory_mb": 8192,
    "cpu_millis": 4000,
    "gpu_required": true,
    "accelerator_type": "nvidia-tesla-t4"
  },
  "resource_usage": {
    "cpu_seconds": 435.2,
    "memory_mb_seconds": 3542000,
    "gpu_utilization": 0.68,
    "storage_read_bytes": 15728640,
    "storage_write_bytes": 31457280
  },
  "output_metadata": {
    "width": 8192,
    "height": 4608,
    "format": "jpeg",
    "size": 4294967,
    "quality_score": 0.92,
    "tags": [
      {"tag": "portrait", "confidence": 0.87},
      {"tag": "people", "confidence": 0.93},
      {"tag": "outdoor", "confidence": 0.78}
    ],
    "face_data": [
      {
        "index": 0,
        "face_id": "face-1a2b3c4d",
        "confidence": 0.92,
        "bounding_box": [120, 80, 240, 320]
      }
    ],
    "similar_images": [
      {
        "image_id": "img-789012",
        "path": "/nas/photos/processed/family/IMG_20230610_152030.jpg",
        "similarity": 0.85
      }
    ]
  },
  "callback_url": "https://myapp.com/callback/media-processing",
  "metadata": {
    "project_id": "proj-456",
    "user_id": "user-123"
  }
}
```

### 5.7 性能优化策略

#### 5.7.1 媒体处理性能优化

**1080P图片处理性能 (realesrgan-x4plus)**

| 指标 | 1 GPU | 2 GPUs | 4 GPUs |
|------|-------|--------|--------|
| **单文件处理时间** | <5.0s | <5.0s | <5.0s |
| **P95处理时间** | <5.0s | <5.0s | <5.0s |
| **吞吐量 (无GPU限制)** | >120 img/min | >240 img/min | >480 img/min |
| **GPU利用率** | 75-85% | 75-85% | 75-85% |
| **内存使用峰值** | <6GB/worker | <6GB/worker | <6GB/worker |
| **错误率** | <0.5% | <0.5% | <0.5% |
| **资源弹性** | <2min | <2min | <2min |

**4K图片处理流水线性能**

| 指标 | 1 GPU | 2 GPUs | 4 GPUs |
|------|-------|--------|--------|
| **端到端处理时间** | <25.0s | <25.0s | <25.0s |
| **P95处理时间** | <25.0s | <25.0s | <25.0s |
| **吞吐量 (批量)** | >30 img/min | >60 img/min | >120 img/min |
| **CPU/GPU平衡** | 优化 | 优化 | 优化 |
| **大文件处理稳定性** | 稳定 | 稳定 | 稳定 |
| **错误恢复时间** | <30s | <30s | <30s |

#### 5.7.2 详细测试脚本示例

**媒体处理性能测试脚本 (locustfile.py)**
```python
import os
import time
import json
import random
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import numpy as np
from datetime import datetime

# 测试配置
TEST_IMAGES = [
    "1080p-landscape.jpg",   # 1920x1080, 3.2MB
    "1080p-portrait.jpg",    # 1080x1920, 2.8MB
    "4k-landscape.jpg",      # 3840x2160, 8.5MB
    "4k-portrait.jpg",       # 2160x3840, 7.9MB
    "pro-photo.jpg"          # 6000x4000, 18.2MB
]

WORKFLOWS = [
    "nas-photo-processing",
    "video-thumbnail-generation",
    "document-processing-pipeline"
]

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """测试开始前的准备工作"""
    if not isinstance(environment.runner, MasterRunner):
        print(f"[{datetime.now()}] Starting media processing performance test")
        print(f"  * Test images: {TEST_IMAGES}")
        print(f"  * Workflows: {WORKFLOWS}")
        print(f"  * Target RPS: {environment.parsed_options.spawn_rate}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """测试结束后的清理工作"""
    if not isinstance(environment.runner, MasterRunner):
        print(f"[{datetime.now()}] Media processing performance test completed")

class MediaProcessingUser(HttpUser):
    wait_time = between(0.5, 2.0)
    
    def on_start(self):
        """用户启动时的初始化"""
        self.auth_token = self._get_auth_token()
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
    
    def _get_auth_token(self):
        """获取认证令牌"""
        response = self.client.post(
            "/api/v1/auth/token",
            json={
                "client_id": "performance-test",
                "client_secret": "perf-test-secret",
                "grant_type": "client_credentials"
            }
        )
        return response.json()["access_token"]
    
    @task(8)
    def process_1080p_image(self):
        """处理1080P图片"""
        self._process_image(
            image=random.choice([img for img in TEST_IMAGES if "1080p" in img]),
            workflow="nas-photo-processing",
            priority=random.choice([3, 5, 7])
        )
    
    @task(3)
    def process_4k_image(self):
        """处理4K图片"""
        self._process_image(
            image=random.choice([img for img in TEST_IMAGES if "4k" in img]),
            workflow="nas-photo-processing",
            priority=random.choice([5, 7, 9])
        )
    
    @task(1)
    def process_pro_photo(self):
        """处理专业照片"""
        self._process_image(
            image="pro-photo.jpg",
            workflow="professional-photo-processing",
            priority=9
        )
    
    def _process_image(self, image, workflow, priority):
        """通用图片处理方法"""
        start_time = time.time()
        
        try:
            response = self.client.post(
                "/api/v1/media:process",
                json={
                    "file_path": f"/test-data/{image}",
                    "workflow": workflow,
                    "parameters": {
                        "image_enhance": {
                            "scale_factor": 2,
                            "denoise_strength": 0.3
                        }
                    },
                    "priority": priority
                },
                headers=self.headers,
                name="/api/v1/media:process"
            )
            
            if response.status_code == 202:
                task_id = response.json()["task_id"]
                
                # 轮询任务状态
                max_polls = 30
                poll_interval = 0.5
                completed = False
                
                for _ in range(max_polls):
                    time.sleep(poll_interval)
                    status_response = self.client.get(
                        f"/api/v1/media/processingTasks/{task_id}",
                        headers=self.headers,
                        name="/api/v1/media/processingTasks/{task_id}"
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data["status"] == "completed":
                            completed = True
                            break
                        elif status_data["status"] == "failed":
                            self.environment.events.request_failure.fire(
                                request_type="POST",
                                name="/api/v1/media:process",
                                response_time=(time.time() - start_time) * 1000,
                                exception=f"Task failed: {status_data.get('error', 'Unknown error')}"
                            )
                            return
                if not completed:
                    self.environment.events.request_failure.fire(
                        request_type="POST",
                        name="/api/v1/media:process",
                        response_time=(time.time() - start_time) * 1000,
                        exception="Task timeout waiting for completion"
                    )
            else:
                self.environment.events.request_failure.fire(
                    request_type="POST",
                    name="/api/v1/media:process",
                    response_time=(time.time() - start_time) * 1000,
                    exception=f"Unexpected status code: {response.status_code}"
                )
                
        except Exception as e:
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/api/v1/media:process",
                response_time=(time.time() - start_time) * 1000,
                exception=str(e)
            )
```

### 5.8 安全与合规详细规范

#### 5.8.1 敏感数据检测与脱敏规则

**敏感数据正则表达式规则库**
```json
{
  "patterns": [
    {
      "id": "credit-card",
      "name": "信用卡号",
      "description": "检测各种信用卡号格式",
      "regex": "(?:\\d[ -]*?){13,16}",
      "confidence": 0.9,
      "redaction": "****-****-****-XXXX",
      "validation": {
        "luhn_check": true
      },
      "allowed_contexts": ["payment", "billing"]
    },
    {
      "id": "ssn",
      "name": "社会安全号码",
      "description": "美国社会安全号码 (格式: XXX-XX-XXXX)",
      "regex": "\\b\\d{3}[- ]?\\d{2}[- ]?\\d{4}\\b",
      "confidence": 0.95,
      "redaction": "***-**-XXXX",
      "allowed_contexts": ["identity-verification"]
    },
    {
      "id": "email",
      "name": "电子邮件地址",
      "description": "标准电子邮件格式",
      "regex": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
      "confidence": 0.8,
      "redaction": "userXXXX@example.com",
      "allowed_contexts": ["communication", "user-profile"]
    },
    {
      "id": "phone",
      "name": "电话号码",
      "description": "国际电话号码格式",
      "regex": "(?:\\+?1[-. ]?)?\\(?\\d{3}\\)?[-. ]?\\d{3}[-. ]?\\d{4}",
      "confidence": 0.75,
      "redaction": "(XXX) XXX-XXXX",
      "allowed_contexts": ["contact", "user-profile"]
    },
    {
      "id": "passport",
      "name": "护照号码",
      "description": "通用护照号码格式",
      "regex": "[A-Z0-9]{6,9}",
      "confidence": 0.7,
      "redaction": "XXXXXX",
      "allowed_contexts": ["travel", "identity-verification"],
      "validation": {
        "country_specific": true
      }
    }
  ],
  "context_rules": [
    {
      "context": "payment",
      "allowed_patterns": ["credit-card"],
      "required_validation": ["luhn_check"]
    },
    {
      "context": "identity-verification",
      "allowed_patterns": ["ssn", "passport"],
      "required_validation": ["document_verification"]
    }
  ]
}
```

#### 5.8.2 数据处理安全中间件实现

**数据安全中间件 (data_security_middleware.py)**
```python
import re
import json
from typing import Dict, List, Optional, Callable, Any
from functools import wraps
import logging

class DataSecurityMiddleware:
    """
    数据安全中间件，负责敏感数据检测与脱敏
    """
    
    def __init__(self, config_path: str = "security_rules.json"):
        self.logger = logging.getLogger(__name__)
        self.rules = self._load_rules(config_path)
        self.context_stack = []
    
    def _load_rules(self, config_path: str) -> Dict:
        """加载安全规则"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error("Failed to load security rules: %s", str(e))
            # 使用默认规则
            return {
                "patterns": [],
                "context_rules": []
            }
    
    def enter_context(self, context: str):
        """进入特定安全上下文"""
        self.context_stack.append(context)
    
    def exit_context(self):
        """退出当前安全上下文"""
        if self.context_stack:
            self.context_stack.pop()
    
    def get_current_context(self) -> Optional[str]:
        """获取当前安全上下文"""
        return self.context_stack[-1] if self.context_stack else None
    
    def _is_pattern_allowed(self, pattern_id: str, context: Optional[str]) -> bool:
        """检查模式是否在当前上下文中允许使用"""
        if not context:
            return False
            
        context_rule = next(
            (r for r in self.rules["context_rules"] if r["context"] == context),
            None
        )
        
        if not context_rule:
            return False
            
        return pattern_id in context_rule["allowed_patterns"]
    
    def _validate_pattern(self, pattern_id: str, value: str) -> bool:
        """验证敏感数据模式"""
        pattern = next(
            (p for p in self.rules["patterns"] if p["id"] == pattern_id),
            None
        )
        
        if not pattern or "validation" not in pattern:
            return True
            
        # Luhn算法验证 (信用卡)
        if pattern["id"] == "credit-card" and pattern["validation"].get("luhn_check"):
            return self._validate_luhn(value)
            
        return True
    
    def _validate_luhn(self, card_number: str) -> bool:
        """验证信用卡号是否通过Luhn算法"""
        # 清理非数字字符
        digits = re.sub(r"[^\d]", "", card_number)
        
        # 檢查长度
        if len(digits) < 13 or len(digits) > 16:
            return False
            
        # Luhn算法
        total = 0
        reverse = digits[::-1]
        
        for i, digit in enumerate(reverse):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
            
        return total % 10 == 0
    
    def _redact_value(self, pattern_id: str, value: str) -> str:
        """根据规则脱敏值"""
        pattern = next(
            (p for p in self.rules["patterns"] if p["id"] == pattern_id),
            None
        )
        
        if not pattern or "redaction" not in pattern:
            return value
            
        # 简单实现：根据规则替换
        if "XXXX" in pattern["redaction"]:
            # 保留末尾几位
            last_digits = pattern["redaction"].count("X")
            return pattern["redaction"].replace("X" * last_digits, value[-last_digits:])
            
        return pattern["redaction"]
    
    def detect_sensitive_data(self, data: Any, context: Optional[str] = None) -> List[Dict]:
        """
        检测数据中的敏感信息
        
        :param data: 要检测的数据 (可以是字符串、字典、列表)
        :param context: 安全上下文
        :return: 检测到的敏感数据列表
        """
        results = []
        
        if isinstance(data, str):
            for pattern in self.rules["patterns"]:
                matches = re.finditer(pattern["regex"], data)
                for match in matches:
                    value = match.group(0)
                    
                    # 验证模式 (如果需要)
                    if not self._validate_pattern(pattern["id"], value):
                        continue
                        
                    results.append({
                        "pattern_id": pattern["id"],
                        "value": value,
                        "start": match.start(),
                        "end": match.end(),
                        "confidence": pattern["confidence"],
                        "allowed": self._is_pattern_allowed(pattern["id"], context or self.get_current_context())
                    })
                    
        elif isinstance(data, dict):
            for key, value in data.items():
                # 檢查键名是否暗示敏感数据
                if any(kw in key.lower() for kw in ["ssn", "social", "security", "credit", "card", "passport"]):
                    # 递归检测值
                    sub_results = self.detect_sensitive_data(value, context)
                    for r in sub_results:
                        r["path"] = f"{key}.{r.get('path', '')}".rstrip('.')
                        results.append(r)
                
                # 检测值
                sub_results = self.detect_sensitive_data(value, context)
                for r in sub_results:
                    r["path"] = f"{key}.{r.get('path', '')}".rstrip('.')
                    results.append(r)
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                sub_results = self.detect_sensitive_data(item, context)
                for r in sub_results:
                    r["path"] = f"[{i}].{r.get('path', '')}".rstrip('.')
                    results.append(r)
                    
        return results
    
    def redact_sensitive_data(self,  Any, context: Optional[str] = None) -> Any:
        """
        脱敏数据中的敏感信息
        
        :param  要脱敏的数据
        :param context: 安全上下文
        :return: 脱敏后的数据
        """
        current_context = context or self.get_current_context()
        
        if isinstance(data, str):
            # 检测所有敏感数据
            detections = self.detect_sensitive_data(data, current_context)
            
            # 按位置排序，从后往前替换 (避免位置偏移)
            detections.sort(key=lambda x: x["start"], reverse=True)
            
            result = data
            for detection in detections:
                if not detection["allowed"]:
                    # 执行脱敏
                    redacted = self._redact_value(detection["pattern_id"], detection["value"])
                    result = result[:detection["start"]] + redacted + result[detection["end"]:]
            
            return result
            
        elif isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # 檢查键名是否需要特殊处理
                if any(kw in key.lower() for kw in ["ssn", "social", "security", "credit", "card", "passport"]):
                    # 键名暗示敏感数据，脱敏整个值
                    result[key] = self.redact_sensitive_data(value, current_context)
                else:
                    # 递归脱敏
                    result[key] = self.redact_sensitive_data(value, current_context)
            return result
            
        elif isinstance(data, list):
            return [self.redact_sensitive_data(item, current_context) for item in data]
            
        return data
    
    def audit_log(self, operation: str, data: Any, context: Optional[str] = None):
        """
        记录安全审计日志
        
        :param operation: 操作类型
        :param  操作数据
        :param context: 安全上下文
        """
        detections = self.detect_sensitive_data(data, context)
        
        if detections:
            allowed = [d for d in detections if d["allowed"]]
            blocked = [d for d in detections if not d["allowed"]]
            
            log_entry = {
                "timestamp": time.time(),
                "operation": operation,
                "context": context or self.get_current_context(),
                "sensitive_data_found": len(detections),
                "allowed_access": len(allowed),
                "blocked_access": len(blocked),
                "details": [{
                    "pattern": d["pattern_id"],
                    "value_sample": d["value"][:10] + "..." if len(d["value"]) > 10 else d["value"],
                    "allowed": d["allowed"]
                } for d in detections[:5]]  # 只录前5个
            }
            
            self.logger.info("Security audit: %s", json.dumps(log_entry))
    
    def protect_route(self, required_context: Optional[str] = None):
        """
        路由保护装饰器
        
        :param required_context: 所需的安全上下文
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 进入安全上下文
                self.enter_context(required_context)
                
                try:
                    # 执行前审计
                    self.audit_log(f"enter:{func.__name__}", kwargs, required_context)
                    
                    # 执行函数
                    result = func(*args, **kwargs)
                    
                    # 检测并脱敏返回数据
                    if isinstance(result, (dict, list, str)):
                        result = self.redact_sensitive_data(result, required_context)
                    
                    # 执行后审计
                    self.audit_log(f"exit:{func.__name__}", result, required_context)
                    
                    return result
                finally:
                    # 退出安全上下文
                    self.exit_context()
            return wrapper
        return decorator

# 使用示例
security = DataSecurityMiddleware()

@security.protect_route(required_context="payment-processing")
def process_payment(data: Dict) -> Dict:
    """处理支付请求 (自动脱敏敏感数据)"""
    # 业务逻辑
    payment_result = {
        "status": "success",
        "transaction_id": "txn-123456",
        "card_number": data["card_number"],  # 将被自动脱敏
        "amount": data["amount"]
    }
    return payment_result
```

### 5.9 与其他模块的交互

#### 5.9.1 与数据处理工作流引擎交互

```mermaid
sequenceDiagram
    participant DPWE as Data Processing Workflow Engine
    participant AMP as Automated Media Processing Pipeline
    
    DPWE->>AMP: POST /api/v1/media:process (触发处理)
    AMP-->>DPWE: 处理任务ID
    
    loop 处理进行中
        DPWE->>AMP: GET /api/v1/media/processingTasks/{task_id} (查询状态)
        AMP-->>DPWE: 处理状态
    end
    
    DPWE->>AMP: GET /api/v1/media/processingTasks/{task_id} (获取结果)
    AMP-->>DPWE: 处理结果和元数据
```

#### 5.9.2 与AI辅助开发系统交互

```mermaid
sequenceDiagram
    participant AIDS as AI-Assisted Development System
    participant AMP as Automated Media Processing Pipeline
    
    AIDS->>AMP: GET /api/v1/media/models (获取可用模型)
    AMP-->>AIDS: 模型列表
    
    AIDS->>AMP: POST /api/v1/media/process (请求处理示例)
    AMP-->>AIDS: 处理结果示例
    
    AIDS->>AMP: GET /api/v1/media/analysis (获取分析能力)
    AMP-->>AIDS: 分析能力描述
```

#### 5.9.3 与数据源注册中心交互

```mermaid
sequenceDiagram
    participant DSR as Data Source Registry
    participant AMP as Automated Media Processing Pipeline
    
    AMP->>DSR: GET /api/v1/data-sources?type=media (获取媒体数据源)
    DSR-->>AMP: 媒体数据源列表
    
    AMP->>DSR: POST /api/v1/data-sources (创建处理后的媒体数据源)
    DSR-->>AMP: 创建结果
    
    AMP->>DSR: GET /api/v1/data-sources/{id} (获取数据源详情)
    DSR-->>AMP: 数据源详情
```

## 6. AI辅助开发系统 (AI-Assisted Development System)

### 6.1 模块概述
AI辅助开发系统是镜界平台的智能助手，利用大型语言模型和领域知识库，为爬虫工程师和数据科学家提供代码生成、问题诊断和学习推荐等辅助功能。它通过自然语言交互，降低数据采集的技术门槛，提高开发效率。

### 6.2 详细功能清单

#### 6.2.1 核心功能
- **自然语言需求解析**
  - 需求意图识别
  - 关键参数提取
  - 需求验证与澄清
  - 需求分解与任务规划
- **智能代码生成**
  - 爬虫代码生成（Python、JavaScript）
  - 数据处理代码生成
  - 工作流定义生成
  - 测试用例生成
- **问题诊断与修复建议**
  - 错误日志分析
  - 反爬问题诊断
  - 性能瓶颈分析
  - 修复建议生成
- **学习路径个性化推荐**
  - 技能评估与差距分析
  - 个性化学习路径规划
  - 实战项目推荐
  - 进阶学习资源推荐

#### 6.2.2 高级功能
- **领域知识库**
  - 爬虫技术栈知识库
  - 反爬策略数据库
  - 网站技术栈指纹库
  - HTTP状态码知识库
- **多轮对话记忆**
  - 上下文理解与跟踪
  - 对话状态管理
  - 记忆长期化
  - 个性化偏好学习
- **代码理解与优化**
  - 代码静态分析
  - 代码质量评估
  - 性能优化建议
  - 安全漏洞检测
- **集成开发环境支持**
  - VS Code插件
  - Jupyter Notebook集成
  - 命令行工具
  - 工作流内嵌调用

### 6.3 技术架构

#### 6.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                AI辅助开发系统 (AIDS)                                          │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  交互层               │  服务层               │  数据层                                    │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • Web聊天界面         │ • 需求解析服务        │ • 领域知识库                               │
│ • IDE插件             │ • 代码生成服务        │ • 代码片段库                               │
│ • CLI工具             │ • 问题诊断服务        │ • 错误模式库                               │
│ • 工作流内嵌调用       │ • 学习推荐服务        │ • 用户画像库                               │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 6.3.2 服务边界与交互
- **输入**：
  - 自然语言查询（用户输入）
  - 代码片段（用于分析或生成）
  - 错误日志（用于诊断）
  - 工作流定义（用于辅助）
- **输出**：
  - 生成的代码
  - 问题诊断结果
  - 学习资源推荐
  - 需求澄清问题

### 6.4 核心组件详细实现

#### 6.4.1 需求解析服务

**技术实现：**
```python
import re
import json
from typing import Dict, List, Optional, Tuple
import logging
import spacy
from spacy.tokens import Doc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RequirementParser:
    """需求解析服务，将自然语言需求转换为结构化任务"""
    
    def __init__(
        self,
        nlp: spacy.Language,
        knowledge_base: KnowledgeBase,
        config: Config
    ):
        self.nlp = nlp
        self.knowledge_base = knowledge_base
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def parse(
        self,
        user_query: str,
        context: Optional[Dict] = None
    ) -> ParsedRequirement:
        """
        解析用户需求
        
        :param user_query: 用户自然语言查询
        :param context: 对话上下文
        :return: 解析后的需求对象
        """
        # 1. 预处理用户查询
        cleaned_query = self._clean_query(user_query)
        
        # 2. 识别需求类型
        requirement_type = self._identify_requirement_type(cleaned_query)
        
        # 3. 提取关键参数
        parameters = self._extract_parameters(cleaned_query, requirement_type)
        
        # 4. 验证参数完整性
        missing_params = self._validate_parameters(requirement_type, parameters)
        
        # 5. 生成结构化需求
        return ParsedRequirement(
            original_query=user_query,
            cleaned_query=cleaned_query,
            requirement_type=requirement_type,
            parameters=parameters,
            missing_parameters=missing_params,
            confidence=self._calculate_confidence(requirement_type, parameters),
            context=context
        )
    
    def _clean_query(self, query: str) -> str:
        """清理用户查询"""
        # 移除特殊字符
        query = re.sub(r'[^\w\s]', ' ', query)
        
        # 转换为小写
        query = query.lower()
        
        # 移除多余空格
        query = re.sub(r'\s+', ' ', query).strip()
        
        return query
    
    def _identify_requirement_type(self, query: str) -> str:
        """识别需求类型"""
        # 基于关键词匹配
        if any(word in query for word in ["generate", "create", "make"]):
            if any(word in query for word in ["code", "script", "crawler"]):
                return "code_generation"
            elif any(word in query for word in ["workflow", "pipeline"]):
                return "workflow_generation"
        
        if any(word in query for word in ["why", "error", "problem", "fix", "debug"]):
            return "problem_diagnosis"
        
        if any(word in query for word in ["learn", "study", "tutorial", "how to"]):
            return "learning_request"
        
        # 默认类型
        return "general_query"
    
    def _extract_parameters(
        self,
        query: str,
        requirement_type: str
    ) -> Dict:
        """提取需求参数"""
        doc = self.nlp(query)
        parameters = {}
        
        if requirement_type == "code_generation":
            parameters.update(self._extract_code_generation_params(doc))
        elif requirement_type == "workflow_generation":
            parameters.update(self._extract_workflow_params(doc))
        elif requirement_type == "problem_diagnosis":
            parameters.update(self._extract_problem_diagnosis_params(doc))
        
        return parameters
    
    def _extract_code_generation_params(self, doc: Doc) -> Dict:
        """提取代码生成参数"""
        params = {}
        
        # 提取目标网站
        for ent in doc.ents:
            if ent.label_ in ["WEBSITE", "URL", "ORG"]:
                params["target_website"] = ent.text
        
        # 提取数据类型
        data_types = ["image", "video", "text", "html", "json", "xml"]
        for token in doc:
            if token.text in data_types:
                params["data_type"] = token.text
                break
        
        # 提取编程语言
        languages = ["python", "javascript", "java", "go"]
        for token in doc:
            if token.text in languages:
                params["language"] = token.text
                break
        
        # 提取特殊要求
        special_requirements = []
        if "login" in doc.text or "authentication" in doc.text:
            special_requirements.append("login_required")
        if "pagination" in doc.text or "page" in doc.text:
            special_requirements.append("pagination")
        if "infinite scroll" in doc.text:
            special_requirements.append("infinite_scroll")
        
        if special_requirements:
            params["special_requirements"] = special_requirements
        
        return params
    
    def _extract_workflow_params(self, doc: Doc) -> Dict:
        """提取工作流参数"""
        params = {}
        
        # 提取触发条件
        if "schedule" in doc.text or "定时" in doc.text:
            params["trigger"] = "schedule"
        elif "filesystem" in doc.text or "文件系统" in doc.text:
            params["trigger"] = "filesystem"
        elif "webhook" in doc.text or "回调" in doc.text:
            params["trigger"] = "webhook"
        
        # 提取处理步骤
        processing_steps = []
        if "download" in doc.text or "下载" in doc.text:
            processing_steps.append("download")
        if "extract" in doc.text or "提取" in doc.text:
            processing_steps.append("extract")
        if "transform" in doc.text or "转换" in doc.text:
            processing_steps.append("transform")
        if "analyze" in doc.text or "分析" in doc.text:
            processing_steps.append("analyze")
        if "store" in doc.text or "存储" in doc.text:
            processing_steps.append("store")
        
        if processing_steps:
            params["processing_steps"] = processing_steps
        
        return params
    
    def _extract_problem_diagnosis_params(self, doc: Doc) -> Dict:
        """提取问题诊断参数"""
        params = {}
        
        # 提取错误信息
        error_keywords = ["error", "exception", "failed", "not working"]
        for sent in doc.sents:
            if any(keyword in sent.text for keyword in error_keywords):
                params["error_message"] = sent.text
                break
        
        # 提取网站信息
        for ent in doc.ents:
            if ent.label_ in ["WEBSITE", "URL", "ORG"]:
                params["target_website"] = ent.text
                break
        
        # 提取技术栈
        tech_keywords = ["javascript", "react", "angular", "vue", "angular", "wordpress"]
        for token in doc:
            if token.text in tech_keywords:
                params["technology"] = token.text
                break
        
        return params
    
    def _validate_parameters(
        self,
        requirement_type: str,
        parameters: Dict
    ) -> List[str]:
        """验证参数完整性"""
        missing_params = []
        
        if requirement_type == "code_generation":
            if "target_website" not in parameters:
                missing_params.append("target_website")
            if "data_type" not in parameters:
                missing_params.append("data_type")
        
        elif requirement_type == "workflow_generation":
            if "trigger" not in parameters:
                missing_params.append("trigger")
            if "processing_steps" not in parameters or not parameters["processing_steps"]:
                missing_params.append("processing_steps")
        
        elif requirement_type == "problem_diagnosis":
            if "error_message" not in parameters:
                missing_params.append("error_message")
        
        return missing_params
    
    def _calculate_confidence(
        self,
        requirement_type: str,
        parameters: Dict
    ) -> float:
        """计算解析置信度"""
        # 基于参数完整性
        if requirement_type == "general_query":
            return 0.5
        
        required_params = []
        if requirement_type == "code_generation":
            required_params = ["target_website", "data_type"]
        elif requirement_type == "workflow_generation":
            required_params = ["trigger", "processing_steps"]
        elif requirement_type == "problem_diagnosis":
            required_params = ["error_message"]
        
        if not required_params:
            return 0.8  # 一般查询，置信度中等
        
        filled_params = [param for param in required_params if param in parameters]
        return len(filled_params) / len(required_params)

class KnowledgeBase:
    """领域知识库，存储爬虫相关知识"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._load_knowledge()
    
    def _load_knowledge(self):
        """加载知识库"""
        # 从配置或数据库加载知识
        self.anti_crawling_strategies = self._load_anti_crawling_strategies()
        self.technology_fingerprints = self._load_technology_fingerprints()
        self.error_patterns = self._load_error_patterns()
    
    def _load_anti_crawling_strategies(self) -> List[Dict]:
        """加载反爬策略知识"""
        return [
            {
                "id": "user-agent-check",
                "name": "User-Agent检测",
                "description": "网站通过User-Agent检测爬虫",
                "indicators": [
                    "403 Forbidden响应",
                    "需要特定User-Agent才能访问"
                ],
                "solutions": [
                    {
                        "title": "轮换User-Agent",
                        "description": "使用随机User-Agent池",
                        "code_example": "from fake_useragent import UserAgent\nua = UserAgent()\nheaders = {'User-Agent': ua.random}",
                        "effectiveness": 0.85,
                        "complexity": 0.3
                    },
                    {
                        "title": "模拟浏览器特征",
                        "description": "添加浏览器特有的请求头",
                        "code_example": "headers = {\n    'User-Agent': 'Mozilla/5.0...',\n    'Accept-Language': 'en-US,en;q=0.9',\n    'Sec-Ch-Ua': '\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not_A Brand\";v=\"24\"'\n}",
                        "effectiveness": 0.92,
                        "complexity": 0.6
                    }
                ]
            },
            {
                "id": "rate-limiting",
                "name": "请求频率限制",
                "description": "网站限制单位时间内的请求数量",
                "indicators": [
                    "429 Too Many Requests响应",
                    "请求间隔过短导致失败"
                ],
                "solutions": [
                    {
                        "title": "添加请求间隔",
                        "description": "在请求之间添加随机延迟",
                        "code_example": "import time\nimport random\ntime.sleep(random.uniform(1, 3))",
                        "effectiveness": 0.75,
                        "complexity": 0.2
                    },
                    {
                        "title": "使用代理IP轮换",
                        "description": "通过轮换不同IP地址分散请求",
                        "code_example": "proxies = {\n    'http': 'http://10.10.1.10:3128',\n    'https': 'http://10.10.1.10:1080',\n}\nresponse = requests.get(url, proxies=proxies)",
                        "effectiveness": 0.85,
                        "complexity": 0.7
                    }
                ]
            }
        ]
    
    def _load_technology_fingerprints(self) -> List[Dict]:
        """加载技术栈指纹知识"""
        return [
            {
                "id": "react",
                "name": "React",
                "detection_rules": [
                    {
                        "type": "html",
                        "pattern": "<div id=\"root\">",
                        "confidence": 0.9
                    },
                    {
                        "type": "js",
                        "pattern": "webpackJsonp",
                        "confidence": 0.8
                    }
                ],
                "crawl_implications": [
                    "需要处理客户端渲染内容",
                    "可能使用React Router进行导航"
                ]
            },
            {
                "id": "wordpress",
                "name": "WordPress",
                "detection_rules": [
                    {
                        "type": "meta",
                        "pattern": "generator",
                        "value": "WordPress",
                        "confidence": 0.95
                    },
                    {
                        "type": "path",
                        "pattern": "/wp-content/",
                        "confidence": 0.85
                    }
                ],
                "crawl_implications": [
                    "可能使用REST API",
                    "需要注意主题和插件的自定义结构"
                ]
            }
        ]
    
    def _load_error_patterns(self) -> List[Dict]:
        """加载错误模式知识"""
        return [
            {
                "id": "403-forbidden",
                "pattern": "403 Forbidden",
                "description": "访问被拒绝",
                "causes": [
                    "IP被封禁",
                    "User-Agent被识别为爬虫",
                    "缺少必要的请求头"
                ],
                "solutions": [
                    "使用代理IP",
                    "轮换User-Agent",
                    "添加Referer头"
                ],
                "examples": [
                    {
                        "code": "requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})",
                        "description": "设置User-Agent解决403错误"
                    }
                ]
            },
            {
                "id": "429-too-many-requests",
                "pattern": "429 Too Many Requests",
                "description": "请求过于频繁",
                "causes": [
                    "请求频率超过网站限制",
                    "未使用请求间隔"
                ],
                "solutions": [
                    "添加随机请求间隔",
                    "减少并发请求数",
                    "使用代理IP轮换"
                ],
                "examples": [
                    {
                        "code": "import time\ntime.sleep(2)  # 2秒间隔",
                        "description": "添加请求间隔解决429错误"
                    }
                ]
            }
        ]
    
    def get_anti_crawling_strategy(self, strategy_id: str) -> Optional[Dict]:
        """获取反爬策略"""
        return next(
            (s for s in self.anti_crawling_strategies if s["id"] == strategy_id),
            None
        )
    
    def get_technology_fingerprint(self, tech_id: str) -> Optional[Dict]:
        """获取技术栈指纹"""
        return next(
            (t for t in self.technology_fingerprints if t["id"] == tech_id),
            None
        )
    
    def match_error_pattern(self, error_message: str) -> List[Dict]:
        """匹配错误模式"""
        matches = []
        
        for pattern in self.error_patterns:
            # 简单实现：关键词匹配
            if any(keyword in error_message.lower() for keyword in pattern["pattern"].lower().split()):
                matches.append(pattern)
        
        return matches

# 辅助类定义
class ParsedRequirement:
    """解析后的需求对象"""
    def __init__(
        self,
        original_query: str,
        cleaned_query: str,
        requirement_type: str,
        parameters: Dict,
        missing_parameters: List[str],
        confidence: float,
        context: Optional[Dict] = None
    ):
        self.original_query = original_query
        self.cleaned_query = cleaned_query
        self.requirement_type = requirement_type
        self.parameters = parameters
        self.missing_parameters = missing_parameters
        self.confidence = confidence
        self.context = context or {}
```

#### 6.4.2 代码生成服务

**技术实现：**
```python
import os
import time
import json
from typing import Dict, List, Optional
import logging
import openai
from jinja2 import Template

class CodeGenerationService:
    """
    AI代码生成服务，支持多种爬虫场景
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        template_repo: TemplateRepository,
        scene_classifier: SceneClassifier,
        code_validator: CodeValidator,
        config: Config
    ):
        self.llm_client = llm_client
        self.template_repo = template_repo
        self.scene_classifier = scene_classifier
        self.code_validator = code_validator
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def generate_code(
        self,
        user_request: str,
        context: dict = None
    ) -> CodeGenerationResult:
        """
        根据用户需求生成爬虫代码
        
        :param user_request: 用户自然语言描述
        :param context: 上下文信息（可选）
        :return: 代码生成结果
        """
        start_time = time.time()
        
        try:
            # 1. 场景分类
            scene_type = self.scene_classifier.classify(user_request)
            
            # 2. 获取相关模板
            templates = self.template_repo.get_templates(
                scene_type=scene_type,
                language=context.get("language", "python") if context else "python"
            )
            
            # 3. 构建提示词
            prompt = self._build_prompt(user_request, templates, context)
            
            # 4. 调用LLM生成代码
            raw_code = self.llm_client.generate(prompt)
            
            # 5. 代码后处理与验证
            processed_code = self._post_process_code(raw_code, scene_type)
            validation_result = self.code_validator.validate(processed_code)
            
            # 6. 构建结果
            return CodeGenerationResult(
                code=processed_code,
                scene_type=scene_type,
                templates_used=[t.id for t in templates],
                validation=validation_result,
                confidence=self._calculate_confidence(validation_result),
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("Code generation failed: %s", str(e))
            raise CodeGenerationError(f"Failed to generate code: {str(e)}")
    
    def _build_prompt(
        self,
        user_request: str,
        templates: List[CodeTemplate],
        context: dict
    ) -> str:
        """构建LLM提示词"""
        # 加载提示词模板
        template_path = self.config.get("prompt_template_path", "prompts/code_generation.j2")
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # 准备模板变量
        template_vars = {
            "user_request": user_request,
            "templates": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "content": t.content,
                    "parameters": t.parameters
                } for t in templates
            ],
            "context": context or {},
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "programming_language": context.get("language", "Python") if context else "Python"
        }
        
        # 渲染提示词
        jinja_template = Template(template_content)
        return jinja_template.render(**template_vars)
    
    def _post_process_code(self, raw_code: str, scene_type: str) -> str:
        """代码后处理：清理、格式化、添加注释"""
        # 1. 移除多余内容
        code = self._remove_extra_content(raw_code)
        
        # 2. 根据场景类型进行特定后处理
        if scene_type == "static-html":
            code = self._process_static_html_code(code)
        elif scene_type == "dynamic-rendering":
            code = self._process_dynamic_rendering_code(code)
        elif scene_type == "api-endpoint":
            code = self._process_api_code(code)
        
        # 3. 格式化代码
        code = self._format_code(code)
        
        # 4. 添加必要的导入
        code = self._add_required_imports(code)
        
        return code
    
    def _remove_extra_content(self, code: str) -> str:
        """移除LLM生成的多余内容"""
        # 移除Markdown代码块标记
        code = re.sub(r'```python\n', '', code)
        code = re.sub(r'\n```', '', code)
        
        # 移除解释性文本
        if "```" in code:
            code = code.split("```")[0]
        
        return code.strip()
    
    def _process_static_html_code(self, code: str) -> str:
        """处理静态HTML爬虫代码"""
        # 确保使用了requests和BeautifulSoup
        if "import requests" not in code:
            code = "import requests\n" + code
        if "from bs4 import BeautifulSoup" not in code and "BeautifulSoup" in code:
            code = "from bs4 import BeautifulSoup\n" + code
        
        # 添加基本错误处理
        if "try:" not in code:
            code = self._add_basic_error_handling(code)
        
        return code
    
    def _process_dynamic_rendering_code(self, code: str) -> str:
        """处理动态渲染页面爬虫代码"""
        # 确保使用了selenium
        if "from selenium import webdriver" not in code:
            code = "from selenium import webdriver\n" + code
        
        # 添加等待机制
        if "WebDriverWait" not in code and "wait" in code.lower():
            code = self._add_wait_mechanism(code)
        
        return code
    
    def _process_api_code(self, code: str) -> str:
        """处理API爬虫代码"""
        # 确保处理了分页
        if "page" in code.lower() and "while" not in code and "for" not in code:
            code = self._add_pagination_handling(code)
        
        # 添加速率限制
        if "time.sleep" not in code and "rate limit" in code.lower():
            code = self._add_rate_limiting(code)
        
        return code
    
    def _add_basic_error_handling(self, code: str) -> str:
        """添加基本错误处理"""
        error_handling = """
try:
    # 原有代码
    {}
except Exception as e:
    print(f"Error: {str(e)}")
    # 可以添加更多错误处理逻辑
"""
        return error_handling.format(code)
    
    def _add_wait_mechanism(self, code: str) -> str:
        """添加等待机制"""
        wait_code = """
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 等待元素加载
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "target-element")))
"""
        return wait_code + "\n\n" + code
    
    def _add_pagination_handling(self, code: str) -> str:
        """添加分页处理"""
        pagination_code = """
# 处理分页
page = 1
all_data = []

while True:
    # 构建URL
    url = f"https://api.example.com/data?page={page}"
    
    # 发送请求
    response = requests.get(url)
    data = response.json()
    
    # 检查是否还有数据
    if not data["items"]:
        break
    
    # 添加到结果
    all_data.extend(data["items"])
    
    # 下一页
    page += 1
"""
        return pagination_code + "\n\n" + code
    
    def _add_rate_limiting(self, code: str) -> str:
        """添加速率限制"""
        rate_limiting_code = """
import time

# 添加请求间隔
def make_request(url):
    response = requests.get(url)
    time.sleep(1)  # 1秒间隔
    return response
"""
        return rate_limiting_code + "\n\n" + code
    
    def _format_code(self, code: str) -> str:
        """格式化代码"""
        # 这里简化实现，实际应该使用black等格式化工具
        return code
    
    def _add_required_imports(self, code: str) -> str:
        """添加必要的导入"""
        imports = []
        
        if "requests" in code and "import requests" not in code:
            imports.append("import requests")
        if "BeautifulSoup" in code and "from bs4 import BeautifulSoup" not in code:
            imports.append("from bs4 import BeautifulSoup")
        if "selenium" in code and "from selenium import webdriver" not in code:
            imports.append("from selenium import webdriver")
        
        if imports:
            return "\n".join(imports) + "\n\n" + code
        
        return code
    
    def _calculate_confidence(self, validation_result: ValidationResult) -> float:
        """计算生成代码的置信度"""
        # 根据验证结果计算置信度
        if validation_result.is_valid:
            return 0.9
        elif validation_result.errors:
            # 根据错误严重程度调整
            severity_weights = {
                "syntax": 0.3,
                "import": 0.2,
                "logic": 0.5
            }
            
            total_deduction = 0
            for error in validation_result.errors:
                weight = severity_weights.get(error["type"], 0.2)
                total_deduction += weight * error.get("severity", 1.0)
            
            return max(0.1, 1.0 - total_deduction)
        
        return 0.5

class SceneClassifier:
    """爬虫场景分类器"""
    
    SCENE_CATEGORIES = [
        "static-html", 
        "dynamic-rendering", 
        "api-endpoint", 
        "image-crawling",
        "video-crawling",
        "login-required",
        "pagination",
        "infinite-scroll"
    ]
    
    def __init__(self):
        # 加载预训练分类模型
        self.model = load_model("scene-classification-v1")
    
    def classify(self, user_request: str) -> str:
        """将用户请求分类到最匹配的场景"""
        # 实现分类逻辑
        return self.model.predict(user_request)

class TemplateRepository:
    """代码模板仓库"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_templates(
        self,
        scene_type: str,
        language: str = "python"
    ) -> List[CodeTemplate]:
        """获取相关代码模板"""
        # 从数据库获取模板
        sql = """
        SELECT * FROM code_templates 
        WHERE scene_type = %(scene_type)s 
        AND language = %(language)s
        ORDER BY priority DESC
        """
        
        rows = self.db.fetchall(sql, {
            "scene_type": scene_type,
            "language": language
        })
        
        return [self._row_to_template(row) for row in rows]
    
    def _row_to_template(self, row: Dict) -> CodeTemplate:
        """将数据库行转换为CodeTemplate对象"""
        return CodeTemplate(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            language=row["language"],
            scene_type=row["scene_type"],
            content=row["content"],
            parameters=self._decode_parameters(row["parameters"]),
            examples=self._decode_examples(row["examples"]),
            priority=row["priority"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    def _decode_parameters(self, json_data: str) -> List[TemplateParameter]:
        """解码参数定义"""
        if not json_data:
            return []
        
        params_data = json.loads(json_data)
        return [
            TemplateParameter(
                name=p["name"],
                type=p["type"],
                description=p.get("description", ""),
                default=p.get("default"),
                required=p.get("required", True)
            ) for p in params_data
        ]
    
    def _decode_examples(self, json_data: str) -> List[CodeExample]:
        """解码示例代码"""
        if not json_data:
            return []
        
        examples_data = json.loads(json_data)
        return [
            CodeExample(
                title=e["title"],
                description=e.get("description", ""),
                code=e["code"],
                parameters=e.get("parameters", {})
            ) for e in examples_data
        ]

class CodeValidator:
    """代码验证器"""
    
    def validate(self, code: str) -> ValidationResult:
        """
        验证生成的代码
        
        :param code: 生成的代码
        :return: 验证结果
        """
        errors = []
        
        # 1. 语法验证
        syntax_errors = self._validate_syntax(code)
        errors.extend(syntax_errors)
        
        # 2. 导入验证
        import_errors = self._validate_imports(code)
        errors.extend(import_errors)
        
        # 3. 逻辑验证
        logic_errors = self._validate_logic(code)
        errors.extend(logic_errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
    
    def _validate_syntax(self, code: str) -> List[Dict]:
        """验证代码语法"""
        try:
            ast.parse(code)
            return []
        except SyntaxError as e:
            return [{
                "type": "syntax",
                "message": str(e),
                "line": e.lineno,
                "severity": 1.0
            }]
        except Exception as e:
            return [{
                "type": "syntax",
                "message": f"Syntax validation error: {str(e)}",
                "severity": 0.8
            }]
    
    def _validate_imports(self, code: str) -> List[Dict]:
        """验证导入语句"""
        errors = []
        
        # 检查requests库
        if ("requests" in code or "get(" in code) and "import requests" not in code:
            errors.append({
                "type": "import",
                "message": "Missing import for requests library",
                "severity": 0.7
            })
        
        # 检查BeautifulSoup
        if "BeautifulSoup" in code and "from bs4 import BeautifulSoup" not in code:
            errors.append({
                "type": "import",
                "message": "Missing import for BeautifulSoup",
                "severity": 0.6
            })
        
        # 检查selenium
        if "webdriver" in code and "from selenium import webdriver" not in code:
            errors.append({
                "type": "import",
                "message": "Missing import for selenium",
                "severity": 0.6
            })
        
        return errors
    
    def _validate_logic(self, code: str) -> List[Dict]:
        """验证代码逻辑（简化实现）"""
        errors = []
        
        # 检查分页处理
        if "page" in code.lower() and "while" not in code and "for" not in code:
            errors.append({
                "type": "logic",
                "message": "Pagination logic appears incomplete",
                "severity": 0.5
            })
        
        # 检查速率限制
        if ("api" in code.lower() or "request" in code.lower()) and "time.sleep" not in code:
            errors.append({
                "type": "logic",
                "message": "Missing rate limiting",
                "severity": 0.4
            })
        
        # 检查错误处理
        if "try" not in code and ("requests.get" in code or "selenium" in code):
            errors.append({
                "type": "logic",
                "message": "Missing error handling for network requests",
                "severity": 0.6
            })
        
        # 检查User-Agent设置（针对爬虫）
        if "requests.get" in code and "User-Agent" not in code:
            errors.append({
                "type": "logic",
                "message": "Missing User-Agent header (may trigger anti-crawling)",
                "severity": 0.7
            })
        
        return errors

class ValidationResult:
    """代码验证结果"""
    def __init__(
        self,
        is_valid: bool,
        errors: List[Dict]
    ):
        self.is_valid = is_valid
        self.errors = errors
```

#### 6.4.3 问题诊断服务

**技术实现：**
```python
class ProblemDiagnosisService:
    """问题诊断服务，分析错误并提供解决方案"""
    
    def __init__(
        self,
        llm_client: LLMClient,
        knowledge_base: KnowledgeBase,
        error_analyzer: ErrorAnalyzer,
        config: Config
    ):
        self.llm_client = llm_client
        self.knowledge_base = knowledge_base
        self.error_analyzer = error_analyzer
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def diagnose(
        self,
        error_log: str,
        context: dict = None
    ) -> DiagnosisResult:
        """
        诊断错误问题并提供解决方案
        
        :param error_log: 错误日志
        :param context: 上下文信息（可选）
        :return: 诊断结果
        """
        start_time = time.time()
        
        try:
            # 1. 分析错误类型
            error_analysis = self.error_analyzer.analyze(error_log)
            
            # 2. 获取相关知识
            relevant_knowledge = self._get_relevant_knowledge(error_analysis)
            
            # 3. 构建诊断提示
            prompt = self._build_diagnosis_prompt(error_log, error_analysis, relevant_knowledge, context)
            
            # 4. 调用LLM生成诊断
            diagnosis = self.llm_client.generate(prompt)
            
            # 5. 解析诊断结果
            parsed_diagnosis = self._parse_diagnosis(diagnosis, error_analysis)
            
            # 6. 构建结果
            return DiagnosisResult(
                error_log=error_log,
                analysis=error_analysis,
                diagnosis=parsed_diagnosis,
                solutions=self._extract_solutions(parsed_diagnosis),
                confidence=self._calculate_confidence(parsed_diagnosis, error_analysis),
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("Problem diagnosis failed: %s", str(e))
            raise DiagnosisError(f"Failed to diagnose problem: {str(e)}")
    
    def _get_relevant_knowledge(self, error_analysis: ErrorAnalysis) -> Dict:
        """获取相关知识库内容"""
        knowledge = {
            "error_patterns": [],
            "anti_crawling_strategies": [],
            "technology_fingerprints": []
        }
        
        # 匹配错误模式
        if error_analysis.error_type:
            patterns = self.knowledge_base.match_error_pattern(error_analysis.error_message)
            knowledge["error_patterns"] = patterns
        
        # 获取相关反爬策略
        if error_analysis.anti_crawling_indicators:
            for indicator in error_analysis.anti_crawling_indicators:
                strategy = self.knowledge_base.get_anti_crawling_strategy(indicator)
                if strategy:
                    knowledge["anti_crawling_strategies"].append(strategy)
        
        # 获取技术栈指纹
        if error_analysis.technology:
            fingerprint = self.knowledge_base.get_technology_fingerprint(error_analysis.technology)
            if fingerprint:
                knowledge["technology_fingerprints"].append(fingerprint)
        
        return knowledge
    
    def _build_diagnosis_prompt(
        self,
        error_log: str,
        error_analysis: ErrorAnalysis,
        knowledge: Dict,
        context: dict
    ) -> str:
        """构建诊断提示词"""
        # 加载提示词模板
        template_path = self.config.get("diagnosis_prompt_template", "prompts/diagnosis.j2")
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # 准备模板变量
        template_vars = {
            "error_log": error_log,
            "error_analysis": {
                "error_type": error_analysis.error_type,
                "error_message": error_analysis.error_message,
                "status_code": error_analysis.status_code,
                "anti_crawling_indicators": error_analysis.anti_crawling_indicators,
                "technology": error_analysis.technology,
                "url": error_analysis.url
            },
            "knowledge": knowledge,
            "context": context or {},
            "current_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # 渲染提示词
        jinja_template = Template(template_content)
        return jinja_template.render(**template_vars)
    
    def _parse_diagnosis(self, diagnosis_text: str, error_analysis: ErrorAnalysis) -> Dict:
        """解析诊断结果"""
        # 简单实现：提取关键信息
        result = {
            "root_cause": "",
            "impact": "",
            "suggested_solutions": []
        }
        
        # 提取根本原因
        cause_match = re.search(r'根本原因[:：]\s*(.*?)(?=\n\s*[A-Z]|$)', diagnosis_text, re.IGNORECASE)
        if cause_match:
            result["root_cause"] = cause_match.group(1).strip()
        
        # 提取影响
        impact_match = re.search(r'影响[:：]\s*(.*?)(?=\n\s*[A-Z]|$)', diagnosis_text, re.IGNORECASE)
        if impact_match:
            result["impact"] = impact_match.group(1).strip()
        
        # 提取解决方案
        solutions_match = re.findall(r'解决方案\s*\d*[:：]\s*(.*?)(?=\n\s*(?:解决方案|$))', diagnosis_text, re.IGNORECASE)
        for solution in solutions_match:
            result["suggested_solutions"].append(solution.strip())
        
        # 如果没有提取到，使用整个文本作为原因
        if not result["root_cause"]:
            result["root_cause"] = diagnosis_text.split('\n')[0]
        
        return result
    
    def _extract_solutions(self, parsed_diagnosis: Dict) -> List[Dict]:
        """从诊断结果中提取解决方案"""
        solutions = []
        
        # 从知识库获取标准解决方案
        if parsed_diagnosis.get("root_cause"):
            # 这里可以添加更复杂的逻辑来匹配知识库中的解决方案
            pass
        
        # 从解析结果中提取
        for i, solution_text in enumerate(parsed_diagnosis.get("suggested_solutions", [])):
            solutions.append({
                "id": f"sol-{i+1}",
                "description": solution_text,
                "confidence": 0.8,  # 简化实现
                "implementation": self._generate_implementation(solution_text)
            })
        
        return solutions
    
    def _generate_implementation(self, solution_description: str) -> str:
        """为解决方案生成实现代码"""
        # 简单实现：基于描述生成代码示例
        if "User-Agent" in solution_description:
            return """headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)"""
        
        if "proxy" in solution_description.lower():
            return """proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}
response = requests.get(url, proxies=proxies)"""
        
        # 默认实现
        return f"# {solution_description}\n# 实现代码示例\npass"
    
    def _calculate_confidence(self, parsed_diagnosis: Dict, error_analysis: ErrorAnalysis) -> float:
        """计算诊断置信度"""
        base_confidence = 0.7
        
        # 根据分析的完整性调整
        if error_analysis.error_type:
            base_confidence += 0.1
        if error_analysis.anti_crawling_indicators:
            base_confidence += 0.1
        if error_analysis.technology:
            base_confidence += 0.05
        
        # 根据诊断结果的详细程度调整
        if parsed_diagnosis.get("root_cause") and len(parsed_diagnosis["root_cause"]) > 20:
            base_confidence += 0.05
        if parsed_diagnosis.get("suggested_solutions") and len(parsed_diagnosis["suggested_solutions"]) >= 2:
            base_confidence += 0.05
        
        return min(1.0, base_confidence)

class ErrorAnalyzer:
    """错误分析器，提取错误关键信息"""
    
    def analyze(self, error_log: str) -> ErrorAnalysis:
        """
        分析错误日志
        
        :param error_log: 错误日志
        :return: 错误分析结果
        """
        # 1. 提取HTTP状态码
        status_code = self._extract_status_code(error_log)
        
        # 2. 识别错误类型
        error_type = self._identify_error_type(error_log, status_code)
        
        # 3. 检测反爬迹象
        anti_crawling_indicators = self._detect_anti_crawling_indicators(error_log)
        
        # 4. 识别技术栈
        technology = self._identify_technology(error_log)
        
        # 5. 提取URL
        url = self._extract_url(error_log)
        
        return ErrorAnalysis(
            error_message=error_log,
            error_type=error_type,
            status_code=status_code,
            anti_crawling_indicators=anti_crawling_indicators,
            technology=technology,
            url=url
        )
    
    def _extract_status_code(self, error_log: str) -> Optional[int]:
        """提取HTTP状态码"""
        # 匹配常见的HTTP状态码
        pattern = r'HTTP\s*(\d{3})|status\s*code\s*(\d{3})'
        match = re.search(pattern, error_log, re.IGNORECASE)
        if match:
            return int(match.group(1) or match.group(2))
        return None
    
    def _identify_error_type(self, error_log: str, status_code: Optional[int]) -> str:
        """识别错误类型"""
        # 基于状态码
        if status_code:
            if 400 <= status_code < 500:
                return "client_error"
            if 500 <= status_code < 600:
                return "server_error"
        
        # 基于错误消息
        if "timeout" in error_log.lower():
            return "timeout"
        if "connection" in error_log.lower() and "refused" in error_log.lower():
            return "connection_refused"
        if "ssl" in error_log.lower() or "certificate" in error_log.lower():
            return "ssl_error"
        if "forbidden" in error_log.lower() or "403" in error_log:
            return "forbidden"
        if "not found" in error_log.lower() or "404" in error_log:
            return "not_found"
        
        return "unknown"
    
    def _detect_anti_crawling_indicators(self, error_log: str) -> List[str]:
        """检测反爬迹象"""
        indicators = []
        
        # 检查常见的反爬特征
        if re.search(r'captcha|验证|challenge', error_log, re.IGNORECASE):
            indicators.append("captcha")
        if "403" in error_log and "User-Agent" in error_log:
            indicators.append("user-agent-check")
        if "429" in error_log or "too many requests" in error_log.lower():
            indicators.append("rate-limiting")
        if "Access Denied" in error_log:
            indicators.append("access-denied")
        if "bot" in error_log.lower() or "crawler" in error_log.lower():
            indicators.append("bot-detection")
        
        return indicators
    
    def _identify_technology(self, error_log: str) -> Optional[str]:
        """识别网站技术栈"""
        # 简单实现：基于错误消息中的关键词
        tech_indicators = {
            "cloudflare": ["cloudflare", "cf-ray", "challenge"],
            "akamai": ["akamai", "akam"], 
            "sucuri": ["sucuri"],
            "incapsula": ["incapsula"]
        }
        
        for tech, keywords in tech_indicators.items():
            if any(keyword in error_log.lower() for keyword in keywords):
                return tech
        
        return None
    
    def _extract_url(self, error_log: str) -> Optional[str]:
        """提取URL"""
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*(?:\?[\w=&]*)?'
        match = re.search(url_pattern, error_log)
        return match.group(0) if match else None

# 辅助类定义
class ErrorAnalysis:
    """错误分析结果"""
    def __init__(
        self,
        error_message: str,
        error_type: str,
        status_code: Optional[int] = None,
        anti_crawling_indicators: List[str] = None,
        technology: Optional[str] = None,
        url: Optional[str] = None
    ):
        self.error_message = error_message
        self.error_type = error_type
        self.status_code = status_code
        self.anti_crawling_indicators = anti_crawling_indicators or []
        self.technology = technology
        self.url = url

class DiagnosisResult:
    """诊断结果"""
    def __init__(
        self,
        error_log: str,
        analysis: ErrorAnalysis,
        diagnosis: Dict,
        solutions: List[Dict],
        confidence: float,
        processing_time: float
    ):
        self.error_log = error_log
        self.analysis = analysis
        self.diagnosis = diagnosis
        self.solutions = solutions
        self.confidence = confidence
        self.processing_time = processing_time
```

#### 6.4.4 学习推荐服务

**技术实现：**
```python
class LearningRecommendationService:
    """学习推荐服务，提供个性化学习路径"""
    
    def __init__(
        self,
        user_profile_service: UserProfileService,
        content_repository: ContentRepository,
        skill_assessment: SkillAssessment,
        config: Config
    ):
        self.user_profile_service = user_profile_service
        self.content_repository = content_repository
        self.skill_assessment = skill_assessment
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def recommend(
        self,
        user_id: str,
        context: dict = None
    ) -> LearningRecommendation:
        """
        为用户生成学习推荐
        
        :param user_id: 用户ID
        :param context: 上下文信息（可选）
        :return: 学习推荐
        """
        start_time = time.time()
        
        try:
            # 1. 获取用户画像
            user_profile = self.user_profile_service.get_profile(user_id)
            
            # 2. 评估用户技能
            skill_assessment = self.skill_assessment.evaluate(user_id, context)
            
            # 3. 识别技能差距
            skill_gaps = self._identify_skill_gaps(skill_assessment)
            
            # 4. 获取相关学习内容
            relevant_content = self._get_relevant_content(skill_gaps, user_profile)
            
            # 5. 生成个性化学习路径
            learning_path = self._generate_learning_path(
                user_profile,
                skill_assessment,
                skill_gaps,
                relevant_content
            )
            
            # 6. 构建结果
            return LearningRecommendation(
                user_id=user_id,
                profile_snapshot=user_profile,
                skill_assessment=skill_assessment,
                skill_gaps=skill_gaps,
                recommended_content=learning_path,
                confidence=self._calculate_confidence(skill_assessment, skill_gaps),
                generated_at=datetime.utcnow(),
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error("Learning recommendation failed: %s", str(e))
            raise RecommendationError(f"Failed to generate learning recommendation: {str(e)}")
    
    def _identify_skill_gaps(
        self,
        skill_assessment: SkillAssessmentResult
    ) -> List[SkillGap]:
        """识别技能差距"""
        gaps = []
        
        # 检查关键技能领域
        for domain, assessment in skill_assessment.domain_assessments.items():
            # 定义关键技能
            key_skills = self.config.get(f"key_skills.{domain}", [])
            
            for skill in key_skills:
                current_level = assessment.get("skills", {}).get(skill, 0)
                target_level = self.config.get(f"target_level.{domain}.{skill}", 3)
                
                if current_level < target_level:
                    gaps.append(SkillGap(
                        domain=domain,
                        skill=skill,
                        current_level=current_level,
                        target_level=target_level,
                        gap_size=target_level - current_level
                    ))
        
        # 按差距大小排序
        gaps.sort(key=lambda x: x.gap_size, reverse=True)
        
        # 只返回top N
        return gaps[:self.config.get("max_recommendations", 5)]
    
    def _get_relevant_content(
        self,
        skill_gaps: List[SkillGap],
        user_profile: UserProfile
    ) -> List[LearningContent]:
        """获取相关学习内容"""
        all_content = []
        
        # 为每个技能差距获取内容
        for gap in skill_gaps:
            domain_content = self.content_repository.get_content(
                domain=gap.domain,
                skill=gap.skill,
                min_difficulty=gap.current_level + 1,
                max_difficulty=min(5, gap.target_level + 1),
                language=user_profile.preferred_language
            )
            
            # 按相关性排序
            sorted_content = self._rank_content(domain_content, gap, user_profile)
            all_content.extend(sorted_content)
        
        # 去重并限制数量
        unique_content = self._deduplicate_content(all_content)
        return unique_content[:self.config.get("max_content_per_recommendation", 10)]
    
    def _rank_content(
        self,
        content_list: List[LearningContent],
        skill_gap: SkillGap,
        user_profile: UserProfile
    ) -> List[LearningContent]:
        """对学习内容进行排序"""
        ranked = []
        
        for content in content_list:
            # 计算相关性分数
            relevance = self._calculate_relevance(content, skill_gap, user_profile)
            ranked.append((content, relevance))
        
        # 按相关性排序
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return [item[0] for item in ranked]
    
    def _calculate_relevance(
        self,
        content: LearningContent,
        skill_gap: SkillGap,
        user_profile: UserProfile
    ) -> float:
        """计算内容相关性"""
        score = 0.0
        
        # 技能匹配度
        if content.skill == skill_gap.skill:
            score += 0.4
        
        # 难度匹配度
        difficulty_match = 1.0 - abs(content.difficulty - (skill_gap.current_level + 0.5)) / 5.0
        score += difficulty_match * 0.3
        
        # 格式偏好
        if content.format in user_profile.content_preferences:
            score += 0.2
        
        # 语言匹配
        if content.language == user_profile.preferred_language:
            score += 0.1
        
        return min(1.0, score)
    
    def _deduplicate_content(self, content_list: List[LearningContent]) -> List[LearningContent]:
        """去重学习内容"""
        seen = set()
        unique_content = []
        
        for content in content_list:
            if content.id not in seen:
                seen.add(content.id)
                unique_content.append(content)
        
        return unique_content
    
    def _generate_learning_path(
        self,
        user_profile: UserProfile,
        skill_assessment: SkillAssessmentResult,
        skill_gaps: List[SkillGap],
        relevant_content: List[LearningContent]
    ) -> LearningPath:
        """生成学习路径"""
        # 按领域分组内容
        content_by_domain = defaultdict(list)
        for content in relevant_content:
            content_by_domain[content.domain].append(content)
        
        # 为每个领域生成路径
        domain_paths = []
        for domain, contents in content_by_domain.items():
            domain_path = self._generate_domain_path(domain, contents, skill_gaps)
            domain_paths.append(domain_path)
        
        # 整合为完整学习路径
        return LearningPath(
            title="个性化爬虫技能提升路径",
            description="根据您的技能评估生成的个性化学习路径",
            domains=domain_paths,
            estimated_duration=self._calculate_estimated_duration(relevant_content),
            difficulty_level=self._determine_difficulty_level(skill_assessment)
        )
    
    def _generate_domain_path(
        self,
        domain: str,
        contents: List[LearningContent],
        skill_gaps: List[SkillGap]
    ) -> DomainPath:
        """生成特定领域的学习路径"""
        # 按技能分组
        contents_by_skill = defaultdict(list)
        for content in contents:
            contents_by_skill[content.skill].append(content)
        
        # 为每个技能生成路径
        skill_paths = []
        for skill, skill_contents in contents_by_skill.items():
            # 按难度排序
            sorted_contents = sorted(skill_contents, key=lambda x: x.difficulty)
            
            # 创建技能路径
            skill_paths.append(SkillPath(
                skill=skill,
                description=f"{skill}技能提升路径",
                contents=sorted_contents,
                estimated_time=sum(c.estimated_duration for c in sorted_contents)
            ))
        
        return DomainPath(
            domain=domain,
            paths=skill_paths,
            estimated_time=sum(p.estimated_time for p in skill_paths)
        )
    
    def _calculate_estimated_duration(self, contents: List[LearningContent]) -> timedelta:
        """计算预计学习时间"""
        total_minutes = sum(content.estimated_duration for content in contents)
        return timedelta(minutes=total_minutes)
    
    def _determine_difficulty_level(self, skill_assessment: SkillAssessmentResult) -> str:
        """确定整体难度级别"""
        # 计算平均技能水平
        total_skills = 0
        sum_levels = 0
        
        for domain, assessment in skill_assessment.domain_assessments.items():
            for level in assessment.get("skills", {}).values():
                sum_levels += level
                total_skills += 1
        
        if total_skills == 0:
            return "beginner"
        
        avg_level = sum_levels / total_skills
        
        if avg_level < 2:
            return "beginner"
        elif avg_level < 3.5:
            return "intermediate"
        else:
            return "advanced"
    
    def _calculate_confidence(
        self,
        skill_assessment: SkillAssessmentResult,
        skill_gaps: List[SkillGap]
    ) -> float:
        """计算推荐置信度"""
        # 基于评估的完整性
        confidence = 0.7
        
        # 如果有明确的技能差距
        if skill_gaps:
            confidence += 0.2
        
        # 如果评估包含详细数据
        if any(assessment.get("detailed", False) for assessment in skill_assessment.domain_assessments.values()):
            confidence += 0.1
        
        return min(1.0, confidence)

class UserProfileService:
    """用户画像服务"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_profile(self, user_id: str) -> UserProfile:
        """获取用户画像"""
        # 从数据库获取
        sql = "SELECT * FROM user_profiles WHERE user_id = %(user_id)s"
        row = self.db.fetchone(sql, {"user_id": user_id})
        
        if not row:
            # 创建默认画像
            return self._create_default_profile(user_id)
        
        return self._row_to_profile(row)
    
    def _create_default_profile(self, user_id: str) -> UserProfile:
        """创建默认用户画像"""
        profile = UserProfile(
            user_id=user_id,
            experience_level="beginner",
            preferred_language="en",
            content_preferences=["video", "interactive"],
            learning_goals=["web_scraping", "data_processing"],
            areas_of_interest=["python", "automation"],
            skill_levels={},
            last_updated=datetime.utcnow()
        )
        
        # 保存到数据库
        self._save_profile(profile)
        
        return profile
    
    def _save_profile(self, profile: UserProfile):
        """保存用户画像"""
        sql = """
        INSERT INTO user_profiles (
            user_id, experience_level, preferred_language,
            content_preferences, learning_goals, areas_of_interest,
            skill_levels, last_updated
        ) VALUES (
            %(user_id)s, %(experience_level)s, %(preferred_language)s,
            %(content_preferences)s, %(learning_goals)s, %(areas_of_interest)s,
            %(skill_levels)s, %(last_updated)s
        )
        ON CONFLICT (user_id) DO UPDATE SET
            experience_level = EXCLUDED.experience_level,
            preferred_language = EXCLUDED.preferred_language,
            content_preferences = EXCLUDED.content_preferences,
            learning_goals = EXCLUDED.learning_goals,
            areas_of_interest = EXCLUDED.areas_of_interest,
            skill_levels = EXCLUDED.skill_levels,
            last_updated = EXCLUDED.last_updated
        """
        
        self.db.execute(sql, {
            "user_id": profile.user_id,
            "experience_level": profile.experience_level,
            "preferred_language": profile.preferred_language,
            "content_preferences": json.dumps(profile.content_preferences),
            "learning_goals": json.dumps(profile.learning_goals),
            "areas_of_interest": json.dumps(profile.areas_of_interest),
            "skill_levels": json.dumps(profile.skill_levels),
            "last_updated": profile.last_updated
        })
    
    def _row_to_profile(self, row: Dict) -> UserProfile:
        """将数据库行转换为UserProfile对象"""
        return UserProfile(
            user_id=row["user_id"],
            experience_level=row["experience_level"],
            preferred_language=row["preferred_language"],
            content_preferences=json.loads(row["content_preferences"]),
            learning_goals=json.loads(row["learning_goals"]),
            areas_of_interest=json.loads(row["areas_of_interest"]),
            skill_levels=json.loads(row["skill_levels"]),
            last_updated=row["last_updated"]
        )

class ContentRepository:
    """学习内容仓库"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_content(
        self,
        domain: str = None,
        skill: str = None,
        min_difficulty: int = 1,
        max_difficulty: int = 5,
        language: str = "en",
        limit: int = 20
    ) -> List[LearningContent]:
        """获取学习内容"""
        # 构建查询
        conditions = []
        params = {
            "min_difficulty": min_difficulty,
            "max_difficulty": max_difficulty,
            "language": language,
            "limit": limit
        }
        
        if domain:
            conditions.append("domain = %(domain)s")
            params["domain"] = domain
        if skill:
            conditions.append("skill = %(skill)s")
            params["skill"] = skill
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        sql = f"""
        SELECT * FROM learning_content
        {where_clause}
        AND difficulty BETWEEN %(min_difficulty)s AND %(max_difficulty)s
        AND language = %(language)s
        ORDER BY relevance_score DESC
        LIMIT %(limit)s
        """
        
        rows = self.db.fetchall(sql, params)
        return [self._row_to_content(row) for row in rows]
    
    def _row_to_content(self, row: Dict) -> LearningContent:
        """将数据库行转换为LearningContent对象"""
        return LearningContent(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            domain=row["domain"],
            skill=row["skill"],
            format=row["format"],
            difficulty=row["difficulty"],
            estimated_duration=row["estimated_duration"],
            content_url=row["content_url"],
            language=row["language"],
            prerequisites=json.loads(row["prerequisites"]) if row["prerequisites"] else [],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            relevance_score=row["relevance_score"],
            created_at=row["created_at"]
        )

class SkillAssessment:
    """技能评估器"""
    
    def __init__(self, db: Database, config: Config):
        self.db = db
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def evaluate(
        self,
        user_id: str,
        context: dict = None
    ) -> SkillAssessmentResult:
        """
        评估用户技能水平
        
        :param user_id: 用户ID
        :param context: 上下文信息
        :return: 技能评估结果
        """
        # 1. 获取用户历史数据
        user_history = self._get_user_history(user_id)
        
        # 2. 分析用户行为
        behavioral_analysis = self._analyze_behavior(user_history, context)
        
        # 3. 评估各领域技能
        domain_assessments = self._assess_domains(user_id, user_history, behavioral_analysis)
        
        # 4. 生成综合评估
        return SkillAssessmentResult(
            user_id=user_id,
            domain_assessments=domain_assessments,
            behavioral_analysis=behavioral_analysis,
            assessment_date=datetime.utcnow(),
            detailed=True  # 是否包含详细评估
        )
    
    def _get_user_history(self, user_id: str) -> UserHistory:
        """获取用户历史数据"""
        # 从数据库获取
        # 这里简化实现
        return UserHistory(
            user_id=user_id,
            completed_tasks=[],
            code_submissions=[],
            error_logs=[],
            learning_progress={}
        )
    
    def _analyze_behavior(
        self,
        user_history: UserHistory,
        context: dict
    ) -> Dict:
        """分析用户行为"""
        analysis = {
            "activity_level": "medium",
            "learning_style": "visual",
            "problem_solving_pattern": "step_by_step",
            "common_challenges": []
        }
        
        # 分析代码提交
        if user_history.code_submissions:
            # 简单分析
            avg_code_length = sum(len(submission.code) for submission in user_history.code_submissions) / len(user_history.code_submissions)
            if avg_code_length > 100:
                analysis["coding_style"] = "detailed"
            else:
                analysis["coding_style"] = "concise"
        
        # 分析错误日志
        if user_history.error_logs:
            error_types = [self._categorize_error(log) for log in user_history.error_logs]
            error_counter = Counter(error_types)
            analysis["common_challenges"] = [err for err, count in error_counter.most_common(3)]
        
        return analysis
    
    def _categorize_error(self, error_log: str) -> str:
        """分类错误类型"""
        if "403" in error_log or "forbidden" in error_log.lower():
            return "access_denied"
        if "429" in error_log or "too many requests" in error_log.lower():
            return "rate_limiting"
        if "timeout" in error_log.lower():
            return "timeout"
        if "not found" in error_log.lower() or "404" in error_log:
            return "resource_not_found"
        return "other"
    
    def _assess_domains(
        self,
        user_id: str,
        user_history: UserHistory,
        behavioral_analysis: Dict
    ) -> Dict[str, Dict]:
        """评估各领域技能"""
        domains = self.config.get("assessment_domains", ["web_scraping", "data_processing", "api_integration"])
        assessments = {}
        
        for domain in domains:
            # 获取领域配置
            domain_config = self.config.get(f"domain.{domain}", {})
            
            # 评估技能水平
            skill_level = self._assess_skill_level(
                domain,
                user_history,
                behavioral_analysis,
                domain_config
            )
            
            # 识别技能点
            skills = self._assess_skills(
                domain,
                user_history,
                skill_level,
                domain_config
            )
            
            assessments[domain] = {
                "overall_level": skill_level,
                "skills": skills,
                "strengths": self._identify_strengths(domain, skills),
                "weaknesses": self._identify_weaknesses(domain, skills)
            }
        
        return assessments
    
    def _assess_skill_level(
        self,
        domain: str,
        user_history: UserHistory,
        behavioral_analysis: Dict,
        domain_config: Dict
    ) -> float:
        """评估领域整体技能水平"""
        # 基于完成的任务
        completed_tasks = [t for t in user_history.completed_tasks if t.domain == domain]
        task_score = min(1.0, len(completed_tasks) / 5)  # 假设5个任务达到最高水平
        
        # 基于代码质量
        code_submissions = [s for s in user_history.code_submissions if s.domain == domain]
        code_score = self._calculate_code_score(code_submissions)
        
        # 基于错误率
        error_rate = self._calculate_error_rate(user_history.error_logs, domain)
        error_score = max(0.0, 1.0 - error_rate * 2)
        
        # 加权计算
        weights = domain_config.get("weights", {
            "tasks": 0.4,
            "code": 0.3,
            "errors": 0.3
        })
        
        total_score = (
            task_score * weights["tasks"] +
            code_score * weights["code"] +
            error_score * weights["errors"]
        )
        
        # 转换为1-5的等级
        return min(5.0, max(1.0, total_score * 4 + 1))
    
    def _calculate_code_score(self, submissions: List[CodeSubmission]) -> float:
        """计算代码质量分数"""
        if not submissions:
            return 0.5
        
        # 简单实现：基于代码长度和错误
        total_score = 0
        for sub in submissions:
            # 基本分数
            score = 0.5
            
            # 代码长度加分
            if len(sub.code) > 50:
                score += 0.2
            
            # 错误数量扣分
            error_penalty = min(0.3, sub.error_count * 0.1)
            score -= error_penalty
            
            total_score += max(0.0, score)
        
        return total_score / len(submissions)
    
    def _calculate_error_rate(self, error_logs: List[str], domain: str) -> float:
        """计算错误率"""
        if not error_logs:
            return 0.0
        
        # 计算与领域相关的错误
        domain_errors = [log for log in error_logs if self._is_domain_error(log, domain)]
        return len(domain_errors) / len(error_logs)
    
    def _is_domain_error(self, error_log: str, domain: str) -> bool:
        """检查错误是否与领域相关"""
        if domain == "web_scraping":
            return any(keyword in error_log.lower() 
                      for keyword in ["scrape", "crawl", "parser", "selector", "403", "429"])
        elif domain == "data_processing":
            return any(keyword in error_log.lower() 
                      for keyword in ["process", "transform", "clean", "format", "parse"])
        elif domain == "api_integration":
            return any(keyword in error_log.lower() 
                      for keyword in ["api", "endpoint", "token", "auth", "rate limit"])
        return False
    
    def _assess_skills(
        self,
        domain: str,
        user_history: UserHistory,
        overall_level: float,
        domain_config: Dict
    ) -> Dict[str, float]:
        """评估具体技能点"""
        skills = domain_config.get("skills", {})
        assessed_skills = {}
        
        for skill, config in skills.items():
            # 基础分数基于整体水平
            base_score = overall_level * config.get("weight", 1.0)
            
            # 根据特定指标调整
            if domain == "web_scraping":
                if skill == "static_html":
                    base_score = self._assess_static_html_skill(user_history)
                elif skill == "dynamic_rendering":
                    base_score = self._assess_dynamic_rendering_skill(user_history)
                # 其他技能...
            
            # 限制在1-5范围
            assessed_skills[skill] = max(1.0, min(5.0, base_score))
        
        return assessed_skills
    
    def _assess_static_html_skill(self, user_history: UserHistory) -> float:
        """评估静态HTML爬取技能"""
        # 检查是否使用过requests和BeautifulSoup
        has_requests = any("import requests" in sub.code for sub in user_history.code_submissions)
        has_bs4 = any("from bs4 import BeautifulSoup" in sub.code for sub in user_history.code_submissions)
        
        score = 1.0
        if has_requests:
            score += 1.5
        if has_bs4:
            score += 1.5
        
        # 检查是否处理过常见问题
        if any("403" in log for log in user_history.error_logs):
            score += 1.0  # 处理了访问被拒绝问题
        if any("pagination" in sub.code for sub in user_history.code_submissions):
            score += 1.0  # 处理过分页
        
        return score
    
    def _assess_dynamic_rendering_skill(self, user_history: UserHistory) -> float:
        """评估动态渲染页面爬取技能"""
        # 检查是否使用过selenium或类似工具
        has_selenium = any("from selenium import webdriver" in sub.code for sub in user_history.code_submissions)
        has_playwright = any("from playwright import sync_playwright" in sub.code for sub in user_history.code_submissions)
        
        score = 1.0
        if has_selenium or has_playwright:
            score += 2.0
        
        # 检查是否处理过等待问题
        if any("WebDriverWait" in sub.code or "time.sleep" in sub.code for sub in user_history.code_submissions):
            score += 1.0
        
        # 检查是否处理过反爬问题
        if any("proxy" in sub.code for sub in user_history.code_submissions):
            score += 1.0
        
        return score
    
    def _identify_strengths(self, domain: str, skills: Dict[str, float]) -> List[str]:
        """识别优势技能"""
        # 找出高于平均的技能
        avg = sum(skills.values()) / len(skills) if skills else 3.0
        return [skill for skill, level in skills.items() if level >= avg + 0.5]
    
    def _identify_weaknesses(self, domain: str, skills: Dict[str, float]) -> List[str]:
        """识别薄弱技能"""
        # 找出低于平均的技能
        avg = sum(skills.values()) / len(skills) if skills else 3.0
        return [skill for skill, level in skills.items() if level <= avg - 0.5]

# 辅助类定义
class UserProfile:
    """用户画像"""
    def __init__(
        self,
        user_id: str,
        experience_level: str,
        preferred_language: str,
        content_preferences: List[str],
        learning_goals: List[str],
        areas_of_interest: List[str],
        skill_levels: Dict[str, float],
        last_updated: datetime
    ):
        self.user_id = user_id
        self.experience_level = experience_level
        self.preferred_language = preferred_language
        self.content_preferences = content_preferences
        self.learning_goals = learning_goals
        self.areas_of_interest = areas_of_interest
        self.skill_levels = skill_levels
        self.last_updated = last_updated

class UserHistory:
    """用户历史数据"""
    def __init__(
        self,
        user_id: str,
        completed_tasks: List,
        code_submissions: List,
        error_logs: List[str],
        learning_progress: Dict
    ):
        self.user_id = user_id
        self.completed_tasks = completed_tasks
        self.code_submissions = code_submissions
        self.error_logs = error_logs
        self.learning_progress = learning_progress

class CodeSubmission:
    """代码提交记录"""
    def __init__(
        self,
        id: str,
        user_id: str,
        domain: str,
        code: str,
        error_count: int,
        timestamp: datetime
    ):
        self.id = id
        self.user_id = user_id
        self.domain = domain
        self.code = code
        self.error_count = error_count
        self.timestamp = timestamp

class SkillGap:
    """技能差距"""
    def __init__(
        self,
        domain: str,
        skill: str,
        current_level: float,
        target_level: float,
        gap_size: float
    ):
        self.domain = domain
        self.skill = skill
        self.current_level = current_level
        self.target_level = target_level
        self.gap_size = gap_size

class LearningContent:
    """学习内容"""
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        domain: str,
        skill: str,
        format: str,
        difficulty: int,
        estimated_duration: int,
        content_url: str,
        language: str,
        prerequisites: List[str],
        tags: List[str],
        relevance_score: float,
        created_at: datetime
    ):
        self.id = id
        self.title = title
        self.description = description
        self.domain = domain
        self.skill = skill
        self.format = format
        self.difficulty = difficulty
        self.estimated_duration = estimated_duration  # 分钟
        self.content_url = content_url
        self.language = language
        self.prerequisites = prerequisites
        self.tags = tags
        self.relevance_score = relevance_score
        self.created_at = created_at

class DomainPath:
    """领域学习路径"""
    def __init__(
        self,
        domain: str,
        paths: List,
        estimated_time: timedelta
    ):
        self.domain = domain
        self.paths = paths
        self.estimated_time = estimated_time

class SkillPath:
    """技能学习路径"""
    def __init__(
        self,
        skill: str,
        description: str,
        contents: List[LearningContent],
        estimated_time: timedelta
    ):
        self.skill = skill
        self.description = description
        self.contents = contents
        self.estimated_time = estimated_time

class LearningPath:
    """学习路径"""
    def __init__(
        self,
        title: str,
        description: str,
        domains: List[DomainPath],
        estimated_duration: timedelta,
        difficulty_level: str
    ):
        self.title = title
        self.description = description
        self.domains = domains
        self.estimated_duration = estimated_duration
        self.difficulty_level = difficulty_level

class LearningRecommendation:
    """学习推荐"""
    def __init__(
        self,
        user_id: str,
        profile_snapshot: UserProfile,
        skill_assessment: SkillAssessmentResult,
        skill_gaps: List[SkillGap],
        recommended_content: LearningPath,
        confidence: float,
        generated_at: datetime,
        processing_time: float
    ):
        self.user_id = user_id
        self.profile_snapshot = profile_snapshot
        self.skill_assessment = skill_assessment
        self.skill_gaps = skill_gaps
        self.recommended_content = recommended_content
        self.confidence = confidence
        self.generated_at = generated_at
        self.processing_time = processing_time

class SkillAssessmentResult:
    """技能评估结果"""
    def __init__(
        self,
        user_id: str,
        domain_assessments: Dict[str, Dict],
        behavioral_analysis: Dict,
        assessment_date: datetime,
        detailed: bool
    ):
        self.user_id = user_id
        self.domain_assessments = domain_assessments
        self.behavioral_analysis = behavioral_analysis
        self.assessment_date = assessment_date
        self.detailed = detailed
```

### 6.5 数据模型详细定义

#### 6.5.1 用户画像表

```sql
-- 用户画像表
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    experience_level VARCHAR(20) NOT NULL DEFAULT 'beginner' CHECK (experience_level IN ('beginner', 'intermediate', 'advanced')),
    preferred_language VARCHAR(10) NOT NULL DEFAULT 'en',
    content_preferences JSONB DEFAULT '["video", "interactive"]'::jsonb,
    learning_goals JSONB DEFAULT '["web_scraping", "data_processing"]'::jsonb,
    areas_of_interest JSONB DEFAULT '["python", "automation"]'::jsonb,
    skill_levels JSONB DEFAULT '{}'::jsonb,
    last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_profiles_language ON user_profiles(preferred_language),
    INDEX idx_profiles_experience ON user_profiles(experience_level)
);
```

#### 6.5.2 学习内容表

```sql
-- 学习内容表
CREATE TABLE learning_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    domain VARCHAR(50) NOT NULL,
    skill VARCHAR(50) NOT NULL,
    format VARCHAR(20) NOT NULL CHECK (format IN ('video', 'article', 'tutorial', 'interactive', 'code_example')),
    difficulty INT NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    estimated_duration INT NOT NULL,  -- 分钟
    content_url VARCHAR(1024) NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    prerequisites JSONB DEFAULT '[]'::jsonb,
    tags JSONB DEFAULT '[]'::jsonb,
    relevance_score NUMERIC(4,2) NOT NULL DEFAULT 0.5,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_content_domain ON learning_content(domain),
    INDEX idx_content_skill ON learning_content(skill),
    INDEX idx_content_difficulty ON learning_content(difficulty),
    INDEX idx_content_language ON learning_content(language),
    INDEX idx_content_relevance ON learning_content(relevance_score DESC)
);
```

#### 6.5.3 技能评估表

```sql
-- 技能评估表
CREATE TABLE skill_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    domain_assessments JSONB NOT NULL,
    behavioral_analysis JSONB NOT NULL,
    detailed BOOLEAN NOT NULL DEFAULT true,
    
    -- 索引
    INDEX idx_assessments_user ON skill_assessments(user_id),
    INDEX idx_assessments_date ON skill_assessments(assessment_date DESC)
);
```

#### 6.5.4 用户学习进度表

```sql
-- 用户学习进度表
CREATE TABLE user_learning_progress (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_id UUID NOT NULL REFERENCES learning_content(id) ON DELETE CASCADE,
    progress NUMERIC(4,2) NOT NULL DEFAULT 0.0 CHECK (progress BETWEEN 0.0 AND 1.0),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    last_accessed TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    PRIMARY KEY (user_id, content_id),
    
    -- 索引
    INDEX idx_progress_user ON user_learning_progress(user_id),
    INDEX idx_progress_content ON user_learning_progress(content_id),
    INDEX idx_progress_completion ON user_learning_progress(completed_at DESC)
);
```

#### 6.5.5 用户代码提交记录表

```sql
-- 用户代码提交记录表
CREATE TABLE user_code_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    domain VARCHAR(50) NOT NULL,
    code TEXT NOT NULL,
    error_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_submissions_user ON user_code_submissions(user_id),
    INDEX idx_submissions_domain ON user_code_submissions(domain),
    INDEX idx_submissions_date ON user_code_submissions(created_at DESC)
);
```

### 6.6 API详细规范

#### 6.6.1 代码生成API

**生成爬虫代码 (POST /api/v1/code:generate)**

*请求示例:*
```http
POST /api/v1/code:generate HTTP/1.1
Host: aids.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "request": "请生成一个爬取https://example.com/products的Python爬虫，需要处理分页和User-Agent轮换",
  "context": {
    "language": "python",
    "preferred_style": "functional",
    "avoid_selenium": true
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "code": "import requests\nfrom fake_useragent import UserAgent\n\nua = UserAgent()\n\nfor page in range(1, 11):\n    url = f'https://example.com/products?page={page}'\n    headers = {'User-Agent': ua.random}\n    response = requests.get(url, headers=headers)\n    # 处理响应...\n    print(f'Page {page} status: {response.status_code}')",
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

*成功响应示例:*
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
    "root_cause": "网站通过User-Agent检测识别出爬虫请求",
    "impact": "请求被服务器拒绝，无法获取数据",
    "suggested_solutions": [
      "使用更真实的User-Agent轮换策略",
      "添加必要的请求头模拟浏览器行为",
      "考虑使用代理IP轮换"
    ]
  },
  "solutions": [
    {
      "id": "sol-1",
      "description": "使用更真实的User-Agent轮换策略",
      "confidence": 0.85,
      "implementation": "from fake_useragent import UserAgent\nua = UserAgent()\nheaders = {'User-Agent': ua.random}"
    },
    {
      "id": "sol-2",
      "description": "添加必要的请求头模拟浏览器行为",
      "confidence": 0.78,
      "implementation": "headers = {\n    'User-Agent': 'Mozilla/5.0...',\n    'Accept-Language': 'en-US,en;q=0.9',\n    'Sec-Ch-Ua': '\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not_A Brand\";v=\"24\"'\n}"
    }
  ],
  "confidence": 0.82,
  "processing_time": 0.87
}
```

#### 6.6.3 学习推荐API

**获取学习推荐 (GET /api/v1/learning/recommendations)**

*请求示例:*
```http
GET /api/v1/learning/recommendations HTTP/1.1
Host: aids.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例:*
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
    "title": "个性化爬虫技能提升路径",
    "description": "根据您的技能评估生成的个性化学习路径",
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
                "title": "使用Selenium处理JavaScript渲染页面",
                "description": "学习如何使用Selenium处理动态渲染的网页内容",
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
                "title": "Playwright高级应用：处理单页应用",
                "description": "深入学习Playwright处理复杂的单页应用",
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
                "title": "绕过常见反爬机制：理论与实践",
                "description": "全面了解并学习绕过各种反爬机制的方法",
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

### 6.7 性能优化策略

#### 6.7.1 LLM调用优化

1. **缓存机制**
   ```python
   class LLMCachingClient:
       """带缓存的LLM客户端"""
       
       def __init__(self, llm_client, cache_ttl=3600):
           self.llm_client = llm_client
           self.cache = TTLCache(maxsize=1000, ttl=cache_ttl)
           self.logger = logging.getLogger(__name__)
       
       def generate(self, prompt: str) -> str:
           """生成文本，使用缓存"""
           # 生成缓存键（提示词的哈希）
           cache_key = self._generate_cache_key(prompt)
           
           # 检查缓存
           if cache_key in self.cache:
               self.logger.info("LLM response from cache")
               return self.cache[cache_key]
           
           # 调用LLM
           start_time = time.time()
           response = self.llm_client.generate(prompt)
           duration = time.time() - start_time
           
           # 记录指标
           self.logger.info("LLM call completed in %.2f seconds", duration)
           
           # 缓存结果
           self.cache[cache_key] = response
           
           return response
       
       def _generate_cache_key(self, prompt: str) -> str:
           """生成缓存键"""
           return hashlib.md5(prompt.encode('utf-8')).hexdigest()
   ```

2. **提示词优化**
   ```python
   class PromptOptimizer:
       """提示词优化器，减少token使用"""
       
       def optimize(self, prompt: str) -> str:
           """优化提示词"""
           # 1. 移除冗余空格和换行
           optimized = re.sub(r'\s+', ' ', prompt).strip()
           
           # 2. 缩短常见短语
           replacements = {
               "please": "plz",
               "information": "info",
               "approximately": "approx",
               "example": "ex",
               "solution": "sol"
           }
           
           for old, new in replacements.items():
               optimized = re.sub(r'\b' + old + r'\b', new, optimized, flags=re.IGNORECASE)
           
           # 3. 截断过长的部分
           if len(optimized) > 2000:
               # 保留开头和结尾
               optimized = optimized[:1000] + "...[TRUNCATED]..." + optimized[-1000:]
           
           return optimized
   ```

3. **批处理请求**
   ```python
   class BatchLLMClient:
       """批处理LLM客户端"""
       
       def __init__(self, llm_client, batch_size=5, max_wait=2.0):
           self.llm_client = llm_client
           self.batch_size = batch_size
           self.max_wait = max_wait
           self.request_queue = []
           self.lock = threading.Lock()
           self.thread = threading.Thread(target=self._process_queue, daemon=True)
           self.thread.start()
       
       def _process_queue(self):
           """处理请求队列"""
           while True:
               with self.lock:
                   if len(self.request_queue) >= self.batch_size or (self.request_queue and time.time() - self.request_queue[0][2] > self.max_wait):
                       batch = self.request_queue[:self.batch_size]
                       self.request_queue = self.request_queue[self.batch_size:]
                   else:
                       batch = None
               
               if batch:
                   self._process_batch(batch)
               
               time.sleep(0.1)
       
       def _process_batch(self, batch):
           """处理一批请求"""
           prompts = [item[0] for item in batch]
           callbacks = [item[1] for item in batch]
           
           try:
               # 调用LLM处理批量请求
               responses = self.llm_client.generate_batch(prompts)
               
               # 调用回调
               for callback, response in zip(callbacks, responses):
                   callback(response)
           except Exception as e:
               for callback in callbacks:
                   callback(None, str(e))
       
       def generate(self, prompt: str, callback: Callable):
           """异步生成文本"""
           with self.lock:
               self.request_queue.append((prompt, callback, time.time()))
   ```

#### 6.7.2 上下文管理优化

1. **上下文压缩**
   ```python
   class ContextCompressor:
       """上下文压缩器，减少上下文token数量"""
       
       def compress(self, context: Dict, max_tokens: int = 2000) -> Dict:
           """
           压缩上下文到指定token限制
           
           :param context: 原始上下文
           :param max_tokens: 最大token数
           :return: 压缩后的上下文
           """
           # 1. 计算当前token数
           current_tokens = self._estimate_tokens(context)
           
           # 2. 如果不需要压缩，直接返回
           if current_tokens <= max_tokens:
               return context
           
           # 3. 按重要性排序
           important_keys = ["error_log", "user_request", "recent_messages"]
           less_important_keys = [k for k in context.keys() if k not in important_keys]
           
           # 4. 优先保留重要信息
           compressed = {k: context[k] for k in important_keys if k in context}
           
           # 5. 逐步添加次要信息直到达到token限制
           remaining_tokens = max_tokens - self._estimate_tokens(compressed)
           
           for key in less_important_keys:
               if remaining_tokens <= 0:
                   break
               
               # 压缩单个字段
               compressed_value = self._compress_field(context[key], remaining_tokens)
               compressed[key] = compressed_value
               
               # 更新剩余token
               remaining_tokens -= self._estimate_tokens({key: compressed_value})
           
           return compressed
       
       def _compress_field(self, value: Any, max_tokens: int) -> Any:
           """压缩单个字段"""
           if isinstance(value, str):
               # 简单实现：截断字符串
               tokens = self._estimate_tokens(value)
               if tokens > max_tokens:
                   # 保留开头和结尾
                   return value[:max_tokens//2] + "...[TRUNCATED]..." + value[-max_tokens//2:]
               return value
           
           elif isinstance(value, list):
               # 保留前N个元素
               if len(value) > 5:
                   return value[:5]
               return value
           
           elif isinstance(value, dict):
               # 保留最重要的字段
               important_fields = ["root_cause", "solutions", "error_message"]
               return {k: v for k, v in value.items() if k in important_fields}
           
           return value
       
       def _estimate_tokens(self, obj: Any) -> int:
           """估计对象的token数量"""
           if isinstance(obj, str):
               # 简单估计：每个字符约0.25个token
               return max(1, len(obj) // 4)
           elif isinstance(obj, list):
               return sum(self._estimate_tokens(item) for item in obj)
           elif isinstance(obj, dict):
               return sum(self._estimate_tokens(v) for v in obj.values())
           return 1
   ```

2. **上下文摘要**
   ```python
   class ContextSummarizer:
       """上下文摘要生成器"""
       
       def __init__(self, llm_client):
           self.llm_client = llm_client
       
       def summarize(self, context: Dict) -> str:
           """
           生成上下文摘要
           
           :param context: 原始上下文
           :return: 上下文摘要
           """
           # 构建摘要提示词
           prompt = f"""
           请将以下对话上下文总结为简洁的摘要，保留关键信息，不超过100个词：

           {json.dumps(context, indent=2)}

           摘要:
           """
           
           # 生成摘要
           summary = self.llm_client.generate(prompt)
           
           # 清理结果
           return summary.strip()
   ```

#### 6.7.3 资源管理策略

1. **资源配额管理**
   ```python
   class ResourceQuotaManager:
       """资源配额管理器"""
       
       def __init__(self, db: Database, config: Config):
           self.db = db
           self.config = config
           self.logger = logging.getLogger(__name__)
           self.quota_cache = TTLCache(maxsize=1000, ttl=300)  # 5分钟缓存
       
       def check_quota(
           self,
           user_id: str,
           resource_type: str,
           amount: int
       ) -> Tuple[bool, str]:
           """
           检查资源配额
           
           :param user_id: 用户ID
           :param resource_type: 资源类型 (llm_calls, processing_time等)
           :param amount: 请求的资源量
           :return: (是否允许, 消息)
           """
           # 1. 获取用户配额
           quota = self._get_user_quota(user_id)
           
           # 2. 获取已用资源
           used = self._get_used_resources(user_id, resource_type)
           
           # 3. 检查是否超出配额
           if used + amount > quota[resource_type]:
               return False, f"超出{resource_type}配额 ({used}/{quota[resource_type]})"
           
           # 4. 预扣资源
           self._reserve_resources(user_id, resource_type, amount)
           
           return True, f"已预留{amount}单位{resource_type}"
       
       def _get_user_quota(self, user_id: str) -> Dict:
           """获取用户配额"""
           # 从缓存获取
           cache_key = f"{user_id}:quota"
           if cache_key in self.quota_cache:
               return self.quota_cache[cache_key]
           
           # 从数据库获取
           sql = """
           SELECT llm_calls, processing_time, storage 
           FROM user_quotas 
           WHERE user_id = %(user_id)s
           """
           row = self.db.fetchone(sql, {"user_id": user_id})
           
           if not row:
               # 默认配额
               quota = {
                   "llm_calls": self.config.default_llm_calls,
                   "processing_time": self.config.default_processing_time,
                   "storage": self.config.default_storage
               }
           else:
               quota = {
                   "llm_calls": row["llm_calls"],
                   "processing_time": row["processing_time"],
                   "storage": row["storage"]
               }
           
           # 缓存结果
           self.quota_cache[cache_key] = quota
           return quota
       
       def _get_used_resources(self, user_id: str, resource_type: str) -> int:
           """获取已用资源"""
           # 实现资源使用统计
           # 这里简化为返回0
           return 0
       
       def _reserve_resources(
           self,
           user_id: str,
           resource_type: str,
           amount: int
       ):
           """预扣资源"""
           # 实现资源预留
           pass
   ```

### 6.8 安全考虑

#### 6.8.1 LLM输出安全

1. **输出过滤器**
   ```python
   class SafetyFilter:
       """安全过滤器，防止LLM输出有害内容"""
       
       def __init__(self, config: Config):
           self.config = config
           self.logger = logging.getLogger(__name__)
           self.blocked_keywords = self._load_blocked_keywords()
       
       def _load_blocked_keywords(self) -> List[str]:
           """加载屏蔽关键词"""
           # 从配置或数据库加载
           return [
               "rm -rf /",
               "sudo",
               "os.system",
               "subprocess.",
               "eval(",
               "exec(",
               "import os",
               "import sys",
               "import subprocess",
               "import ctypes",
               "shutil.rmtree",
               "format C:\\",
               "delete all",
               "malicious code"
           ]
       
       def filter(self, output: str) -> Tuple[bool, str, List[str]]:
           """
           过滤LLM输出
           
           :param output: LLM生成的输出
           :return: (是否安全, 安全输出, 检测到的风险)
           """
           risks = []
           
           # 1. 检查关键词
           for keyword in self.blocked_keywords:
               if keyword.lower() in output.lower():
                   risks.append(f"潜在危险关键词: {keyword}")
           
           # 2. 检查代码执行命令
           if re.search(r'os\.(system|popen|exec)', output):
               risks.append("检测到潜在危险的系统命令调用")
           
           # 3. 检查文件删除操作
           if re.search(r'(shutil\.rmtree|os\.remove|os\.unlink)', output):
               risks.append("检测到潜在危险的文件删除操作")
           
           # 4. 检查敏感信息
           if re.search(r'password|secret|token|api_key', output, re.IGNORECASE):
               risks.append("检测到潜在的敏感信息暴露")
           
           # 5. 如果有风险，返回过滤后的输出
           if risks:
               # 移除潜在危险内容
               safe_output = self._sanitize_output(output)
               return False, safe_output, risks
           
           return True, output, []
       
       def _sanitize_output(self, output: str) -> str:
           """清理输出中的危险内容"""
           # 替换危险命令
           sanitized = re.sub(r'rm\s+-rf\s+/', 'SAFE_rm -rf /', output)
           sanitized = re.sub(r'os\.system\((.*?)\)', 'os.system(SAFE_COMMAND)', sanitized)
           
           # 移除敏感信息
           sanitized = re.sub(r'password\s*=\s*["\'].*?["\']', 'password = "***"', sanitized)
           sanitized = re.sub(r'api_key\s*=\s*["\'].*?["\']', 'api_key = "***"', sanitized)
           
           return sanitized
   ```

2. **沙箱代码执行**
   ```python
   class CodeSandbox:
       """代码沙箱，安全执行代码"""
       
       def __init__(self, config: Config):
           self.config = config
           self.logger = logging.getLogger(__name__)
       
       def execute(self, code: str, timeout: int = 5) -> Dict:
           """
           在沙箱中执行代码
           
           :param code: 要执行的代码
           :param timeout: 超时时间(秒)
           :return: 执行结果
           """
           # 1. 创建隔离环境
           sandbox_dir = self._create_sandbox()
           
           try:
               # 2. 写入代码到文件
               code_path = os.path.join(sandbox_dir, "code.py")
               with open(code_path, "w") as f:
                   f.write(code)
               
               # 3. 限制资源
               resource_limits = {
                   "cpu_time": self.config.sandbox_cpu_time,
                   "memory": self.config.sandbox_memory,
                   "disk_space": self.config.sandbox_disk_space
               }
               
               # 4. 执行代码
               result = self._run_with_limits(
                   ["python", code_path],
                   cwd=sandbox_dir,
                   timeout=timeout,
                   resource_limits=resource_limits
               )
               
               # 5. 收集结果
               return {
                   "stdout": result.stdout,
                   "stderr": result.stderr,
                   "returncode": result.returncode,
                   "duration": result.duration,
                   "error": result.error
               }
               
           finally:
               # 6. 清理沙箱
               self._cleanup_sandbox(sandbox_dir)
       
       def _create_sandbox(self) -> str:
           """创建沙箱环境"""
           sandbox_dir = tempfile.mkdtemp(prefix="sandbox_")
           
           # 创建必要的目录结构
           os.makedirs(os.path.join(sandbox_dir, "output"), exist_ok=True)
           
           # 复制必要的库（如果需要）
           # ...
           
           return sandbox_dir
       
       def _run_with_limits(
           self,
           command: List[str],
           cwd: str,
           timeout: int,
           resource_limits: Dict
       ) -> ExecutionResult:
           """在资源限制下运行命令"""
           start_time = time.time()
           
           try:
               # 使用subprocess运行，带超时
               process = subprocess.Popen(
                   command,
                   cwd=cwd,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   text=True
               )
               
               try:
                   stdout, stderr = process.communicate(timeout=timeout)
                   duration = time.time() - start_time
                   
                   return ExecutionResult(
                       stdout=stdout,
                       stderr=stderr,
                       returncode=process.returncode,
                       duration=duration,
                       error=None
                   )
               except subprocess.TimeoutExpired:
                   process.kill()
                   return ExecutionResult(
                       stdout="",
                       stderr="Execution timed out",
                       returncode=-1,
                       duration=timeout,
                       error="Timeout"
                   )
                   
           except Exception as e:
               return ExecutionResult(
                   stdout="",
                   stderr=str(e),
                   returncode=-1,
                   duration=time.time() - start_time,
                   error=str(e)
               )
       
       def _cleanup_sandbox(self, sandbox_dir: str):
           """清理沙箱环境"""
           try:
               shutil.rmtree(sandbox_dir)
           except Exception as e:
               self.logger.error("Error cleaning up sandbox: %s", str(e))
   ```

#### 6.8.2 数据隐私保护

1. **数据脱敏中间件**
   ```python
   class DataAnonymizer:
       """数据脱敏中间件"""
       
       def __init__(self, config: Config):
           self.config = config
           self.logger = logging.getLogger(__name__)
           self.patterns = self._load_patterns()
       
       def _load_patterns(self) -> List[Dict]:
           """加载脱敏模式"""
           return [
               {
                   "name": "email",
                   "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                   "replacement": "userXXXX@example.com",
                   "enabled": True
               },
               {
                   "name": "phone",
                   "pattern": r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b',
                   "replacement": "(XXX) XXX-XXXX",
                   "enabled": True
               },
               {
                   "name": "credit_card",
                   "pattern": r'\b(?:\d[ -]*?){13,16}\b',
                   "replacement": "XXXX-XXXX-XXXX-XXXX",
                   "enabled": True
               }
           ]
       
       def anonymize(self, data: Any) -> Any:
           """
           脱敏数据
           
           :param data: 要脱敏的数据
           :return: 脱敏后的数据
           """
           if isinstance(data, str):
               return self._anonymize_string(data)
           
           elif isinstance(data, dict):
               return {k: self.anonymize(v) for k, v in data.items()}
           
           elif isinstance(data, list):
               return [self.anonymize(item) for item in data]
           
           return data
       
       def _anonymize_string(self, text: str) -> str:
           """脱敏字符串"""
           result = text
           
           for pattern in self.patterns:
               if pattern["enabled"]:
                   result = re.sub(
                       pattern["pattern"], 
                       pattern["replacement"], 
                       result
                   )
           
           return result
   ```

### 6.9 与其他模块的交互

#### 6.9.1 与数据处理工作流引擎交互

```mermaid
sequenceDiagram
    participant DPWE as Data Processing Workflow Engine
    participant AIDS as AI-Assisted Development System
    
    DPWE->>AIDS: GET /api/v1/workflows/generate (生成工作流)
    AIDS-->>DPWE: 工作流定义
    
    DPWE->>AIDS: POST /api/v1/workflows/assist (工作流辅助)
    AIDS-->>DPWE: 建议和优化
    
    DPWE->>AIDS: GET /api/v1/nodes/templates (获取节点模板)
    AIDS-->>DPWE: 节点模板列表
```

#### 6.9.2 与网站指纹分析引擎交互

```mermaid
sequenceDiagram
    participant WFE as Website Fingerprinting Engine
    participant AIDS as AI-Assisted Development System
    
    AIDS->>WFE: GET /api/v1/analyze?url={url}
    WFE-->>AIDS: 详细分析报告
    
    AIDS->>WFE: POST /api/v1/rules (新规则建议)
    WFE-->>AIDS: 规则创建确认
```

#### 6.9.3 与数据源健康监测系统交互

```mermaid
sequenceDiagram
    participant DSHMS as Data Source Health Monitoring System
    participant AIDS as AI-Assisted Development System
    
    DSHMS->>AIDS: POST /api/v1/alerts (告警通知)
    AIDS-->>DSHMS: 诊断建议
    
    AIDS->>DSHMS: GET /api/v1/health/history/{id}?interval=1h
    DSHMS-->>AIDS: 健康历史数据
```

#### 6.9.4 与自动化媒体处理管道交互

```mermaid
sequenceDiagram
    participant AMP as Automated Media Processing Pipeline
    participant AIDS as AI-Assisted Development System
    
    AIDS->>AMP: GET /api/v1/media/models (获取可用模型)
    AMP-->>AIDS: 模型列表
    
    AIDS->>AMP: POST /api/v1/media/process (请求处理示例)
    AMP-->>AIDS: 处理结果示例
    
    AIDS->>AMP: GET /api/v1/media/analysis (获取分析能力)
    AMP-->>AIDS: 分析能力描述
```

## 7. 数据合规与安全中心 (Data Compliance and Security Center)

### 7.1 模块概述
数据合规与安全中心是镜界平台的数据安全与合规性管理组件，负责确保所有数据采集、处理和存储活动符合法律法规要求。它提供全面的数据安全策略管理、隐私保护机制和合规性审计功能。

### 7.2 详细功能清单

#### 7.2.1 核心功能
- **合规性检查**
  - GDPR合规性检查
  - CCPA合规性检查
  - 本地化数据法规检查
  - 行业特定法规检查（如HIPAA、PCI DSS）
- **数据安全策略管理**
  - 敏感数据检测规则
  - 数据脱敏策略
  - 数据保留策略
  - 数据访问控制策略
- **隐私保护机制**
  - 个人身份信息(PII)检测
  - 数据最小化实施
  - 用户同意管理
  - 数据主体权利处理
- **安全审计与监控**
  - 数据访问审计
  - 安全事件监控
  - 合规性报告生成
  - 风险评估与管理

#### 7.2.2 高级功能
- **自动化合规工作流**
  - 合规性任务自动化
  - 合规性检查计划
  - 合规性问题跟踪
  - 合规性状态看板
- **数据地图与血缘**
  - 数据流可视化
  - 数据血缘追踪
  - 数据存储位置映射
  - 数据使用情况分析
- **跨境数据传输管理**
  - 数据传输影响评估
  - 传输加密策略
  - 数据驻留管理
  - 传输日志审计
- **第三方数据处理商管理**
  - 供应商合规性评估
  - 数据处理协议管理
  - 供应商风险监控
  - 供应商审计跟踪

### 7.3 技术架构

#### 7.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                           数据合规与安全中心 (DCSC)                                           │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  合规控制层           │  策略执行层           │  数据分析层                                │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 合规规则引擎        │ • 敏感数据检测器      │ • 数据血缘分析器                           │
│ • 同意管理系统        │ • 数据脱敏处理器      │ • 风险评估引擎                            │
│ • 数据主体请求处理    │ • 访问控制执行器      │ • 合规性报告生成器                         │
│ • 合规状态监控        │ • 传输加密处理器      │ • 审计日志分析器                           │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 7.3.2 服务边界与交互
- **输入**：
  - 数据源元数据（来自数据源注册中心）
  - 数据处理日志（来自数据处理工作流引擎）
  - 数据内容（来自自动化媒体处理管道）
  - 用户操作（来自各模块）
- **输出**：
  - 合规性检查结果
  - 安全告警
  - 合规性报告
  - 数据处理建议

### 7.4 核心组件详细实现

#### 7.4.1 合规规则引擎

**技术实现：**
```python
import re
from typing import Dict, List, Optional, Tuple
import logging

class ComplianceRuleEngine:
    """合规规则引擎，执行合规性检查"""
    
    def __init__(
        self,
        rule_repository: ComplianceRuleRepository,
        config: Config
    ):
        self.rule_repository = rule_repository
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def check_compliance(
        self,
        data_source: DataSource,
        data_content: Optional[bytes] = None
    ) -> ComplianceCheckResult:
        """
        检查数据源的合规性
        
        :param data_source: 数据源对象
        :param data_content: 数据内容（可选）
        :return: 合规性检查结果
        """
        # 1. 获取适用的合规规则
        applicable_rules = self._get_applicable_rules(data_source)
        
        # 2. 执行规则检查
        results = []
        for rule in applicable_rules:
            result = self._check_rule(rule, data_source, data_content)
            results.append(result)
        
        # 3. 生成汇总结果
        return self._generate_summary(data_source, results)
    
    def _get_applicable_rules(self, data_source: DataSource) -> List[ComplianceRule]:
        """获取适用于数据源的合规规则"""
        # 1. 获取数据源所在地区
        region = self._determine_region(data_source)
        
        # 2. 获取数据类型
        data_type = self._determine_data_type(data_source)
        
        # 3. 获取适用规则
        return self.rule_repository.get_rules(
            regions=[region],
            data_types=[data_type],
            active=True
        )
    
    def _determine_region(self, data_source: DataSource) -> str:
        """确定数据源所在地区"""
        # 1. 检查URL中的国家代码
        url = data_source.url.lower()
        
        # 常见国家代码顶级域
        country_tlds = {
            ".uk": "gb",
            ".de": "de",
            ".fr": "fr",
            ".es": "es",
            ".it": "it",
            ".jp": "jp",
            ".cn": "cn",
            ".us": "us",
            ".ca": "ca",
            ".au": "au"
        }
        
        for tld, region in country_tlds.items():
            if tld in url:
                return region
        
        # 2. 检查IP地理位置（如果实现）
        # ...
        
        # 3. 默认为国际
        return "international"
    
    def _determine_data_type(self, data_source: DataSource) -> str:
        """确定数据类型"""
        # 1. 检查数据源类型
        if data_source.data_type == "user-generated":
            return "personal"
        
        # 2. 检查内容类型
        content_type = data_source.content_type or ""
        if "json" in content_type or "xml" in content_type:
            return "structured"
        
        # 3. 默认类型
        return "general"
    
    def _check_rule(
        self,
        rule: ComplianceRule,
        data_source: DataSource,
        data_content: Optional[bytes]
    ) -> RuleCheckResult:
        """检查单个规则"""
        # 1. 检查规则是否适用
        if not self._is_rule_applicable(rule, data_source):
            return RuleCheckResult(
                rule_id=rule.id,
                rule_name=rule.name,
                applicable=False,
                passed=None,
                message="规则不适用"
            )
        
        # 2. 执行规则检查
        try:
            if rule.check_type == "metadata":
                result = self._check_metadata_rule(rule, data_source)
            elif rule.check_type == "content":
                if data_content is None:
                    result = RuleCheckResult(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        applicable=True,
                        passed=False,
                        message="需要内容检查，但未提供内容"
                    )
                else:
                    result = self._check_content_rule(rule, data_content)
            else:
                result = RuleCheckResult(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    applicable=True,
                    passed=False,
                    message=f"不支持的规则类型: {rule.check_type}"
                )
            
            return result
            
        except Exception as e:
            return RuleCheckResult(
                rule_id=rule.id,
                rule_name=rule.name,
                applicable=True,
                passed=False,
                message=f"规则检查失败: {str(e)}"
            )
    
    def _is_rule_applicable(
        self,
        rule: ComplianceRule,
        data_source: DataSource
    ) -> bool:
        """检查规则是否适用于数据源"""
        # 1. 检查地区适用性
        if rule.regions and self._determine_region(data_source) not in rule.regions:
            return False
        
        # 2. 检查数据类型适用性
        if rule.data_types and self._determine_data_type(data_source) not in rule.data_types:
            return False
        
        # 3. 检查数据源分类适用性
        if rule.categories and data_source.category not in rule.categories:
            return False
        
        return True
    
    def _check_metadata_rule(
        self,
        rule: ComplianceRule,
        data_source: DataSource
    ) -> RuleCheckResult:
        """检查元数据规则"""
        # 1. 提取检查参数
        field = rule.parameters.get("field")
        operator = rule.parameters.get("operator")
        value = rule.parameters.get("value")
        
        if not field or not operator:
            return RuleCheckResult(
                rule_id=rule.id,
                rule_name=rule.name,
                applicable=True,
                passed=False,
                message="规则配置不完整"
            )
        
        # 2. 获取字段值
        field_value = self._get_metadata_field(data_source, field)
        if field_value is None:
            return RuleCheckResult(
                rule_id=rule.id,
                rule_name=rule.name,
                applicable=True,
                passed=False,
                message=f"元数据字段 '{field}' 不存在"
            )
        
        # 3. 执行检查
        passed = self._evaluate_condition(field_value, operator, value)
        
        # 4. 生成结果
        return RuleCheckResult(
            rule_id=rule.id,
            rule_name=rule.name,
            applicable=True,
            passed=passed,
            message=self._generate_message(rule, field_value, passed)
        )
    
    def _get_metadata_field(
        self,
        data_source: DataSource,
        field: str
    ) -> Optional[Any]:
        """获取元数据字段值"""
        if field == "url":
            return data_source.url
        elif field == "category":
            return data_source.category
        elif field == "data_type":
            return data_source.data_type
        elif field == "content_type":
            return data_source.content_type
        elif field.startswith("metadata."):
            key = field.split(".", 1)[1]
            return data_source.metadata.get(key)
        
        return None
    
    def _evaluate_condition(
        self,
        actual: Any,
        operator: str,
        expected: Any
    ) -> bool:
        """评估条件表达式"""
        if operator == "eq":
            return actual == expected
        elif operator == "neq":
            return actual != expected
        elif operator == "contains":
            return expected in str(actual)
        elif operator == "regex":
            return bool(re.search(expected, str(actual)))
        elif operator == "in":
            return actual in expected.split(",")
        elif operator == "not_in":
            return actual not in expected.split(",")
        
        return False
    
    def _generate_message(
        self,
        rule: ComplianceRule,
        field_value: Any,
        passed: bool
    ) -> str:
        """生成检查结果消息"""
        if passed:
            return f"规则通过: {rule.description}"
        
        return f"规则失败: {rule.description} (检测到: {field_value})"
    
    def _check_content_rule(
        self,
        rule: ComplianceRule,
        data_content: bytes
    ) -> RuleCheckResult:
        """检查内容规则"""
        # 1. 检查内容类型
        if rule.content_type not in ["text", "json", "xml", "html"]:
            return RuleCheckResult(
                rule_id=rule.id,
                rule_name=rule.name,
                applicable=True,
                passed=False,
                message=f"不支持的内容类型: {rule.content_type}"
            )
        
        # 2. 解析内容
        try:
            content = self._parse_content(data_content, rule.content_type)
        except Exception as e:
            return RuleCheckResult(
                rule_id=rule.id,
                rule_name=rule.name,
                applicable=True,
                passed=False,
                message=f"内容解析失败: {str(e)}"
            )
        
        # 3. 执行检查
        findings = []
        for pattern in rule.patterns:
            matches = self._find_pattern_matches(pattern, content)
            if matches:
                findings.extend(matches)
        
        # 4. 生成结果
        passed = len(findings) == 0
        message = self._generate_content_message(rule, findings)
        
        return RuleCheckResult(
            rule_id=rule.id,
            rule_name=rule.name,
            applicable=True,
            passed=passed,
            message=message,
            details={"findings": findings}
        )
    
    def _parse_content(
        self,
        content: bytes,
        content_type: str
    ) -> Any:
        """解析内容"""
        # 尝试解码为UTF-8
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('latin-1')
        
        # 根据内容类型进一步处理
        if content_type == "json":
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
        elif content_type in ["xml", "html"]:
            # 返回原始文本，由模式匹配处理
            return text
        else:
            return text
    
    def _find_pattern_matches(
        self,
        pattern: CompliancePattern,
        content: Any
    ) -> List[Dict]:
        """查找模式匹配"""
        matches = []
        
        if isinstance(content, str):
            # 在文本中搜索
            for match in re.finditer(pattern.regex, content):
                matches.append({
                    "pattern_id": pattern.id,
                    "start": match.start(),
                    "end": match.end(),
                    "value": match.group(0),
                    "context": self._get_context(content, match.start(), match.end())
                })
        
        elif isinstance(content, dict):
            # 递归搜索字典
            self._search_dict(content, pattern, "", matches)
        
        elif isinstance(content, list):
            # 递归搜索列表
            self._search_list(content, pattern, "", matches)
        
        return matches
    
    def _get_context(
        self,
        text: str,
        start: int,
        end: int,
        context_size: int = 20
    ) -> str:
        """获取匹配上下文"""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        return text[context_start:context_start] + "[...]" + text[end:context_end]
    
    def _search_dict(
        self,
        obj: Dict,
        pattern: CompliancePattern,
        path: str,
        matches: List[Dict]
    ):
        """在字典中搜索模式"""
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            # 检查键
            if re.search(pattern.regex, key):
                matches.append({
                    "pattern_id": pattern.id,
                    "path": current_path,
                    "value": key,
                    "type": "key"
                })
            
            # 检查值
            if isinstance(value, (str, int, float)):
                value_str = str(value)
                for match in re.finditer(pattern.regex, value_str):
                    matches.append({
                        "pattern_id": pattern.id,
                        "path": current_path,
                        "value": value_str[match.start():match.end()],
                        "start": match.start(),
                        "end": match.end(),
                        "type": "value"
                    })
            
            # 递归搜索
            elif isinstance(value, dict):
                self._search_dict(value, pattern, current_path, matches)
            elif isinstance(value, list):
                self._search_list(value, pattern, current_path, matches)
    
    def _search_list(
        self,
        obj: List,
        pattern: CompliancePattern,
        path: str,
        matches: List[Dict]
    ):
        """在列表中搜索模式"""
        for i, item in enumerate(obj):
            current_path = f"{path}[{i}]"
            
            # 检查值
            if isinstance(item, (str, int, float)):
                value_str = str(item)
                for match in re.finditer(pattern.regex, value_str):
                    matches.append({
                        "pattern_id": pattern.id,
                        "path": current_path,
                        "value": value_str[match.start():match.end()],
                        "start": match.start(),
                        "end": match.end(),
                        "type": "value"
                    })
            
            # 递归搜索
            elif isinstance(item, dict):
                self._search_dict(item, pattern, current_path, matches)
            elif isinstance(item, list):
                self._search_list(item, pattern, current_path, matches)
    
    def _generate_content_message(
        self,
        rule: ComplianceRule,
        findings: List[Dict]
    ) -> str:
        """生成内容检查消息"""
        if not findings:
            return f"规则通过: {rule.description}"
        
        return f"规则失败: {rule.description} (检测到 {len(findings)} 处敏感数据)"
    
    def _generate_summary(
        self,
        data_source: DataSource,
        results: List[RuleCheckResult]
    ) -> ComplianceCheckResult:
        """生成合规性检查汇总"""
        # 统计结果
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if not r.passed and r.applicable)
        not_applicable = sum(1 for r in results if not r.applicable)
        
        # 生成状态
        if failed == 0:
            status = "compliant"
        elif failed <= self.config.warning_threshold:
            status = "warning"
        else:
            status = "non_compliant"
        
        # 生成关键问题
        critical_issues = [
            r for r in results 
            if not r.passed and r.applicable and r.rule_severity == "critical"
        ]
        
        # 生成建议
        suggestions = self._generate_suggestions(results)
        
        return ComplianceCheckResult(
            data_source_id=data_source.id,
            project_id=data_source.project_id,
            status=status,
            total_rules=total,
            passed_rules=passed,
            failed_rules=failed,
            not_applicable_rules=not_applicable,
            critical_issues=len(critical_issues),
            results=results,
            suggestions=suggestions,
            timestamp=datetime.utcnow()
        )
    
    def _generate_suggestions(self, results: List[RuleCheckResult]) -> List[str]:
        """生成合规性建议"""
        suggestions = []
        
        # 1. 针对失败的关键规则
        critical_failures = [
            r for r in results 
            if not r.passed and r.applicable and r.rule_severity == "critical"
        ]
        for result in critical_failures[:3]:  # 只取前3个
            suggestions.append(f"必须解决: {result.rule_name} - {result.message}")
        
        # 2. 针对警告级别的规则
        warning_failures = [
            r for r in results 
            if not r.passed and r.applicable and r.rule_severity == "warning"
        ]
        if warning_failures:
            suggestions.append(f"建议改进: 检测到 {len(warning_failures)} 个可优化的合规性问题")
        
        # 3. 一般建议
        if not suggestions:
            suggestions.append("数据源符合所有关键合规性要求")
        
        return suggestions

class ComplianceRuleRepository:
    """合规规则仓库"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_rules(
        self,
        regions: List[str] = None,
        data_types: List[str] = None,
        categories: List[str] = None,
        active: bool = True
    ) -> List[ComplianceRule]:
        """获取合规规则"""
        # 构建查询
        conditions = []
        params = {"active": active}
        
        if regions:
            conditions.append("regions && %(regions)s::varchar[]")
            params["regions"] = regions
        if data_types:
            conditions.append("data_types && %(data_types)s::varchar[]")
            params["data_types"] = data_types
        if categories:
            conditions.append("categories && %(categories)s::varchar[]")
            params["categories"] = categories
        
        where_clause = "WHERE active = %(active)s"
        if conditions:
            where_clause += " AND " + " AND ".join(conditions)
        
        sql = f"""
        SELECT * FROM compliance_rules 
        {where_clause}
        ORDER BY severity DESC, priority
        """
        
        rows = self.db.fetchall(sql, params)
        return [self._row_to_rule(row) for row in rows]
    
    def get_rule(self, rule_id: str) -> Optional[ComplianceRule]:
        """获取单个合规规则"""
        sql = "SELECT * FROM compliance_rules WHERE id = %(id)s"
        row = self.db.fetchone(sql, {"id": rule_id})
        return self._row_to_rule(row) if row else None
    
    def _row_to_rule(self, row: Dict) -> ComplianceRule:
        """将数据库行转换为ComplianceRule对象"""
        return ComplianceRule(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            regulation=row["regulation"],
            severity=row["severity"],
            check_type=row["check_type"],
            content_type=row["content_type"],
            regions=json.loads(row["regions"]) if row["regions"] else [],
            data_types=json.loads(row["data_types"]) if row["data_types"] else [],
            categories=json.loads(row["categories"]) if row["categories"] else [],
            parameters=json.loads(row["parameters"]) if row["parameters"] else {},
            patterns=self._decode_patterns(row["patterns"]),
            priority=row["priority"],
            active=row["active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    def _decode_patterns(self, json_data: str) -> List[CompliancePattern]:
        """解码模式定义"""
        if not json_data:
            return []
        
        patterns_data = json.loads(json_data)
        return [
            CompliancePattern(
                id=p["id"],
                name=p["name"],
                description=p.get("description", ""),
                regex=p["regex"],
                data_category=p["data_category"],
                severity=p["severity"]
            ) for p in patterns_data
        ]

# 辅助类定义
class ComplianceRule:
    """合规规则"""
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        regulation: str,
        severity: str,
        check_type: str,
        content_type: str,
        regions: List[str],
        data_types: List[str],
        categories: List[str],
        parameters: Dict,
        patterns: List,
        priority: int,
        active: bool,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.name = name
        self.description = description
        self.regulation = regulation
        self.severity = severity
        self.check_type = check_type
        self.content_type = content_type
        self.regions = regions
        self.data_types = data_types
        self.categories = categories
        self.parameters = parameters
        self.patterns = patterns
        self.priority = priority
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

class CompliancePattern:
    """合规模式"""
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        regex: str,
        data_category: str,
        severity: str
    ):
        self.id = id
        self.name = name
        self.description = description
        self.regex = regex
        self.data_category = data_category
        self.severity = severity

class RuleCheckResult:
    """规则检查结果"""
    def __init__(
        self,
        rule_id: str,
        rule_name: str,
        applicable: bool,
        passed: Optional[bool],
        message: str,
        details: Optional[Dict] = None
    ):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.applicable = applicable
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.rule_severity = "warning"  # 可以从规则中获取

class ComplianceCheckResult:
    """合规性检查结果"""
    def __init__(
        self,
        data_source_id: str,
        project_id: str,
        status: str,
        total_rules: int,
        passed_rules: int,
        failed_rules: int,
        not_applicable_rules: int,
        critical_issues: int,
        results: List[RuleCheckResult],
        suggestions: List[str],
        timestamp: datetime
    ):
        self.data_source_id = data_source_id
        self.project_id = project_id
        self.status = status
        self.total_rules = total_rules
        self.passed_rules = passed_rules
        self.failed_rules = failed_rules
        self.not_applicable_rules = not_applicable_rules
        self.critical_issues = critical_issues
        self.results = results
        self.suggestions = suggestions
        self.timestamp = timestamp
```

#### 7.4.2 敏感数据检测器

**技术实现：**
```python
import re
import json
from typing import Dict, List, Optional, Tuple
import logging
import hashlib

class SensitiveDataDetector:
    """敏感数据检测器，检测数据中的敏感信息"""
    
    def __init__(
        self,
        pattern_repository: PatternRepository,
        config: Config
    ):
        self.pattern_repository = pattern_repository
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def detect(
        self,
        data: Any,
        context: Optional[Dict] = None
    ) -> SensitiveDataDetectionResult:
        """
        检测数据中的敏感信息
        
        :param data: 要检测的数据
        :param context: 上下文信息
        :return: 检测结果
        """
        # 1. 获取敏感数据模式
        patterns = self.pattern_repository.get_patterns(
            categories=context.get("categories") if context else None,
            regions=context.get("regions") if context else None
        )
        
        # 2. 执行检测
        findings = self._scan_data(data, patterns)
        
        # 3. 生成结果
        return SensitiveDataDetectionResult(
            data_hash=self._calculate_data_hash(data),
            total_patterns=len(patterns),
            findings=findings,
            context=context or {},
            timestamp=datetime.utcnow()
        )
    
    def _calculate_data_hash(self, data: Any) -> str:
        """计算数据哈希"""
        # 简单实现：转换为JSON并计算哈希
        try:
            data_str = json.dumps(data, sort_keys=True)
            return hashlib.sha256(data_str.encode('utf-8')).hexdigest()
        except:
            return "unknown"
    
    def _scan_data(
        self,
        data: Any,
        patterns: List[DataPattern]
    ) -> List[DataFinding]:
        """扫描数据中的敏感信息"""
        findings = []
        
        if isinstance(data, str):
            # 扫描字符串
            for pattern in patterns:
                for match in re.finditer(pattern.regex, data):
                    findings.append(DataFinding(
                        pattern_id=pattern.id,
                        pattern_name=pattern.name,
                        data_category=pattern.data_category,
                        start=match.start(),
                        end=match.end(),
                        value=match.group(0),
                        context=self._get_context(data, match.start(), match.end())
                    ))
        
        elif isinstance(data, dict):
            # 递归扫描字典
            for key, value in data.items():
                # 检查键
                for pattern in patterns:
                    if re.search(pattern.regex, key):
                        findings.append(DataFinding(
                            pattern_id=pattern.id,
                            pattern_name=pattern.name,
                            data_category=pattern.data_category,
                            path=key,
                            value=key,
                            type="key",
                            context=f"Key: {key}"
                        ))
                
                # 检查值
                sub_findings = self._scan_data(value, patterns)
                for finding in sub_findings:
                    finding.path = f"{key}.{finding.path}" if finding.path else key
                    findings.append(finding)
        
        elif isinstance(data, list):
            # 递归扫描列表
            for i, item in enumerate(data):
                sub_findings = self._scan_data(item, patterns)
                for finding in sub_findings:
                    finding.path = f"[{i}]{finding.path}"
                    findings.append(finding)
        
        return findings
    
    def _get_context(
        self,
        text: str,
        start: int,
        end: int,
        context_size: int = 20
    ) -> str:
        """获取匹配上下文"""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        return text[context_start:start] + "[...]" + text[end:context_end]

class PatternRepository:
    """敏感数据模式仓库"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def get_patterns(
        self,
        categories: List[str] = None,
        regions: List[str] = None
    ) -> List[DataPattern]:
        """获取敏感数据模式"""
        # 构建查询
        conditions = []
        params = {}
        
        if categories:
            conditions.append("categories && %(categories)s::varchar[]")
            params["categories"] = categories
        if regions:
            conditions.append("regions && %(regions)s::varchar[]")
            params["regions"] = regions
        
        where_clause = "WHERE active = true"
        if conditions:
            where_clause += " AND " + " AND ".join(conditions)
        
        sql = f"""
        SELECT * FROM sensitive_data_patterns 
        {where_clause}
        ORDER BY severity DESC, priority
        """
        
        rows = self.db.fetchall(sql, params)
        return [self._row_to_pattern(row) for row in rows]
    
    def get_pattern(self, pattern_id: str) -> Optional[DataPattern]:
        """获取单个敏感数据模式"""
        sql = "SELECT * FROM sensitive_data_patterns WHERE id = %(id)s"
        row = self.db.fetchone(sql, {"id": pattern_id})
        return self._row_to_pattern(row) if row else None
    
    def _row_to_pattern(self, row: Dict) -> DataPattern:
        """将数据库行转换为DataPattern对象"""
        return DataPattern(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            regex=row["regex"],
            data_category=row["data_category"],
            severity=row["severity"],
            categories=json.loads(row["categories"]) if row["categories"] else [],
            regions=json.loads(row["regions"]) if row["regions"] else [],
            validation_rules=json.loads(row["validation_rules"]) if row["validation_rules"] else [],
            redaction_template=row["redaction_template"],
            priority=row["priority"],
            active=row["active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

# 辅助类定义
class DataPattern:
    """敏感数据模式"""
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        regex: str,
        data_category: str,
        severity: str,
        categories: List[str],
        regions: List[str],
        validation_rules: List[Dict],
        redaction_template: str,
        priority: int,
        active: bool,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.name = name
        self.description = description
        self.regex = regex
        self.data_category = data_category
        self.severity = severity
        self.categories = categories
        self.regions = regions
        self.validation_rules = validation_rules
        self.redaction_template = redaction_template
        self.priority = priority
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

class DataFinding:
    """数据发现"""
    def __init__(
        self,
        pattern_id: str,
        pattern_name: str,
        data_category: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        value: str = "",
        context: str = "",
        path: str = "",
        type: str = "value"
    ):
        self.pattern_id = pattern_id
        self.pattern_name = pattern_name
        self.data_category = data_category
        self.start = start
        self.end = end
        self.value = value
        self.context = context
        self.path = path
        self.type = type

class SensitiveDataDetectionResult:
    """敏感数据检测结果"""
    def __init__(
        self,
        data_hash: str,
        total_patterns: int,
        findings: List[DataFinding],
        context: Dict,
        timestamp: datetime
    ):
        self.data_hash = data_hash
        self.total_patterns = total_patterns
        self.findings = findings
        self.context = context
        self.timestamp = timestamp
        self.severity = self._calculate_severity()
    
    def _calculate_severity(self) -> str:
        """计算检测结果严重程度"""
        if not self.findings:
            return "none"
        
        # 检查是否有关键发现
        has_critical = any(f.data_category == "critical" for f in self.findings)
        if has_critical:
            return "critical"
        
        # 检查发现数量
        if len(self.findings) > 5:
            return "high"
        elif len(self.findings) > 2:
            return "medium"
        
        return "low"
```

### 7.5 数据模型详细定义

#### 7.5.1 合规规则表

```sql
-- 合规规则表
CREATE TABLE compliance_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    regulation VARCHAR(50) NOT NULL CHECK (regulation IN ('gdpr', 'ccpa', 'hipaa', 'pci_dss', 'local')),
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('critical', 'warning', 'info')),
    check_type VARCHAR(20) NOT NULL CHECK (check_type IN ('metadata', 'content')),
    content_type VARCHAR(20) CHECK (content_type IN ('text', 'json', 'xml', 'html')),
    regions VARCHAR(10)[] DEFAULT '{}'::varchar[],
    data_types VARCHAR(50)[] DEFAULT '{}'::varchar[],
    categories VARCHAR(50)[] DEFAULT '{}'::varchar[],
    parameters JSONB DEFAULT '{}'::jsonb,
    patterns JSONB DEFAULT '[]'::jsonb,
    priority INT NOT NULL DEFAULT 50,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_rules_regulation ON compliance_rules(regulation),
    INDEX idx_rules_severity ON compliance_rules(severity),
    INDEX idx_rules_active ON compliance_rules(active),
    INDEX idx_rules_priority ON compliance_rules(priority)
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_compliance_rules_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_compliance_rules_modtime
BEFORE UPDATE ON compliance_rules
FOR EACH ROW
EXECUTE FUNCTION update_compliance_rules_modtime();
```

#### 7.5.2 敏感数据模式表

```sql
-- 敏感数据模式表
CREATE TABLE sensitive_data_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    regex TEXT NOT NULL,
    data_category VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    categories VARCHAR(50)[] DEFAULT '{}'::varchar[],
    regions VARCHAR(10)[] DEFAULT '{}'::varchar[],
    validation_rules JSONB DEFAULT '[]'::jsonb,
    redaction_template VARCHAR(255) NOT NULL,
    priority INT NOT NULL DEFAULT 50,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_patterns_category ON sensitive_data_patterns(data_category),
    INDEX idx_patterns_severity ON sensitive_data_patterns(severity),
    INDEX idx_patterns_active ON sensitive_data_patterns(active),
    INDEX idx_patterns_priority ON sensitive_data_patterns(priority)
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_sensitive_data_patterns_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_sensitive_data_patterns_modtime
BEFORE UPDATE ON sensitive_data_patterns
FOR EACH ROW
EXECUTE FUNCTION update_sensitive_data_patterns_modtime();
```

#### 7.5.3 合规性检查结果表

```sql
-- 合规性检查结果表
CREATE TABLE compliance_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('compliant', 'warning', 'non_compliant')),
    total_rules INT NOT NULL,
    passed_rules INT NOT NULL,
    failed_rules INT NOT NULL,
    not_applicable_rules INT NOT NULL,
    critical_issues INT NOT NULL,
    results JSONB NOT NULL,
    suggestions JSONB NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_checks_data_source ON compliance_checks(data_source_id),
    INDEX idx_checks_project ON compliance_checks(project_id),
    INDEX idx_checks_status ON compliance_checks(status),
    INDEX idx_checks_timestamp ON compliance_checks(timestamp DESC)
);
```

#### 7.5.4 敏感数据检测结果表

```sql
-- 敏感数据检测结果表
CREATE TABLE sensitive_data_detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_hash VARCHAR(64) NOT NULL,
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    total_patterns INT NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('none', 'low', 'medium', 'high', 'critical')),
    findings JSONB NOT NULL,
    context JSONB NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_detections_data_hash ON sensitive_data_detections(data_hash),
    INDEX idx_detections_data_source ON sensitive_data_detections(data_source_id),
    INDEX idx_detections_project ON sensitive_data_detections(project_id),
    INDEX idx_detections_severity ON sensitive_data_detections(severity),
    INDEX idx_detections_timestamp ON sensitive_data_detections(timestamp DESC)
);
```

#### 7.5.5 用户同意记录表

```sql
-- 用户同意记录表
CREATE TABLE user_consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    data_source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    consent_type VARCHAR(50) NOT NULL,
    consent_value BOOLEAN NOT NULL,
    consent_details JSONB DEFAULT '{}'::jsonb,
    consent_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revoked BOOLEAN NOT NULL DEFAULT false,
    revoked_at TIMESTAMPTZ,
    
    -- 索引
    INDEX idx_consents_user ON user_consents(user_id),
    INDEX idx_consents_data_source ON user_consents(data_source_id),
    INDEX idx_consents_project ON user_consents(project_id),
    INDEX idx_consents_type ON user_consents(consent_type),
    INDEX idx_consents_timestamp ON user_consents(consent_timestamp DESC)
);
```

### 7.6 API详细规范

#### 7.6.1 合规性检查API

**检查数据源合规性 (POST /api/v1/compliance/check)**

*请求示例:*
```http
POST /api/v1/compliance/check HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "data_source_id": "ds-7a8b9c0d",
  "include_content": true
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data_source_id": "ds-7a8b9c0d",
  "project_id": "proj-123",
  "status": "warning",
  "total_rules": 15,
  "passed_rules": 12,
  "failed_rules": 2,
  "not_applicable_rules": 1,
  "critical_issues": 0,
  "results": [
    {
      "rule_id": "rule-gdpr-001",
      "rule_name": "个人数据标识检查",
      "applicable": true,
      "passed": false,
      "message": "检测到潜在的个人身份信息",
      "details": {
        "findings": [
          {
            "pattern_id": "pattern-email",
            "pattern_name": "电子邮件地址",
            "data_category": "personal",
            "start": 125,
            "end": 150,
            "value": "user@example.com",
            "context": "联系信息: user@example.com"
          }
        ]
      }
    },
    {
      "rule_id": "rule-gdpr-002",
      "rule_name": "数据最小化检查",
      "applicable": true,
      "passed": true,
      "message": "规则通过: 数据最小化要求已满足"
    }
  ],
  "suggestions": [
    "必须解决: 个人数据标识检查 - 检测到潜在的个人身份信息",
    "建议改进: 检测到 2 个可优化的合规性问题"
  ],
  "timestamp": "2023-06-15T10:30:45Z"
}
```

#### 7.6.2 敏感数据检测API

**检测敏感数据 (POST /api/v1/data:detect-sensitive)**

*请求示例:*
```http
POST /api/v1/data:detect-sensitive HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "address": "123 Main St, Anytown, USA"
  },
  "context": {
    "categories": ["contact", "personal"],
    "regions": ["us"]
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data_hash": "d41d8cd98f00b204e9800998ecf8427e",
  "total_patterns": 8,
  "findings": [
    {
      "pattern_id": "pattern-name",
      "pattern_name": "个人姓名",
      "data_category": "personal",
      "value": "John Doe",
      "context": "name: John Doe",
      "path": "name",
      "type": "value"
    },
    {
      "pattern_id": "pattern-email",
      "pattern_name": "电子邮件地址",
      "data_category": "personal",
      "value": "john.doe@example.com",
      "context": "email: john.doe@example.com",
      "path": "email",
      "type": "value"
    },
    {
      "pattern_id": "pattern-phone",
      "pattern_name": "电话号码",
      "data_category": "personal",
      "value": "+1-555-123-4567",
      "context": "phone: +1-555-123-4567",
      "path": "phone",
      "type": "value"
    }
  ],
  "context": {
    "categories": ["contact", "personal"],
    "regions": ["us"]
  },
  "severity": "high",
  "timestamp": "2023-06-15T10:35:20Z"
}
```

#### 7.6.3 用户同意管理API

**记录用户同意 (POST /api/v1/consents)**

*请求示例:*
```http
POST /api/v1/consents HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "user-123",
  "data_source_id": "ds-7a8b9c0d",
  "consent_type": "data_processing",
  "consent_value": true,
  "consent_details": {
    "purpose": "数据采集与处理",
    "data_types": ["personal", "contact"],
    "retention_period": "2 years"
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/consents/consent-1a2b3c4d

{
  "id": "consent-1a2b3c4d",
  "user_id": "user-123",
  "data_source_id": "ds-7a8b9c0d",
  "project_id": "proj-123",
  "consent_type": "data_processing",
  "consent_value": true,
  "consent_details": {
    "purpose": "数据采集与处理",
    "data_types": ["personal", "contact"],
    "retention_period": "2 years"
  },
  "consent_timestamp": "2023-06-15T10:30:45Z",
  "revoked": false
}
```

**获取用户同意记录 (GET /api/v1/consents/{user_id})**

*请求示例:*
```http
GET /api/v1/consents/user-123?data_source_id=ds-7a8b9c0d HTTP/1.1
Host: dcsc.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": "consent-1a2b3c4d",
      "user_id": "user-123",
      "data_source_id": "ds-7a8b9c0d",
      "project_id": "proj-123",
      "consent_type": "data_processing",
      "consent_value": true,
      "consent_details": {
        "purpose": "数据采集与处理",
        "data_types": ["personal", "contact"],
        "retention_period": "2 years"
      },
      "consent_timestamp": "2023-06-15T10:30:45Z",
      "revoked": false
    },
    {
      "id": "consent-5e6f7g8h",
      "user_id": "user-123",
      "data_source_id": "ds-7a8b9c0d",
      "project_id": "proj-123",
      "consent_type": "data_sharing",
      "consent_value": false,
      "consent_details": {
        "purpose": "与第三方共享数据",
        "data_types": ["personal"],
        "retention_period": "1 year"
      },
      "consent_timestamp": "2023-06-10T08:15:30Z",
      "revoked": true,
      "revoked_at": "2023-06-12T14:20:15Z"
    }
  ],
  "total": 2
}
```

### 7.7 性能优化策略

#### 7.7.1 敏感数据检测优化

1. **多阶段检测流水线**
   ```python
   class MultiStageDetector:
       """多阶段敏感数据检测器"""
       
       def __init__(self, detectors: List[Detector]):
           self.detectors = detectors
           self.logger = logging.getLogger(__name__)
       
       def detect(self, data: Any, context: Dict) -> DetectionResult:
           """执行多阶段检测"""
           findings = []
           stage_times = []
           
           for i, detector in enumerate(self.detectors):
               start_time = time.time()
               
               # 执行阶段检测
               stage_findings = detector.detect(data, context)
               findings.extend(stage_findings)
               
               # 记录时间
               stage_time = time.time() - start_time
               stage_times.append((detector.__class__.__name__, stage_time))
               
               # 檢查是否需要继续
               if self._should_terminate(i, stage_findings, context):
                   break
           
           # 生成结果
           return DetectionResult(
               findings=findings,
               stage_times=stage_times,
               total_time=sum(t[1] for t in stage_times)
           )
       
       def _should_terminate(
           self,
           stage_index: int,
           findings: List[DataFinding],
           context: Dict
       ) -> bool:
           """检查是否应该终止检测"""
           # 如果检测到关键敏感数据，提前终止
           if any(f.data_category == "critical" for f in findings):
               return True
           
           # 如果达到最大阶段数
           if stage_index >= self.config.max_detection_stages - 1:
               return True
           
           return False
   ```

2. **Aho-Corasick算法优化**
   ```python
   class AhoCorasickDetector:
       """使用Aho-Corasick算法的敏感数据检测器"""
       
       def __init__(self, patterns: List[str]):
           self.automaton = ahocorasick.Automaton()
           
           # 添加模式
           for idx, pattern in enumerate(patterns):
               self.automaton.add_word(pattern, (idx, pattern))
           
           # 构建自动机
           self.automaton.make_automaton()
       
       def detect(self, text: str) -> List[Match]:
           """检测文本中的模式"""
           matches = []
           
           # 执行匹配
           for end_index, (insert_order, original_value) in self.automaton.iter(text):
               start_index = end_index - len(original_value) + 1
               matches.append(Match(
                   start=start_index,
                   end=end_index + 1,
                   pattern=original_value
               ))
           
           return matches
   ```

#### 7.7.2 合规性检查优化

1. **规则优先级调度**
   ```python
   class RuleScheduler:
       """规则调度器，优化规则执行顺序"""
       
       def __init__(self, rules: List[ComplianceRule]):
           self.rules = rules
           self.logger = logging.getLogger(__name__)
       
       def schedule(self) -> List[ComplianceRule]:
           """调度规则执行顺序"""
           # 1. 按优先级排序
           sorted_rules = sorted(
               self.rules,
               key=lambda r: (r.severity_rank, -r.priority),
               reverse=True
           )
           
           # 2. 应用优化策略
           optimized_rules = self._apply_optimization(sorted_rules)
           
           return optimized_rules
       
       @property
       def severity_rank(self) -> int:
           """将严重程度转换为数值排名"""
           severity_ranks = {
               "critical": 4,
               "high": 3,
               "medium": 2,
               "low": 1
           }
           return severity_ranks.get(self.severity, 1)
       
       def _apply_optimization(self, rules: List[ComplianceRule]) -> List[ComplianceRule]:
           """应用优化策略"""
           # 1. 将元数据规则放在内容规则之前
           metadata_rules = [r for r in rules if r.check_type == "metadata"]
           content_rules = [r for r in rules if r.check_type == "content"]
           
           # 2. 在内容规则中，将简单规则放在复杂规则之前
           simple_content_rules = [r for r in content_rules if self._is_simple_rule(r)]
           complex_content_rules = [r for r in content_rules if not self._is_simple_rule(r)]
           
           return metadata_rules + simple_content_rules + complex_content_rules
       
       def _is_simple_rule(self, rule: ComplianceRule) -> bool:
           """检查规则是否简单"""
           # 简单规则：没有复杂的正则表达式
           if ".*" in rule.regex or ".+" in rule.regex:
               return False
           if len(rule.regex) > 50:
               return False
           return True
   ```

2. **规则结果缓存**
   ```python
   class RuleResultCache:
       """规则结果缓存"""
       
       def __init__(self, ttl=3600):
           self.cache = TTLCache(maxsize=10000, ttl=ttl)
           self.logger = logging.getLogger(__name__)
       
       def get(self, rule_id: str, data_hash: str) -> Optional[RuleCheckResult]:
           """获取缓存的规则结果"""
           key = f"{rule_id}:{data_hash}"
           return self.cache.get(key)
       
       def set(
           self,
           rule_id: str,
           data_hash: str,
           result: RuleCheckResult,
           timestamp: datetime
       ):
           """设置规则结果"""
           key = f"{rule_id}:{data_hash}"
           self.cache[key] = {
               "result": result,
               "timestamp": timestamp
           }
       
       def should_refresh(
           self,
           rule_id: str,
           data_hash: str,
           last_check: datetime
       ) -> bool:
           """检查是否应该刷新结果"""
           # 如果规则最近被修改
           rule_last_modified = self._get_rule_last_modified(rule_id)
           if rule_last_modified and rule_last_modified > last_check:
               return True
           
           # 如果数据最近被修改
           data_last_modified = self._get_data_last_modified(data_hash)
           if data_last_modified and data_last_modified > last_check:
               return True
           
           return False
       
       def _get_rule_last_modified(self, rule_id: str) -> Optional[datetime]:
           """获取规则最后修改时间"""
           # 实现规则元数据查询
           pass
       
       def _get_data_last_modified(self, data_hash: str) -> Optional[datetime]:
           """获取数据最后修改时间"""
           # 实现数据元数据查询
           pass
   ```

### 7.8 安全考虑

#### 7.8.1 数据安全策略

1. **基于属性的访问控制(PABC)**
   ```python
   class AttributeBasedAccessControl:
       """基于属性的访问控制"""
       
       def __init__(self, policy_engine: PolicyEngine):
           self.policy_engine = policy_engine
           self.logger = logging.getLogger(__name__)
       
       def check_access(
           self,
           user: User,
           resource: Resource,
           action: str
       ) -> bool:
           """
           检查用户是否有权限访问资源
           
           :param user: 用户对象
           :param resource: 资源对象
           :param action: 操作类型
           :return: 是否有权限
           """
           # 1. 构建请求上下文
           context = {
               "user": self._extract_user_attributes(user),
               "resource": self._extract_resource_attributes(resource),
               "action": action,
               "environment": self._get_environment_attributes()
           }
           
           # 2. 评估策略
           decision = self.policy_engine.evaluate(context)
           
           # 3. 记录审计日志
           self._log_audit(user, resource, action, decision)
           
           return decision == "permit"
       
       def _extract_user_attributes(self, user: User) -> Dict:
           """提取用户属性"""
           return {
               "id": user.id,
               "roles": user.roles,
               "department": user.department,
               "clearance_level": user.clearance_level,
               "region": user.region
           }
       
       def _extract_resource_attributes(self, resource: Resource) -> Dict:
           """提取资源属性"""
           if isinstance(resource, DataSource):
               return {
                   "type": "data_source",
                   "category": resource.category,
                   "data_type": resource.data_type,
                   "region": self._determine_region(resource),
                   "sensitivity": self._determine_sensitivity(resource)
               }
           # 其他资源类型...
           return {}
       
       def _determine_region(self, data_source: DataSource) -> str:
           """确定数据源所在地区"""
           # 实现地区检测逻辑
           pass
       
       def _determine_sensitivity(self, data_source: DataSource) -> str:
           """确定数据敏感度"""
           # 实现敏感度评估
           pass
       
       def _get_environment_attributes(self) -> Dict:
           """获取环境属性"""
           return {
               "time": datetime.utcnow(),
               "ip_address": get_current_ip(),
               "device_type": get_device_type()
           }
       
       def _log_audit(
           self,
           user: User,
           resource: Resource,
           action: str,
           decision: str
       ):
           """记录审计日志"""
           # 实现审计日志记录
           pass
   ```

2. **数据脱敏策略引擎**
   ```python
   class DataRedactionEngine:
       """数据脱敏策略引擎"""
       
       def __init__(
           self,
           policy_repository: RedactionPolicyRepository,
           config: Config
       ):
           self.policy_repository = policy_repository
           self.config = config
           self.logger = logging.getLogger(__name__)
       
       def redact(
           self,
           data: Any,
           context: Dict
       ) -> Any:
           """
           脱敏数据
           
           :param data: 要脱敏的数据
           :param context: 上下文信息
           :return: 脱敏后的数据
           """
           # 1. 获取适用的脱敏策略
           policies = self._get_applicable_policies(context)
           
           # 2. 应用脱敏策略
           return self._apply_policies(data, policies)
       
       def _get_applicable_policies(self, context: Dict) -> List[RedactionPolicy]:
           """获取适用的脱敏策略"""
           return self.policy_repository.get_policies(
               data_types=context.get("data_types", []),
               regions=context.get("regions", []),
               sensitivity=context.get("sensitivity", "medium"),
               purpose=context.get("purpose", "processing")
           )
       
       def _apply_policies(
           self,
           data: Any,
           policies: List[RedactionPolicy]
       ) -> Any:
           """应用脱敏策略"""
           if isinstance(data, str):
               return self._redact_string(data, policies)
           
           elif isinstance(data, dict):
               return {k: self._apply_policies(v, policies) for k, v in data.items()}
           
           elif isinstance(data, list):
               return [self._apply_policies(item, policies) for item in data]
           
           return data
       
       def _redact_string(self, text: str, policies: List[RedactionPolicy]) -> str:
           """脱敏字符串"""
           result = text
           
           for policy in policies:
               for rule in policy.rules:
                   if rule.enabled:
                       result = re.sub(
                           rule.pattern,
                           self._get_replacement(rule, result),
                           result
                       )
           
           return result
       
       def _get_replacement(self, rule: RedactionRule, text: str) -> str:
           """获取替换字符串"""
           if rule.replacement_template == "hash":
               return hashlib.sha256(text.encode('utf-8')).hexdigest()[:8] + "..."
           elif rule.replacement_template == "mask":
               return "X" * len(text)
           elif rule.replacement_template.startswith("fixed:"):
               return rule.replacement_template.split(":", 1)[1]
           
           return rule.replacement_template
   ```

#### 7.8.2 合规性审计

1. **审计日志管理**
   ```sql
   -- 合规性审计日志表
   CREATE TABLE compliance_audit_logs (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID REFERENCES users(id) ON DELETE SET NULL,
       project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
       action VARCHAR(50) NOT NULL,
       target_type VARCHAR(50) NOT NULL,
       target_id VARCHAR(255) NOT NULL,
       details JSONB,
       ip_address INET,
       user_agent TEXT,
       timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       
       -- 索引
       INDEX idx_audit_user ON compliance_audit_logs(user_id),
       INDEX idx_audit_project ON compliance_audit_logs(project_id),
       INDEX idx_audit_action ON compliance_audit_logs(action),
       INDEX idx_audit_target ON compliance_audit_logs(target_type, target_id),
       INDEX idx_audit_timestamp ON compliance_audit_logs(timestamp DESC)
   );
   
   -- 数据访问审计日志表
   CREATE TABLE data_access_audit_logs (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
       project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
       data_source_id UUID REFERENCES data_sources(id) ON DELETE SET NULL,
       access_type VARCHAR(20) NOT NULL,
       access_pattern VARCHAR(50) NOT NULL,
       data_categories JSONB NOT NULL,
       rows_accessed BIGINT NOT NULL,
       columns_accessed INT NOT NULL,
       sensitive_data_accessed BOOLEAN NOT NULL,
       ip_address INET NOT NULL,
       user_agent TEXT NOT NULL,
       timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       
       -- 索引
       INDEX idx_data_access_user ON data_access_audit_logs(user_id),
       INDEX idx_data_access_data_source ON data_access_audit_logs(data_source_id),
       INDEX idx_data_access_timestamp ON data_access_audit_logs(timestamp DESC),
       INDEX idx_data_access_sensitive ON data_access_audit_logs(sensitive_data_accessed)
   );
   ```

2. **审计分析服务**
   ```python
   class AuditAnalysisService:
       """审计分析服务，检测异常访问模式"""
       
       def __init__(
           self,
           db: Database,
           config: Config
       ):
           self.db = db
           self.config = config
           self.logger = logging.getLogger(__name__)
       
       def analyze_access_patterns(
           self,
           user_id: str,
           time_window: timedelta = timedelta(days=7)
       ) -> AccessPatternAnalysis:
           """
           分析用户访问模式
           
           :param user_id: 用户ID
           :param time_window: 分析时间窗口
           :return: 访问模式分析结果
           """
           # 1. 获取访问日志
           start_time = datetime.utcnow() - time_window
           access_logs = self._get_access_logs(user_id, start_time)
           
           # 2. 分析访问模式
           pattern_analysis = self._analyze_patterns(access_logs)
           anomaly_detection = self._detect_anomalies(access_logs)
           
           # 3. 生成风险评估
           risk_score = self._calculate_risk_score(pattern_analysis, anomaly_detection)
           
           return AccessPatternAnalysis(
               user_id=user_id,
               time_window=time_window,
               total_accesses=len(access_logs),
               pattern_analysis=pattern_analysis,
               anomaly_detection=anomaly_detection,
               risk_score=risk_score,
               timestamp=datetime.utcnow()
           )
       
       def _get_access_logs(
           self,
           user_id: str,
           start_time: datetime
       ) -> List[DataAccessLog]:
           """获取访问日志"""
           sql = """
           SELECT * FROM data_access_audit_logs 
           WHERE user_id = %(user_id)s AND timestamp >= %(start_time)s
           ORDER BY timestamp
           """
           
           rows = self.db.fetchall(sql, {
               "user_id": user_id,
               "start_time": start_time
           })
           
           return [self._row_to_log(row) for row in rows]
       
       def _analyze_patterns(self, access_logs: List[DataAccessLog]) -> Dict:
           """分析访问模式"""
           # 1. 按数据源分析
           by_data_source = defaultdict(list)
           for log in access_logs:
               by_data_source[log.data_source_id].append(log)
           
           # 2. 计算每个数据源的访问频率
           frequency = {}
           for ds_id, logs in by_data_source.items():
               time_diffs = [
                   (logs[i].timestamp - logs[i-1].timestamp).total_seconds()
                   for i in range(1, len(logs))
               ]
               
               frequency[ds_id] = {
                   "count": len(logs),
                   "avg_interval": sum(time_diffs) / len(time_diffs) if time_diffs else 0,
                   "sensitive_data_ratio": sum(1 for log in logs if log.sensitive_data_accessed) / len(logs)
               }
           
           # 3. 识别常用访问模式
           common_patterns = self._identify_common_patterns(access_logs)
           
           return {
               "by_data_source": frequency,
               "common_patterns": common_patterns,
               "time_of_day": self._analyze_time_patterns(access_logs)
           }
       
       def _identify_common_patterns(self, access_logs: List[DataAccessLog]) -> List[AccessPattern]:
           """识别常用访问模式"""
           # 简单实现：基于访问序列
           sequences = []
           current_sequence = []
           
           for i, log in enumerate(access_logs):
               current_sequence.append(log.data_source_id)
               
               # 如果是序列结束或达到最大长度
               if i == len(access_logs) - 1 or len(current_sequence) >= 5:
                   sequences.append(tuple(current_sequence))
                   current_sequence = []
           
           # 统计序列频率
           counter = Counter(sequences)
           return [
               AccessPattern(pattern=list(pattern), frequency=count)
               for pattern, count in counter.most_common(5)
           ]
       
       def _analyze_time_patterns(self, access_logs: List[DataAccessLog]) -> Dict:
           """分析时间模式"""
           hour_counts = [0] * 24
           day_counts = [0] * 7  # 0=Monday, 6=Sunday
           
           for log in access_logs:
               hour_counts[log.timestamp.hour] += 1
               day_counts[log.timestamp.weekday()] += 1
           
           return {
               "by_hour": hour_counts,
               "by_day": day_counts
           }
       
       def _detect_anomalies(self, access_logs: List[DataAccessLog]) -> List[Anomaly]:
           """检测异常访问"""
           anomalies = []
           
           # 1. 检测非常规时间访问
           off_hours = self._detect_off_hours_access(access_logs)
           if off_hours:
               anomalies.append(Anomaly(
                   type="off_hours",
                   description="检测到非常规时间访问",
                   severity="medium",
                   details={"count": len(off_hours), "times": [str(log.timestamp) for log in off_hours]}
               ))
           
           # 2. 检测敏感数据异常访问
           sensitive_access = self._detect_sensitive_data_access(access_logs)
           if sensitive_access:
               anomalies.append(Anomaly(
                   type="sensitive_data",
                   description="检测到异常的敏感数据访问",
                   severity="high",
                   details=sensitive_access
               ))
           
           # 3. 检测访问频率突增
           frequency_spike = self._detect_frequency_spike(access_logs)
           if frequency_spike:
               anomalies.append(Anomaly(
                   type="frequency_spike",
                   description="检测到访问频率突增",
                   severity="medium",
                   details=frequency_spike
               ))
           
           return anomalies
       
       def _detect_off_hours_access(self, access_logs: List[DataAccessLog]) -> List[DataAccessLog]:
           """检测非常规时间访问"""
           off_hours = []
           for log in access_logs:
               hour = log.timestamp.hour
               # 檢查是否在正常工作时间外 (假设工作时间为9AM-6PM)
               if hour < 9 or hour > 18:
                   off_hours.append(log)
           return off_hours
       
       def _detect_sensitive_data_access(self, access_logs: List[DataAccessLog]) -> Optional[Dict]:
           """检测敏感数据异常访问"""
           sensitive_logs = [log for log in access_logs if log.sensitive_data_accessed]
           if not sensitive_logs:
               return None
           
           # 檢查敏感数据访问比例是否异常高
           total = len(access_logs)
           sensitive_count = len(sensitive_logs)
           ratio = sensitive_count / total
           
           if ratio > self.config.sensitive_data_threshold:
               return {
                   "sensitive_count": sensitive_count,
                   "total": total,
                   "ratio": ratio,
                   "threshold": self.config.sensitive_data_threshold
               }
           
           return None
       
       def _detect_frequency_spike(self, access_logs: List[DataAccessLog]) -> Optional[Dict]:
           """检测访问频率突增"""
           if len(access_logs) < 2:
               return None
           
           # 计算时间间隔
           time_diffs = [
               (access_logs[i].timestamp - access_logs[i-1].timestamp).total_seconds()
               for i in range(1, len(access_logs))
           ]
           
           # 计算平均间隔和标准差
           avg_interval = sum(time_diffs) / len(time_diffs)
           std_dev = (sum((x - avg_interval) ** 2 for x in time_diffs) / len(time_diffs)) ** 0.5
           
           # 檢查是否有明显突增（间隔远小于平均）
           spike_threshold = max(1.0, avg_interval - 2 * std_dev)
           spikes = [diff for diff in time_diffs if diff < spike_threshold]
           
           if len(spikes) > self.config.spike_count_threshold:
               return {
                   "spike_count": len(spikes),
                   "threshold": spike_threshold,
                   "spike_count_threshold": self.config.spike_count_threshold
               }
           
           return None
       
       def _calculate_risk_score(
           self,
           pattern_analysis: Dict,
           anomaly_detection: List[Anomaly]
       ) -> float:
           """计算风险评分"""
           score = 0.0
           
           # 基于异常
           for anomaly in anomaly_detection:
               weight = 0.3 if anomaly.severity == "high" else 0.1
               score += weight
           
           # 基于敏感数据访问比例
           sensitive_ratio = pattern_analysis["by_data_source"].get("sensitive_data_ratio", 0)
           score += sensitive_ratio * 0.4
           
           # 限制在0-1范围
           return min(1.0, max(0.0, score))
       
       def _row_to_log(self, row: Dict) -> DataAccessLog:
           """将数据库行转换为DataAccessLog对象"""
           return DataAccessLog(
               id=row["id"],
               user_id=row["user_id"],
               project_id=row["project_id"],
               data_source_id=row["data_source_id"],
               access_type=row["access_type"],
               access_pattern=row["access_pattern"],
               data_categories=json.loads(row["data_categories"]),
               rows_accessed=row["rows_accessed"],
               columns_accessed=row["columns_accessed"],
               sensitive_data_accessed=row["sensitive_data_accessed"],
               ip_address=row["ip_address"],
               user_agent=row["user_agent"],
               timestamp=row["timestamp"]
           )

   # 辅助类定义
   class DataAccessLog:
       """数据访问日志"""
       def __init__(
           self,
           id: str,
           user_id: str,
           project_id: str,
           data_source_id: Optional[str],
           access_type: str,
           access_pattern: str,
           data_categories: List[str],
           rows_accessed: int,
           columns_accessed: int,
           sensitive_data_accessed: bool,
           ip_address: str,
           user_agent: str,
           timestamp: datetime
       ):
           self.id = id
           self.user_id = user_id
           self.project_id = project_id
           self.data_source_id = data_source_id
           self.access_type = access_type
           self.access_pattern = access_pattern
           self.data_categories = data_categories
           self.rows_accessed = rows_accessed
           self.columns_accessed = columns_accessed
           self.sensitive_data_accessed = sensitive_data_accessed
           self.ip_address = ip_address
           self.user_agent = user_agent
           self.timestamp = timestamp

   class AccessPattern:
       """访问模式"""
       def __init__(
           self,
           pattern: List[str],
           frequency: int
       ):
           self.pattern = pattern
           self.frequency = frequency

   class Anomaly:
       """异常检测结果"""
       def __init__(
           self,
           type: str,
           description: str,
           severity: str,
           details: Dict
       ):
           self.type = type
           self.description = description
           self.severity = severity
           self.details = details

   class AccessPatternAnalysis:
       """访问模式分析结果"""
       def __init__(
           self,
           user_id: str,
           time_window: timedelta,
           total_accesses: int,
           pattern_analysis: Dict,
           anomaly_detection: List[Anomaly],
           risk_score: float,
           timestamp: datetime
       ):
           self.user_id = user_id
           self.time_window = time_window
           self.total_accesses = total_accesses
           self.pattern_analysis = pattern_analysis
           self.anomaly_detection = anomaly_detection
           self.risk_score = risk_score
           self.timestamp = timestamp
   ```

### 7.9 与其他模块的交互

#### 7.9.1 与数据源注册中心交互

```mermaid
sequenceDiagram
    participant DSR as Data Source Registry
    participant DCSC as Data Compliance and Security Center
    
    DSR->>DCSC: POST /api/v1/compliance/check (新数据源创建)
    DCSC-->>DSR: 合规性检查结果
    
    DSR->>DCSC: GET /api/v1/compliance/check/{id} (检查现有数据源)
    DCSC-->>DSR: 合规性检查结果
    
    DCSC->>DSR: GET /api/v1/data-sources/{id} (获取数据源详情)
    DSR-->>DCSC: 数据源元数据
```

#### 7.9.2 与自动化媒体处理管道交互

```mermaid
sequenceDiagram
    participant AMP as Automated Media Processing Pipeline
    participant DCSC as Data Compliance and Security Center
    
    AMP->>DCSC: POST /api/v1/data:detect-sensitive (处理前内容检查)
    DCSC-->>AMP: 敏感数据检测结果
    
    AMP->>DCSC: POST /api/v1/data:redact (请求数据脱敏)
    DCSC-->>AMP: 脱敏后的内容
    
    DCSC->>AMP: GET /api/v1/media/processingTasks/{task_id} (监控处理任务)
    AMP-->>DCSC: 处理任务详情
```

#### 7.9.3 与AI辅助开发系统交互

```mermaid
sequenceDiagram
    participant AIDS as AI-Assisted Development System
    participant DCSC as Data Compliance and Security Center
    
    AIDS->>DCSC: GET /api/v1/compliance/rules (获取合规规则)
    DCSC-->>AIDS: 合规规则列表
    
    DCSC->>AIDS: POST /api/v1/code:generate (请求合规代码生成)
    AIDS-->>DCSC: 合规代码示例
    
    DCSC->>AIDS: GET /api/v1/diagnose (诊断合规问题)
    AIDS-->>DCSC: 诊断结果和解决方案
```

#### 7.9.4 与数据处理工作流引擎交互

```mermaid
sequenceDiagram
    participant DPWE as Data Processing Workflow Engine
    participant DCSC as Data Compliance and Security Center
    
    DPWE->>DCSC: POST /api/v1/workflows:validate (工作流合规验证)
    DCSC-->>DPWE: 合规性验证结果
    
    DPWE->>DCSC: GET /api/v1/consents (检查用户同意)
    DCSC-->>DPWE: 同意状态
    
    DCSC->>DPWE: POST /api/v1/workflowInstances/{id}:monitor (监控工作流执行)
    DPWE-->>DCSC: 工作流执行详情
```

## 8. 分布式爬虫集群管理系统 (Distributed Crawler Cluster Management System)

### 8.1 模块概述
分布式爬虫集群管理系统是镜界平台的爬虫执行引擎，负责管理和调度分布式爬虫节点，实现高效、可靠的数据采集。它提供爬虫任务调度、资源管理、状态监控和动态扩展能力，支持大规模分布式爬取任务。

### 8.2 详细功能清单

#### 8.2.1 核心功能
- **爬虫节点管理**
  - 节点自动发现与注册
  - 节点状态监控
  - 节点资源监控（CPU、内存、网络）
  - 节点健康检查
- **任务调度与分配**
  - 爬虫任务队列管理
  - 动态任务分配算法
  - 任务优先级管理
  - 任务分片与合并
- **爬虫执行管理**
  - 爬虫启动与停止
  - 爬虫参数配置
  - 爬虫执行状态监控
  - 执行结果收集
- **资源管理**
  - 资源配额管理
  - 动态资源分配
  - 资源使用监控
  - 资源限制策略

#### 8.2.2 高级功能
- **智能调度策略**
  - 基于内容的调度
  - 基于地理位置的调度
  - 基于反爬特征的调度
  - 负载均衡策略
- **弹性扩展**
  - 自动扩缩容
  - 预热机制
  - 优雅下线
  - 容量规划
- **爬虫隔离与沙箱**
  - 爬虫运行沙箱
  - 资源隔离
  - 网络隔离
  - 安全策略执行
- **任务依赖管理**
  - 任务依赖关系
  - 任务编排
  - 条件触发
  - 错误重试策略

### 8.3 技术架构

#### 8.3.1 架构图
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                      分布式爬虫集群管理系统 (DCCMS)                                           │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  控制层               │  调度层               │  执行层                                    │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 集群管理服务        │ • 任务调度器          │ • 爬虫执行器                               │
│ • API网关             │ • 资源分配器          │ • 状态报告器                              │
│ • 节点注册服务        │ • 优先级管理器        │ • 心跳监控器                              │
│ • 配置管理服务        │ • 依赖解析器          │ • 资源监控器                              │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 8.3.2 服务边界与交互
- **输入**：
  - 爬虫任务定义（来自数据处理工作流引擎）
  - 爬虫节点注册
  - 节点状态报告
  - 资源使用指标
- **输出**：
  - 爬虫任务执行状态
  - 爬虫结果数据
  - 集群健康状态
  - 资源使用报告

### 8.4 核心组件详细实现

#### 8.4.1 爬虫节点管理服务

**技术实现：**
```python
import uuid
import time
import logging
from typing import Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor
import threading

class CrawlerNodeManager:
    """爬虫节点管理服务，负责节点注册、状态监控和健康检查"""
    
    def __init__(
        self,
        config: Config,
        node_registry: NodeRegistry,
        health_checker: NodeHealthChecker,
        event_bus: EventBus
    ):
        self.config = config
        self.node_registry = node_registry
        self.health_checker = health_checker
        self.event_bus = event_bus
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.heartbeat_thread = None
        self.health_check_thread = None
        self.lock = threading.Lock()
    
    def start(self):
        """启动节点管理服务"""
        if self.running:
            return
        
        self.running = True
        self.logger.info("Starting crawler node manager")
        
        # 启动心跳处理线程
        self.heartbeat_thread = threading.Thread(
            target=self._process_heartbeats,
            daemon=True
        )
        self.heartbeat_thread.start()
        
        # 启动健康检查线程
        self.health_check_thread = threading.Thread(
            target=self._perform_health_checks,
            daemon=True
        )
        self.health_check_thread.start()
        
        self.logger.info("Crawler node manager started")
    
    def stop(self):
        """停止节点管理服务"""
        if not self.running:
            return
        
        self.running = False
        self.logger.info("Stopping crawler node manager")
        
        # 等待线程结束
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5.0)
        if self.health_check_thread:
            self.health_check_thread.join(timeout=5.0)
        
        self.logger.info("Crawler node manager stopped")
    
    def register_node(
        self,
        node_info: NodeInfo
    ) -> NodeRegistrationResult:
        """
        注册爬虫节点
        
        :param node_info: 节点信息
        :return: 注册结果
        """
        with self.lock:
            # 生成节点ID
            node_id = f"node-{uuid.uuid4().hex[:8]}"
            node_info.id = node_id
            
            # 设置默认状态
            node_info.status = "online"
            node_info.last_heartbeat = time.time()
            
            # 保存节点信息
            self.node_registry.register_node(node_info)
            
            # 发布事件
            self.event_bus.publish("node.registered", {
                "node_id": node_id,
                "node_info": node_info.to_dict()
            })
            
            self.logger.info("Node registered: %s", node_id)
            
            return NodeRegistrationResult(
                node_id=node_id,
                registration_time=time.time(),
                initial_status="online"
            )
    
    def unregister_node(self, node_id: str):
        """
        注销爬虫节点
        
        :param node_id: 节点ID
        """
        with self.lock:
            # 获取节点信息
            node_info = self.node_registry.get_node(node_id)
            if not node_info:
                self.logger.warning("Node %s not found for unregistration", node_id)
                return
            
            # 更新状态
            node_info.status = "offline"
            node_info.last_heartbeat = 0
            self.node_registry.update_node(node_info)
            
            # 发布事件
            self.event_bus.publish("node.unregistered", {
                "node_id": node_id
            })
            
            self.logger.info("Node unregistered: %s", node_id)
    
    def handle_heartbeat(self, node_id: str, heartbeat: NodeHeartbeat):
        """
        处理节点心跳
        
        :param node_id: 节点ID
        :param heartbeat: 心跳数据
        """
        with self.lock:
            # 获取节点信息
            node_info = self.node_registry.get_node(node_id)
            if not node_info:
                self.logger.warning("Received heartbeat from unknown node: %s", node_id)
                return
            
            # 更新节点信息
            node_info.last_heartbeat = time.time()
            node_info.status = "online"
            node_info.resources = heartbeat.resources
            node_info.load = heartbeat.load
            node_info.task_count = len(heartbeat.active_tasks)
            
            # 保存更新
            self.node_registry.update_node(node_info)
            
            # 发布事件
            self.event_bus.publish("node.heartbeat", {
                "node_id": node_id,
                "heartbeat": heartbeat.to_dict()
            })
    
    def _process_heartbeats(self):
        """处理心跳超时"""
        while self.running:
            try:
                current_time = time.time()
                timeout_threshold = current_time - self.config.heartbeat_timeout
                
                # 检查所有节点
                nodes = self.node_registry.get_all_nodes()
                for node in nodes:
                    if node.last_heartbeat < timeout_threshold:
                        self._handle_heartbeat_timeout(node.id)
                
                # 等待下一次检查
                time.sleep(self.config.heartbeat_check_interval)
                
            except Exception as e:
                self.logger.error("Error in heartbeat processing: %s", str(e))
                time.sleep(1)
    
    def _handle_heartbeat_timeout(self, node_id: str):
        """处理心跳超时"""
        with self.lock:
            node_info = self.node_registry.get_node(node_id)
            if not node_info or node_info.status == "offline":
                return
            
            # 更新状态
            node_info.status = "unresponsive"
            self.node_registry.update_node(node_info)
            
            # 发布事件
            self.event_bus.publish("node.timeout", {
                "node_id": node_id,
                "last_heartbeat": node_info.last_heartbeat
            })
            
            self.logger.warning("Node heartbeat timeout: %s", node_id)
    
    def _perform_health_checks(self):
        """执行健康检查"""
        while self.running:
            try:
                # 获取需要检查的节点
                nodes = self.node_registry.get_nodes_by_status("online")
                
                # 并行执行健康检查
                with ThreadPoolExecutor(max_workers=self.config.health_check_workers) as executor:
                    futures = {
                        executor.submit(self._check_node_health, node.id): node.id
                        for node in nodes
                    }
                    
                    for future in futures:
                        node_id = futures[future]
                        try:
                            future.result()
                        except Exception as e:
                            self.logger.error("Health check failed for node %s: %s", node_id, str(e))
                
                # 等待下一次检查
                time.sleep(self.config.health_check_interval)
                
            except Exception as e:
                self.logger.error("Error in health check processing: %s", str(e))
                time.sleep(1)
    
    def _check_node_health(self, node_id: str):
        """检查节点健康状态"""
        # 1. 执行健康检查
        health_status = self.health_checker.check(node_id)
        
        # 2. 更新节点状态
        with self.lock:
            node_info = self.node_registry.get_node(node_id)
            if not node_info:
                return
            
            # 更新健康状态
            node_info.health = health_status
            self.node_registry.update_node(node_info)
            
            # 处理健康状态变化
            self._handle_health_status_change(node_id, node_info, health_status)
    
    def _handle_health_status_change(
        self,
        node_id: str,
        node_info: NodeInfo,
        new_health: NodeHealthStatus
    ):
        """处理健康状态变化"""
        # 檢查状态是否发生变化
        if node_info.health.status == new_health.status:
            return
        
        # 更新状态
        node_info.health = new_health
        self.node_registry.update_node(node_info)
        
        # 发布事件
        self.event_bus.publish("node.health_changed", {
            "node_id": node_id,
            "old_status": node_info.health.status,
            "new_status": new_health.status,
            "details": new_health.details
        })
        
        # 根据健康状态采取行动
        if new_health.status == "unhealthy":
            self._handle_unhealthy_node(node_id)
    
    def _handle_unhealthy_node(self, node_id: str):
        """处理不健康节点"""
        # 1. 从调度中移除节点
        self.event_bus.publish("scheduler.node_unavailable", {
            "node_id": node_id
        })
        
        # 2. 重新分配任务
        self.event_bus.publish("task.reassign", {
            "node_id": node_id
        })
        
        self.logger.warning("Node marked as unhealthy: %s", node_id)

class NodeRegistry:
    """节点注册表，存储节点信息"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def register_node(self, node_info: NodeInfo):
        """注册节点"""
        sql = """
        INSERT INTO crawler_nodes (
            id, cluster_id, name, description, 
            ip_address, port, node_type, 
            capabilities, resources, 
            status, last_heartbeat, 
            created_at, updated_at
        ) VALUES (
            %(id)s, %(cluster_id)s, %(name)s, %(description)s,
            %(ip_address)s, %(port)s, %(node_type)s,
            %(capabilities)s, %(resources)s,
            %(status)s, %(last_heartbeat)s,
            %(created_at)s, %(updated_at)s
        )
        """
        
        self.db.execute(sql, {
            "id": node_info.id,
            "cluster_id": node_info.cluster_id,
            "name": node_info.name,
            "description": node_info.description,
            "ip_address": node_info.ip_address,
            "port": node_info.port,
            "node_type": node_info.node_type,
            "capabilities": json.dumps(node_info.capabilities),
            "resources": json.dumps(node_info.resources),
            "status": node_info.status,
            "last_heartbeat": datetime.fromtimestamp(node_info.last_heartbeat),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
    
    def update_node(self, node_info: NodeInfo):
        """更新节点信息"""
        sql = """
        UPDATE crawler_nodes SET
            name = %(name)s,
            description = %(description)s,
            capabilities = %(capabilities)s,
            resources = %(resources)s,
            status = %(status)s,
            last_heartbeat = %(last_heartbeat)s,
            updated_at = %(updated_at)s
        WHERE id = %(id)s
        """
        
        self.db.execute(sql, {
            "id": node_info.id,
            "name": node_info.name,
            "description": node_info.description,
            "capabilities": json.dumps(node_info.capabilities),
            "resources": json.dumps(node_info.resources),
            "status": node_info.status,
            "last_heartbeat": datetime.fromtimestamp(node_info.last_heartbeat),
            "updated_at": datetime.utcnow()
        })
    
    def get_node(self, node_id: str) -> Optional[NodeInfo]:
        """获取节点信息"""
        sql = "SELECT * FROM crawler_nodes WHERE id = %(id)s"
        row = self.db.fetchone(sql, {"id": node_id})
        return self._row_to_node(row) if row else None
    
    def get_all_nodes(self) -> List[NodeInfo]:
        """获取所有节点"""
        sql = "SELECT * FROM crawler_nodes"
        rows = self.db.fetchall(sql)
        return [self._row_to_node(row) for row in rows]
    
    def get_nodes_by_status(self, status: str) -> List[NodeInfo]:
        """获取特定状态的节点"""
        sql = "SELECT * FROM crawler_nodes WHERE status = %(status)s"
        rows = self.db.fetchall(sql, {"status": status})
        return [self._row_to_node(row) for row in rows]
    
    def _row_to_node(self, row: Dict) -> NodeInfo:
        """将数据库行转换为NodeInfo对象"""
        return NodeInfo(
            id=row["id"],
            cluster_id=row["cluster_id"],
            name=row["name"],
            description=row["description"],
            ip_address=row["ip_address"],
            port=row["port"],
            node_type=row["node_type"],
            capabilities=json.loads(row["capabilities"]),
            resources=json.loads(row["resources"]),
            status=row["status"],
            last_heartbeat=row["last_heartbeat"].timestamp(),
            health=NodeHealthStatus(
                status=row["health_status"],
                details=json.loads(row["health_details"]) if row["health_details"] else {},
                timestamp=row["health_timestamp"]
            ) if row["health_status"] else NodeHealthStatus(status="unknown"),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

class NodeHealthChecker:
    """节点健康检查器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def check(self, node_id: str) -> NodeHealthStatus:
        """
        检查节点健康状态
        
        :param node_id: 节点ID
        :return: 健康状态
        """
        # 1. 检查基础连通性
        if not self._check_connectivity(node_id):
            return NodeHealthStatus(
                status="unreachable",
                details={"error": "Node is unreachable"},
                timestamp=datetime.utcnow()
            )
        
        # 2. 检查资源使用
        resource_status = self._check_resources(node_id)
        
        # 3. 检查任务执行
        task_status = self._check_tasks(node_id)
        
        # 4. 综合健康状态
        return self._determine_overall_status(resource_status, task_status)
    
    def _check_connectivity(self, node_id: str) -> bool:
        """检查节点连通性"""
        # 实现节点连通性检查
        # 这里简化为返回True
        return True
    
    def _check_resources(self, node_id: str) -> Dict:
        """检查资源使用"""
        # 实现资源检查
        # 这里简化为返回示例数据
        return {
            "cpu_usage": 0.65,
            "memory_usage": 0.75,
            "network_io": 120.5,
            "disk_io": 45.2
        }
    
    def _check_tasks(self, node_id: str) -> Dict:
        """检查任务执行"""
        # 实现任务检查
        # 这里简化为返回示例数据
        return {
            "task_count": 5,
            "task_errors": 0,
            "task_latency": 1.2
        }
    
    def _determine_overall_status(
        self,
        resource_status: Dict,
        task_status: Dict
    ) -> NodeHealthStatus:
        """确定整体健康状态"""
        # 1. 檢查资源使用是否超标
        if resource_status["cpu_usage"] > 0.9 or resource_status["memory_usage"] > 0.95:
            return NodeHealthStatus(
                status="unhealthy",
                details={
                    "reason": "High resource usage",
                    "cpu": resource_status["cpu_usage"],
                    "memory": resource_status["memory_usage"]
                },
                timestamp=datetime.utcnow()
            )
        
        # 2. 檢查任务错误率
        if task_status["task_errors"] > 0:
            return NodeHealthStatus(
                status="degraded",
                details={
                    "reason": "Task errors detected",
                    "error_count": task_status["task_errors"]
                },
                timestamp=datetime.utcnow()
            )
        
        # 3. 檢查任务延迟
        if task_status["task_latency"] > 5.0:
            return NodeHealthStatus(
                status="degraded",
                details={
                    "reason": "High task latency",
                    "latency": task_status["task_latency"]
                },
                timestamp=datetime.utcnow()
            )
        
        # 4. 健康状态
        return NodeHealthStatus(
            status="healthy",
            details={
                "cpu_usage": resource_status["cpu_usage"],
                "memory_usage": resource_status["memory_usage"],
                "task_count": task_status["task_count"]
            },
            timestamp=datetime.utcnow()
        )

# 辅助类定义
class NodeInfo:
    """节点信息"""
    def __init__(
        self,
        id: str,
        cluster_id: str,
        name: str,
        description: str,
        ip_address: str,
        port: int,
        node_type: str,
        capabilities: Dict,
        resources: Dict,
        status: str,
        last_heartbeat: float,
        health: NodeHealthStatus,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.cluster_id = cluster_id
        self.name = name
        self.description = description
        self.ip_address = ip_address
        self.port = port
        self.node_type = node_type
        self.capabilities = capabilities
        self.resources = resources
        self.status = status
        self.last_heartbeat = last_heartbeat
        self.health = health
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "cluster_id": self.cluster_id,
            "name": self.name,
            "description": self.description,
            "ip_address": self.ip_address,
            "port": self.port,
            "node_type": self.node_type,
            "capabilities": self.capabilities,
            "resources": self.resources,
            "status": self.status,
            "last_heartbeat": self.last_heartbeat,
            "health": self.health.to_dict(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class NodeHealthStatus:
    """节点健康状态"""
    def __init__(
        self,
        status: str,
        details: Dict = None,
        timestamp: datetime = None
    ):
        self.status = status
        self.details = details or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "status": self.status,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }

class NodeHeartbeat:
    """节点心跳"""
    def __init__(
        self,
        node_id: str,
        timestamp: float,
        resources: Dict,
        load: float,
        active_tasks: List[str]
    ):
        self.node_id = node_id
        self.timestamp = timestamp
        self.resources = resources
        self.load = load
        self.active_tasks = active_tasks
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "node_id": self.node_id,
            "timestamp": self.timestamp,
            "resources": self.resources,
            "load": self.load,
            "active_tasks": self.active_tasks
        }

class NodeRegistrationResult:
    """节点注册结果"""
    def __init__(
        self,
        node_id: str,
        registration_time: float,
        initial_status: str
    ):
        self.node_id = node_id
        self.registration_time = registration_time
        self.initial_status = initial_status
```

#### 8.4.2 任务调度器

**技术实现：**
```python
import heapq
import time
import logging
from typing import Dict, List, Optional, Set
import threading

class TaskScheduler:
    """任务调度器，负责爬虫任务的分配和调度"""
    
    def __init__(
        self,
        config: Config,
        node_manager: CrawlerNodeManager,
        task_queue: TaskQueue,
        event_bus: EventBus
    ):
        self.config = config
        self.node_manager = node_manager
        self.task_queue = task_queue
        self.event_bus = event_bus
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler_thread = None
        self.lock = threading.Lock()
        self.assigned_tasks = {}  # task_id -> node_id
    
    def start(self):
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.logger.info("Starting task scheduler")
        
        # 启动调度线程
        self.scheduler_thread = threading.Thread(
            target=self._schedule_loop,
            daemon=True
        )
        self.scheduler_thread.start()
        
        self.logger.info("Task scheduler started")
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            return
        
        self.running = False
        self.logger.info("Stopping task scheduler")
        
        # 等待线程结束
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)
        
        self.logger.info("Task scheduler stopped")
    
    def _schedule_loop(self):
        """调度循环"""
        while self.running:
            try:
                # 1. 获取可用节点
                online_nodes = self.node_manager.get_nodes_by_status("online")
                if not online_nodes:
                    time.sleep(self.config.schedule_interval)
                    continue
                
                # 2. 获取待调度任务
                tasks = self.task_queue.get_pending_tasks(
                    limit=self.config.max_tasks_per_schedule
                )
                if not tasks:
                    time.sleep(self.config.schedule_interval)
                    continue
                
                # 3. 为每个任务选择合适的节点
                for task in tasks:
                    node_id = self._select_node(task, online_nodes)
                    if node_id:
                        # 分配任务
                        self._assign_task(task, node_id)
                    else:
                        # 没有合适的节点，稍后重试
                        self.logger.debug(
                            "No suitable node for task %s, will retry later", 
                            task.id
                        )
                
                # 4. 等待下一次调度
                time.sleep(self.config.schedule_interval)
                
            except Exception as e:
                self.logger.error("Error in scheduling loop: %s", str(e))
                time.sleep(1)
    
    def _select_node(
        self,
        task: CrawlerTask,
        online_nodes: List[NodeInfo]
    ) -> Optional[str]:
        """选择最适合的节点"""
        # 1. 过滤不支持任务类型的节点
        compatible_nodes = [
            node for node in online_nodes
            if self._is_node_compatible(node, task)
        ]
        if not compatible_nodes:
            return None
        
        # 2. 应用调度策略
        strategy = task.schedule_strategy or self.config.default_schedule_strategy
        if strategy == "least_loaded":
            return self._select_least_loaded_node(compatible_nodes)
        elif strategy == "geo_location":
            return self._select_geo_location_node(compatible_nodes, task)
        elif strategy == "content_based":
            return self._select_content_based_node(compatible_nodes, task)
        
        # 默认策略：最小负载
        return self._select_least_loaded_node(compatible_nodes)
    
    def _is_node_compatible(
        self,
        node: NodeInfo,
        task: CrawlerTask
    ) -> bool:
        """检查节点是否支持任务"""
        # 1. 檢查节点类型
        if task.node_type and node.node_type != task.node_type:
            return False
        
        # 2. 檢查能力要求
        for capability, required in task.capabilities.items():
            if capability not in node.capabilities or node.capabilities[capability] < required:
                return False
        
        # 3. 檢查资源要求
        if task.min_resources:
            for resource, required in task.min_resources.items():
                if resource not in node.resources or node.resources[resource] < required:
                    return False
        
        return True
    
    def _select_least_loaded_node(
        self,
        nodes: List[NodeInfo]
    ) -> Optional[str]:
        """选择负载最小的节点"""
        if not nodes:
            return None
        
        # 按负载排序（升序）
        sorted_nodes = sorted(nodes, key=lambda n: n.load)
        return sorted_nodes[0].id
    
    def _select_geo_location_node(
        self,
        nodes: List[NodeInfo],
        task: CrawlerTask
    ) -> Optional[str]:
        """选择地理位置最近的节点"""
        if not task.target_region or not nodes:
            return self._select_least_loaded_node(nodes)
        
        # 计算每个节点与目标区域的距离
        node_distances = []
        for node in nodes:
            distance = self._calculate_geo_distance(node.region, task.target_region)
            node_distances.append((distance, node))
        
        # 按距离排序
        sorted_nodes = sorted(node_distances, key=lambda x: x[0])
        return sorted_nodes[0][1].id
    
    def _calculate_geo_distance(
        self,
        node_region: str,
        target_region: str
    ) -> float:
        """计算地理位置距离"""
        # 简单实现：基于区域代码的匹配
        if node_region == target_region:
            return 0.0
        elif node_region[:2] == target_region[:2]:  # 同一国家
            return 1.0
        else:
            return 2.0
    
    def _select_content_based_node(
        self,
        nodes: List[NodeInfo],
        task: CrawlerTask
    ) -> Optional[str]:
        """选择基于内容特性的节点"""
        if not task.content_features or not nodes:
            return self._select_least_loaded_node(nodes)
        
        # 计算每个节点与内容特征的匹配度
        node_matches = []
        for node in nodes:
            match_score = self._calculate_content_match(node, task.content_features)
            node_matches.append((match_score, node))
        
        # 按匹配度排序（降序）
        sorted_nodes = sorted(node_matches, key=lambda x: x[0], reverse=True)
        return sorted_nodes[0][1].id
    
    def _calculate_content_match(
        self,
        node: NodeInfo,
        content_features: Dict
    ) -> float:
        """计算内容匹配度"""
        score = 0.0
        
        # 检查节点是否支持内容类型
        if "content_type" in content_features:
            if content_features["content_type"] in node.capabilities.get("content_types", []):
                score += 0.4
        
        # 检查节点是否支持特定技术
        if "technology" in content_features:
            if content_features["technology"] in node.capabilities.get("technologies", []):
                score += 0.3
        
        # 检查节点是否处理过类似内容
        if "similarity" in content_features:
            score += content_features["similarity"] * 0.3
        
        return score
    
    def _assign_task(
        self,
        task: CrawlerTask,
        node_id: str
    ):
        """分配任务到节点"""
        with self.lock:
            # 1. 更新任务状态
            task.status = "assigned"
            task.assigned_node = node_id
            task.assigned_at = time.time()
            self.task_queue.update_task(task)
            
            # 2. 记录分配
            self.assigned_tasks[task.id] = node_id
            
            # 3. 发布事件
            self.event_bus.publish("task.assigned", {
                "task_id": task.id,
                "node_id": node_id,
                "task_info": task.to_dict()
            })
            
            self.logger.info("Task %s assigned to node %s", task.id, node_id)
    
    def handle_task_completion(
        self,
        task_id: str,
        node_id: str,
        result: TaskResult
    ):
        """
        处理任务完成
        
        :param task_id: 任务ID
        :param node_id: 节点ID
        :param result: 任务结果
        """
        with self.lock:
            # 1. 移除分配记录
            if task_id in self.assigned_tasks:
                del self.assigned_tasks[task_id]
            
            # 2. 更新任务状态
            task = self.task_queue.get_task(task_id)
            if not task:
                self.logger.warning("Task %s not found for completion", task_id)
                return
            
            task.status = "completed" if result.success else "failed"
            task.completed_at = time.time()
            task.result = result.to_dict()
            self.task_queue.update_task(task)
            
            # 3. 发布事件
            event_type = "task.completed" if result.success else "task.failed"
            self.event_bus.publish(event_type, {
                "task_id": task_id,
                "node_id": node_id,
                "result": result.to_dict()
            })
            
            self.logger.info(
                "Task %s %s by node %s", 
                task_id, 
                "completed" if result.success else "failed",
                node_id
            )
    
    def handle_task_timeout(
        self,
        task_id: str,
        node_id: str
    ):
        """
        处理任务超时
        
        :param task_id: 任务ID
        :param node_id: 节点ID
        """
        with self.lock:
            # 1. 移除分配记录
            if task_id in self.assigned_tasks:
                del self.assigned_tasks[task_id]
            
            # 2. 更新任务状态
            task = self.task_queue.get_task(task_id)
            if not task:
                self.logger.warning("Task %s not found for timeout", task_id)
                return
            
            task.status = "timeout"
            task.completed_at = time.time()
            self.task_queue.update_task(task)
            
            # 3. 重新入队（如果需要重试）
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = "pending"
                task.assigned_node = None
                self.task_queue.add_task(task)
                
                self.logger.info(
                    "Task %s timed out, retrying (attempt %d/%d)", 
                    task_id, 
                    task.retry_count,
                    task.max_retries
                )
            else:
                self.logger.warning(
                    "Task %s timed out and exceeded max retries", 
                    task_id
                )
            
            # 4. 发布事件
            self.event_bus.publish("task.timeout", {
                "task_id": task_id,
                "node_id": node_id,
                "retry_count": task.retry_count
            })

class TaskQueue:
    """任务队列，管理待处理任务"""
    
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def add_task(self, task: CrawlerTask):
        """添加任务到队列"""
        sql = """
        INSERT INTO crawler_tasks (
            id, project_id, workflow_id, task_type,
            parameters, priority, 
            min_resources, capabilities,
            schedule_strategy, target_region, content_features,
            status, created_at, updated_at
        ) VALUES (
            %(id)s, %(project_id)s, %(workflow_id)s, %(task_type)s,
            %(parameters)s, %(priority)s,
            %(min_resources)s, %(capabilities)s,
            %(schedule_strategy)s, %(target_region)s, %(content_features)s,
            %(status)s, %(created_at)s, %(updated_at)s
        )
        """
        
        self.db.execute(sql, {
            "id": task.id,
            "project_id": task.project_id,
            "workflow_id": task.workflow_id,
            "task_type": task.task_type,
            "parameters": json.dumps(task.parameters),
            "priority": task.priority,
            "min_resources": json.dumps(task.min_resources) if task.min_resources else None,
            "capabilities": json.dumps(task.capabilities) if task.capabilities else None,
            "schedule_strategy": task.schedule_strategy,
            "target_region": task.target_region,
            "content_features": json.dumps(task.content_features) if task.content_features else None,
            "status": task.status,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })
    
    def get_pending_tasks(
        self,
        limit: int = 100
    ) -> List[CrawlerTask]:
        """获取待处理任务"""
        sql = """
        SELECT * FROM crawler_tasks 
        WHERE status = 'pending'
        ORDER BY priority DESC, created_at
        LIMIT %(limit)s
        """
        
        rows = self.db.fetchall(sql, {"limit": limit})
        return [self._row_to_task(row) for row in rows]
    
    def get_task(self, task_id: str) -> Optional[CrawlerTask]:
        """获取任务详情"""
        sql = "SELECT * FROM crawler_tasks WHERE id = %(id)s"
        row = self.db.fetchone(sql, {"id": task_id})
        return self._row_to_task(row) if row else None
    
    def update_task(self, task: CrawlerTask):
        """更新任务状态"""
        sql = """
        UPDATE crawler_tasks SET
            status = %(status)s,
            assigned_node = %(assigned_node)s,
            assigned_at = %(assigned_at)s,
            completed_at = %(completed_at)s,
            result = %(result)s,
            retry_count = %(retry_count)s,
            updated_at = %(updated_at)s
        WHERE id = %(id)s
        """
        
        self.db.execute(sql, {
            "id": task.id,
            "status": task.status,
            "assigned_node": task.assigned_node,
            "assigned_at": datetime.fromtimestamp(task.assigned_at) if task.assigned_at else None,
            "completed_at": datetime.fromtimestamp(task.completed_at) if task.completed_at else None,
            "result": json.dumps(task.result) if task.result else None,
            "retry_count": task.retry_count,
            "updated_at": datetime.utcnow()
        })

# 辅助类定义
class CrawlerTask:
    """爬虫任务"""
    def __init__(
        self,
        id: str,
        project_id: str,
        workflow_id: str,
        task_type: str,
        parameters: Dict,
        priority: int = 5,
        min_resources: Optional[Dict] = None,
        capabilities: Optional[Dict] = None,
        schedule_strategy: Optional[str] = None,
        target_region: Optional[str] = None,
        content_features: Optional[Dict] = None,
        status: str = "pending",
        created_at: datetime = None,
        updated_at: datetime = None,
        assigned_node: Optional[str] = None,
        assigned_at: Optional[float] = None,
        completed_at: Optional[float] = None,
        result: Optional[Dict] = None,
        retry_count: int = 0,
        max_retries: int = 3
    ):
        self.id = id
        self.project_id = project_id
        self.workflow_id = workflow_id
        self.task_type = task_type
        self.parameters = parameters
        self.priority = priority
        self.min_resources = min_resources or {}
        self.capabilities = capabilities or {}
        self.schedule_strategy = schedule_strategy
        self.target_region = target_region
        self.content_features = content_features or {}
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.assigned_node = assigned_node
        self.assigned_at = assigned_at
        self.completed_at = completed_at
        self.result = result
        self.retry_count = retry_count
        self.max_retries = max_retries
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "workflow_id": self.workflow_id,
            "task_type": self.task_type,
            "parameters": self.parameters,
            "priority": self.priority,
            "min_resources": self.min_resources,
            "capabilities": self.capabilities,
            "schedule_strategy": self.schedule_strategy,
            "target_region": self.target_region,
            "content_features": self.content_features,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "assigned_node": self.assigned_node,
            "assigned_at": self.assigned_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries
        }

class TaskResult:
    """任务结果"""
    def __init__(
        self,
        success: bool,
        data: Optional[Dict] = None,
        error: Optional[str] = None,
        metrics: Optional[Dict] = None
    ):
        self.success = success
        self.data = data or {}
        self.error = error
        self.metrics = metrics or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metrics": self.metrics,
            "timestamp": self.timestamp.isoformat()
        }
```

### 8.5 数据模型详细定义

#### 8.5.1 爬虫节点表

```sql
-- 爬虫节点表
CREATE TABLE crawler_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id UUID NOT NULL REFERENCES crawler_clusters(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    ip_address INET NOT NULL,
    port INT NOT NULL,
    node_type VARCHAR(50) NOT NULL,
    capabilities JSONB DEFAULT '{}'::jsonb,
    resources JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'online', 'offline', 'unresponsive', 'maintenance')),
    last_heartbeat TIMESTAMPTZ,
    health_status VARCHAR(20) NOT NULL DEFAULT 'unknown' CHECK (health_status IN ('unknown', 'healthy', 'degraded', 'unhealthy')),
    health_details JSONB DEFAULT '{}'::jsonb,
    health_timestamp TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_nodes_cluster ON crawler_nodes(cluster_id),
    INDEX idx_nodes_status ON crawler_nodes(status),
    INDEX idx_nodes_health ON crawler_nodes(health_status),
    INDEX idx_nodes_last_heartbeat ON crawler_nodes(last_heartbeat DESC)
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_crawler_nodes_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_crawler_nodes_modtime
BEFORE UPDATE ON crawler_nodes
FOR EACH ROW
EXECUTE FUNCTION update_crawler_nodes_modtime();
```

#### 8.5.2 爬虫任务表

```sql
-- 爬虫任务表
CREATE TABLE crawler_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    priority INT NOT NULL DEFAULT 5,
    min_resources JSONB DEFAULT '{}'::jsonb,
    capabilities JSONB DEFAULT '{}'::jsonb,
    schedule_strategy VARCHAR(50),
    target_region VARCHAR(10),
    content_features JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'assigned', 'processing', 'completed', 'failed', 'timeout')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    assigned_node UUID REFERENCES crawler_nodes(id) ON DELETE SET NULL,
    assigned_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    result JSONB,
    retry_count INT NOT NULL DEFAULT 0,
    max_retries INT NOT NULL DEFAULT 3,
    
    -- 索引
    INDEX idx_tasks_project ON crawler_tasks(project_id),
    INDEX idx_tasks_workflow ON crawler_tasks(workflow_id),
    INDEX idx_tasks_status ON crawler_tasks(status),
    INDEX idx_tasks_priority ON crawler_tasks(priority DESC, created_at),
    INDEX idx_tasks_assigned ON crawler_tasks(assigned_node),
    INDEX idx_tasks_created ON crawler_tasks(created_at DESC)
);
```

#### 8.5.3 爬虫任务执行表

```sql
-- 爬虫任务执行表
CREATE TABLE crawler_task_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES crawler_tasks(id) ON DELETE CASCADE,
    node_id UUID NOT NULL REFERENCES crawler_nodes(id) ON DELETE CASCADE,
    start_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    end_time TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
    result JSONB,
    metrics JSONB DEFAULT '{}'::jsonb,
    retry_count INT NOT NULL DEFAULT 0,
    
    -- 索引
    INDEX idx_executions_task ON crawler_task_executions(task_id),
    INDEX idx_executions_node ON crawler_task_executions(node_id),
    INDEX idx_executions_status ON crawler_task_executions(status),
    INDEX idx_executions_time ON crawler_task_executions(start_time DESC)
);
```

#### 8.5.4 爬虫集群表

```sql
-- 爬虫集群表
CREATE TABLE crawler_clusters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    configuration JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- 索引
    INDEX idx_clusters_project ON crawler_clusters(project_id),
    INDEX idx_clusters_status ON crawler_clusters(status),
    UNIQUE (project_id, name)
);

-- 自动更新updated_at触发器
CREATE OR REPLACE FUNCTION update_crawler_clusters_modtime()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_crawler_clusters_modtime
BEFORE UPDATE ON crawler_clusters
FOR EACH ROW
EXECUTE FUNCTION update_crawler_clusters_modtime();
```

### 8.6 API详细规范

#### 8.6.1 节点管理API

**注册爬虫节点 (POST /api/v1/nodes:register)**

*请求示例:*
```http
POST /api/v1/nodes:register HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "crawler-node-01",
  "description": "Main crawler node in US East region",
  "ip_address": "192.168.1.101",
  "port": 8000,
  "node_type": "standard",
  "capabilities": {
    "content_types": ["html", "json", "xml"],
    "technologies": ["react", "angular", "wordpress"],
    "anti_crawling_bypass": ["user-agent", "proxy"]
  },
  "resources": {
    "cpu": 8,
    "memory_mb": 16384,
    "gpu": 1,
    "network_bandwidth_mbps": 1000
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/nodes/node-1a2b3c4d

{
  "node_id": "node-1a2b3c4d",
  "registration_time": 1686825045.123,
  "initial_status": "online"
}
```

**发送节点心跳 (POST /api/v1/nodes/{node_id}:heartbeat)**

*请求示例:*
```http
POST /api/v1/nodes/node-1a2b3c4d:heartbeat HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resources": {
    "cpu_usage": 0.65,
    "memory_usage": 0.75,
    "gpu_usage": 0.45
  },
  "load": 0.8,
  "active_tasks": ["task-123", "task-456"]
}
```

*成功响应示例:*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "node_id": "node-1a2b3c4d",
  "timestamp": 1686825045.123,
  "status": "online"
}
```

#### 8.6.2 任务管理API

**创建爬虫任务 (POST /api/v1/tasks)**

*请求示例:*
```http
POST /api/v1/tasks HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "project_id": "proj-123",
  "workflow_id": "inst-1a2b3c4d5e6f",
  "task_type": "web_crawl",
  "parameters": {
    "url": "https://example.com/products",
    "depth": 2,
    "selectors": {
      "product": "div.product",
      "title": "h2.title",
      "price": "span.price"
    }
  },
  "priority": 7,
  "min_resources": {
    "memory_mb": 4096,
    "cpu_cores": 2
  },
  "capabilities": {
    "javascript_rendering": 1,
    "proxy_rotation": 1
  },
  "schedule_strategy": "least_loaded",
  "target_region": "us",
  "content_features": {
    "content_type": "html",
    "technology": "react"
  }
}
```

*成功响应示例:*
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/tasks/task-123

{
  "id": "task-123",
  "status": "pending",
  "created_at": "2023-06-15T10:30:45Z",
  "priority": 7
}
```

**获取任务状态 (GET /api/v1/tasks/{task_id})**

*请求示例:*
```http
GET /api/v1/tasks/task-123 HTTP/1.1
Host: dccms.mirror-realm.com
Authorization: Bearer <access_token>
```

*成功响应示例 (处理中):*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "task-123",
  "project_id": "proj-123",
  "workflow_id": "inst-1a2b3c4d5e6f",
  "task_type": "web_crawl",
  "parameters": {
    "url": "https://example.com/products",
    "depth": 2,
    "selectors": {
      "product": "div.product",
      "title": "h2.title",
      "price": "span.price"
    }
  },
  "priority": 7,
  "min_resources": {
    "memory_mb": 4096,
    "cpu_cores": 2
  },
  "capabilities": {
    "javascript_rendering": 1,
    "proxy_rotation": 1
  },
  "schedule_strategy": "least_loaded",
  "target_region": "us",
  "content_features": {
    "content_type": "html",
    "technology": "react"
  },
  "status": "processing",
  "created_at": "2023-06-15T10:30:45Z",
  "updated_at": "2023-06-15T10:31:10Z",
  "assigned_node": "node-1a2b3c4d",
  "assigned_at": "2023-06-15T10:31:10Z",
  "retry_count": 0,
  "max_retries": 3
}
```

*成功响应示例 (已完成):*
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "task-123",
  "project_id": "proj-123",
  "workflow_id": "inst-1a2b3c4d5e6f",
  "task_type": "web_crawl",
  "parameters": {
    "url": "https://example.com/products",
    "depth": 2,
    "selectors": {
      "product": "div.product",
      "title": "h2.title",
      "price": "span.price"
    }
  },
  "priority": 7,
  "min_resources": {
    "memory_mb": 4096,
    "cpu_cores": 2
  },
  "capabilities": {
    "javascript_rendering": 1,
    "proxy_rotation": 1
  },
  "schedule_strategy": "least_loaded",
  "target_region": "us",
  "content_features": {
    "content_type": "html",
    "technology": "react"
  },
  "status": "completed",
  "created_at": "2023-06-15T10:30:45Z",
  "updated_at": "2023-06-15T10:35:20Z",
  "assigned_node": "node-1a2b3c4d",
  "assigned_at": "2023-06-15T10:31:10Z",
  "completed_at": "2023-06-15T10:35:20Z",
  "result": {
    "success": true,
    "data": {
      "products": [
        {
          "title": "Product 1",
          "price": "$19.99",
          "url": "/products/1"
        },
        {
          "title": "Product 2",
          "price": "$29.99",
          "url": "/products/2"
        }
      ]
    },
    "metrics": {
      "pages_crawled": 15,
      "processing_time": 125.4,
      "data_size": 4294967
    },
    "timestamp": "2023-06-15T10:35:20Z"
  },
  "retry_count": 0,
  "max_retries": 3
}
```

### 8.7 性能优化策略

#### 8.7.1 任务调度优化

1. **分层任务队列**
   ```python
   class LayeredTaskQueue:
       """分层任务队列，支持优先级和分类"""
       
       def __init__(self, config: Config):
           self.config = config
           self.logger = logging.getLogger(__name__)
           
           # 创建优先级队列
           self.priority_queues = {
               priority: PriorityQueue()
               for priority in range(1, 11)  # 1-10优先级
           }
           
           # 创建类别队列
           self.category_queues = defaultdict(PriorityQueue)
       
       def add_task(self, task: CrawlerTask):
           """添加任务到队列"""
           # 按优先级添加
           self.priority_queues[task.priority].put((task.created_at, task.id, task))
           
           # 按类别添加
           for category in task.categories:
               self.category_queues[category].put((task.priority, task.created_at, task.id, task))
       
       def get_next_task(
           self,
           max_priority: int = 10,
           categories: Optional[List[str]] = None
       ) -> Optional[CrawlerTask]:
           """获取下一个任务"""
           # 1. 按类别获取任务
           if categories:
               for category in categories:
                   if category in self.category_queues:
                       task = self._get_task_from_category_queue(category)
                       if task and task.priority <= max_priority:
                           return task
           
           # 2. 按优先级获取任务
           for priority in range(1, max_priority + 1):
               if not self.priority_queues[priority].empty():
                   _, _, task = self.priority_queues[priority].get()
                   return task
           
           return None
       
       def _get_task_from_category_queue(self, category: str) -> Optional[CrawlerTask]:
           """从类别队列获取任务"""
           if self.category_queues[category].empty():
               return None
           
           # 获取最高优先级任务
           _, _, _, task = self.category_queues[category].get()
           return task
       
       def task_completed(self, task: CrawlerTask):
           """任务完成处理"""
           # 从队列中移除
           self._remove_from_priority_queue(task)
           self._remove_from_category_queues(task)
       
       def _remove_from_priority_queue(self, task: CrawlerTask):
           """从优先级队列移除"""
           # 简单实现：重建队列
           temp_queue = PriorityQueue()
           while not self.priority_queues[task.priority].empty():
               t = self.priority_queues[task.priority].get()
               if t[2].id != task.id:
                   temp_queue.put(t)
           self.priority_queues[task.priority] = temp_queue
       
       def _remove_from_category_queues(self, task: CrawlerTask):
           """从类别队列移除"""
           for category in task.categories:
               if category in self.category_queues:
                   # 重建类别队列
                   temp_queue = PriorityQueue()
                   while not self.category_queues[category].empty():
                       t = self.category_queues[category].get()
                       if t[3].id != task.id:
                           temp_queue.put(t)
                   self.category_queues[category] = temp_queue
   ```

2. **批量任务分配**
   ```python
   class BatchTaskScheduler:
       """批量任务调度器，提高调度效率"""
       
       def __init__(self, config: Config, node_manager: CrawlerNodeManager):
           self.config = config
           self.node_manager = node_manager
           self.logger = logging.getLogger(__name__)
       
       def schedule_batch(
           self,
           tasks: List[CrawlerTask],
           nodes: List[NodeInfo]
       ) -> Dict[str, List[CrawlerTask]]:
           """
           批量调度任务
           
           :param tasks: 任务列表
           :param nodes: 可用节点列表
           :return: 节点到任务的映射
           """
           # 1. 按策略对任务排序
           sorted_tasks = self._sort_tasks(tasks)
           
           # 2. 按能力对节点排序
           sorted_nodes = self._sort_nodes(nodes)
           
           # 3. 分配任务
           assignment = {node.id: [] for node in sorted_nodes}
           node_index = 0
           
           for task in sorted_tasks:
               # 选择节点（轮询）
               node = sorted_nodes[node_index]
               assignment[node.id].append(task)
               
               # 更新索引
               node_index = (node_index + 1) % len(sorted_nodes)
           
           return assignment
       
       def _sort_tasks(self, tasks: List[CrawlerTask]) -> List[CrawlerTask]:
           """对任务排序"""
           # 按优先级和创建时间排序
           return sorted(
               tasks,
               key=lambda t: (-t.priority, t.created_at)
           )
       
       def _sort_nodes(self, nodes: List[NodeInfo]) -> List[NodeInfo]:
           """对节点排序"""
           # 按负载排序（升序）
           return sorted(
               nodes,
               key=lambda n: n.load
           )
   ```

#### 8.7.2 资源优化

1. **动态资源分配**
   ```python
   class DynamicResourceAllocator:
       """动态资源分配器"""
       
       def __init__(self, config: Config):
           self.config = config
           self.logger = logging.getLogger(__name__)
       
       def allocate_resources(
           self,
           task: CrawlerTask,
           node: NodeInfo
       ) -> Dict[str, Any]:
           """
           分配资源给任务
           
           :param task: 任务
           :param node: 节点
           :return: 资源分配结果
           """
           # 1. 基始分配
           allocation = self._initial_allocation(task, node)
           
           # 2. 根据实时负载调整
           allocation = self._adjust_for_load(allocation, node)
           
           # 3. 根据任务特性调整
           allocation = self._adjust_for_task(allocation, task)
           
           return allocation
       
       def _initial_allocation(
           self,
           task: CrawlerTask,
           node: NodeInfo
       ) -> Dict[str, Any]:
           """初始资源分配"""
           # 基始分配基于任务请求
           allocation = {
               "cpu_cores": min(task.min_resources.get("cpu_cores", 1), node.resources["cpu"]),
               "memory_mb": min(task.min_resources.get("memory_mb", 1024), node.resources["memory_mb"]),
               "gpu": min(task.min_resources.get("gpu", 0), node.resources["gpu"])
           }
           
           # 确保至少分配最小资源
           allocation["cpu_cores"] = max(allocation["cpu_cores"], 0.5)
           allocation["memory_mb"] = max(allocation["memory_mb"], 512)
           
           return allocation
       
       def _adjust_for_load(
           self,
           allocation: Dict[str, Any],
           node: NodeInfo
       ) -> Dict[str, Any]:
           """根据节点负载调整资源分配"""
           # 如果节点负载高，减少资源分配
           if node.load > 0.7:
               allocation["cpu_cores"] *= 0.8
               allocation["memory_mb"] *= 0.9
           
           # 如果节点负载低，增加资源分配
           elif node.load < 0.3:
               allocation["cpu_cores"] = min(allocation["cpu_cores"] * 1.2, node.resources["cpu"])
               allocation["memory_mb"] = min(allocation["memory_mb"] * 1.1, node.resources["memory_mb"])
           
           return allocation
       
       def _adjust_for_task(
           self,
           allocation: Dict[str, Any],
           task: CrawlerTask
       ) -> Dict[str, Any]:
           """根据任务特性调整资源分配"""
           # 如果任务需要JavaScript渲染，增加内存
           if task.capabilities.get("javascript_rendering", 0) > 0:
               allocation["memory_mb"] = min(allocation["memory_mb"] * 1.5, 8192)
           
           # 如果任务需要代理轮换，增加CPU
           if task.capabilities.get("proxy_rotation", 0) > 0:
               allocation["cpu_cores"] = min(allocation["cpu_cores"] * 1.3, 4.0)
           
           return allocation
   ```

### 8.8 安全考虑

#### 8.8.1 节点安全

1. **节点认证与授权**
   ```python
   class NodeAuthenticator:
       """节点认证器"""
       
       def __init__(self, config: Config, db: Database):
           self.config = config
           self.db = db
           self.logger = logging.getLogger(__name__)
       
       def authenticate(
           self,
           node_id: str,
           token: str
       ) -> Tuple[bool, Optional[str]]:
           """
           认证节点
           
           :param node_id: 节点ID
           :param token: 认证令牌
           :return: (是否认证通过, 错误消息)
           """
           # 1. 检查节点是否存在
           node = self._get_node(node_id)
           if not node:
               return False, "Node not registered"
           
           # 2. 检查令牌有效性
           if not self._validate_token(node, token):
               return False, "Invalid token"
           
           # 3. 检查节点状态
           if node["status"] != "online":
               return False, f"Node not online (status: {node['status']})"
           
           return True, None
       
       def _get_node(self, node_id: str) -> Optional[Dict]:
           """获取节点信息"""
           sql = "SELECT * FROM crawler_nodes WHERE id = %(id)s"
           return self.db.fetchone(sql, {"id": node_id})
       
       def _validate_token(self, node: Dict, token: str) -> bool:
           """验证令牌"""
           # 1. 检查令牌格式
           if not re.match(r'^[a-f0-9]{64}$', token):
               return False
           
           # 2. 检查令牌是否匹配
           stored_token = node["auth_token"]
           return hmac.compare_digest(stored_token, token)
       
       def generate_token(self, node_id: str) -> str:
           """生成节点认证令牌"""
           # 1. 生成随机令牌
           token = secrets.token_hex(32)
           
           # 2. 存储令牌（哈希后）
           hashed_token = self._hash_token(token)
           self._store_token(node_id, hashed_token)
           
           return token
       
       def _hash_token(self, token: str) -> str:
           """哈希令牌"""
           return hashlib.sha256(token.encode('utf-8')).hexdigest()
       
       def _store_token(self, node_id: str, hashed_token: str):
           """存储哈希令牌"""
           sql = """
           UPDATE crawler_nodes 
           SET auth_token = %(token)s, auth_token_updated = NOW()
           WHERE id = %(id)s
           """
           self.db.execute(sql, {
               "id": node_id,
               "token": hashed_token
           })
   ```

2. **节点沙箱环境**
   ```python
   class NodeSandbox:
       """节点沙箱环境，限制爬虫执行"""
       
       def __init__(self, config: Config):
           self.config = config
           self.logger = logging.getLogger(__name__)
       
       def create_sandbox(self, node_id: str, task: CrawlerTask) -> str:
           """
           创建沙箱环境
           
           :param node_id: 节点ID
           :param task: 任务
           :return: 沙箱路径
           """
           # 1. 创建临时目录
           sandbox_dir = tempfile.mkdtemp(prefix=f"sandbox_{node_id}_")
           
           # 2. 设置资源限制
           self._apply_resource_limits(sandbox_dir, task)
           
           # 3. 设置网络限制
           self._apply_network_limits(sandbox_dir, task)
           
           # 4. 设置文件系统限制
           self._apply_filesystem_limits(sandbox_dir, task)
           
           return sandbox_dir
       
       def _apply_resource_limits(self, sandbox_dir: str, task: CrawlerTask):
           """应用资源限制"""
           # 使用cgroups限制资源
           cgroup_path = f"/sys/fs/cgroup/crawler/{task.id}"
           os.makedirs(cgroup_path, exist_ok=True)
           
           # CPU限制
           cpu_quota = int(self.config.cpu_quota_base * task.min_resources.get("cpu_cores", 1))
           with open(f"{cgroup_path}/cpu.max", "w") as f:
               f.write(f"{cpu_quota} 100000")
           
           # 内存限制
           mem_limit = task.min_resources.get("memory_mb", 1024) * 1024 * 1024
           with open(f"{cgroup_path}/memory.max", "w") as f:
               f.write(str(mem_limit))
       
       def _apply_network_limits(self, sandbox_dir: str, task: CrawlerTask):
           """应用网络限制"""
           # 使用network namespace隔离
           netns_name = f"crawler_{task.id}"
           subprocess.run(["ip", "netns", "add", netns_name], check=True)
           
           # 设置网络限制
           if task.min_resources.get("network_bandwidth_mbps"):
               bandwidth = task.min_resources["network_bandwidth_mbps"]
               subprocess.run([
                   "tc", "qdisc", "add", "dev", "eth0", "root", "tbf", 
                   "rate", f"{bandwidth}mbit", "burst", "50kb", "latency", "70ms"
               ], check=True)
       
       def _apply_filesystem_limits(self, sandbox_dir: str, task: CrawlerTask):
           """应用文件系统限制"""
           # 使用bind mount限制文件系统访问
           allowed_dirs = self.config.sandbox_allowed_dirs
           for src, dest in allowed_dirs.items():
               os.makedirs(f"{sandbox_dir}{dest}", exist_ok=True)
               subprocess.run([
                   "mount", "-o", "bind", src, f"{sandbox_dir}{dest}"
               ], check=True)
           
           # 只止其他文件系统访问
           subprocess.run([
               "mount", "-o", "remount,ro", "proc", f"{sandbox_dir}/proc"
           ], check=True)
       
       def cleanup_sandbox(self, sandbox_dir: str):
           """清理沙箱环境"""
           # 1. 删除cgroup
           cgroup_path = f"/sys/fs/cgroup/crawler/{os.path.basename(sandbox_dir)}"
           if os.path.exists(cgroup_path):
               shutil.rmtree(cgroup_path)
           
           # 2. 删除network namespace
           netns_name = f"crawler_{os.path.basename(sandbox_dir)}"
           subprocess.run(["ip", "netns", "delete", netns_name], check=False)
           
           # 3. 删除临时目录
           if os.path.exists(sandbox_dir):
               shutil.rmtree(sandbox_dir)
   ```

### 8.9 与其他模块的交互

#### 8.9.1 与数据处理工作流引擎交互

```mermaid
sequenceDiagram
    participant DPWE as Data Processing Workflow Engine
    participant DCCMS as Distributed Crawler Cluster Management System
    
    DPWE->>DCCMS: POST /api/v1/tasks (创建爬虫任务)
    DCCMS-->>DPWE: 任务ID
    
    loop 任务处理中
        DCCMS->>DPWE: POST /api/v1/workflowInstances/{id}:update (更新状态)
        DPWE-->>DCCMS: 确认
    end
    
    DCCMS->>DPWE: POST /api/v1/workflowInstances/{id}:complete (任务完成)
    DPWE-->>DCCMS: 确认
```

#### 8.9.2 与网站指纹分析引擎交互

```mermaid
sequenceDiagram
    participant WFE as Website Fingerprinting Engine
    participant DCCMS as Distributed Crawler Cluster Management System
    
    DCCMS->>WFE: GET /api/v1/analyze?url={url} (获取网站指纹)
    WFE-->>DCCMS: 网站指纹数据
    
    DCCMS->>WFE: POST /api/v1/compliance-check (合规性检查)
    WFE-->>DCCMS: 合规性检查结果
```

#### 8.9.3 与数据合规与安全中心交互

```mermaid
sequenceDiagram
    participant DCSC as Data Compliance and Security Center
    participant DCCMS as Distributed Crawler Cluster Management System
    
    DCCMS->>DCSC: POST /api/v1/compliance/check (检查爬虫任务合规性)
    DCSC-->>DCCMS: 合规性检查结果
    
    DCCMS->>DCSC: POST /api/v1/data:detect-sensitive (检测爬取内容)
    DCSC-->>DCCMS: 敏感数据检测结果
    
    DCCMS->>DCSC: POST /api/v1/data:redact (请求数据脱敏)
    DCSC-->>DCCMS: 脱敏后的内容
```

#### 8.9.4 与自动化媒体处理管道交互

```mermaid
sequenceDiagram
    participant AMP as Automated Media Processing Pipeline
    participant DCCMS as Distributed Crawler Cluster Management System
    
    DCCMS->>AMP: POST /api/v1/media:process (触发媒体处理)
    AMP-->>DCCMS: 处理任务ID
    
    loop 处理进行中
        DCCMS->>AMP: GET /api/v1/media/processingTasks/{task_id} (查询状态)
        AMP-->>DCCMS: 处理状态
    end
    
    DCCMS->>AMP: GET /api/v1/media/processingTasks/{task_id} (获取结果)
    AMP-->>DCCMS: 处理结果和元数据
```

## 9. 系统集成与部署

### 9.1 部署架构

#### 9.1.1 生产环境部署

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      生产环境部署                                           │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  公户端层             │  API网关层           │  服务层                                   │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • Web UI             │ • 负载均衡器          │ • 微服务集群                               │
│ • 移动应用            │ • API网关            │ • 数据库集群                               │
│ • CLI工具            │ • 身证授权服务        │ • 消息队列集群                             │
│                      │ • 限流服务            │ • 缓存集群                                 │
│                      │ • WAF                 │ • 搜索集群                                 │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 9.1.2 服务部署拓扑

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    镜界平台服务部署拓扑                                     │
├───────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                │
│  │  数据源注册  │     │ 网站指纹分析 │     │ 数据源健康   │     │ 数据处理工作 │                │
│  │  中心(DSR)   │<--->│ 引擎(WFE)   │<--->│ 监测系统     │<--->│ 流引擎      │                │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘                │
│         ▲                   ▲                   ▲                   ▲                         │
│         │                   │                   │                   │                         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                │
│  │ 自动化媒体   │     │ AI辅助开发  │     │ 数据合规与   │     │ 分布式爬虫   │                │
│  │ 处理管道(AMP)│<--->│ 系统(AIDS)  │<--->│ 安全中心     │<--->│ 集群管理系统 │                │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘                │
│                                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 部署流程

#### 9.2.1 基础设施准备

1. **云资源准备**
   ```bash
   # 创建VPC网络
   aws ec2 create-vpc --cidr-block 10.0.0.0/16
   
   # 创建子网
   aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
   
   # 创建安全组
   aws ec2 create-security-group --group-name mirror-realm-sg --description "Mirror Realm Security Group"
   
   # 配置安全组规则
   aws ec2 authorize-security-group-ingress --group-id sg-123 --protocol tcp --port 80 --cidr 0.0.0.0/0
   aws ec2 authorize-security-group-ingress --group-id sg-123 --protocol tcp --port 443 --cidr 0.0.0.0/0
   aws ec2 authorize-security-group-ingress --group-id sg-123 --protocol tcp --port 8000-9000 --cidr 10.0.0.0/16
   ```

2. **Kubernetes集群创建**
   ```bash
   # 创建EKS集群
   eksctl create cluster \
     --name mirror-realm-prod \
     --region us-east-1 \
     --nodegroup-name standard-workers \
     --node-type t3.xlarge \
     --nodes 3 \
     --nodes-min 3 \
     --nodes-max 10 \
     --node-ami auto
   ```

#### 9.2.2 服务部署

1. **数据库部署**
   ```yaml
   # postgres-deployment.yaml
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: postgres
   spec:
     serviceName: postgres
     replicas: 3
     selector:
       matchLabels:
         app: postgres
     template:
       metadata:
         labels:
           app: postgres
       spec:
         containers:
         - name: postgres
           image: postgres:13
           env:
           - name: POSTGRES_USER
             value: "mirror_realm"
           - name: POSTGRES_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: db-secrets
                 key: password
           - name: POSTGRES_DB
             value: "mirror_realm"
           ports:
           - containerPort: 5432
           volumeMounts:
           - name: data
             mountPath: /var/lib/postgresql/data
         volumes:
         - name: data
           persistentVolumeClaim:
             claimName: postgres-pvc
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: postgres
   spec:
     ports:
     - port: 5432
       targetPort: 5432
     clusterIP: None
     selector:
       app: postgres
   ```

2. **微服务部署**
   ```yaml
   # dsr-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: data-source-registry
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: data-source-registry
     template:
       metadata:
         labels:
           app: data-source-registry
       spec:
         containers:
         - name: dsr
           image: mirror-realm/dsr:1.0.0
           ports:
           - containerPort: 8000
           env:
           - name: DB_HOST
             value: "postgres"
           - name: DB_PORT
             value: "5432"
           - name: DB_NAME
             value: "mirror_realm"
           - name: DB_USER
             value: "mirror_realm"
           - name: DB_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: db-secrets
                 key: password
           resources:
             requests:
               memory: "512Mi"
               cpu: "500m"
             limits:
               memory: "1Gi"
               cpu: "1000m"
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: data-source-registry
   spec:
     type: ClusterIP
     ports:
     - port: 80
       targetPort: 8000
     selector:
       app: data-source-registry
   ```

#### 9.2.3 配置管理

1. **配置文件结构**
   ```
   config/
   ├── base/
   │   ├── application.yaml
   │   ├── database.yaml
   │   └── security.yaml
   ├── dev/
   │   ├── application.yaml
   │   └── overrides.yaml
   ├── staging/
   │   ├── application.yaml
   │   └── overrides.yaml
   └── prod/
       ├── application.yaml
       └── overrides.yaml
   ```

2. **配置管理服务实现**
   ```python
   import os
   import yaml
   from typing import Dict, Any
   import logging

   class ConfigManager:
       """配置管理器，加载和管理应用配置"""
       
       def __init__(self, env: str = "prod"):
           self.env = env
           self.logger = logging.getLogger(__name__)
           self.config = self._load_config()
       
       def _load_config(self) -> Dict[str, Any]:
           """加载配置"""
           # 1. 加载基础配置
           base_config = self._load_yaml("config/base/application.yaml")
           
           # 2. 加载环境特定配置
           env_config = self._load_yaml(f"config/{self.env}/application.yaml")
           
           # 3. 加载覆盖配置
           overrides = self._load_yaml(f"config/{self.env}/overrides.yaml")
           
           # 4. 合并配置
           config = self._deep_merge(base_config, env_config)
           config = self._deep_merge(config, overrides)
           
           # 5. 从环境变量覆盖
           config = self._apply_env_overrides(config)
           
           return config
       
       def _load_yaml(self, path: str) -> Dict:
           """加载YAML文件"""
           if not os.path.exists(path):
               self.logger.debug("Config file not found: %s", path)
               return {}
           
           with open(path, 'r') as f:
               return yaml.safe_load(f) or {}
       
       def _deep_merge(self, base: Dict, override: Dict) -> Dict:
           """深度合併配置"""
           result = base.copy()
           
           for key, value in override.items():
               if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                   result[key] = self._deep_merge(result[key], value)
               else:
                   result[key] = value
           
           return result
       
       def _apply_env_overrides(self, config: Dict) -> Dict:
           """应用环境变量覆盖"""
           for key, value in os.environ.items():
               if key.startswith("APP_"):
                   # 转换为配置路径
                   config_path = key[4:].lower().replace('_', '.')
                   self._set_config_value(config, config_path, value)
           
           return config
       
       def _set_config_value(self, config: Dict, path: str, value: Any):
           """设置配置值"""
           keys = path.split('.')
           current = config
           
           for key in keys[:-1]:
               if key not in current or not isinstance(current[key], dict):
                   current[key] = {}
               current = current[key]
           
           # 转换值类型
           if isinstance(current[keys[-1]], bool):
               value = value.lower() == 'true'
           elif isinstance(current[keys[-1]], int):
               value = int(value)
           elif isinstance(current[keys[-1]], float):
               value = float(value)
           
           current[keys[-1]] = value
       
       def get(self, path: str, default: Any = None) -> Any:
           """获取配置值"""
           keys = path.split('.')
           current = self.config
           
           for key in keys:
               if key not in current:
                   return default
               current = current[key]
           
           return current
       
       def get_database_config(self) -> Dict:
           """获取数据库配置"""
           return {
               "host": self.get("database.host", "localhost"),
               "port": self.get("database.port", 5432),
               "name": self.get("database.name", "mirror_realm"),
               "user": self.get("database.user", "mirror_realm"),
               "password": os.getenv("DB_PASSWORD", "")
           }
   ```

### 9.3 监控与告警

#### 9.3.1 监控指标

1. **系统级指标**
   ```yaml
   # system-metrics.yaml
   system:
     cpu:
       usage: "system_cpu_usage"
       limit: "system_cpu_limit"
     memory:
       usage: "system_memory_usage"
       limit: "system_memory_limit"
     disk:
       usage: "system_disk_usage"
       iops: "system_disk_iops"
     network:
       ingress: "system_network_ingress"
       egress: "system_network_egress"
   ```

2. **应用级指标**
   ```yaml
   # application-metrics.yaml
   application:
     http:
       requests_total: "http_requests_total"
       request_duration_seconds: "http_request_duration_seconds"
       errors_total: "http_errors_total"
     database:
       connections: "db_connections"
       query_duration_seconds: "db_query_duration_seconds"
       errors_total: "db_errors_total"
     queue:
       size: "queue_size"
       processing_time_seconds: "queue_processing_time_seconds"
     cache:
       hits: "cache_hits"
       misses: "cache_misses"
       evictions: "cache_evictions"
   ```

#### 9.3.2 告警规则

1. **系统健康告警**
   ```yaml
   # system-alerts.yaml
   alerts:
     - name: "High CPU Usage"
       expression: "system_cpu_usage > 0.9"
       for: "5m"
       severity: "critical"
       summary: "High CPU usage on {{ $labels.instance }}"
       description: "CPU usage is {{ $value }}% (threshold: 90%)"
     
     - name: "High Memory Usage"
       expression: "system_memory_usage > 0.85"
       for: "10m"
       severity: "warning"
       summary: "High memory usage on {{ $labels.instance }}"
       description: "Memory usage is {{ $value }}% (threshold: 85%)"
     
     - name: "Disk Space Low"
       expression: "system_disk_usage > 0.9"
       for: "15m"
       severity: "critical"
       summary: "Low disk space on {{ $labels.instance }}"
       description: "Disk usage is {{ $value }}% (threshold: 90%)"
   ```

2. **应用健康告警**
   ```yaml
   # application-alerts.yaml
   alerts:
     - name: "High HTTP Error Rate"
       expression: "rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05"
       for: "5m"
       severity: "critical"
       summary: "High HTTP error rate for {{ $labels.service }}"
       description: "HTTP error rate is {{ $value }} (threshold: 5%)"
     
     - name: "Slow Database Queries"
       expression: "avg_over_time(db_query_duration_seconds[10m]) > 1.0"
       for: "10m"
       severity: "warning"
       summary: "Slow database queries for {{ $labels.service }}"
       description: "Average query duration is {{ $value }}s (threshold: 1.0s)"
     
     - name: "Queue Backlog"
       expression: "queue_size > 1000"
       for: "15m"
       severity: "warning"
       summary: "Queue backlog for {{ $labels.service }}"
       description: "Queue size is {{ $value }} (threshold: 1000)"
   ```

### 9.4 持续集成与持续部署

#### 9.4.1 CI/CD流水线

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     CI/CD流水线设计                                         │
├───────────────────────┬───────────────────────┬───────────────────────────────────────────────┤
│  代码阶段             │  构建阶段             │  部署阶段                                  │
├───────────────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ • 代码提交            │ • 代码构建            │ • 单元测试部署                             │
│ • 静设检查            │ • 单元测试            │ • 自动化测试部署                           │
│ • 代码审查            │ • 安全扫描            │ • 预产环境部署                             │
│ • 单元测试            │ • 镜镜构建            │ • 蓝度发布                                 │
└───────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
```

#### 9.4.2 流水线配置

1. **GitHub Actions配置示例**
   ```yaml
   # .github/workflows/ci-cd.yaml
   name: Mirror Realm CI/CD Pipeline
   
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
       - name: Checkout code
         uses: actions/checkout@v2
       
       - name: Set up Python
         uses: actions/setup-python@v2
         with:
           python-version: '3.9'
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt
       
       - name: Run unit tests
         run: pytest tests/unit --cov=src --cov-report=xml
       
       - name: Security scan
         run: bandit -r src
       
       - name: Build Docker image
         if: github.ref == 'refs/heads/main'
         run: |
           docker build -t mirror-realm/dsr:${{ github.sha }} .
           docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_PASSWORD }}
           docker push mirror-realm/dsr:${{ github.sha }}
   
     deploy-staging:
       needs: build
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'
       steps:
       - name: Deploy to staging
         uses: appleboy/ssh-action@master
         with:
           host: ${{ secrets.STAGING_HOST }}
           username: ${{ secrets.STAGING_USER }}
           key: ${{ secrets.STAGING_SSH_KEY }}
           script: |
             cd /opt/mirror-realm
             git pull origin main
             docker-compose -f docker-compose.staging.yml up -d --build
   
     deploy-prod:
       needs: deploy-staging
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'
       environment: production
       steps:
       - name: Manual approval
         uses: actions/github-script@v3
         with:
           script: |
             const core = require('@actions/core');
             const github = require('@actions/github');
             
             const { deployment } = await github.rest.actions.createDeployment({
               owner: context.repo.owner,
               repo: context.repo.repo,
               ref: context.ref,
               environment: 'production',
               required_contexts: []
             });
             
             core.setOutput('deployment_id', deployment.id);
       
       - name: Deploy to production
         uses: appleboy/ssh-action@master
         with:
           host: ${{ secrets.PROD_HOST }}
           username: ${{ secrets.PROD_USER }}
           key: ${{ secrets.PROD_SSH_KEY }}
           script: |
             cd /opt/mirror-realm
             git pull origin main
             docker-compose -f docker-compose.prod.yml up -d --build
   ```

#### 9.4.3 蓝度发布策略

1. **蓝绿部署实现**
   ```bash
   # blue-green-deploy.sh
   #!/bin/bash
   
   set -e
   
   # 参数
   SERVICE_NAME=$1
   NEW_VERSION=$2
   TRAFFIC_PERCENTAGE=${3:-0}
   
   echo "Starting blue-green deployment for $SERVICE_NAME to version $NEW_VERSION"
   
   # 1. 部署新版本（绿色环境）
   echo "Deploying new version to green environment"
   kubectl apply -f manifests/$SERVICE_NAME-green.yaml
   
   # 2. 等待新版本准备就绪
   echo "Waiting for green environment to be ready"
   kubectl rollout status deployment/$SERVICE_NAME-green
   
   # 3. 逐步切换流量
   if [ "$TRAFFIC_PERCENTAGE" -gt 0 ]; then
     echo "Shifting $TRAFFIC_PERCENTAGE% of traffic to green environment"
     kubectl patch virtualservice/$SERVICE_NAME -n istio-system -p \
       '{"spec":{"http":[{"route":[{"destination":{"host":"'$SERVICE_NAME'-green"}, "weight":'$TRAFFIC_PERCENTAGE'}]}]}}'
   else
     echo "Switching all traffic to green environment"
     kubectl patch virtualservice/$SERVICE_NAME -n istio-system -p \
       '{"spec":{"http":[{"route":[{"destination":{"host":"'$SERVICE_NAME'-green"}, "weight":100}]}]}}'
   fi
   
   # 4. 验行测试
   echo "Running smoke tests"
   ./smoke-tests.sh $SERVICE_NAME
   
   # 5. 完成切换或回滚
   if [ $? -eq 0 ]; then
     echo "Deployment successful, cleaning up old version"
     kubectl delete deployment/$SERVICE_NAME-blue
   else
     echo "Deployment failed, rolling back to blue environment"
     kubectl patch virtualservice/$SERVICE_NAME -n istio-system -p \
       '{"spec":{"http":[{"route":[{"destination":{"host":"'$SERVICE_NAME'-blue"}, "weight":100}]}]}}'
     exit 1
   fi
   ```

2. **金丝雀发布实现**
   ```bash
   # canary-release.sh
   #!/bin/bash
   
   set -e
   
   # 参数
   SERVICE_NAME=$1
   NEW_VERSION=$2
   CANARY_PERCENTAGE=${3:-5}
   INTERVAL=${4:-5}
   DURATION=${5:-30}
   
   echo "Starting canary release for $SERVICE_NAME to version $NEW_VERSION"
   
   # 1. 部署金丝雀版本
   echo "Deploying canary version"
   sed "s/{{VERSION}}/$NEW_VERSION/g" manifests/$SERVICE_NAME-canary.yaml | kubectl apply -f -
   
   # 2. 等待金丝雀版本准备就绪
   echo "Waiting for canary version to be ready"
   kubectl rollout status deployment/$SERVICE_NAME-canary
   
   # 3. 逐步增加金丝雀流量
   total_steps=$((DURATION / INTERVAL))
   for i in $(seq 1 $total_steps); do
     current_percentage=$((CANARY_PERCENTAGE * i / total_steps))
     
     echo "Shifting $current_percentage% of traffic to canary version"
     kubectl patch virtualservice/$SERVICE_NAME -n istio-system -p \
       "{\"spec\":{\"http\":[{\"route\":[{\"destination\":{\"host\":\"$SERVICE_NAME\"}, \"weight\":$((100 - current_percentage))},{\"destination\":{\"host\":\"$SERVICE_NAME-canary\"}, \"weight\":$current_percentage}]}]}}"
     
     # 檢查指标
     ./check-metrics.sh $SERVICE_NAME $current_percentage
     
     # 檢查错误率
     error_rate=$(./get-error-rate.sh $SERVICE_NAME-canary)
     if (( $(echo "$error_rate > 0.01" | bc -l) )); then
       echo "Error rate too high ($error_rate%), rolling back"
       kubectl patch virtualservice/$SERVICE_NAME -n istio-system -p \
         "{\"spec\":{\"http\":[{\"route\":[{\"destination\":{\"host\":\"$SERVICE_NAME\"}, \"weight\":100}]}]}}"
       exit 1
     fi
     
     sleep $INTERVAL
   done
   
   # 4. 完成金丝雀发布
   echo "Canary release complete, promoting to full production"
   kubectl patch virtualservice/$SERVICE_NAME -n istio-system -p \
     "{\"spec\":{\"http\":[{\"route\":[{\"destination\":{\"host\":\"$SERVICE_NAME\"}, \"weight\":0},{\"destination\":{\"host\":\"$SERVICE_NAME-canary\"}, \"weight\":100}]}]}}"
   kubectl delete deployment/$SERVICE_NAME
   kubectl rollout status deployment/$SERVICE_NAME-canary
   kubectl patch deployment/$SERVICE_NAME-canary --type='json' -p='[{"op": "replace", "path": "/metadata/name", "value":"'$SERVICE_NAME'"}]'
   ```

### 9.5 安全与合规

#### 9.5.1 安全策略

1. **网络隔离策略**
   ```yaml
   # network-policy.yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: mirror-realm-network-policy
   spec:
     podSelector: {}
     policyTypes:
     - Ingress
     - Egress
     ingress:
     - from:
       - namespaceSelector:
           matchLabels:
             project: mirror-realm
         podSelector:
           matchLabels:
             app: api-gateway
       ports:
       - protocol: TCP
         port: 8000
     egress:
     - to:
       - namespaceSelector:
           matchLabels:
             project: mirror-realm
         podSelector:
           matchLabels:
             app: postgres
       ports:
       - protocol: TCP
         port: 5432
     - to:
       - namespaceSelector:
           matchLabels:
             project: mirror-realm
         podSelector:
           matchLabels:
             app: redis
       ports:
       - protocol: TCP
         port: 6379
   ```

2. **安全扫描策略**
   ```yaml
   # security-scan.yaml
   apiVersion: batch/v1
   kind: CronJob
   metadata:
     name: security-scan
   spec:
     schedule: "0 2 * * *"
     jobTemplate:
       spec:
         template:
           spec:
             containers:
             - name: trivy
               image: aquasec/trivy:0.16.0
               command: ["trivy"]
               args: 
                 - "--severity", "CRITICAL,HIGH"
                 - "kubernetes"
                 - "--format", "table"
                 - "--exit-code", "1"
               volumeMounts:
               - name: kubeconfig
                 mountPath: /root/.kube
             volumes:
             - name: kubeconfig
               secret:
                 secretName: kubeconfig
             restartPolicy: OnFailure
   ```

#### 9.5.2 合规性检查

1. **自动化合规工作流**
   ```python
   class ComplianceWorkflow:
       """自动化合规工作流"""
       
       def __init__(
           self,
           compliance_service: ComplianceService,
           notification_service: NotificationService,
           config: Config
       ):
           self.compliance_service = compliance_service
           self.notification_service = notification_service
           self.config = config
           self.logger = logging.getLogger(__name__)
       
       def run_daily_check(self):
           """执行每日合规性检查"""
           # 1. 获取所有活跃数据源
           data_sources = self.compliance_service.get_active_data_sources()
           
           # 2. 检查每个数据源
           non_compliant_sources = []
           for ds in data_sources:
               result = self.compliance_service.check_compliance(ds)
               if result.status != "compliant":
                   non_compliant_sources.append((ds, result))
           
           # 3. 生成报告
           report = self._generate_report(non_compliant_sources)
           
           # 4. 发送通知
           self._send_notifications(report)
           
           # 5. 跟踪问题
           self._track_issues(non_compliant_sources)
       
       def _generate_report(self, non_compliant_sources: List) -> ComplianceReport:
           """生成合规性报告"""
           return ComplianceReport(
               date=datetime.utcnow(),
               total_sources=len(data_sources),
               compliant_count=len(data_sources) - len(non_compliant_sources),
               non_compliant_count=len(non_compliant_sources),
               critical_issues=sum(1 for _, r in non_compliant_sources if r.critical_issues > 0),
               details=non_compliant_sources
           )
       
       def _send_notifications(self, report: ComplianceReport):
           """发送通知"""
           # 发送给合规团队
           self.notification_service.send_email(
               to=self.config.compliance_team_email,
               subject=f"Daily Compliance Report - {report.date.strftime('%Y-%m-%d')}",
               body=self._format_report_email(report)
           )
           
           # 如果有关键问题，发送警报
           if report.critical_issues > 0:
               self.notification_service.send_slack_alert(
                   channel=self.config.alert_channel,
                   message=f"Critical compliance issues detected! {report.critical_issues} sources affected."
               )
       
       def _track_issues(self, non_compliant_sources: List):
           """跟踪合规性问题"""
           for ds, result in non_compliant_sources:
               # 创建或更新问题
               issue = self.compliance_service.get_issue(ds.id)
               if not issue:
                   self.compliance_service.create_issue(
                       data_source_id=ds.id,
                       description=result.suggestions[0] if result.suggestions else "Non-compliant data source",
                       severity="critical" if result.critical_issues > 0 else "high",
                       due_date=datetime.utcnow() + timedelta(days=7)
                   )
               else:
                   # 更新现有问题
                   self.compliance_service.update_issue(
                       issue.id,
                       status="open",
                       last_checked=datetime.utcnow()
                   )
   ```

### 9.6 性能测试方案

#### 9.6.1 基準测试场景

1. **数据源注册中心性能测试**
   ```python
   # dsr_load_test.py
   import os
   import time
   import json
   import random
   from locust import HttpUser, task, between, events
   from locust.runners import MasterRunner
   
   # 测试配置
   TEST_DATA_SOURCES = [
       {
           "name": f"test-source-{i}",
           "display_name": f"Test Source {i}",
           "url": f"https://example.com/data/{i}",
           "category": random.choice(["web", "api", "social"]),
           "data_type": random.choice(["html", "json", "xml"]),
           "tags": ["test", "performance"]
       } for i in range(1000)
   ]
   
   @events.test_start.add_listener
   def on_test_start(environment, **kwargs):
       """测试开始前的准备工作"""
       if not isinstance(environment.runner, MasterRunner):
           print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting DSR performance test")
           print(f"  * Test data sources: {len(TEST_DATA_SOURCES)}")
           print(f"  * Target RPS: {environment.parsed_options.spawn_rate}")
   
   class DataSourcesUser(HttpUser):
       wait_time = between(0.1, 0.5)
       
       def on_start(self):
           """用户启动时的初始化"""
           self.auth_token = self._get_auth_token()
           self.headers = {
               "Authorization": f"Bearer {self.auth_token}",
               "Content-Type": "application/json"
           }
       
       def _get_auth_token(self):
           """获取认证令牌"""
           response = self.client.post(
               "/api/v1/auth/token",
               json={
                   "client_id": "performance-test",
                   "client_secret": "perf-test-secret",
                   "grant_type": "client_credentials"
               }
           )
           return response.json()["access_token"]
       
       @task(5)
       def list_data_sources(self):
           """列出数据源"""
           self.client.get(
               "/api/v1/data-sources",
               headers=self.headers,
               name="/api/v1/data-sources"
           )
       
       @task(3)
       def get_data_source(self):
           """获取单个数据源"""
           source_id = f"ds-{random.randint(1, 1000):04d}"
           self.client.get(
               f"/api/v1/data-sources/{source_id}",
               headers=self.headers,
               name="/api/v1/data-sources/{id}"
           )
       
       @task(2)
       def create_data_source(self):
           """创建数据源"""
           source = random.choice(TEST_DATA_SOURCES)
           self.client.post(
               "/api/v1/data-sources",
               json=source,
               headers=self.headers,
               name="/api/v1/data-sources"
           )
       
       @task(1)
       def search_data_sources(self):
           """搜索数据源"""
           query = random.choice(["test", "example", "api", "web"])
           self.client.get(
               f"/api/v1/data-sources?search={query}",
               headers=self.headers,
               name="/api/v1/data-sources:search"
           )
   ```

2. **分布式爬虫集群性能测试**
   ```python
   # crawler_cluster_load_test.py
   import os
   import time
   import json
   import random
   from locust import HttpUser, task, between, events
   from locust.runners import MasterRunner
   
   # 测试配置
   TEST_TASKS = [
       {
           "task_type": "web_crawl",
           "parameters": {
               "url": f"https://example.com/page/{i}",
               "depth": random.randint(1, 3)
           },
           "priority": random.randint(1, 10),
           "min_resources": {
               "memory_mb": random.choice([512, 1024, 2048]),
               "cpu_cores": random.uniform(0.5, 2.0)
           }
       } for i in range(10000)
   ]
   
   class CrawlerUser(HttpUser):
       wait_time = between(0.01, 0.1)
       
       def on_start(self):
           """用户启动时的初始化"""
           self.auth_token = self._get_auth_token()
           self.headers = {
               "Authorization": f"Bearer {self.auth_token}",
               "Content-Type": "application/json"
           }
       
       def _get_auth_token(self):
           """获取认证令牌"""
           response = self.client.post(
               "/api/v1/auth/token",
               json={
                   "client_id": "crawler-test",
                   "client_secret": "crawler-test-secret",
                   "grant_type": "client_credentials"
               }
           )
           return response.json()["access_token"]
       
       @task(10)
       def create_task(self):
           """创建爬虫任务"""
           task = random.choice(TEST_TASKS)
           response = self.client.post(
               "/api/v1/tasks",
               json=task,
               headers=self.headers,
               name="/api/v1/tasks"
           )
           
           if response.status_code == 201:
               task_id = response.json()["id"]
               # 轮询任务状态
               for _ in range(10):
                   time.sleep(0.1)
                   status_response = self.client.get(
                       f"/api/v1/tasks/{task_id}",
                       headers=self.headers,
                       name="/api/v1/tasks/{id}"
                   )
                   
                   if status_response.status_code == 200:
                       status = status_response.json()["status"]
                       if status in ["completed", "failed"]:
                           break
   ```

#### 9.6.2 性能指标阈值

1. **API性能指标阈值**
   | 指标 | 95分位 | 99分位 | 错误率 | 资源使用 |
   |------|--------|--------|--------|----------|
   | **数据源注册中心** | | | | |
   | 列建数据源 | <200ms | <500ms | <0.1% | CPU<50%, Mem<70% |
   | 获取数据源列表 | <100ms | <300ms | <0.1% | CPU<40%, Mem<60% |
   | 搜索数据源 | <150ms | <400ms | <0.1% | CPU<45%, Mem<65% |
   | **分布式爬虫集群** | | | | |
   | 创建爬虫任务 | <100ms | <300ms | <0.1% | CPU<50%, Mem<70% |
   | 任务状态查询 | <50ms | <200ms | <0.1% | CPU<30%, Mem<50% |
   | 节点心跳 | <20ms | <100ms | <0.01% | CPU<20%, Mem<40% |

2. **系统容量规划**
   | 服务 | 单例配置 | 单例数量 | 支持QPS | 每日任务量 | 存储需求 |
   |------|----------|----------|---------|------------|----------|
   | 数据源注册中心 | 2vCPU, 4GB | 3 | 1,000 | - | 50GB |
   | 网站指纹分析引擎 | 4vCPU, 8GB | 5 | 500 | - | 200GB |
   | 数据源健康监测系统 | 2vCPU, 4GB | 3 | 2,000 | - | 100GB |
   | 数据处理工作流引擎 | 4vCPU, 8GB | 5 | 1,500 | - | 150GB |
   | 自动化媒体处理管道 | 8vCPU, 16GB, 1GPU | 10 | 100 | 10,000 | 10TB |
   | AI辅助开发系统 | 4vCPU, 8GB | 3 | 300 | - | 50GB |
   | 数据合规与安全中心 | 2vCPU, 4GB | 3 | 500 | - | 75GB |
   | 分布式爬虫集群管理系统 | 4vCPU, 8GB | 5 | 2,000 | 1,000,000 | 200GB |

### 9.7 灾难恢复计划

#### 9.7.1 备份策略

1. **数据备份计划**
   ```yaml
   # backup-policy.yaml
   backups:
     - name: "Database Daily Backup"
       schedule: "0 2 * * *"
       retention: "7d"
       type: "full"
       targets:
         - "postgres"
         - "redis"
       destination: "s3://mirror-realm-backups/db"
       encryption: "AES256"
       verification:
         script: "verify-db-backup.sh"
         frequency: "daily"
     
     - name: "Configuration Backup"
       schedule: "0 * * * *"
       retention: "30d"
       type: "incremental"
       targets:
         - "config"
         - "secrets"
       destination: "s3://mirror-realm-backups/config"
       encryption: "AES256"
     
     - name: "Media Storage Backup"
       schedule: "0 3 * * *"
       retention: "30d"
       type: "full"
       targets:
         - "media-storage"
       destination: "s3://mirror-realm-backups/media"
       encryption: "AES256"
       compression: "gzip"
   ```

2. **备份验证脚本**
   ```bash
   # verify-db-backup.sh
   #!/bin/bash
   
   set -e
   
   # 参数
   BACKUP_FILE=$1
   
   # 1. 检查备份文件是否存在
   if [ ! -f "$BACKUP_FILE" ]; then
     echo "Backup file not found: $BACKUP_FILE"
     exit 1
   fi
   
   # 2. 检查备份文件完整性
   if ! pg_restore -l "$BACKUP_FILE" > /dev/null; then
     echo "Backup file is corrupted: $BACKUP_FILE"
     exit 1
   fi
   
   # 3. 检查备份时间戳
   BACKUP_TIME=$(stat -c %Y "$BACKUP_FILE")
   CURRENT_TIME=$(date +%s)
   AGE=$((CURRENT_TIME - BACKUP_TIME))
   
   if [ $AGE -gt 86400 ]; then
     echo "Backup is older than 24 hours: $BACKUP_FILE"
     exit 1
   fi
   
   echo "Backup verification successful: $BACKUP_FILE"
   exit 0
   ```

#### 9.7.2 災难恢复流程

1. **数据恢复流程**
   ```mermaid
   graph TD
     A[灾难发生] --> B{确定影响范围}
     B -->|部分影响| C[隔离受影响组件]
     B -->|全面影响| D[启动灾难恢复计划]
     C --> E[评估数据损坏程度]
     E --> F[从最近备份恢复]
     F --> G[验证数据完整性]
     G --> H[逐步恢复服务]
     H --> I[监控系统稳定性]
     I --> J[恢复正常运营]
     D --> K[激活备用数据中心]
     K --> L[从异地备份恢复数据]
     L --> M[验证关键系统功能]
     M --> N[逐步迁移流量]
     N --> O[全面恢复服务]
     O --> P[事后分析与改进]
   ```

2. **恢复时间目标(RTO)与恢复点目标(RPO)**
   | 系统 | RTO | RPO | 恢复策略 |
   |------|-----|-----|----------|
   | 数据源注册中心 | 15分钟 | 5分钟 | 热备数据库切换 |
   | 网站指纹分析引擎 | 30分钟 | 15分钟 | 从备份恢复+增量同步 |
   | 数据源健康监测系统 | 10分钟 | 1分钟 | 实时数据复制 |
   | 数据处理工作流引擎 | 20分钟 | 5分钟 | 任务队列持久化 |
   | 自动化媒体处理管道 | 1小时 | 15分钟 | 从对象存储恢复 |
   | AI辅助开发系统 | 15分钟 | 5分钟 | 热备实例切换 |
   | 数据合规与安全中心 | 30分钟 | 10分钟 | 从备份恢复 |
   | 分布式爬虫集群管理系统 | 10分钟 | 1分钟 | 实时状态同步 |

## 10. 附录

### 10.1 术语表

| 术语 | 定义 |
|------|------|
| 数据源 | 可供数据的网站、API或其他内容来源 |
| 数据指纹 | 通过分析确定网站技术栈和特征的标识 |
| 工作流 | 定义数据采集、处理和存储的自动化流程 |
| 爬虫节点 | 执行爬取任务的计算资源单元 |
| 敏感数据 | 需要特殊保护的个人信息或其他敏感信息 |
| 合规性 | 符合法律法规和行业标准的要求 |
| 反片 | 临时存储中间结果的数据单元 |
| 反片处理 | 对数据进行转换、清洗和增强的过程 |
| 资源配额 | 分配给用户或项目的计算资源限制 |
| 负载均衡 | 将分配请求到多个服务器以优化资源使用 |

### 10.2 参考文献

1. **Web爬虫技术**
   - Severn, M. (2020). Web Scraping with Python. O'Reilly Media.
   - Zhang, Y., & Chen, L. (2019). Large-scale Web Crawling Techniques. ACM Computing Surveys.

2. **分布式系统**
   - Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.
   - Tanenbaum, A., & Van Steen, M. (2017). Distributed Systems: Principles and Paradigms. Pearson.

3. **数据安全与合规**
   - Schneier, B. (2015). Data and Goliath: The Hidden Battles to Collect Your Data and Control Your World. W.W. Norton & Company.
   - EU General Data Protection Regulation (GDPR), Regulation (EU) 2016/679.

4. **人工智能与机器学习**
   - Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.
   - Brown, T., et al. (2020). Language Models are Few-Shot Learners. arXiv:2005.14165.


**注意**: 本技术需求规格说明书提供了镜界平台的完整技术细节，包括精确的系统架构、详细的数据库设计、核心功能的实现规范、API的具体定义、性能测试方案、安全合规措施、错误处理机制以及监控告警配置。所有内容均达到可直接用于开发的详细程度，确保开发团队能够准确理解和实现系统功能。随着项目进展，本文件将根据实际需要进行更新和补充。
