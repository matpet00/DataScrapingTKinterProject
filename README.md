<h1>Project Title: Financial Data Scraper, Visualization, & Export Tool </h1>
Overview:
This OOP Python-based  Demo project presents a comprehensive demo solution for extracting dividend-related financial data from specified websites, manipulating and visualizing the data, and exporting it to Excel files.<br>
Leveraging Selenium for web scraping, Pandas for data manipulation, Tkinter for the graphical user interface (GUI), and Matplotlib for data visualization, this tool streamlines the entire process of data extraction, analysis, and exportation.
<br>
<h2>Key Components & Functionalities: </h2>

<h3>Scraper Class</h3>

Utilizes Selenium WebDriver to scrape dividend-related data from targeted websites that uses Javascript to send data to front-end. So no static table.
It Fetches table data, formats headers, and casts values to respective data types for further processing.

<h3>DataHandler Class</h3>

Processes the scraped data, converting it into structured formats suitable for manipulation.
Converts data into Pandas DataFrames for enhanced handling, analysis, and exportation.

<h3>ExcelHandler Class</h3>

Facilitates the export of processed financial data to Excel files, allowing users to save, share, and analyze data conveniently.

<h3>Chart Class</h3>

Generates graphical representations (e.g., bar charts) based on the financial data extracted, aiding in data visualization and analysis.

<h3>DemoApp Class (GUI)</h3> 

Implements a Tkinter-based graphical user interface (GUI) for user interaction.
Offers functionalities to trigger data scraping, display tables into pandastable that provide further analysis options, visualize financial data through charts, and export data to Excel files effortlessly. Integrates with other classes.

<h3>Purpose:</h3>
This project aims to simplify the entire process of extracting dividend-related financial data from web sources, handling, visualizing, and exporting it to Excel files. The tool provides a user-friendly interface for users to scrape, analyze, visualize, and export financial data seamlessly.

<h3>Disclaimer:</h3>
I dont own the data from the targeted web and they are used in small scale and just to showcase programming skills.

