---
layout: post
title: Arduino-cli
tags: Homebrew cli, Terminal
---

In this tutorial, let's explore the setup process of Arduino CLI in the Mac OS.
The process just takes only 10 minutes.

_Installing Homebrew_

Open up a terminal window and install homebrew with the following
command:

<style>
  .container {
    position: relative;
  }

  textarea {
    width: 100%;
    height: 100px;
  }

  button {
    position: absolute;
    top: 0;
    right: 0;
  }
</style>

<div class="container">
    <textarea placeholder='/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'></textarea>
    <button onclick="copyText()">Copy Text</button>
</div>

<script>
function copyText() {
    var textToCopy = document.querySelector("textarea");
    textToCopy.select();
    document.execCommand("copy");
    alert("Text copied to clipboard!");
}
</script>

_Adding Homwbrew to the path_

After installing, add it to the path(replace "[username]" with your actual username):

<style>
  .container {
    position: relative;
  }

  textarea {
    width: 100%;
    height: 100px;
  }

  button {
    position: absolute;
    top: 0;
    right: 0;
  }
</style>

<div class="container">
    <textarea placeholder='echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/[username]/.zprofile'></textarea>
    <button onclick="copyText()">Copy Text</button>
</div>

<script>
function copyText() {
    var textToCopy = document.querySelector("textarea");
    textToCopy.select();
    document.execCommand("copy");
    alert("Text copied to clipboard!");
}
</script>
