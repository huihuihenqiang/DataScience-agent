# DataScience-agent
基于mcp和garphrag制作的kaggle data science自动解决agent

在这项工作中，我们研究了基于大型语言模型 （LLM） 的代理在自动化数据科学任务方面的潜力，目的是理解任务要求，然后构建和训练最适合的机器学习模型。尽管他们取得了广泛的成功，但现有的 LLM 代理在这种情况下会因生成不合理的实验计划而受到阻碍。为此，我们提出了 DS-Agent，这是一种利用 LLM 代理和基于案例的推理 （CBR） 的新型自动框架。在开发阶段，DS Agent 遵循 CBR 框架构建自动迭代流水线，可以灵活地利用 Kaggle 的专业知识，并通过反馈机制促进持续的性能改进。此外，DS-Agent 通过简化的 CBR 范式实现了低资源部署阶段，以将过去从开发阶段开始的成功解决方案改编为直接代码生成，从而显着降低了对 LLM 基础功能的需求。根据经验，带有 GPT-4 的 DS-Agent 在开发阶段实现了 100% 的成功率，同时在部署阶段与其他 LLM 相比，平均一次通过率提高了 36%。在这两个阶段，DS-Agent 在性能方面都取得了最佳排名，使用 GPT-1.60 每次运行的成本分别为 0.13 USD 和 4 USD。我们的数据和代码在 https：//github.com/guosyjlu/DS-Agent 上开源。
graph
![图片](https://github.com/user-attachments/assets/adf52cde-1f16-4b52-a98b-3e51fe04da06)


mcp





评估
我们选择了 30 个数据科学任务，具有三种数据模态，包括文本、时间序列和表格数据，以及回归和分类两种基本任务类型。
评估指标。我们主要从三个方面来评价智能体的能力：
（1） 完成构建 ML 模型。我们采用成功率，即代理是否能在固定的步骤数内以无错误的方式构建 ML 模型。
（2） 构建的 ML 模型的性能。我们使用最佳排名作为评估指标来评估代理的自动化数据科学能力。
（3） 资源成本。由于我们在这项工作中主要使用闭源 LLM，因此我们将消耗的资金用于评估资源成本。
![图片](https://github.com/user-attachments/assets/f8e338ab-9d60-4352-944d-496126331db1)


| Model/Agent       | JS  | HR  | BPP | WR  | DAG | BQ  | TFC | WTH | ELE | SRC | UGL | HB  | CA  | CS  | MH  | SS  | CO  | SD  | Avg |
|-------------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| one-shot          | 37.0| 35.0| 35.0| 31.0| 35.0| 32.0| 29.0| 32.0| 30.0| 44.0| 54.0| 46.0| 73.1| 66.6| 65.8| 63.6| 33.7| 72.0| 45.3|
| zero-shot         | 37.0| 35.0| 30.1| 28.6| 27.1| 28.3| 27.1| 28.1| 28.1| 33.1| 48.4| 24.1| 29.0| 35.0| 28.8| 35.7| 25.2| 42.3| 30.8|
| DS-Agent          | 6.0 | 22.6| 15.0| 25.6| 15.1| 13.1| 17.3| 14.4| 14.4| 20.0| 13.0| 23.0| 29.0| 19.3| 7.6 | 2.0 | 37.0| 19.5| 17.1|
| DS-MGAgent        | 18.6| 17.0| 14.6| 25.2| 6.2 | 18.8| 15.7| 6.3 | 8.1 | 20.0| 11.4| 21.2| 19.0| 32.6| 14.5| 8.2 | 13.0| 12.4| 12.7|




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
