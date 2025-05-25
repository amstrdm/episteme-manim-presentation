#!/bin/bash

echo "STARTING RENDER"
manim-slides render presentation.py

echo "PREVIEWING"
manim-slides Presentation
