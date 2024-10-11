# PERSONALIZED VISUAL INSTRUCTION TUNING
Official Repository of the paper: Personalized Visual Instruct Tuning 
<img width="800" alt="image" src="https://github.com/user-attachments/assets/91a21871-cd8c-4beb-b9d5-ce16a6c1cf1a">

# To Do List
[] Release PVIT-3M dataset [here](https://huggingface.co/datasets/Sterzhang/PVIT-3M).

[] Release scripts for generating PVIT dataset.

[] Release our code for training.

# Introduction
Recent advancements in multimodal large language models (MLLMs) have demonstrated significant progress; however, these models exhibit a notable limitation,
which we refer to as “face blindness”. Specifically, they can engage in general
conversations but fail to conduct personalized dialogues targeting at specific individuals. This deficiency hinders the application of MLLMs in personalized settings,
such as tailored visual assistants on mobile devices, or domestic robots that need
to recognize members of the family. In this paper, we introduce Personalized
Visual Instruction Tuning (PVIT), a novel data curation and training framework
designed to enable MLLMs to identify target individuals within an image and
engage in personalized and coherent dialogues. Our approach involves the development of a sophisticated pipeline that autonomously generates training data
containing personalized conversations. This pipeline leverages the capabilities of
various visual experts, image generation models, and (multi-modal) large language
models. To evaluate the personalized potential of MLLMs, we present a benchmark
called P-Bench, which encompasses various question types with different levels of
difficulty. The experiments demonstrate a substantial personalized performance
enhancement after fine-tuning with our curated dataset.

# Case Study
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/d50fa03f-fdb6-41ff-ab25-806578d29f3e">


# Citation
Our paper is now available at: [https://arxiv.org/abs/2410.07113](https://arxiv.org/abs/2410.07113)

```bibtex
@misc{pi2024personalizedvisualinstructiontuning,
      title={Personalized Visual Instruction Tuning}, 
      author={Renjie Pi and Jianshu Zhang and Tianyang Han and Jipeng Zhang and Rui Pan and Tong Zhang},
      year={2024},
      eprint={2410.07113},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2410.07113}, 
}
```

