<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Python][python-shield]][python-url]
[![Coverage][coverage-shield]][coverage-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Tests](#tests)
* [Usage](#usage)
* [Contributing](#contributing)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project

Simple high-level api for all features of hebrew calendar.  
[**Explore the swagger »**](https://api.ginzburg.io/zmanim)


### Built With

* [Python 3.7](https://www.python.org/downloads/release/python-377/)
* [FastAPI](https://github.com/tiangolo/fastapi)
* [KosherJava's](https://kosherjava.com/zmanim-project) [python port](https://github.com/pinnymz/python-zmanim)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation
#### Docker
1. Run `docker run -p 8000:8000 benyomin/zmanim-api:latest`
2. Open http://localhost:8000 in your browser to explore the swagger.

#### Python
1) Clone/fork the repo
2) Use pipenv for build environment and install dependencies: `pipenv install`
3) Go to project folder: `cd %repo_location%/zmanim_api`
4) Run `python main.py`
5) Open http://localhost:8000 in your browser to explore the swagger

### Tests
Run tests: `pytest test/`  
Run with coverage: `coverage run -m pytest -v test/` or `pipenv run tests`



<!-- USAGE EXAMPLES -->
## Usage

Request:  
**`GET`** `http://localhost:8000/shabbat?cl_offset=18&lat=32.09&lng=34.86`  
Response:
```json
{
  "candle_lighting": "2020-10-09T17:56:00+03:00",
  "havdala": "2020-10-10T18:50:00+03:00",
  "settings": {
    "date": "2020-10-05",
    "cl_offset": 18,
    "havdala_opinion": "tzeis_8_5_degrees",
    "coordinates": [32.09, 34.86],
    "elevation": 0
  },
  "torah_part": "shemini_atzeres",
  "late_cl_warning": false
}
```

_For more examples, please refer to the [Swagger docs](https://api.ginzburg.io/zmanim)_



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- CONTACT -->
## Contact

* Telegram - [@benyomin](https://t.me/benyomin)  
* [Email](mailto:benyomin.94@gmail.com)

Project Link: [https://github.com/benyaming/zmanim_api](https://github.com/benyaming/zmanim_api)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/github/pipenv/locked/python-version/benyaming/zmanim_api?style=flat-square
[python-url]: https://img.shields.io/github/pipenv/locked/python-version/benyaming/zmanim_api?style=flat-square
[coverage-shield]: https://img.shields.io/codecov/c/github/benyaming/zmanim_api/master?style=flat-square
[coverage-url]: https://img.shields.io/codecov/c/github/benyaming/zmanim_api/master?style=flat-square
[contributors-shield]: https://img.shields.io/github/contributors/benyaming/zmanim_api.svg?style=flat-square
[contributors-url]: https://github.com/benyaming/zmanim_api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/benyaming/zmanim_api.svg?style=flat-square
[forks-url]: https://github.com/benyaming/zmanim_api/network/members
[stars-shield]: https://img.shields.io/github/stars/benyaming/zmanim_api.svg?style=flat-square
[stars-url]: https://github.com/benyaming/zmanim_api/stargazers
[issues-shield]: https://img.shields.io/github/issues/benyaming/zmanim_api.svg?style=flat-square
[issues-url]: https://github.com/benyaming/repo/zmanim_api
[license-shield]: https://img.shields.io/github/license/benyaming/zmanim_api.svg?style=flat-square
[license-url]: https://github.com/benyaming/zmanim_api/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/benyaming

``
