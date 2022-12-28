import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor,helper

st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    #st.dataframe(df)

    # fetching unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show analysis"):
        num_messages,words,num_media_message,links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media")
            st.title(num_media_message)

        with col4:
            st.header("Links shared")
            st.title(links)

        # monthly timeline
        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily timeline
        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title("Activity map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Mosy Busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Mosy Busy month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            st.pyplot(fig)

        st.title('Weekly Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding bussiest users in the group
        if selected_user == "overall":
            st.title("Most busy Users")
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("most common words")
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")

        st.pyplot(fig)