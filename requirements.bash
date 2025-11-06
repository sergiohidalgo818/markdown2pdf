#!/bin/bash
sudo apt update
sudo apt install -y \
  python3 \
  python3-pip \
  texlive-xetex \
  texlive-fonts-recommended \
  texlive-plain-generic \
  texlive-latex-recommended \
  texlive-latex-extra

sudo apt remove pandoc -y
wget https://github.com/jgm/pandoc/releases/download/3.8.1/pandoc-3.8.1-1-amd64.deb

sudo dpkg -i pandoc-3.8.1-1-amd64.deb

rm pandoc-3.8.1-1-amd64.deb
