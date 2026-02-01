# 量化策略学习指南

## 📚 推荐学习的开源项目

### 1. 综合性量化交易库

| 项目 | 链接 | 特点 |
|------|------|------|
| **je-suis-tm/quant-trading** | https://github.com/je-suis-tm/quant-trading | 23+策略实现，VIX、模式识别、Monte Carlo、期权策略等 |
| **Nikhil-Adithyan/Algorithmic-Trading-with-Python** | https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Python | Python算法交易库，包含23个程序 |
| **wilsonfreitas/awesome-quant** | https://github.com/wilsonfreitas/awesome-quant | 量化资源大合集，库、工具、资源导航 |
| **chrisconlan/algorithmic-trading-with-python** | https://github.com/chrisconlan/algorithmic-trading-with-python | 《Algorithmic Trading with Python》配套代码 |
| **nautechsystems/nautilus_trader** | https://github.com/nautechsystems/nautilus_trader | 高性能生产级量化交易平台 |

### 2. 策略类型学习

#### 📈 趋势跟踪策略 (Momentum)

**核心思想**: 顺势而为，买入上涨的资产，卖出下跌的资产

**典型指标**:
- MACD (移动平均收敛散度)
- ADX (平均方向性指数)
- 移动平均线交叉 (MA Crossover)

**学习资源**:
```
GitHub搜索关键词: momentum-trading-strategy, trend-following
```

#### 🔄 均值回归策略 (Mean Reversion)

**核心思想**: 价格会围绕均值波动，当偏离均值时反向操作

**典型指标**:
- RSI (相对强弱指数)
- 布林带 (Bollinger Bands)
- Z-Score 标准化

**学习资源**:
- https://machinelearning-basics.com/mean-reversion-trading-strategy-using-python/
- https://eodhd.com/financial-academy/backtesting-strategies-examples/backtesting-a-killer-mean-reversion-trading-strategy-with-python
- https://www.quantifiedstrategies.com/mean-reversion-trading-strategy/

**代码示例**:
```python
import pandas as pd
import numpy as np

def mean_reversion_strategy(prices, window=20, threshold=2):
    """均值回归策略"""
    # 计算移动平均和标准差
    ma = prices.rolling(window).mean()
    std = prices.rolling(window).std()
    
    # 计算Z-Score
    z_score = (prices - ma) / std
    
    # 交易信号
    signal = np.where(z_score > threshold, -1,  # 价格高于均值，做空
                   np.where(z_score < -threshold, 1, 0))  # 价格低于均值，做多
    
    return signal
```

#### 🔗 统计套利策略 (Statistical Arbitrage)

**核心思想**: 利用相关资产的价格偏离进行套利

**典型方法**:
- 协整检验 (Cointegration Test)
- 配对交易 (Pairs Trading)
- 因子模型 (Factor Model)

**学习资源**:
- https://hudsonthames.org/definitive-guide-to-pairs-trading/
- https://blog.quantinsti.com/pairs-trading-basics/
- https://github.com/QuantConnect/Research/blob/master/Analysis/05%20Pairs%20Trading%20Strategy%20Based%20on%20Cointegration.ipynb

**代码示例**:
```python
from statsmodels.tsa.stattools import coint
import pandas as pd

def find_cointegrated_pairs(data):
    """寻找协整配对"""
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                score, pvalue, _ = coint(data.iloc[:, i], data.iloc[:, j])
                score_matrix[i, j] = score
                pvalue_matrix[i, j] = pvalue
    
    return score_matrix, pvalue_matrix
```

#### 🎯 高频交易策略 (HFT)

**核心思想**: 利用微小价格波动和速度优势获利

**典型策略**:
- 做市 (Market Making)
- 事件驱动 (Event-Driven)
- 套利 (Arbitrage)

**学习资源**:
- https://github.com/je-suis-tm/quant-trading (包含做市策略)
- https://www.bis.org/publ/work955.pdf (BIS研究报告)

#### 💰 网格交易策略 (Grid Trading)

**核心思想**: 在价格上下设置网格，低买高卖

**特点**:
- 适合震荡行情
- 风险较低
- 需要较长时间运行

```python
def grid_trading_strategy(prices, grid_count=10, grid_range=0.1):
    """网格交易策略"""
    grid_levels = np.linspace(
        prices.iloc[0] * (1 - grid_range),
        prices.iloc[0] * (1 + grid_range),
        grid_count
    )
    
    # 在每个网格价位挂单
    for level in grid_levels:
        if level < prices.iloc[0]:
            # 下方网格：买入
            pass
        else:
            # 上方网格：卖出
            pass
    
    return grid_levels
```

### 3. 推荐学习的经典策略

| 策略名称 | 类型 | 复杂度 | 学习优先级 |
|----------|------|--------|------------|
| RSI均值回归 | 均值回归 | ⭐ | ⭐⭐⭐ |
| 布林带交易 | 均值回归 | ⭐ | ⭐⭐⭐ |
| MACD交叉 | 趋势跟踪 | ⭐⭐ | ⭐⭐⭐ |
| 双均线策略 | 趋势跟踪 | ⭐ | ⭐⭐⭐ |
| 配对交易 | 统计套利 | ⭐⭐⭐ | ⭐⭐ |
| 网格交易 | 震荡交易 | ⭐⭐ | ⭐⭐ |
| ATR止损 | 风险管理 | ⭐ | ⭐⭐⭐ |
| 凯利公式 | 资金管理 | ⭐⭐⭐ | ⭐⭐ |

### 4. 必备技能清单

#### 技术技能
- [ ] Python高级编程
- [ ] Pandas数据分析
- [ ] NumPy数值计算
- [ ] Backtrader/Zipline回测框架
- [ ] 概率论与数理统计
- [ ] 时间序列分析

#### 金融知识
- [ ] 市场微观结构
- [ ] 订单簿分析
- [ ] 交易成本模型
- [ ] 风险管理基础
- [ ] 资产定价理论

#### 进阶主题
- [ ] 机器学习在金融中的应用
- [ ] 强化学习交易策略
- [ ] 自然语言处理(情绪分析)
- [ ] 图神经网络(关联分析)

### 5. 学习路径建议

```
第一阶段: 基础 (1-2周)
├── 掌握Python和Pandas
├── 学习技术指标计算
├── 实现简单均线策略
└── 回测框架入门

第二阶段: 策略深化 (2-4周)
├── 深入学习均值回归
├── 掌握配对交易
├── 理解统计套利
└── 优化策略参数

第三阶段: 进阶 (4-8周)
├── 学习机器学习策略
├── 探索深度学习模型
├── 研究强化学习
└── 开发自己的策略

第四阶段: 实战 (持续)
├── 模拟盘测试
├── 实盘小资金验证
├── 策略迭代优化
└── 风险管理完善
```

### 6. 推荐书籍

| 书名 | 作者 | 主题 |
|------|------|------|
| 《Algorithmic Trading with Python》 | Chris Conlan | Python量化实战 |
| 《Advances in Financial Machine Learning》 | Marcos Lopez de Prado | 金融机器学习 |
| 《Quantitative Trading》 | Ernest Chan | 量化交易入门 |
| 《Trading and Exchanges》 | Larry Harris | 市场微观结构 |
| 《Inside the Black Box》 | Rishi K. Narang | 量化基金揭秘 |

### 7. 在线资源

- **QuantConnect**: https://www.quantconnect.com/
- **Backtrader**: https://www.backtrader.com/
- **Zipline**: https://zipline-live.gitbook.io/zipline/
- **Quantopian** (已关闭，但文档丰富)

### 8. 当前项目参考

我们的项目结构:
```
/root/.openclaw/workspace/TestTradeBntoLighter/
├── main.py                    # 主程序
├── execution/
│   └── order_manager.py       # 订单管理
├── telegram_bot.py            # Telegram监控
└── lighter-key.json           # API密钥
```

可以学习的策略:
1. **改进HFT策略**: 添加更精确的订单簿分析
2. **引入机器学习**: 使用LSTM预测价格方向
3. **多策略组合**: 均值回归 + 趋势跟踪组合
4. **风险管理**: 添加ATR止损和仓位管理

---

## 📝 学习计划

### 本周目标
- [ ] 跑通一个简单策略(均线交叉)
- [ ] 理解当前HFT策略代码
- [ ] 学习Backtraker回测框架

### 下周目标
- [ ] 实现配对交易策略
- [ ] 添加机器学习预测模块
- [ ] 优化资金管理

---

*持续更新中...*
