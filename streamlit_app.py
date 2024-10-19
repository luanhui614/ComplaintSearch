import streamlit as st
import requests
import pandas as pd

# Read the CSV file into a DataFrame
csv_path = '/workspaces/ComplaintSearch/data/searchApptest.csv'
df = pd.read_csv(csv_path)

# Define the Jina API details
url = 'https://api.jina.ai/v1/rerank'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer jina_6a203dd796fe4653a555daad3b22bd46MQ0dJX6GMD8g_6jVGBjpdNQsIdgB'
}

# Streamlit App
st.title("Content Records Finder App")

# Sidebar
st.sidebar.header("Search Parameters")
input_text = st.sidebar.text_input("Enter complaint content:")
top_n = st.sidebar.selectbox("Number of results to display:", [1, 2, 3, 4, 5])

if st.sidebar.button("Search"):
    # Extract the '投诉内容' column from the DataFrame
    documents = df['投诉内容'].tolist()

    # Prepare the data for the API request
    data = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": input_text,
        "top_n": top_n,
        "documents": documents
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)

    # Check the response
    if response.status_code == 200:
        response_json = response.json()
        relevant_documents = response_json.get('results', [])
        
        # Display the relevant 投诉内容 and corresponding columns
        st.header("Relevant 投诉内容 and Corresponding Columns")
        for doc in relevant_documents:
            if isinstance(doc['document'], dict):
                doc_text = doc['document'].get('text', '')
            else:
                doc_text = doc['document']
            
            # Normalize the document text for comparison
            doc_text_normalized = ''.join(doc_text.split())
            
            # Find the index of the matching document in the original list
            for i, original_doc in enumerate(documents):
                original_doc_normalized = ''.join(original_doc.split())
                if doc_text_normalized == original_doc_normalized:
                    doc_index = i
                    break
            
            relevant_row = df.iloc[doc_index]
            
            st.write(f"TS_ID: {relevant_row['TS_ID']}")
            st.write(f"接件日期: {relevant_row['接件日期']}")
            st.write(f"投诉人姓名: {relevant_row['投诉人姓名']}")
            st.write(f"投诉人联系电话: {relevant_row['投诉人联系电话']}")
            st.write(f"涉及科室/病区: {relevant_row['涉及科室/病区']}")
            st.write(f"涉事人员: {relevant_row['涉事人员']}")
            st.write(f"投诉内容: {doc_text}")
            st.write("-" * 40)
    else:
        st.error(f"Error: {response.status_code}, {response.text}")

if st.sidebar.button("Clear"):
    st.experimental_rerun()

# Instructions
st.write("Enter your complaint content in the sidebar and click 'Search' to find the matched records of complaint content.")
