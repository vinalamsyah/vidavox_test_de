# ETL Pipeline for Multi-Modal Data
---
### Pre-requisites
Before setting-up this project, please make sure that [Docker](https://www.docker.com/products/docker-desktop/) is installed properly.

---
### Setup
1. Open the terminal on your computer
2. Change your terminal directory to the project's folder
3. Run the following command
`docker compose up -d --build`
4. Wait for the installation process to complete
5. The application is up and running
---
### How to Extract Data From A PDF File
1. Prepare the PDF file you want to extract the data from.
2. Put it in the following directory: `[This project's directory]/etl/input`
3. The program will detect any changes and run automatically.
---
### How to View Extracted Data
You can access the extracted data at [localhost](http://localhost)