# -*- coding: utf-8 -*-
"""Welcome To Colab

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
"""



pip install utils

from fastai.vision.all import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np
matplotlib.rc('image', cmap='Greys')

wild = r'wild animal images'

animal = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128))

dls = animal.dataloaders(wild)

animal = animal.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms=aug_transforms())
dls = animal.dataloaders(wild)

learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(4)

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(3, nrows=1)

learn.export()

wild = Path()
wild.ls(file_exts='.pkl')

learn_inf = load_learner(wild/'export.pkl')

learn_inf.predict('wild animal images/wolf/00000509_224resized.png')

learn_inf.dls.vocab

import ipywidgets as widgets

btn_upload = widgets.FileUpload()
btn_upload

img = PILImage.create(btn_upload.data[0])
img

out_pl = widgets.Output()
out_pl.clear_output()
with out_pl: display(img.to_thumb(128,128))
out_pl

pred,pred_idx,probs = learn_inf.predict(img)

lbl_pred = widgets.Label()
lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
lbl_pred

btn_run = widgets.Button(description='Classify')
btn_run

def on_click_classify(change):
    img = PILImage.create(btn_upload.data[-1])
    out_pl.clear_output()
    with out_pl: display(img.to_thumb(128,128))
    pred,pred_idx,probs = learn_inf.predict(img)
    lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'

btn_run.on_click(on_click_classify)

btn_upload = widgets.FileUpload()

vbox_layout = widgets.VBox([widgets.Label('Select your animal!'), btn_upload, btn_run, out_pl, lbl_pred])


display(vbox_layout)