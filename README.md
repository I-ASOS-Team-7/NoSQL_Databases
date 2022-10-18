# NoSQL Databases

## **About The Project**

This Project was created during [I-ASOS Software Architecture](https://uim.fei.stuba.sk/predmet/i-asos/) course at [FEI STU](https://www.fei.stuba.sk/english.html?page_id=793). The main goal of it was to experiment and compare with different types of NoSQL Databases. We have experimented with [CouchDB](https://couchdb.apache.org/), [Neo4j](https://neo4j.com/), [MongoDB](https://www.mongodb.com/) and [Redis](https://redis.io/).

Check out the **[Documentation](#)** and **[Presentation](#)** for more information.

### **Built With**

* [![Docker][Docker]][Docker-url]
* [![Neo4j][Neo4j]][Neo4j-url]
* [![MongoDB][MongoDB]][MongoDB-url]
* [![Redis][Redis]][Redis-url]
* [![Python 3.10][Python]][Python-url]
* [![Pandas][Pandas]][Pandas-url]
* [![Plotly][Plotly]][Plotly-url]

### **Prerequisites**

* **Python 3.10.x** - It is either installed on your Linux distribution or on other Operating Systems you can get it from the [Official Website](https://www.python.org/downloads/release/python-3100/), [Microsoft Store](https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us&gl=US) or through `Windows Subsystem for Linux (WSL)` using this [article](https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d).
* **Docker** - To run this project you will need Docker and Docker Compose set up. You can find several setups for [Windows](https://docs.docker.com/desktop/install/windows-install/), [Mac](https://docs.docker.com/desktop/install/mac-install/) and [Linux](https://docs.docker.com/desktop/install/linux-install/) 
* **Data** - In this project we are using a modified version of [Hakan Özlers mongodb-json-files](https://github.com/ozlerhakan/mongodb-json-files/tree/master/datasets) which can be downloaded [here](https://drive.google.com/drive/folders/1TnD_PGOMWJcGT4znmncVOXfDy-qiy4QR?usp=sharing). For Neo4j we have used the [arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv?resource=download). After everything is downloaded you should organize data files this way.

[![Folder Structure][folder-struct-screenshot]](#)

### **Usage**
1. Clone the repo
   ```sh
   git clone https://github.com/I-ASOS-Team-7/NoSQL_Databases.git
   ```
2. Navigate to the project folder and create a new Python Virtual Environment.
   ```sh
   python -m venv venv
   ```
3. Activate the Python Virtual Environment.
    - On Windows
    ```cmd
    .\venv\Scripts\Activate.ps1
    ```
    - On Linux
    ```sh
    source "./venv/bin/activate"
    ```

4. Install Project Dependencies.
    ```sh
    pip install -r requirements.txt
    ```

5. Start up Docker.
    ```sh
    docker-compose up --build
    ```

6. Run the script.
    - On Windows
    ```cmd
    python src\main.py
    ```
    - On Linux
    ```sh
    python src/main.py
    ```
## Contact
- Bc. Ladislav Rajcsányi -  [Raychani1](https://github.com/Raychani1)  -  [rajcsanyi.ladislav.it@gmail.com](mailto:rajcsanyi.ladislav.it@gmail.com)
- Bc. Maksim Mištec -  [MaksimMistec](https://github.com/MaksimMistec)
- Bc. Tomáš Kukumberg -  [TomasKukumberg](https://github.com/TomasKukumberg)
- Bc. Alexander Sárközy-  [Drugun](https://github.com/Drugun)

## **License**

Distributed under the **MIT License**. See [LICENSE]() for more information.

## **Acknowledgments**
* [CJ Sullivan: Create a graph database in Neo4j using Python (Towards Data Science Article)](https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4)
* [Hakan Özler: MongoDB JSON Data](https://github.com/ozlerhakan/mongodb-json-files)
* [Othneil Drew: Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<!-- MARKDOWN LINKS & IMAGES -->
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Plotly]: https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white
[Plotly-url]: https://plotly.com/
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Neo4j]: https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white
[Neo4j-url]: https://neo4j.com/
[MongoDB]: https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white
[MongoDB-url]: https://www.mongodb.com/
[Redis]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/

[folder-struct-screenshot]: https://raw.githubusercontent.com/Raychani1/raychani1.github.io/main/projects/python/i_asos_team_7_project/readme_images/data_folder_structure.png
