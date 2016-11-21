#!/bin/bash
sass home.scss:home.css --style compressed
sass app.scss:app.css --style compressed
sass login.scss:login.css --style compressed
sass account.scss:account.css --style compressed
sass webkit.scss:webkit.css --style compressed
sass safari.scss:safari.css --style compressed
cd mturk
sass highlight.scss:highlight.css --style compressed
cd ..