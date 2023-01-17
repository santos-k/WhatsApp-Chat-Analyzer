import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from PIL import Image

import dataset
import functions

im = Image.open("what.ico")
st.set_page_config(
    page_title="WhatsApp Analysis",
    page_icon=im,
    layout="wide",
)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("Do Visit @: ")
with col2:
    st.markdown("[Linkedin](https://www.linkedin.com/in/santos-k)")
with col3:
    st.markdown("[Kaggle](https://www.kaggle.com/kuchhbhi)")
with col4:
    st.markdown("[Github](https://github.com/santos-k)")
with col5:
    st.markdown("[Tableau](https://public.tableau.com/app/profile/santosh.kumar3246)")

# st.markdown('<font color=‘red’>THIS TEXT WILL BE RED</font>', unsafe_allow_html=True)

st.sidebar.title('WhatsApp Chat Analysis')
col1, col2, col3, col4 = st.sidebar.columns([1, 2, 2, 1])
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/479px-WhatsApp.svg.png', width=90)
with col3:
    st.image('analy.png', width=90)

st.sidebar.caption(
    'This application lets you analyze Whatsapp conversations in a very comprehensive manner, with charts, metrics, '
    'and other forms of analysis.')
st.title('WhatsApp Chat Analyzer')
st.markdown('Developed with Streamlit, Developed by Santosh')

with st.expander('See!!.. How it works?'):
    st.subheader('Steps to Analyze:')
    st.markdown(
        '1. Export the chat by going to WhatsApp on your phone, opening the chat, clicking on the three dots, '
        'selecting "More," and then choosing "Export Chat" without media. Save the file to your desired location.')
    st.markdown(
        '2. Browse or drag and drop the chat file.')
    st.markdown('3. Select a user or group to analyze, or leave the default setting of "All" to analyze for all users.')
    st.markdown('4. Click the "Show Analysis" button.')
    st.markdown(
        '5. Enable "Wide mode" for a better viewing experience in settings, or close the sidebar on mobile for improved'
        ' view.')
    st.markdown(
        '6. To analyze for a single user, select their name from the dropdown and click "Show Analysis" again.')
    st.markdown(
        '7. Repeat the steps for additional chats.')

# file upload
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat text file:")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode(encoding='utf-8')
    df = dataset.make_Dataframe(data)

    # extracting all unique username from df['name'], to show the name list
    user_list = sorted(df['user'].unique())
    # getting the selected username from dropdown list
    selected_user = st.sidebar.multiselect('Select Username', user_list)
    if st.sidebar.button("Show Analysis"):
        users_name = None
        if selected_user:
            df = df[df['user'].isin(selected_user)]
            users_name = selected_user
        else:
            df = df
            users_name = 'All'
        noOfUsers, noOfmsgs, noOfWords, noOfMedia, noOfLinks, missedCall = functions.get_msg_stats(df)
        # displaying stats
        st.subheader(f'Selected Users: {users_name}')

        col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])

        start_dt = str(df['date'].iloc[0])[:10]
        last_dt = str(df['date'].iloc[-1])[:10]
        col2.metric('Chat From:', start_dt)
        col3.metric('Chat To:', last_dt)
        col4.metric("Total Members", noOfUsers)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Messages", noOfmsgs)
        col2.metric("Total Words Used", noOfWords)
        col3.metric('Total Media Shared', noOfMedia)
        col4.metric('Total Links Shared', noOfLinks)
        col5.metric("Total Missed Calls", missedCall)

        # bar plot of user activity
        with st.expander("Which members are the most active in the chat?...click '+' to see details"):
            st.markdown(
                'The graph shows the activity level of all members in the chat, represented by a bar chart. '
                'The longest bar represents the highest level of contribution in the chat, and the names of '
                'the members are listed on the X-axis. The second graph illustrates the average number of messages '
                'among all members and shows how much a member\'s activity is above or below the average.')

        user_count = df['user'].value_counts()
        st.bar_chart(user_count)

        with st.expander("Messages by users...click '+' to see more details"):
            st.markdown(
                'This graph is known as a Donut chart. It is a circular statistical graphic that is '
                'divided into slices to illustrate numerical proportion. The names of the members are '
                'shown on the right side, with each color representing a member in the chart. You can '
                'remove a member from the chart by clicking on the color of their name.')

        # pie chart of user activity percentage
        user_count = df['user'].value_counts().reset_index()
        user_count.columns = ['member', 'message']
        fig = px.pie(user_count, names='member', values='message', hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Dark2)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig, use_container_width=True)

        # Top 5 Most and Less active members
        col1, col2, col3 = st.columns([1.5, 0.2, 1.5])
        top5 = df['user'].value_counts().sort_values(ascending=False).reset_index().iloc[0:5]
        top5.columns = ['Member', 'Message']
        with col1:
            st.markdown('Most Active Members')
            st.dataframe(top5)

        last5 = df['user'].value_counts().sort_values().reset_index().iloc[0:5]
        last5.columns = ['Member', 'Message']
        with col3:
            st.markdown('Less Active Members')
            st.dataframe(last5)

        if selected_user == 'All':
            # chat started and ended by members
            with st.expander(f"Who started and ended chat most of time?... Click on '+' to see more details."):
                st.markdown(
                    "The chart on the right shows the percentage of chats started by each member on a daily basis. "
                    "The chart on the right shows the percentage of chats ended by each member on a daily basis.")

            col1, col2 = st.columns(2)
            chat_started, chat_ended = functions.chat_start_end_by(df)
            fig = px.pie(chat_started, names='Member', values='Count', hole=0.3,
                         color_discrete_sequence=px.colors.qualitative.Safe)
            fig.update_layout(title_text=f'Chat Started by', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)
            with col1:
                # st.markdown('Chat Started by members in each day')
                st.plotly_chart(fig, use_container_width=True)

            fig = px.pie(chat_ended, names='Member', values='Count', hole=0.3)
            fig.update_layout(title_text=f'Chat Ended by', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)

            with col2:
                # st.markdown('Chat Ended by members in each day')
                st.plotly_chart(fig, use_container_width=True)

        # wordcloud
        with st.expander(f"The words that have occurred the most number of times... click '+' to see more details"):
            st.markdown(
                'This graph is known as a Word Map. It illustrates the frequency of words used in the chat, '
                'with the size of the words indicating the number of occurrences. The top 10 most frequently '
                'used words and a list of all words used with their counts are shown below the chart. There are '
                'two word map charts, one without stop words and another with stopwords. Stopwords are words that '
                'are used in sentence formation/creation, but have no meaning and are not useful for analysis. '
                'Examples include: is, am, i, there, where, why, haan, h, ye, abhi, kaha, etc. We have tried to '
                'remove stopwords, but sometimes it\'s difficult to recognize them due to misspelling. Like you '
                'know how some people use words like haaaaan, haan, ha, haai, h, hain, please, pls, plzz, plzzzz, '
                'plssss. These words are understandable by humans, but the computer may not recognize them.')
        word_img, word_df = functions.wordMap_without_stopwords(df)
        fig, ax = plt.subplots()
        ax.imshow(word_img)
        plt.axis('off')
        st.markdown('Wordmap without stopwords(most 75 words)')
        st.pyplot(fig)

        col1, col2, col3 = st.columns([2, 0.2, 1.7])
        with col1:
            # bar chart of most used words
            fig = px.bar(word_df.sort_values(by='count', ascending=False).head(10), x='count', y='words', color='count')
            fig.update_layout(title_text=f'10 Most Words Used', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown(f'List of 30 most sed words')
            st.dataframe(word_df.sort_values(by='count', ascending=False).reset_index(drop=True).head(30))

        word_img, word_df = functions.wordMap_with_stopwords(df)
        fig, ax = plt.subplots()
        ax.imshow(word_img)
        # plt.title(f'Most Used Words in Chat by {selected_user}', fontdict={'fontsize': 15}, loc='center', color='r')
        plt.axis('off')
        st.markdown('Wordmap with stopwords(most 75 words)')
        st.pyplot(fig)

        col1, col2, col3 = st.columns([2, 0.2, 1.7])
        with col1:
            # bar chart of most used words
            fig = px.bar(word_df.sort_values(by='count', ascending=False).head(10), x='count', y='words', color='count')
            fig.update_layout(title_text=f'10 Most Words Used', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown(f'List of 30 most used words')
            st.dataframe(word_df.sort_values(by='count', ascending=False).reset_index(drop=True).head(30))

        with st.expander(f"Who has sent the longest messages?... click '+' to see more details"):
            st.markdown(
                'This graph, known as a Box Plot, displays the distribution of numerical data by showing the minimum, '
                'first quartile, median, third quartile and maximum values. The middle box represents the area where '
                '50% of the data lies, and dots outside the box represent data that is particularly high or low in '
                'comparison to the rest of the data.')
            st.image('boxplot.png')

        # boxplot of message chars
        fig = px.box(df, x='user', y='message_chars', color='user',
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     labels={'user': 'Member Name', 'message_chars': 'Characters in message'})
        st.plotly_chart(fig, use_container_width=True)

        # Emoji Used
        with st.expander(f"Most used emoji in chat?... click '+' to see more details"):
            st.markdown(
                'This graph is known as Pie Chart.  \nSome emoji which look like box is not recognised by system')

        emoji_df = functions.get_emojis(df)

        col1, col2, col3 = st.columns([2, 0.3, 1])
        with col1:
            # st.markdown('Top 10 Most used Emoji')
            fig = px.pie(emoji_df.head(10), names='emoji', values='counts',
                         color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(title_text=f'Top 10 Most used Emoji', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.empty()
        with col3:
            st.markdown(f'List of all used emoji')
            st.dataframe(emoji_df)

        # sunburst
        with st.expander(f"User and their messages in month and day ... click '+' to see more details"):
            st.markdown(
                "The graph below is known as a Sunburst, which is similar to a pie chart but with additional features. "
                "It shows hierarchical relationships through a series of concentric rings, where each ring corresponds "
                "to a level in the hierarchy. Each ring is segmented proportionally to represent its constituent "
                "details. You can click on an inner slice to expand the middle ring, and click on a middle ring slice "
                "to expand the outer ring for more detailed information.")
        col1, col2 = st.columns(2)
        # if selected_user == 'All':
        with col1:
            fig = px.sunburst(df, path=['user', 'day_name'], color_discrete_sequence=px.colors.qualitative.G10)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.sunburst(df, path=['year', 'month_name', 'day_name'],
                              color_discrete_sequence=px.colors.qualitative.Dark24)
            st.plotly_chart(fig, use_container_width=True)

        with st.expander(f"Activity Over the periods!... click '+' to see more details"):
            st.markdown(
                'This graph is known as Line Chart.  \nIt shows how activity gradually increasing or decreasing by over period ')

        # line chart daily activity of day and message
        x = df['day_name'].value_counts().sort_index()
        fig = px.line(x=x.index, y=x.values, markers=True, labels={'y': 'Message Count', 'x': 'Day Name'}, height=400,
                      width=400, color_discrete_sequence=px.colors.cmocean.deep)
        fig.update_layout(title_text='Weekly Chat Behavior by All', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # line chart daily activity of day and message
        x = df['day'].value_counts().sort_index()
        fig = px.line(x=x.index, y=x.values, markers=True, labels={'y': 'Message Count', 'x': 'Day'}, height=400,
                      width=400)
        fig.update_layout(title_text='Daily Chat Behavior by All', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # Activity of All Users on a single Day of month
        x = df[['day', 'user']].value_counts().reset_index().sort_values(by='day')
        fig = px.line(x, x='day', y=0, markers=True, labels={'0': 'Message Count', 'day': 'Day'}, color='user')
        fig.update_layout(title_text=f'Daily Activity of {selected_user} ', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # line chart of month and message
        x = df['month'].value_counts().sort_index()
        fig = px.line(x=x.index, y=x.values, markers=True, labels={'y': 'Message Count', 'x': 'Month'},
                      color_discrete_sequence=px.colors.cmocean.deep)
        fig.update_layout(title_text=' Monthly Activity of All Users', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # Activity of All Users on a single month
        x = df[['month', 'user']].value_counts().reset_index().sort_values(by='month')
        fig = px.line(x, x='month', y=0, markers=True, labels={'0': 'Message Count', 'month': 'Month'}, color='user')
        fig.update_layout(title_text=f'Monthly Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # line chart of year and message
        x = df['year'].value_counts().sort_index()
        st.write('Line Chart of Yearly Activity of All Users (X-axis: Year, Y-axis: Message Count')
        st.line_chart(x)

        # Activity of All Users on a single Day of month
        x = df[['year', 'user']].value_counts().reset_index().sort_values(by='year')
        fig = px.line(x, x='year', y=0, markers=True, labels={'0': 'Message Count', 'year': 'Year'}, color='user')
        fig.update_layout(title_text=f'Yearly Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # line chart of date and message
        x = df['date'].value_counts().sort_index()
        st.write('Line Chart with Date wise Activity of All Users(X-axis: Date, Y-axis: Message Count')
        st.line_chart(x)

        # Activity of All Users on a single Day of month
        x = df[['date', 'user']].value_counts().reset_index().sort_values(by='date')
        fig = px.line(x, x='date', y=0, markers=True, labels={'0': 'Message Count', 'date': 'Date'}, color='user')
        fig.update_layout(title_text=f'Date wise Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        with st.expander(f"{selected_user} Activity ... click '+' to see more details"):
            st.markdown(
                "The below graph is known as a Heatmap Chart. It is used to visualize data over a two-dimensional grid "
                "where individual values are represented as colors. Darker colors indicate a lower possibility, while "
                "brighter colors indicate a higher possibility.Please check the color scale and follow the code. If any"
                " day's name or month's name is missing, it means that there was no chat on that day or month."
            )
        crosstab = functions.crosstab_dayNmonth(df['day_name'], df['month_name'])
        fig = px.imshow(crosstab, text_auto=True)
        fig.update_layout(title_text=f'Weekly Over Monthly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap Day and Month Activity
        fig = px.imshow(pd.crosstab(df['month'], df['day']), text_auto=True)
        fig.update_layout(title_text=f'Daily over Monthly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap weekdays and Month Activity
        fig = px.imshow(pd.crosstab(df['day_name'], df['day']), text_auto=True, width=700)
        fig.update_layout(title_text=f'Weekly Over Daily  Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap Day and hour Activity
        fig = px.imshow(pd.crosstab(df['hour'], df['day']), text_auto=True, color_continuous_scale=['black', 'red'])
        fig.update_layout(title_text=f'Daily Over Hourly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap weekday and hour Activity
        fig = px.imshow(pd.crosstab(df['hour'], df['day_name']), text_auto=True)
        fig.update_layout(title_text=f'Weekly Over Hourly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap minute and hour Activity
        fig = px.imshow(pd.crosstab(df['hour'], df['minute']), text_auto=True)
        fig.update_layout(title_text=f'Minutes Over Hourly Chat Activity    of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        df['message_chars'] = df['message'].apply(lambda z: len(z))
        longest_msg = df.sort_values(by='message_chars', ascending=False)[
            ['date', 'hour', 'minute', 'user', 'message', 'message_chars']].head(5).reset_index(drop=True)
        longest_msg['date'] = longest_msg['date'].apply(lambda x: str(x)[:10])
        longest_msg['time'] = longest_msg['hour'].apply(lambda x: str(x)) + ":" + longest_msg['minute'].apply(
            lambda x: str(x))
        st.markdown(f"Top 5 longest Message of {selected_user}")
        st.table(longest_msg[['date', 'time', 'user', 'message', 'message_chars']])

        a = df.groupby(by='date')
        top = a.size().sort_values(ascending=False).index[0]
        top5_msg = a.get_group(top).sort_values(by='message_chars', ascending=False)[
            ['date', 'day_name', 'user', 'message']].head(5).reset_index(drop=True)
        top5_msg['date'] = top5_msg['date'].apply(lambda x: str(x)[:10])
        st.markdown(f'5 Longest message in every single day by {selected_user}')
        st.table(top5_msg)

        links = functions.get_liks(df)
        st.markdown('Links Shared')
        st.dataframe(links)

        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')

        st.subheader('Stay tune for more updates!!')

        col1, col2, col3 = st.columns(3)
        # display gif file from url

        with col2:
            st.markdown('\n')
            st.markdown('\n')
            st.markdown('\n')
            st.markdown(
                "![Thank You!!](https://www.animatedimages.org/data/media/466/animated-thank-you-image-0011.gif)")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown("Do Visit @: ")
        with col2:
            st.markdown("[Linkedin](https://www.linkedin.com/in/santos-k)")
        with col3:
            st.markdown("[Kaggle](https://www.kaggle.com/kuchhbhi)")
        with col4:
            st.markdown("[Github](https://github.com/santos-k)")
        with col5:
            st.markdown("[Tableau](https://public.tableau.com/app/profile/santosh.kumar3246)")
