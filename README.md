<div id="top"></div>

<p>
   <a href="https://pepy.tech/project/piewordle/" alt="Downloads">
      <img src="https://static.pepy.tech/personalized-badge/piewordle?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" align="right">
   </a>
   <a href="https://pypi.org/project/piewordle/" alt="Visitors">
      <img src="https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithub.com%2FSilenZcience%2FPieWordle&label=Visitors&icon=person-circle&color=%23479f76" align="right">
   </a>
   <a href="https://github.com/SilenZcience/PieWordle/tree/main/piewordle" alt="CodeSize">
      <img src="https://img.shields.io/github/languages/code-size/SilenZcience/PieWordle?color=purple" align="right">
   </a>
</p>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">PieWordle</h2>
   <p align="center">
      A Recreation of Wordle in Python.
      <br/>
      <a href="https://github.com/SilenZcience/PieWordle/blob/main/piewordle/wordle.py">
         <strong>Explore the code »</strong>
      </a>
      <br/>
      <br/>
      <a href="https://github.com/SilenZcience/PieWordle/issues">Report Bug</a>
      ·
      <a href="https://github.com/SilenZcience/PieWordle/issues">Request Feature</a>
   </p>
</div>


<details>
   <summary>Table of Contents</summary>
   <ol>
      <li>
         <a href="#about-the-project">About The Project</a>
         <ul>
            <li><a href="#made-with">Made With</a></li>
         </ul>
      </li>
      <li>
         <a href="#getting-started">Getting Started</a>
         <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
            <li><a href="#installation">Installation</a></li>
         </ul>
      </li>
      <li><a href="#usage">Usage</a>
         <ul>
         <li><a href="#examples">Examples</a></li>
         </ul>
      </li>
      <li><a href="#license">License</a></li>
      <li><a href="#contact">Contact</a></li>
   </ol>
</details>

<div id="about-the-project"></div>

## About The Project




<div id="made-with"></div>

### Made With
[![MadeWith-Python]](https://www.python.org/)
[![Python][Python-Version]](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>
<div id="getting-started"></div>

## Getting Started

<div id="prerequisites"></div>

### Prerequisites

- Using PieWordle demands a Python-Interpreter (>= 3.7).

<div id="installation"></div>

### Installation
[![Version][CurrentVersion]](https://pypi.org/project/piewordle/)

Simply install the python package (via [PyPI-piewordle](https://pypi.org/project/piewordle/)):
```console
python -m pip install --upgrade piewordle
```

**OR alternatively** you can use the compiled version (*`Windows only`*):

Simply download the [pwordle.exe](https://raw.githubusercontent.com/SilenZcience/PieWordle/main/bin/pwordle.exe) file.

> Update the ./bin/pwordle.version file and run: ```pyinstaller ./piewordle/__main__.py --onefile --clean --dist ./bin --version-file ./bin/pwordle.version -n pwordle```.

<p align="right">(<a href="#top">back to top</a>)</p>
<div id="usage"></div>

## Usage

```console
pwordle [OPTION]...
```

```console
options:
  -h, --help     show this help message and exit
  -v, --version  show the current version.
  --daily        guess the daily wordle.
  -g GUESSES     define the amount of guesses the player has. default is 6.
  -?             allow not existing words.
  --de           use german words.
  -w WORDS       define custom wordle options. Seperator is ';'.
```

<div id="examples"></div>

### Examples

<details open>
	<summary><b>📂 Images 📂</b></summary>
   </br>

   <p float="left">
      <img src="https://raw.githubusercontent.com/SilenZcience/PieWordle/main/img/example1.png" width="49%"/>
      <img src="https://raw.githubusercontent.com/SilenZcience/PieWordle/main/img/example2.png" width="49%"/>
   </p>

</details>

```console
pwordle --daily -?
```

<p align="right">(<a href="#top">back to top</a>)</p>

<div id="license"></div>

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SilenZcience/PieWordle/blob/main/LICENSE) file for details

<div id="contact"></div>

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green


[MadeWith-Python]: https://img.shields.io/badge/Made%20with-Python-brightgreen
[Python-Version]: https://img.shields.io/badge/Python-3.7%20--%203.14%20%7C%20pypy--3.7%20--%20pypy--3.10-blue

[CurrentVersion]: https://img.shields.io/pypi/v/piewordle.svg

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange
