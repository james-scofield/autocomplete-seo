import streamlit as st
import requests,json
import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
listcomplete = []

left, right = st.columns(2)

form = left.form("template_form")
keyword = form.text_input("Enter Keyword")
source = form.selectbox(
    "Google/Youtube",
    ["Google","Youtube"],
    index=0,
)
total = form.slider("Number", 10,15,5)
submit = form.form_submit_button("Apply")


cr = "countryUS"  #  https://developers.google.com/custom-search/docs/xml_results_appendices#country-collection-values   
gl = "US"   #  https://developers.google.com/custom-search/docs/xml_results_appendices#country-codes
lr = "lang_en"  #  https://developers.google.com/custom-search/docs/xml_results_appendices#language-collection-values
hl = "en"  
def google_autocomplete(keyword,uplimit,counter):
    googlekeywords={}
    listg=[]
   
    for i in keyword:
        URL="https://google.com/complete/search?client=chrome"+"&q=" + i + "&pws=0" + "&cr=" + cr + "&gl=" + gl + "&lr=" + lr + "&hl=" + hl
        headers = {'User-agent': "Mozilla/5.0"} 
        response = requests.get(URL, headers=headers) 
        result = json.loads(response.content.decode('utf-8'))
        googlekeywords[counter+1] = []
        googlekeywords[counter+1] = result[1]
        counter = counter+1
    for i in googlekeywords.values():
            listg=listg+i
            listg=list(set(listg))
            if len(listg) >= uplimit:
                return listg
    return google_autocomplete(listg,uplimit,counter)
    

def youtube_autocomplete(keyword,uplimit,counter):
    youtubekeywords={}
    listy=[]
   
    for i in keyword:
        URL="http://google.com/complete/search?client=youtube&gs_ri=youtube&ds=yt"+"&q=" + i + "&pws=0" + "&cr=" + cr + "&gl=" + gl + "&lr=" + lr + "&hl=" + hl
        headers = {'User-agent': "Mozilla/5.0"} 
        response = requests.get(URL, headers=headers)
        result = (response.content.decode('utf-8'))

        youtubekeywords[counter+1] = []
        youtubekeywords[counter+1] = [b[0] for b in json.loads(result[19:-1])[1]]
        
        
        counter = counter+1
    for i in youtubekeywords.values():
            listy=listy+i
            listy=list(set(listy))
            if len(listy) >= uplimit:
                return listy
    return youtube_autocomplete(listy,uplimit,counter)
if submit:
    if source == "Google":
        right.write(google_autocomplete([keyword],8,0))
    elif source == "Youtube":
        right.write(youtube_autocomplete([keyword],8,0))
