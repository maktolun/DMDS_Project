#Mounting Google Drive to access files in the folder
from google.colab import drive
drive.mount('/content/drive')

#Changing directory to working directory
%cd /content/drive/MyDrive/Colab_Notebooks/project

#Installing Predi-XY by pip
!pip install predixy

#Running Predi-XY as a terminal command
!predixy /content/drive/MyDrive/Colab_Notebooks/project/furandimer.xyz
