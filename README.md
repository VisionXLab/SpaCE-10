# SpaCE-10: A Comprehensive Benchmark for Multimodal Large Language Models in Compositional Spatial Intelligence

<div align="center">

<h1><img src="assets/space-10-logo.png" width="5%"> SpaCE-10: A Comprehensive Benchmark for Multimodal Large Language Models in Compositional Spatial Intelligence</h1>

[Ziyang Gong](https://scholar.google.com/citations?user=cWip8QgAAAAJ)<sup>1*</sup>,
[Wenhao Li](https://scholar.google.com/citations?user=XXXXX)<sup>2*</sup>,
[Oliver Ma]()<sup>3</sup>,
[Songyuan Li](https://scholar.google.com/citations?user=XXXXX)<sup>4</sup>,
[Jiayi Ji](https://scholar.google.com/citations?user=XXXXX)<sup>5</sup>,
[Xue Yang](https://scholar.google.com/citations?user=XXXXX)<sup>1</sup>,
[Gen Luo](https://scholar.google.com/citations?user=XXXXX)<sup>3</sup>,
[Junchi Yan](https://scholar.google.com/citations?user=XXXXX)<sup>1†</sup>,
[Rongrong Ji](https://scholar.google.com/citations?user=XXXXX)<sup>2†</sup>

<sup>1</sup> Shanghai Jiao Tong University, 
<sup>2</sup> Xiamen University, 
<sup>3</sup> Shanghai AI Lab, 
<sup>4</sup> Sun Yat-sen University, 
<sup>5</sup> National University of Singapore

<sup>*</sup> Equal contribution, <sup>†</sup> Corresponding author

<img src="https://visitor-badge.laobi.icu/badge?page_id=SpaCE-10-benchmark.readme&left_color=lightgrey&right_color=green">
<img src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen">
<img src="https://img.shields.io/github/stars/YOUR_USERNAME/SpaCE-10?style=social">

<a href="https://space10-benchmark.github.io"><img src="https://img.shields.io/badge/🌐_Project_Page-blue?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/HuggingFace-model-yellow?style=for-the-badge&logo=huggingface"></a>
<a href="#"><img src="https://img.shields.io/badge/BaiduNetDisk-download-blue?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/ScanNet++-Scenes-green?style=for-the-badge"></a>

<br><br>
<img src="assets/teaser.png" width="100%">
<br><br>

</div>

---

# 🔥 News

- 📢 [2025/06/01] SpaCE-10 paper is under review! We have released the dataset and evaluation toolkit.
- 🏗️ [2025/05/15] Teaser and benchmark examples updated. Check out the atomic and compositional QA tasks.
- 🤖 [2025/05/01] Baseline results with GPT-4o, InternVL, Claude-3, LLaVA and more are available.

---

# 🧠 What is SpaCE-10?

**SpaCE-10** is a **compositional spatial reasoning benchmark** for evaluating **Multimodal Large Language Models (MLLMs)** in indoor 3D environments. It spans:

- ✅ 10 **atomic spatial capabilities**
- ✅ 8 **compositional QA types**
- ✅ 5,000+ QA pairs
- ✅ 811 indoor scenes (ScanNet++, ScanNet, 3RScan, ARKitScene)

SpaCE-10 emphasizes **scene generalization**, **compositional reasoning**, and **multi-view fusion** under open-vocabulary QA settings.

---

# 📦 Dataset

| Item | Details |
|------|---------|
| QA Pairs | 5,000+ |
| Scenes | 811 |
| Tasks | Atomic QA, Compositional QA |
| Modality | 3D Point Clouds + Language |
| Format | JSON + SceneMesh (.ply) |

> 📥 Download dataset and evaluation toolkit [here](https://huggingface.co/YOUR_ORG/SpaCE-10)

---

# 🏁 Benchmark Capabilities

| Category       | Example Tasks                        |
|----------------|--------------------------------------|
| Atomic         | Relative position, orientation       |
| Compositional  | Scene planning, spatial chaining     |
| Reasoning Mode | Multiple-choice QA, point QA         |
| Modal Input    | 3D scene / multi-view / language     |

<p align="center">
  <img src="assets/qa_examples.png" width="90%">
</p>

---

# ⚙️ Quick Start

Coming soon:

```bash
git clone https://github.com/YOUR_USERNAME/SpaCE-10.git
cd SpaCE-10
pip install -r requirements.txt
python run_eval.py --model gpt-4o
