DataScience-agent

基于mcp和garphrag制作的kaggle data science自动解决agent

评估 我们选择了 30 个数据科学任务，具有三种数据模态，包括文本、时间序列和表格数据，以及回归和分类两种基本任务类型。 评估指标。我们主要从三个方面来评价智能体的能力： （1） 完成构建 ML 模型。我们采用成功率，即代理是否能在固定的步骤数内以无错误的方式构建 ML 模型。 （2） 构建的 ML 模型的性能。我们使用最佳排名作为评估指标来评估代理的自动化数据科学能力。 （3） 资源成本。由于我们在这项工作中主要使用闭源 LLM，因此我们将消耗的资金用于评估资源成本。 图片
Model/Agent 	JS 	HR 	BPP 	WR 	DAG 	BQ 	TFC 	WTH 	ELE 	SRC 	UGL 	HB 	CA 	CS 	MH 	SS 	CO 	SD 	Avg
one-shot 	37.0 	35.0 	35.0 	31.0 	35.0 	32.0 	29.0 	32.0 	30.0 	44.0 	54.0 	46.0 	73.1 	66.6 	65.8 	63.6 	33.7 	72.0 	45.3
zero-shot 	37.0 	35.0 	30.1 	28.6 	27.1 	28.3 	27.1 	28.1 	28.1 	33.1 	48.4 	24.1 	29.0 	35.0 	28.8 	35.7 	25.2 	42.3 	30.8
DS-Agent 	6.0 	22.6 	15.0 	25.6 	15.1 	13.1 	17.3 	14.4 	14.4 	20.0 	13.0 	23.0 	29.0 	19.3 	7.6 	2.0 	37.0 	19.5 	17.1
DS-MGAgent 	18.6 	17.0 	14.6 	25.2 	6.2 	18.8 	15.7 	6.3 	8.1 	20.0 	11.4 	21.2 	19.0 	32.6 	14.5 	8.2 	13.0 	12.4 	12.7

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
