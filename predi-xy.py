from google.colab import drive
drive.mount('/content/drive')

%cd /content/drive/MyDrive/Colab_Notebooks/project

!pip install predixy

!predixy /content/drive/MyDrive/Colab_Notebooks/project/furandimer.xyz
