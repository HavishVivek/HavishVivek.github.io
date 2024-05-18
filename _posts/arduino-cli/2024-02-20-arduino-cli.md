---
layout: postssss
title: Arduino-cli
tags: Homebrew cli, Terminal
---

In this tutorial, let's explore the setup process of Arduino CLI in the Mac OS.
The process just takes only 10 minutes.

_Installing Homebrew_

Open up a terminal window and install homebrew with the following
command:

<html lang="en">
<head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
.copy-link {
  --height: 36px;

display: flex;
max-width: 250px;
}

.copy-link-input {
flex-grow: 1;
padding: 0 8px;
font-size: 14px;
border: 1px solid #cccccc;
border-right: none;
outline: none;
}

.copy-link-input:hover {
background: #eeeeee;
}

.copy-link-button {
flex-shrink: 0;
width: var(--height);
height: var(--height);
display: flex;
align-items: center;
justify-content: center;
background: #dddddd;
color: #333333;
outline: none;
border: 1px solid #cccccc;
cursor: pointer;
}

.copy-link-button:hover {
background: #cccccc;
}
</style>

</head>
<body>
 <div class="copy-link">
 <input type="text" class="copy-link-input" value='/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"' readonly>
  <button type="button" class="copy-link-button">
    <span class="material-icons">content_copy</span>
  </button>
</div>
<script>
document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
  const inputField = copyLinkParent.querySelector(".copy-link-input");
  const copyButton = copyLinkParent.querySelector(".copy-link-button");
  const text = inputField.value;

inputField.addEventListener("focus", () => inputField.select());

copyButton.addEventListener("click", () => {
inputField.select();
navigator.clipboard.writeText(text);

    inputField.value = "Copied!";
    copyButton.innerHTML = '<span class="material-icons">done</span>';

    setTimeout(() => {
        inputField.value = text;
        copyButton.innerHTML = '<span class="material-icons">content_copy</span>';
    }, 2000);

});
});
</script>

</body>
</html>

_Adding Homebrew to the path_

After install, add it to the path(replace"[username]" with your actual username):

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        .copy-link {
            --height: 36px;
            display: flex;
            max-width: 250px;
            margin-bottom: 10px; /* Add space between each .copy-link div */
        }

        .copy-link-input {
            flex-grow: 1;
            padding: 0 8px;
            font-size: 14px;
            border: 1px solid #cccccc;
            border-right: none;
            outline: none;
        }

        .copy-link-input:hover {
            background: #eeeeee;
        }

        .copy-link-button {
            flex-shrink: 0;
            width: var(--height);
            height: var(--height);
            display: flex;
            align-items: center;
            justify-content: center;
            background: #dddddd;
            color: #333333;
            outline: none;
            border: 1px solid #cccccc;
            cursor: pointer;
        }

        .copy-link-button:hover {
            background: #cccccc;
        }

        /* Add margin to the last two .copy-link-button elements */
        .copy-link:nth-last-child(-n+2) .copy-link-button {
            margin-right: 10px; /* Adjust the value as needed */
        }
    </style>

</head>
<body>
    <div class="copy-link">
        <input type="text" class="copy-link-input" value="echo 'eval &quot;$(/opt/homebrew/bin/brew shellenv)&quot;' >> /Users/[username]/.zprofile" readonly>
        <button type="button" class="copy-link-button">
            <span class="material-icons">content_copy</span>
        </button>
    </div>
    <script>
        document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
            const inputField = copyLinkParent.querySelector(".copy-link-input");
            const copyButton = copyLinkParent.querySelector(".copy-link-button");
            let text = inputField.value;

            inputField.addEventListener("focus", () => inputField.select());

            copyButton.addEventListener("click", () => {
                navigator.clipboard.writeText(text).then(() => {
                    inputField.value = "Copied!";
                    copyButton.innerHTML = '<span class="material-icons">done</span>';

                    setTimeout(() => {
                        inputField.value = text;
                        copyButton.innerHTML = '<span class="material-icons">content_copy</span>';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        });
    </script>

</body>
</html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
        .copy-link {
            --height: 36px;
            display: flex;
            max-width: 250px;
            margin-bottom: 10px; /* Add space between each .copy-link div */
        }

        .copy-link-input {
            flex-grow: 1;
            padding: 0 8px;
            font-size: 14px;
            border: 1px solid #cccccc;
            border-right: none;
            outline: none;
        }

        .copy-link-input:hover {
            background: #eeeeee;
        }

        .copy-link-button {
            flex-shrink: 0;
            width: var(--height);
            height: var(--height);
            display: flex;
            align-items: center;
            justify-content: center;
            background: #dddddd;
            color: #333333;
            outline: none;
            border: 1px solid #cccccc;
            cursor: pointer;
        }

        .copy-link-button:hover {
            background: #cccccc;
        }

        /* Add margin to the last two .copy-link-button elements */
        .copy-link:nth-last-child(-n+2) .copy-link-button {
            margin-right: 10px; /* Adjust the value as needed */
        }
    </style>

</head>
<body>
    <div class="copy-link">
        <input type="text" class="copy-link-input" value="eval &quot;$(&#x2F;opt&#x2F;homebrew&#x2F;bin&#x2F;brew shellenv)&quot;" readonly>
        <button type="button" class="copy-link-button">
            <span class="material-icons">content_copy</span>
        </button>
    </div>
    <script>
        document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
            const inputField = copyLinkParent.querySelector(".copy-link-input");
            const copyButton = copyLinkParent.querySelector(".copy-link-button");
            let text = inputField.value;

            inputField.addEventListener("focus", () => inputField.select());

            copyButton.addEventListener("click", () => {
                navigator.clipboard.writeText(text).then(() => {
                    inputField.value = "Copied!";
                    copyButton.innerHTML = '<span class="material-icons">done</span>';

                    setTimeout(() => {
                        inputField.value = text;
                        copyButton.innerHTML = '<span class="material-icons">content_copy</span>';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        });
    </script>

</body>
</html>

_Installing arduino-cli_

To install, run

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        .copy-link {
            --height: 36px;
            display: flex;
            max-width: 250px;
        }

        .copy-link-input {
            flex-grow: 1;
            padding: 0 8px;
            font-size: 14px;
            border: 1px solid #cccccc;
            border-right: none;
            outline: none;
        }

        .copy-link-input:hover {
            background: #eeeeee;
        }

        .copy-link-button {
            flex-shrink: 0;
            width: var(--height);
            height: var(--height);
            display: flex;
            align-items: center;
            justify-content: center;
            background: #dddddd;
            color: #333333;
            outline: none;
            border: 1px solid #cccccc;
            cursor: pointer;
        }

        .copy-link-button:hover {
            background: #cccccc;
        }
    </style>

</head>
<body>
    <div class="copy-link">
        <input type="text" class="copy-link-input" value="brew install arduino-cli" readonly>
        <button type="button" class="copy-link-button">
            <span class="material-icons">content_copy</span>
        </button>
    </div>
    <script>
        document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
            const inputField = copyLinkParent.querySelector(".copy-link-input");
            const copyButton = copyLinkParent.querySelector(".copy-link-button");
            let text = inputField.value;

            inputField.addEventListener("focus", () => inputField.select());

            copyButton.addEventListener("click", () => {
                navigator.clipboard.writeText(text).then(() => {
                    inputField.value = "Copied!";
                    copyButton.innerHTML = '<span class="material-icons">done</span>';

                    setTimeout(() => {
                        inputField.value = text;
                        copyButton.innerHTML = '<span class="material-icons">content_copy</span>';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        });
    </script>

</body>
</html>

to check arduino-cli is installed, run

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        .copy-link {
            --height: 36px;
            display: flex;
            max-width: 250px;
        }

        .copy-link-input {
            flex-grow: 1;
            padding: 0 8px;
            font-size: 14px;
            border: 1px solid #cccccc;
            border-right: none;
            outline: none;
        }

        .copy-link-input:hover {
            background: #eeeeee;
        }

        .copy-link-button {
            flex-shrink: 0;
            width: var(--height);
            height: var(--height);
            display: flex;
            align-items: center;
            justify-content: center;
            background: #dddddd;
            color: #333333;
            outline: none;
            border: 1px solid #cccccc;
            cursor: pointer;
        }

        .copy-link-button:hover {
            background: #cccccc;
        }
    </style>

</head>
<body>
    <div class="copy-link">
        <input type="text" class="copy-link-input" value="arduino-cli -h" readonly>
        <button type="button" class="copy-link-button">
            <span class="material-icons">content_copy</span>
        </button>
    </div>
    <script>
        document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
            const inputField = copyLinkParent.querySelector(".copy-link-input");
            const copyButton = copyLinkParent.querySelector(".copy-link-button");
            let text = inputField.value;

            inputField.addEventListener("focus", () => inputField.select());

            copyButton.addEventListener("click", () => {
                navigator.clipboard.writeText(text).then(() => {
                    inputField.value = "Copied!";
                    copyButton.innerHTML = '<span class="material-icons">done</span>';

                    setTimeout(() => {
                        inputField.value = text;
                        copyButton.innerHTML = '<span class="material-icons">content_copy</span>';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        });
    </script>

</body>
</html>
