# WhatsApp-Chat-Analyzer
This project is focused on analyzing WhatsApp chat logs and providing various charts and visualizations that help understand patterns and trends in conversations.

This project is focused on analyzing WhatsApp chat logs and presenting the data in various charts and visualizations. The main goal of the project is to make it easy for users to understand patterns and trends in their WhatsApp conversations.

Users can analyze both individual and group chats. The project uses the Streamlit library for web application development, Matplotlib, Plotly, and Pandas for data visualization, PIL for opening image files, and various other libraries for data processing and analysis. The project consists of three main files: app.py, dataset.py, and functions.py. 
To use the webapp, users will need to export their WhatsApp chat logs as a text file and upload it to the website. The website will then provide various charts and visualizations of the data.

## Files
1. app.py
2. functions.py
3. dataset.py
4. stop_hinglish.txt
5. analy.png,boxplot.png,thankyou.gif, what.ico
6. requirements.txt
7. Procfile
8. setup.sh
    
## Data Analysis Provided
- Summarized data about the chat, including:
  - Chat starting and ending date
  - Total members in the chat
  - Total messages, including messages, missed calls, media, and links
  - Total words of messages
  - Total media files shared
  - Total links shared
  - Total missed calls
- Bar chart of the number of messages sent by members
- Pie chart of the number of messages sent in percentage
- Pie chart of who started and ended the chat most of the time
- Word map of the 75 most used words in the chat, with and without stopwords
- Box plot of who sent the longest messages
- Pie chart of the most used emojis
- Sunburst chart of members and their weekly messages (and yearly, monthly, weekly)
- Line chart of daily chat activity (same for monthly and yearly) for all members and individuals
- Heatmap representing which features have occurred more frequently
- Table of the 5 longest messages in the entire chat
- Table of the 5 longest messages of the highest chat activity on a single day
- Table of all shared links in the chat

## Charts and Visualizations
- Bar charts
- Line charts
- Box plots
- Word maps
- Sunburst charts
- Heatmaps

## Charts and Visualizations
- Bar charts
- Line charts
- Box plots
- Word maps
- Sunburst charts
- Heatmaps

# How to Use
- Export your WhatsApp chat logs as a text file.
- Open WhatsApp on your mobile device
- Open any chat
- Click on the three vertical dots in the upper right corner
- Click on "More"
- Click on "Export Chat" and proceed with "Without Media"
- Save the file in a location of your choice
- Visit https://whatsapp-santosh.herokuapp.com/
- Browse or drag and drop your file into the designated box on the website
- Select the member you wish to analyze from the dropdown menu or select "All"
- Click "Show Analysis" to view the charts and visualizations of the data.


## License
This project is licensed under the MIT License - see the [LICENSE.md]() file for details

## Conclusion
This WhatsApp Chat Analysis project is a great tool for understanding patterns and trends in your WhatsApp conversations. It provides a wide range of data analysis and visualization options that make it easy to understand the data and draw insights. The project is designed to be user-friendly and easy to use, and the code is open-source and available on GitHub, making it easy to customize and extend. Overall, this project is a valuable resource for anyone looking to analyze their WhatsApp chats and gain a deeper understanding of their communication patterns.

![image](https://user-images.githubusercontent.com/40932902/212856255-3feb4d3f-9a99-4156-b7b3-baa3a3cd7c60.png)


