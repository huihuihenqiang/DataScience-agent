# DataScience-agent
基于mcp和garphrag制作的kaggle data science自动解决agent





评估
我们选择了 30 个数据科学任务，具有三种数据模态，包括文本、时间序列和表格数据，以及回归和分类两种基本任务类型。
评估指标。我们主要从三个方面来评价智能体的能力：
（1） 完成构建 ML 模型。我们采用成功率，即代理是否能在固定的步骤数内以无错误的方式构建 ML 模型。
（2） 构建的 ML 模型的性能。我们使用最佳排名作为评估指标来评估代理的自动化数据科学能力。
（3） 资源成本。由于我们在这项工作中主要使用闭源 LLM，因此我们将消耗的资金用于评估资源成本。
![图片](https://github.com/user-attachments/assets/f8e338ab-9d60-4352-944d-496126331db1)




Cite：本项目的所有数据集，包括benchmark和cbr中的案例都来自于以下的论文。
```md
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
```
