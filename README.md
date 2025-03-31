# DataScience-agent
## 基于mcp和garphrag制作的kaggle data science agent
尽管基于大型语言模型 （LLM） 的代理在自动化数据科学任务方面取得了广泛的成功，以 ![DS-Agent](https://github.com/guosyjlu/DS-Agent)为例，它利用了 LLM 代理和基于案例的推理 （CBR），可以灵活地利用 Kaggle 的专业知识，并通过反馈机制促进持续的性能改进。但是，仍然需要人类处理大部分工作，agent只负责生成对应的代码。由于，最近agent技术取得了很大的突破，使用mcp和graphrag制作数据科学自动处理的工作流成为可能。

DataScience-mg-agent通过Graphrag检索人类优秀案例，辅助agent回答问题。同时，本agent还配有联网搜索、本地知识库搜索、本地文件操作、sql处理、自动python代码生成与执行、试验报告生成等功能。将过去agent代码生成,人类debug的模式改变为从开发阶段开始就由agent自己规划策略、自己使用工具、自己执行代码、自己总结报告的全新模式，从而显着降低了人类的工作量，解放双手。同时，最后我们还对agnet的成功案例进行了评估。

## GraphRag/mcp
GraphRag适合用在总结性问题上，

![图片](https://github.com/user-attachments/assets/a70918e7-2b52-4bfb-a103-719a3e56c3d5)

## example
### 题目
```txt
You are solving this data science tasks of binary classification: 
The dataset presented here (the Software Defects Dataset) comprises a lot of numerical features. We have splitted the dataset into three parts of train, valid and test. Your task is to predict the defects item, which is a binary label with 0 and 1. The evaluation metric is the area under ROC curve (AUROC).
We provide an overall pipeline in train.py. Now fill in the provided train.py script to train a binary classification model to get a good performance on this task.

```
### 报告总结
![生成的文件](https://huihuihenqiang.github.io/article/THPML%20book/report.html)


##
评估 我们选择了 30 个数据科学任务，具有三种数据模态，包括文本、时间序列和表格数据，以及回归和分类两种基本任务类型。 评估指标。我们主要从三个方面来评价智能体的能力： （1） 完成构建 ML 模型。我们采用成功率，即代理是否能在固定的步骤数内以无错误的方式构建 ML 模型。 （2） 构建的 ML 模型的性能。我们使用最佳排名作为评估指标来评估代理的自动化数据科学能力。 （3） 资源成本。由于我们在这项工作中主要使用闭源 LLM，因此我们将消耗的资金用于评估资源成本。 




![屏幕截图 2025-03-31 173832](https://github.com/user-attachments/assets/ba52f560-d462-4168-b20e-5d6b3022af91)



| Model/Agent       | JS  | HR  | BPP | WR  | DAG | BQ  | TFC | WTH | ELE | SRC | UGL | HB  | CA  | CS  | MH  | SS  | CO  | SD  | Avg |
|-------------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| zero-shot         | 6.0 | 22.6| 15.0| 25.6| 15.1| 13.1| 17.3| 14.4| 14.4| 20.0| 13.0| 23.0| 29.0| 19.3| 7.6 | 2.0 | 37.0| 19.5| 17.1|
| one-shot          | 36.7| 31.8| 35.0| 29.0| 29.4| 32.0| 29.0| 32.0| 30.0| 37.3| 45.7| 33.6| 1.0 | 15.3| 23.2| 17.9| 28.3| 28.0| 28.2|
| DS-Agent          | 35.1| 24.4| 13.8| 26.6| 29.6| 28.8| 23.1| 30.1| 26.6| 26.7| 41.6| 36.7| 29.1| 21.9| 35.3| 28.9| 21.4| 23.2| 28.0|
| DS-MGAgent        | 18.6| 16.0| 14.6| 5.2 | 6.2 | 18.8| 15.7| 6.3 | 8.1 | 20.0| 11.4| 21.2| 14.0| 32.6| 14.5| 8.2 | 13.0| 12.4| 12.7|


Cite：本项目的所有数据集，包括benchmark和cbr中的案例都来自于以下的论文。

@InProceedings{DS-Agent,
  title = 	 {{DS}-Agent: Automated Data Science by Empowering Large Language Models with Case-Based Reasoning},
  author =       {Guo, Siyuan and Deng, Cheng and Wen, Ying and Chen, Hechang and Chang, Yi and Wang, Jun},
  booktitle = 	 {Proceedings of the 41st International Conference on Machine Learning},
  pages = 	 {16813--16848},
  year = 	 {2024},
  volume = 	 {235},
  series = 	 {Proceedings of Machine Learning Research},
  publisher =    {PMLR}
}
